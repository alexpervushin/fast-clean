from abc import ABC, abstractmethod
from typing import Generic, Type, TypeVar
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import attributes

from microservices.shared.domain.entities import BaseEntity
from microservices.shared.domain.exceptions import NotFoundError
from microservices.shared.domain.repositories import BaseRepositoryProtocol
from microservices.shared.domain.value_objects import Pagination
from microservices.shared.infrastructure.database.orm import BaseModel
from microservices.shared.infrastructure.database.session import (
    AsyncSessionProtocol,
)

D = TypeVar("D", bound=BaseEntity)
M = TypeVar("M", bound=BaseModel)


class BaseRepository(Generic[D, M], BaseRepositoryProtocol[D], ABC):
    model_type: Type[M]

    def __init__(self, db: AsyncSessionProtocol) -> None:
        if not hasattr(self, "model_type"):
            raise NotImplementedError(
                "Subclasses must define the 'model_type' class attribute."
            )
        self.db = db

    @abstractmethod
    def _map_to_orm(self, domain_obj: D) -> M: ...

    @abstractmethod
    def _map_to_domain(self, orm_obj: M) -> D: ...

    async def get_by_id(self, obj_id: UUID) -> D:
        orm_obj = await self.db.get(self.model_type, obj_id)

        if orm_obj is None:
            msg = f"{self.model_type.__name__} with ID {obj_id} not found"
            raise NotFoundError(msg)

        return self._map_to_domain(orm_obj)

    async def get_all(self) -> list[D]:
        stmt = select(self.model_type)
        result = await self.db.execute(stmt)
        orm_objs = result.scalars().all()
        return [self._map_to_domain(orm_obj) for orm_obj in orm_objs]

    async def get_all_paginated(self, pagination: Pagination) -> list[D]:
        stmt = select(self.model_type).limit(pagination.limit).offset(pagination.offset)
        result = await self.db.execute(stmt)
        orm_objs = result.scalars().all()
        return [self._map_to_domain(orm_obj) for orm_obj in orm_objs]

    async def create(self, domain_obj: D) -> D:
        orm_obj = self._map_to_orm(domain_obj)
        self.db.add(orm_obj)
        await self.db.flush([orm_obj])
        await self.db.refresh(orm_obj)
        return self._map_to_domain(orm_obj)

    async def update(self, domain_obj: D) -> D:
        orm_obj_to_merge = self._map_to_orm(domain_obj)
        merged_orm_obj = await self.db.merge(orm_obj_to_merge)
        if merged_orm_obj not in self.db.dirty and not attributes.instance_state(merged_orm_obj).transient:
             pass
        else:
             await self.db.flush([merged_orm_obj])

        return self._map_to_domain(merged_orm_obj)


    async def delete(self, obj_id: UUID) -> None:
        orm_obj = await self.db.get(self.model_type, obj_id)

        if orm_obj is None:
            raise NotFoundError(
                f"{self.model_type.__name__} with id {obj_id} not found for deletion"
            )

        await self.db.delete(orm_obj)
