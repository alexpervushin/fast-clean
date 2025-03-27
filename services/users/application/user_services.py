from services.shared.domain.id_generator import IdGeneratorProtocol
from services.shared.domain.security import PasswordHasherProtocol
from services.shared.infrastructure.database import TransactionManager
from services.users.application.commands import (
    RegisterUserInteractor,
    UpdateUserInteractor,
)
from services.users.application.dtos import (
    CreateUserInputDTO,
    UpdateUserInputDTO,
    UpdateUserOutputDTO,
)
from services.users.application.interfaces import UserServiceProtocol
from services.users.domain.repositories import UserRepositoryProtocol


class UserService(UserServiceProtocol):
    def __init__(
        self,
        repository: UserRepositoryProtocol,
        transaction_manager: TransactionManager,
        password_hasher: PasswordHasherProtocol,
        id_generator: IdGeneratorProtocol,
    ):
        self.repository = repository
        self.transaction_manager = transaction_manager
        self.password_hasher = password_hasher
        self.id_generator = id_generator

    async def register_user(self, dto: CreateUserInputDTO) -> None:
        async with self.transaction_manager:
            interactor = RegisterUserInteractor(
                repository=self.repository,
                password_hasher=self.password_hasher,
                dto=dto,
                id_generator=self.id_generator,
            )
            result = await interactor()
            return result

    async def update_user(
        self, dto: UpdateUserInputDTO, user_id
    ) -> UpdateUserOutputDTO:
        async with self.transaction_manager:
            interactor = UpdateUserInteractor(
                repository=self.repository,
                dto=dto,
                user_id=user_id,
            )
            result = await interactor()
            return result