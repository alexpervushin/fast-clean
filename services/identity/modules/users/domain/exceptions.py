from services.identity.core.domain.exceptions import (
    AuthenticationError,
    AuthorizationError,
    ConflictError,
    NotFoundError,
)


class UserNotFound(NotFoundError):
    """Raised when a user is not found."""


class UserAlreadyExistsError(ConflictError):
    """Raised when attempting to create a user that already exists."""


class InvalidCredentialsError(AuthenticationError):
    """Raised when user credentials are invalid."""


class UnauthorizedUserError(AuthorizationError):
    """Raised when a user is not authorized to perform an action."""