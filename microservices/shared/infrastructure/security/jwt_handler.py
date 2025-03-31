import time
from typing import Protocol
from uuid import UUID

import jwt
from pydantic import BaseModel, Field

from microservices.shared.domain.exceptions import AuthenticationError
from microservices.shared.infrastructure.config import JWT as JWTSettings


class JWTPayload(BaseModel):
    sub: str = Field(...)
    exp: int = Field(...)
    iat: int = Field(...)


class JWTHandlerProtocol(Protocol):
    def create_access_token(self, user_id: UUID) -> str: ...
    def decode_token(self, token: str) -> UUID: ...


class PyJWTHandler(JWTHandlerProtocol):
    def __init__(self, settings: JWTSettings):
        self.secret_key = settings.secret_key
        self.algorithm = settings.algorithm
        self.expire_minutes = settings.access_token_expire_minutes

    def create_access_token(self, user_id: UUID) -> str:
        to_encode = {
            "sub": str(user_id),
            "exp": int(time.time()) + self.expire_minutes * 60,
            "iat": int(time.time()),
        }
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def decode_token(self, token: str) -> UUID:
        try:
            payload_dict = jwt.decode(
                token, self.secret_key, algorithms=[self.algorithm]
            )
            payload = JWTPayload(**payload_dict)
            return UUID(payload.sub)
        except jwt.ExpiredSignatureError as e:
            raise AuthenticationError("Token has expired") from e
        except jwt.PyJWTError as e:
            raise AuthenticationError("Could not validate credentials") from e
        except Exception as e:
            raise AuthenticationError("Invalid token payload") from e