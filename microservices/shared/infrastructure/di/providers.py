from typing import AsyncGenerator

from dishka import Provider, Scope, provide
from pydantic_settings import BaseSettings
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from microservices.shared.domain.id_generator import IdGeneratorProtocol
from microservices.shared.domain.security import PasswordHasherProtocol
from microservices.shared.infrastructure.config import JWT as JWTSettings
from microservices.shared.infrastructure.database.session import (
    AsyncSessionProtocol,
    TransactionManager,
    create_async_session_maker,
    create_engine,
)
from microservices.shared.infrastructure.security.jwt_handler import (
    JWTHandlerProtocol,
    PyJWTHandler,
)
from microservices.shared.infrastructure.security.password_hasher import (
    ArgonPasswordHasher,
)
from microservices.shared.infrastructure.utils.id_generator import UuidGenerator


class SharedDatabaseProvider(Provider):
    @provide(scope=Scope.APP)
    def get_engine(self, settings: BaseSettings) -> AsyncEngine:
        if not hasattr(settings, "postgres"):
            raise AttributeError("Settings object must have a 'postgres' attribute")
        return create_engine(settings)

    @provide(scope=Scope.APP)
    def get_session_maker(
        self,
        engine: AsyncEngine,
    ) -> async_sessionmaker[AsyncSession]:
        return create_async_session_maker(engine)

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self,
        session_maker: async_sessionmaker[AsyncSession],
    ) -> AsyncGenerator[AsyncSession, None]:
        async with session_maker() as session:
            yield session

    @provide(scope=Scope.REQUEST)
    def get_transaction_manager(
        self,
        session: AsyncSessionProtocol,
    ) -> TransactionManager:
        return TransactionManager(session)

    @provide(scope=Scope.REQUEST)
    async def get_async_session_protocol(
        self,
        session: AsyncSession,
    ) -> AsyncSessionProtocol:
        return session


class SharedIdGeneratorProvider(Provider):
    @provide(scope=Scope.APP)
    def get_id_generator(self) -> IdGeneratorProtocol:
        return UuidGenerator()


class SharedSecurityProvider(Provider):
    @provide(scope=Scope.APP)
    def get_jwt_settings(self, settings: BaseSettings) -> JWTSettings:
        if not hasattr(settings, "jwt"):
             raise AttributeError("Settings object must have a 'jwt' attribute")
        return settings.jwt

    @provide(scope=Scope.APP)
    def get_jwt_handler(self, jwt_settings: JWTSettings) -> JWTHandlerProtocol:
        return PyJWTHandler(settings=jwt_settings)

    @provide(scope=Scope.APP)
    def get_password_hasher(self) -> PasswordHasherProtocol:
        return ArgonPasswordHasher()