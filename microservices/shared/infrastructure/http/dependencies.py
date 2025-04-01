from typing import Annotated
from uuid import UUID

from fastapi import Depends
from fastapi.security import HTTPBearer

from microservices.shared.domain.exceptions import AuthenticationError
from microservices.shared.infrastructure.security.jwt_handler import JWTHandlerProtocol

token_auth_scheme = HTTPBearer()


async def get_validated_token(
    token: Annotated[HTTPBearer | None, Depends(token_auth_scheme)] = None,
) -> str:
    if token is None or not token.credentials:
        raise AuthenticationError("Authentication required")
    return token.credentials


def decode_token_and_get_user_id(
    token_credentials: str, jwt_handler: JWTHandlerProtocol
) -> UUID:
    try:
        user_id = jwt_handler.decode_token(token_credentials)
        return user_id
    except AuthenticationError as e:
        raise e
    except Exception as e:
        raise AuthenticationError("Invalid token or user identifier") from e
