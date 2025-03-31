from uuid import UUID

from microservices.users.application.dtos import UserOutputDTO
from microservices.users.domain.ports import UserRepositoryProtocol


class GetUserByIdQuery:
    def __init__(self, user_repository: UserRepositoryProtocol):
        self.user_repository = user_repository

    async def __call__(self, user_id: UUID) -> UserOutputDTO:
        user = await self.user_repository.get_by_id(user_id)
        return UserOutputDTO(
            id=user.id,
            name=user.name,
            email=user.email,
        )


