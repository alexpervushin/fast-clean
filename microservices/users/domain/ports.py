from typing import Protocol

from microservices.shared.domain.ports import BaseRepositoryProtocol
from microservices.users.domain.entities import User


class UserRepositoryProtocol(BaseRepositoryProtocol[User], Protocol):
    async def get_by_email(self, email: str) -> User: ...
