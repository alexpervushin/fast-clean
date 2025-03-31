from microservices.shared.domain.security import PasswordHasherProtocol
from microservices.shared.infrastructure.security.jwt_handler import JWTHandlerProtocol
from microservices.users.domain.exceptions import InvalidCredentialsError
from microservices.users.domain.repositories import UserRepositoryProtocol

# TODO: add interactor


class AuthService:
    def __init__(
        self,
        user_repository: UserRepositoryProtocol,
        password_hasher: PasswordHasherProtocol,
        jwt_handler: JWTHandlerProtocol,
    ):
        self.user_repository = user_repository
        self.password_hasher = password_hasher
        self.jwt_handler = jwt_handler

    async def authenticate_user(self, email: str, password: str) -> str:
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