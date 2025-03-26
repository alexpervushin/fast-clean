from services.identity.core.domain.exceptions import DomainException


class AppException(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class DomainToAppExceptionTranslator:
    @staticmethod
    def translate(domain_exception: DomainException) -> AppException:
        return AppException(domain_exception.message)