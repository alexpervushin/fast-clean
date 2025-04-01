from typing import Protocol
from uuid import UUID

from microservices.shared.domain.ports import BaseRepositoryProtocol
from microservices.settings.domain.entities import DataSource


class DataSourceRepositoryProtocol(BaseRepositoryProtocol[DataSource], Protocol):
    async def get_by_id_and_user(self, source_id: UUID, user_id: UUID) -> DataSource: ...

    async def get_all_by_user(self, user_id: UUID) -> list[DataSource]: ...

    async def delete_by_id_and_user(self, source_id: UUID, user_id: UUID) -> None: ...