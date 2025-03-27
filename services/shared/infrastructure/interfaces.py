from collections.abc import Sequence
from typing import (
    Any,
    Optional,
    Protocol,
    TypeVar,
    Union,
)

from sqlalchemy.engine import Result
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql import Select

T = TypeVar("T")
M = TypeVar("M", bound=DeclarativeBase)


# Порт определяется внутренним слоем, однако для удобства интерфейс находится здесь. Этот протокол тесно связан с SQLalchemy


class AsyncSessionProtocol(Protocol):
    async def commit(self) -> None: ...

    async def rollback(self) -> None: ...

    def add(self, instance: Any) -> None: ...

    async def refresh(self, instance: Any) -> None: ...

    async def get(
        self,
        entity: type[M],
        ident: Any,
        *,
        options: Optional[Sequence[Any]] = None,
    ) -> Optional[M]: ...

    async def execute(
        self,
        statement: Union[Select[Any], Any],
        params: Optional[dict[str, Any]] = None,
    ) -> Result[Any]: ...
