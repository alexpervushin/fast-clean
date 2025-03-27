from uuid import UUID

from microservices.shared.domain.id_generator import IdGeneratorProtocol
from microservices.shared.domain.security import PasswordHasherProtocol
from microservices.shared.infrastructure.database.session import TransactionManager
from microservices.shared.infrastructure.utils.decorators import manage_transaction
from microservices.users.application.commands import (
    RegisterUserInteractor,
    UpdateUserInteractor,
)
from microservices.users.application.dtos import (
    CreateUserInputDTO,
    UpdateUserInputDTO,
    UpdateUserOutputDTO,
)
from microservices.users.application.interfaces import UserServiceProtocol
from microservices.users.domain.repositories import UserRepositoryProtocol


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

    @manage_transaction
    async def register_user(self, dto: CreateUserInputDTO) -> None:
        interactor = RegisterUserInteractor(
            repository=self.repository,
            password_hasher=self.password_hasher,
            dto=dto,
            id_generator=self.id_generator,
        )
        await interactor()

    @manage_transaction
    async def update_user(
        self, dto: UpdateUserInputDTO, user_id: UUID
    ) -> UpdateUserOutputDTO:
        interactor = UpdateUserInteractor(
            repository=self.repository,
            dto=dto,
            user_id=user_id,
        )
        result = await interactor()
        return result