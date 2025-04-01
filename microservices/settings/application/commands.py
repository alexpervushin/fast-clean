from typing import Any, Dict
from uuid import UUID

from microservices.shared.domain.ports import IdGeneratorProtocol
from microservices.shared.infrastructure.database.session import TransactionManager
from microservices.shared.infrastructure.utils.decorators import manage_transaction
from microservices.settings.application.dtos import (
    AddDataSourceInputDTO,
    DataSourceOutputDTO,
    UpdateDataSourceInputDTO,
)
from microservices.settings.domain.entities import DataSource
from microservices.settings.domain.exceptions import (
    InvalidDataSourceTypeError,
)
from microservices.settings.domain.ports import DataSourceRepositoryProtocol
from microservices.settings.domain.value_objects import (
    DATA_SOURCE_CONFIG_MAP,
    DataSourceType,
)


def _validate_config(
    source_type: DataSourceType, config: Dict[str, Any]
) -> Dict[str, Any]:
    if source_type not in DATA_SOURCE_CONFIG_MAP:
        raise InvalidDataSourceTypeError(str(source_type))

    return config


class AddDataSourceCommand:
    def __init__(
        self,
        repository: DataSourceRepositoryProtocol,
        id_generator: IdGeneratorProtocol,
        transaction_manager: TransactionManager,
    ):
        self.repository = repository
        self.id_generator = id_generator
        self.transaction_manager = transaction_manager

    @manage_transaction
    async def __call__(self, dto: AddDataSourceInputDTO) -> DataSourceOutputDTO:
        validated_config = _validate_config(dto.type, dto.config)

        new_id = self.id_generator.generate_id()
        data_source = DataSource(
            id=new_id,
            user_id=dto.user_id,
            type=dto.type,
            name=dto.name,
            config=validated_config,
            is_enabled=dto.is_enabled if dto.is_enabled is not None else True,
        )
        created_source = await self.repository.create(data_source)
        return DataSourceOutputDTO(
            id=created_source.id,
            user_id=created_source.user_id,
            type=created_source.type,
            name=created_source.name,
            config=created_source.config,
            is_enabled=created_source.is_enabled,
        )


class UpdateDataSourceCommand:
    def __init__(
        self,
        repository: DataSourceRepositoryProtocol,
        transaction_manager: TransactionManager,
    ):
        self.repository = repository
        self.transaction_manager = transaction_manager

    @manage_transaction
    async def __call__(
        self, source_id: UUID, user_id: UUID, dto: UpdateDataSourceInputDTO
    ) -> DataSourceOutputDTO:
        data_source = await self.repository.get_by_id_and_user(source_id, user_id)
        updated = False
        if dto.name is not None and data_source.name != dto.name:
            data_source.update_name(dto.name)
            updated = True

        if dto.config is not None:
            validated_config = _validate_config(data_source.type, dto.config)
            if data_source.config != validated_config:
                 data_source.update_config(validated_config)
                 updated = True

        if dto.is_enabled is not None and data_source.is_enabled != dto.is_enabled:
            if dto.is_enabled:
                data_source.enable()
            else:
                data_source.disable()
            updated = True

        if updated:
            updated_source = await self.repository.update(data_source)
        else:
            updated_source = data_source

        return DataSourceOutputDTO(
            id=updated_source.id,
            user_id=updated_source.user_id,
            type=updated_source.type,
            name=updated_source.name,
            config=updated_source.config,
            is_enabled=updated_source.is_enabled,
        )


class DeleteDataSourceCommand:
    def __init__(
        self,
        repository: DataSourceRepositoryProtocol,
        transaction_manager: TransactionManager,
    ):
        self.repository = repository
        self.transaction_manager = transaction_manager

    @manage_transaction
    async def __call__(self, source_id: UUID, user_id: UUID) -> None:
        await self.repository.delete_by_id_and_user(source_id, user_id)