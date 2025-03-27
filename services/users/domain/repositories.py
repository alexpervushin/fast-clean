from typing import Protocol

from services.shared.domain.repositories import BaseRepositoryProtocol
from services.users.domain.entities import User


class UserRepositoryProtocol(BaseRepositoryProtocol[User], Protocol):
    async def get_by_email(self, email: str) -> User: ...
