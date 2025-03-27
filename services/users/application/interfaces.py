from typing import Protocol

from services.users.application.dtos import (
    CreateUserInputDTO,
    UpdateUserInputDTO,
    UpdateUserOutputDTO,
)


class RegisterUserInteractorProtocol(Protocol):
    async def __call__(self) -> None: ...


class UpdateUserInteractorProtocol(Protocol):
    async def __call__(self) -> UpdateUserOutputDTO: ...


class UserServiceProtocol(Protocol):
    async def register_user(self, dto: CreateUserInputDTO) -> None: ...

    async def update_user(
        self, dto: UpdateUserInputDTO, user_id
    ) -> UpdateUserOutputDTO: ...