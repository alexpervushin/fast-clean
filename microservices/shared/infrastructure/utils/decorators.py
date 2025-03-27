import functools
from typing import Any, Callable, Concatenate, Coroutine, TypeVar

from typing_extensions import ParamSpec

from microservices.shared.infrastructure.database.session import TransactionManager

P = ParamSpec("P")
R = TypeVar("R")
T = TypeVar("T", bound=Any)


def manage_transaction(
    func: Callable[Concatenate[T, P], Coroutine[Any, Any, R]],
) -> Callable[Concatenate[T, P], Coroutine[Any, Any, R]]:
    @functools.wraps(func)
    async def wrapper(self: T, *args: P.args, **kwargs: P.kwargs) -> R:
        if not hasattr(self, "transaction_manager") or not isinstance(
            self.transaction_manager, TransactionManager
        ):
            raise AttributeError(
                f"{self.__class__.__name__} instance must have a 'transaction_manager' attribute of type TransactionManager"
            )

        async with self.transaction_manager:
            result = await func(self, *args, **kwargs)
        return result
    return wrapper