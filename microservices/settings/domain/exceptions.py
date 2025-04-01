from microservices.shared.domain.exceptions import NotFoundError, ConflictError


class DataSourceNotFound(NotFoundError):
    def __init__(self, source_id: str | None = None, user_id: str | None = None):
        if source_id:
            message = f"Data source with id {source_id} not found"
            if user_id:
                message += f" for user {user_id}"
        elif user_id:
            message = f"No data sources found for user {user_id}"
        else:
            message = "Data source not found"
        super().__init__(message)


class InvalidDataSourceTypeError(ConflictError):
    def __init__(self, type_provided: str):
        message = f"Invalid or unsupported data source type: {type_provided}"
        super().__init__(message)

class InvalidDataSourceConfigError(ConflictError):
    def __init__(self, source_type: str, error_details: str):
        message = f"Invalid configuration for data source type '{source_type}': {error_details}"
        super().__init__(message)