from typing import (
    Any,
    Optional,
)

import sqlalchemy.pool
from pydantic_settings import BaseSettings
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from services.shared.infrastructure.interfaces import AsyncSessionProtocol


def create_engine(settings: BaseSettings) -> AsyncEngine:
    return create_async_engine(
        settings.postgres.url,
        poolclass=sqlalchemy.pool.AsyncAdaptedQueuePool,
    )


def create_async_session_maker(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )


class TransactionManager:
    def __init__(self, session: AsyncSessionProtocol) -> None:
        self._session = session

    async def __aenter__(self) -> "TransactionManager":
        return self

    async def __aexit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[Any],
    ) -> None:
        if exc_type is not None:
            await self._session.rollback()
        else:
            await self._session.commit()

    @property
    def session(self) -> AsyncSessionProtocol:
        return self._session
