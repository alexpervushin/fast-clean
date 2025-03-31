from dishka import Provider, Scope, make_async_container, provide
from pydantic_settings import BaseSettings

from microservices.shared.domain.id_generator import IdGeneratorProtocol
from microservices.shared.domain.security import PasswordHasherProtocol
from microservices.shared.infrastructure.database.session import (
    AsyncSessionProtocol,
    TransactionManager,
)
from microservices.shared.infrastructure.di.providers import (
    SharedDatabaseProvider,
    SharedIdGeneratorProvider,
    SharedSecurityProvider,
)
from microservices.shared.infrastructure.security.jwt_handler import JWTHandlerProtocol
from microservices.users.application.auth_service import AuthService
from microservices.users.application.user_service import UserService
from microservices.users.domain.repositories import UserRepositoryProtocol
from microservices.users.infrastructure.config import Settings, get_settings
from microservices.users.infrastructure.persistence.repositories import (
    UserRepository,
)


class ConfigProvider(Provider):
    @provide(scope=Scope.APP)
    async def provide_settings(self) -> Settings:
        return get_settings()

    @provide(scope=Scope.APP)
    async def provide_base_settings(self) -> BaseSettings:
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


class AuthProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_auth_service(
        self,
        repository: UserRepositoryProtocol,
        password_hasher: PasswordHasherProtocol,
        jwt_handler: JWTHandlerProtocol,
    ) -> AuthService:
        return AuthService(
            user_repository=repository,
            password_hasher=password_hasher,
            jwt_handler=jwt_handler,
        )


container = make_async_container(
    ConfigProvider(),
    SharedDatabaseProvider(),
    SharedSecurityProvider(),
    SharedIdGeneratorProvider(),
    UserProvider(),
    AuthProvider(),
)