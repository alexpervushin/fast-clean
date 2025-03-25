from uuid import uuid4

from services.identity.common.domain.entities import User
from services.identity.modules.users.application.dtos import (
    CreateUserInputDTO,
    UpdateUserInputDTO,
    UpdateUserOutputDTO,
)
from services.identity.modules.users.domain.repositories import UserRepositoryProtocol
from services.identity.modules.users.domain.validators import UserValidator


class RegisterUserInteractor:
    def __init__(
            self,
            repository: UserRepositoryProtocol,
            password_hasher: PasswordHasher,
            dto: CreateUserInputDTO
    ):
        self.repository = repository
        self.password_hasher = password_hasher
        self.name = dto.name
        self.email = dto.email
        self.password = dto.password

    async def __call__(self) -> None:
        await UserValidator.check_email_unique(self.email, self.repository)
        hashed_password = await self.password_hasher.hash_password(self.password)
        user = User(
            id=uuid4(),
            name=self.name,
            email=self.email,
            hashed_password=hashed_password
        )
        await self.repository.create(user)


class UpdateUserInteractor:
    def __init__(self, repository: UserRepositoryProtocol, dto: UpdateUserInputDTO, user_id) -> None:
        self.repository = repository
        self.user_id = user_id
        self.name = dto.name
        self.email = dto.email

    async def __call__(self) -> UpdateUserOutputDTO:
        user = await self.repository.get_by_id(self.user_id)

        if self.email is not None and user.email != self.email:
            await UserValidator.check_email_unique(self.email, self.repository)
            user.change_email(self.email)

        if self.name is not None:
            user.name = self.name

        await self.repository.update(user)
        return user

