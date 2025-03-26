from services.identity.modules.users.domain.exceptions import (
    NotFoundError,
    UserAlreadyExistsError,
)
from services.identity.modules.users.domain.repositories import UserRepositoryProtocol


class UserValidator:
    @staticmethod
    async def check_email_unique(email: str, repo: UserRepositoryProtocol) -> None:
        try:
            await repo.get_by_email(email)
        except NotFoundError:
            return
        raise UserAlreadyExistsError
