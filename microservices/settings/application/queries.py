from uuid import UUID

from microservices.settings.application.dtos import DataSourceOutputDTO
from microservices.settings.domain.ports import DataSourceRepositoryProtocol


class GetDataSourceByIdQuery:
    def __init__(self, repository: DataSourceRepositoryProtocol):
        self.repository = repository

    async def __call__(self, source_id: UUID, user_id: UUID) -> DataSourceOutputDTO:
        data_source = await self.repository.get_by_id_and_user(source_id, user_id)
        return DataSourceOutputDTO(
            id=data_source.id,
            user_id=data_source.user_id,
            type=data_source.type,
            name=data_source.name,
            config=data_source.config,
            is_enabled=data_source.is_enabled,
        )


class ListDataSourcesQuery:
    def __init__(self, repository: DataSourceRepositoryProtocol):
        self.repository = repository

    async def __call__(self, user_id: UUID) -> list[DataSourceOutputDTO]:
        data_sources = await self.repository.get_all_by_user(user_id)
        return [
            DataSourceOutputDTO(
                id=ds.id,
                user_id=ds.user_id,
                type=ds.type,
                name=ds.name,
                config=ds.config,
                is_enabled=ds.is_enabled,
            )
            for ds in data_sources
        ]