from dataclasses import dataclass
from typing import Any, Dict, Optional
from uuid import UUID

from microservices.settings.domain.value_objects import DataSourceType


@dataclass
class AddDataSourceInputDTO:
    user_id: UUID
    type: DataSourceType
    name: str
    config: Dict[str, Any]
    is_enabled: Optional[bool] = True


@dataclass
class UpdateDataSourceInputDTO:
    name: Optional[str] = None
    config: Optional[Dict[str, Any]] = None
    is_enabled: Optional[bool] = None


@dataclass
class DataSourceOutputDTO:
    id: UUID
    user_id: UUID
    type: DataSourceType
    name: str
    config: Dict[str, Any]
    is_enabled: bool