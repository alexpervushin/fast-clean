class DomainException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class NotFoundError(DomainException):
    """Base exception for all not found errors."""


class ConflictError(DomainException):
    """Base exception for all conflict errors."""


class ValidationError(DomainException):
    """Base exception for all validation errors."""


class AuthenticationError(DomainException):
    """Base exception for all authentication errors."""


class AuthorizationError(DomainException):
    """Base exception for all authorization errors."""