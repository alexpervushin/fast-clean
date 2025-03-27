from passlib.context import CryptContext

from services.shared.domain.security import PasswordHasherProtocol

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


class ArgonPasswordHasher(PasswordHasherProtocol):
    async def hash(self, password: str) -> str:
        return pwd_context.hash(password)

    async def verify(self, password: str, hashed_password: str) -> bool:
        return pwd_context.verify(password, hashed_password)