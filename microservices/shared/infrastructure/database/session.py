from collections.abc import Sequence
from typing import (
    Any,
    Optional,
    Protocol,
    TypeVar,
    Union,
)

import sqlalchemy.pool
from pydantic_settings import BaseSettings
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql import Select

T = TypeVar("T")
M = TypeVar("M", bound=DeclarativeBase)


class AsyncSessionProtocol(Protocol):
    async def commit(self) -> None: ...

    async def rollback(self) -> None: ...

    def add(self, instance: Any) -> None: ...

    async def delete(self, instance: Any) -> None: ...

    async def flush(self, objects: Optional[Sequence[Any]] = None) -> None: ...

    async def refresh(self, instance: Any) -> None: ...

    async def get(
        self,
        entity: type[M],
        ident: Any,
        *,
        options: Optional[Sequence[Any]] = None,
    ) -> Optional[M]: ...

    async def merge(self, instance: Any) -> Any: ...

    async def execute(
        self,
        statement: Union[Select[Any], Any],
        params: Optional[dict[str, Any]] = None,
    ) -> Result[Any]: ...



def create_engine(settings: BaseSettings) -> AsyncEngine:
    return create_async_engine(
        settings.postgres.url, # noqa
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
