from uuid import UUID

from microservices.shared.domain.id_generator import IdGeneratorProtocol
from microservices.shared.domain.security import PasswordHasherProtocol
from microservices.users.application.dtos import (
    CreateUserInputDTO,
    UpdateUserInputDTO,
    UpdateUserOutputDTO,
)
from microservices.users.application.interfaces import (
    RegisterUserInteractorProtocol,
    UpdateUserInteractorProtocol,
)
from microservices.users.domain.entities import User
from microservices.users.domain.repositories import (
    UserRepositoryProtocol,
)
from microservices.users.domain.validators import UserValidator


class RegisterUserInteractor(RegisterUserInteractorProtocol):
    def __init__(
        self,
        repository: UserRepositoryProtocol,
        password_hasher: PasswordHasherProtocol,
        dto: CreateUserInputDTO,
        id_generator: IdGeneratorProtocol,
    ):
        self.repository = repository
        self.password_hasher = password_hasher
        self.id_generator = id_generator
        self.name = dto.name
        self.email = dto.email
        self.password = dto.password

    async def __call__(self) -> None:
        await UserValidator.check_email_unique(self.email, self.repository)
        hashed_password = await self.password_hasher.hash(self.password)

        new_user_id = self.id_generator.generate_id()

        user = User(
            id=new_user_id,
            name=self.name,
            email=self.email,
            hashed_password=hashed_password,
        )
        await self.repository.create(user)


class UpdateUserInteractor(UpdateUserInteractorProtocol):
    def __init__(
        self,
        repository: UserRepositoryProtocol,
        dto: UpdateUserInputDTO,
        user_id: UUID
    ) -> None:
        self.repository = repository
        self.user_id = user_id
        self.name = dto.name
        self.email = dto.email

    async def __call__(self) -> UpdateUserOutputDTO:
        user = await self.repository.get_by_id(self.user_id)

        email_changed = False
        if self.email is not None and user.email != self.email:
            await UserValidator.check_email_unique(self.email, self.repository)
            user.change_email(self.email)
            email_changed = True

        name_changed = False
        if self.name is not None and user.name != self.name:
            user.change_name(self.name)
            name_changed = True

        if email_changed or name_changed:
            await self.repository.update(user)

        dto = UpdateUserOutputDTO(
            name=user.name,
            email=user.email,
        )

        return dto