from microservices.shared.domain.exceptions import (
    AuthenticationError,
    AuthorizationError,
    ConflictError,
    NotFoundError,
)


class UserNotFound(NotFoundError):
    """Raised when a user is not found."""
    def __init__(self, user_id=None):
        message = f"User with id {user_id} not found" if user_id else "User not found"
        super().__init__(message)


class UserAlreadyExistsError(ConflictError):
    """Raised when attempting to create a user that already exists."""
    def __init__(self, message="User already exists"):
        super().__init__(message)


class InvalidCredentialsError(AuthenticationError):
    """Raised when user credentials are invalid."""
    def __init__(self):
        super().__init__("Invalid credentials")


class UnauthorizedUserError(AuthorizationError):
    """Raised when a user is not authorized to perform an action."""
    def __init__(self):
        super().__init__("User not authorized")