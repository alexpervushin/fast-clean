from sqlalchemy import select

from microservices.shared.domain.exceptions import NotFoundError
from microservices.shared.infrastructure.database.repositories import BaseRepository
from microservices.users.domain.entities import User
from microservices.users.domain.repositories import UserRepositoryProtocol
from microservices.users.infrastructure.persistence.orm import UserModel


class UserRepository(BaseRepository[User, UserModel], UserRepositoryProtocol):
    model_type = UserModel

    def _map_to_domain(self, obj: UserModel) -> User:
        return User(
            id=obj.id,
            email=obj.email,
            name=obj.name,
            hashed_password=obj.hashed_password,
        )

    def _map_to_orm(self, obj: User) -> UserModel:
        return UserModel(
            id=obj.id,
            email=obj.email,
            name=obj.name,
            hashed_password=obj.hashed_password,
        )

    async def get_by_email(self, email: str) -> User:
        stmt = select(self.model_type).where(self.model_type.email == email)
        result = (await self.db.execute(stmt)).scalar_one_or_none()
        if result is None:
            raise NotFoundError(f"User with email {email} not found")
        return self._map_to_domain(result)