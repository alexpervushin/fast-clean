from dishka import Provider, Scope, provide

from services.shared.domain.id_generator import IdGeneratorProtocol
from services.shared.domain.security import PasswordHasherProtocol
from services.shared.infrastructure.database import TransactionManager
from services.shared.infrastructure.interfaces import AsyncSessionProtocol
from services.users.application.user_services import UserService
from services.users.domain.repositories import UserRepositoryProtocol
from services.users.infrastructure.repositories.users_repository import (
    UserRepository,
)
from services.users.infrastructure.settings import Settings, get_settings


class ConfigProvider(Provider):
    @provide(scope=Scope.APP)
    async def provide_settings(self) -> Settings:
        return get_settings()


class UserProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_user_repository(
        self, session: AsyncSessionProtocol
    ) -> UserRepositoryProtocol:
        return UserRepository(session)

    @provide(scope=Scope.REQUEST)
    def get_user_service(
        self,
        repository: UserRepositoryProtocol,
        transaction_manager: TransactionManager,
        password_hasher: PasswordHasherProtocol,
        id_generator: IdGeneratorProtocol,
    ) -> UserService:
        return UserService(
            repository=repository,
            transaction_manager=transaction_manager,
            password_hasher=password_hasher,
            id_generator=id_generator,
        )