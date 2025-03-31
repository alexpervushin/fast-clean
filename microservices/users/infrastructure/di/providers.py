from dishka import Provider, Scope, make_async_container, provide
from pydantic_settings import BaseSettings

from microservices.shared.domain.ports import (
    IdGeneratorProtocol,
    PasswordHasherProtocol,
)
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
from microservices.users.application.commands import (
    AuthenticateUserCommand,
    RegisterUserCommand,
    UpdateUserCommand,
)
from microservices.users.application.queries import (
    GetUserByIdQuery,
)
from microservices.users.domain.ports import UserRepositoryProtocol
from microservices.users.infrastructure.config import Settings, get_settings
from microservices.users.infrastructure.persistence.repositories import (
    UserRepository,
)


class ConfigProvider(Provider):
    @provide(scope=Scope.APP)
    async def provide_settings(self) -> Settings:
        return get_settings()

    @provide(scope=Scope.APP)
    async def provide_base_settings(self, settings: Settings) -> BaseSettings:
        return settings


class UserProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_user_repository(
        self, session: AsyncSessionProtocol
    ) -> UserRepositoryProtocol:
        return UserRepository(session)

    @provide(scope=Scope.REQUEST)
    def get_register_user_command(
        self,
        repository: UserRepositoryProtocol,
        password_hasher: PasswordHasherProtocol,
        id_generator: IdGeneratorProtocol,
        transaction_manager: TransactionManager,
    ) -> RegisterUserCommand:
        return RegisterUserCommand(
            repository=repository,
            password_hasher=password_hasher,
            id_generator=id_generator,
            transaction_manager=transaction_manager,
        )

    @provide(scope=Scope.REQUEST)
    def get_update_user_command(
        self,
        repository: UserRepositoryProtocol,
        transaction_manager: TransactionManager,
    ) -> UpdateUserCommand:
        return UpdateUserCommand(
            repository=repository,
            transaction_manager=transaction_manager,
        )

    @provide(scope=Scope.REQUEST)
    def get_user_by_id_query(
        self,
        user_repository: UserRepositoryProtocol,
    ) -> GetUserByIdQuery:
        return GetUserByIdQuery(
            user_repository=user_repository,
        )


class AuthProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_authenticate_user_command(
        self,
        user_repository: UserRepositoryProtocol,
        password_hasher: PasswordHasherProtocol,
        jwt_handler: JWTHandlerProtocol,
    ) -> AuthenticateUserCommand:
        return AuthenticateUserCommand(
            user_repository=user_repository,
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