from uuid import UUID

from microservices.shared.domain.ports import (
    IdGeneratorProtocol,
    PasswordHasherProtocol,
)
from microservices.shared.infrastructure.database.session import TransactionManager
from microservices.shared.infrastructure.security.jwt_handler import JWTHandlerProtocol
from microservices.shared.infrastructure.utils.decorators import manage_transaction
from microservices.users.application.dtos import (
    CreateUserInputDTO,
    UpdateUserInputDTO,
    UpdateUserOutputDTO,
)
from microservices.users.domain.entities import User
from microservices.users.domain.exceptions import InvalidCredentialsError
from microservices.users.domain.ports import UserRepositoryProtocol
from microservices.users.domain.validators import UserValidator


class RegisterUserCommand:
    def __init__(
        self,
        repository: UserRepositoryProtocol,
        password_hasher: PasswordHasherProtocol,
        id_generator: IdGeneratorProtocol,
        transaction_manager: TransactionManager,
    ):
        self.repository = repository
        self.password_hasher = password_hasher
        self.id_generator = id_generator
        self.transaction_manager = transaction_manager

    @manage_transaction
    async def __call__(self, dto: CreateUserInputDTO) -> None:
        await UserValidator.check_email_unique(dto.email, self.repository)
        hashed_password = await self.password_hasher.hash(dto.password)
        new_user_id = self.id_generator.generate_id()

        user = User(
            id=new_user_id,
            name=dto.name,
            email=dto.email,
            hashed_password=hashed_password,
        )
        await self.repository.create(user)


class UpdateUserCommand:
    def __init__(
        self,
        repository: UserRepositoryProtocol,
        transaction_manager: TransactionManager,
    ) -> None:
        self.repository = repository
        self.transaction_manager = transaction_manager

    @manage_transaction
    async def __call__(self, user_id: UUID, dto: UpdateUserInputDTO) -> UpdateUserOutputDTO:
        user = await self.repository.get_by_id(user_id)

        email_changed = False
        if dto.email is not None and user.email != dto.email:
            await UserValidator.check_email_unique(dto.email, self.repository)
            user.change_email(dto.email)
            email_changed = True

        name_changed = False
        if dto.name is not None and user.name != dto.name:
            user.change_name(dto.name)
            name_changed = True

        if email_changed or name_changed:
            await self.repository.update(user)

        output_dto = UpdateUserOutputDTO(
            name=user.name,
            email=user.email,
        )
        return output_dto


class AuthenticateUserCommand:
    def __init__(
        self,
        user_repository: UserRepositoryProtocol,
        password_hasher: PasswordHasherProtocol,
        jwt_handler: JWTHandlerProtocol,
    ):
        self.user_repository = user_repository
        self.password_hasher = password_hasher
        self.jwt_handler = jwt_handler

    async def __call__(self, email: str, password: str) -> str:
        try:
            user = await self.user_repository.get_by_email(email)
        except Exception:
            raise InvalidCredentialsError()

        is_valid_password = await self.password_hasher.verify(
            password, user.hashed_password
        )
        if not is_valid_password:
            raise InvalidCredentialsError()

        access_token = self.jwt_handler.create_access_token(user_id=user.id)
        return access_token