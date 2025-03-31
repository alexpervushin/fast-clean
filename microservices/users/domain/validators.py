from microservices.users.domain.exceptions import (
    NotFoundError,
    UserAlreadyExistsError,
)
from microservices.users.domain.ports import UserRepositoryProtocol


class UserValidator:
    @staticmethod
    async def check_email_unique(email: str, repo: UserRepositoryProtocol) -> None:
        try:
            await repo.get_by_email(email)
        except NotFoundError:
            return
        raise UserAlreadyExistsError(f"User with email {email} already exists")