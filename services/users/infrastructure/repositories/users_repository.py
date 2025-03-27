from sqlalchemy import select

from services.shared.domain.exceptions import NotFoundError
from services.shared.infrastructure.repositories.base_repository import BaseRepository
from services.users.domain.entities import User
from services.users.domain.repositories import UserRepositoryProtocol
from services.users.infrastructure.orm.users_models import UserModel


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