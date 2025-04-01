from uuid import UUID

from sqlalchemy import delete, select

from microservices.shared.infrastructure.database.repositories import BaseRepository
from microservices.settings.domain.entities import DataSource
from microservices.settings.domain.exceptions import DataSourceNotFound
from microservices.settings.domain.ports import DataSourceRepositoryProtocol
from microservices.settings.infrastructure.persistence.orm import DataSourceModel


class DataSourceRepository(
    BaseRepository[DataSource, DataSourceModel], DataSourceRepositoryProtocol
):
    model_type = DataSourceModel

    def _map_to_domain(self, obj: DataSourceModel) -> DataSource:
        return DataSource(
            id=obj.id,
            user_id=obj.user_id,
            type=obj.type,
            name=obj.name,
            config=obj.config,
            is_enabled=obj.is_enabled,
        )

    def _map_to_orm(self, obj: DataSource) -> DataSourceModel:
        config_dict = obj.config if isinstance(obj.config, dict) else {}
        return DataSourceModel(
            id=obj.id,
            user_id=obj.user_id,
            type=obj.type,
            name=obj.name,
            config=config_dict,
            is_enabled=obj.is_enabled,
        )

    async def get_by_id_and_user(self, source_id: UUID, user_id: UUID) -> DataSource:
        stmt = select(self.model_type).where(
            self.model_type.id == source_id, self.model_type.user_id == user_id
        )
        result = (await self.db.execute(stmt)).scalar_one_or_none()
        if result is None:
            raise DataSourceNotFound(source_id=str(source_id), user_id=str(user_id))
        return self._map_to_domain(result)

    async def get_all_by_user(self, user_id: UUID) -> list[DataSource]:
        stmt = select(self.model_type).where(self.model_type.user_id == user_id)
        result = await self.db.execute(stmt)
        orm_objs = result.scalars().all()
        return [self._map_to_domain(orm_obj) for orm_obj in orm_objs]

    async def delete_by_id_and_user(self, source_id: UUID, user_id: UUID) -> None:
        await self.get_by_id_and_user(source_id, user_id)
        stmt = delete(self.model_type).where(
            self.model_type.id == source_id, self.model_type.user_id == user_id
        )
        await self.db.execute(stmt)
