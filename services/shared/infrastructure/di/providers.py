from typing import AsyncGenerator

from dishka import Provider, Scope, provide
from pydantic_settings import BaseSettings
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from services.shared.domain.id_generator import IdGeneratorProtocol
from services.shared.domain.security import PasswordHasherProtocol
from services.shared.infrastructure.database import (
    TransactionManager,
    create_async_session_maker,
    create_engine,
)
from services.shared.infrastructure.id_generator import UuidGenerator
from services.shared.infrastructure.interfaces import AsyncSessionProtocol
from services.shared.infrastructure.security import ArgonPasswordHasher


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


class SharedPasswordHasherProvider(Provider):
    @provide(scope=Scope.APP)
    def get_password_hasher(self) -> PasswordHasherProtocol:
        return ArgonPasswordHasher()


class SharedIdGeneratorProvider(Provider):
    @provide(scope=Scope.APP)
    def get_id_generator(self) -> IdGeneratorProtocol:
        return UuidGenerator()