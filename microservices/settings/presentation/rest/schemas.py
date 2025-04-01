from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, model_validator

from microservices.settings.domain.value_objects import DataSourceType


class DataSourceBase(BaseModel):
    type: DataSourceType
    name: str
    config: Dict[str, Any]
    is_enabled: Optional[bool]


class AddDataSourceRequest(DataSourceBase):
    pass


class UpdateDataSourceRequest(BaseModel):
    name: Optional[str]
    config: Optional[Dict[str, Any]]
    is_enabled: Optional[bool]

    @model_validator(mode='after')
    def check_at_least_one_field_present(self) -> 'UpdateDataSourceRequest':
        if self.name is None and self.config is None and self.is_enabled is None:
            raise ValueError("At least one field (name, config, is_enabled) must be provided for update.")
        return self


class DataSourceResponse(BaseModel):
    id: UUID
    type: DataSourceType
    name: str
    config: Dict[str, Any]
    is_enabled: bool



class ListDataSourcesResponse(BaseModel):
    data: List[DataSourceResponse]