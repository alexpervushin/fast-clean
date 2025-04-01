from dataclasses import dataclass, field
from typing import Any, Dict
from uuid import UUID

from microservices.shared.domain.entities import BaseEntity
from microservices.settings.domain.value_objects import DataSourceType


@dataclass
class DataSource(BaseEntity):
    user_id: UUID
    type: DataSourceType
    name: str
    config: Dict[str, Any] = field(default_factory=dict)
    is_enabled: bool = True

    def update_config(self, new_config: Dict[str, Any]) -> None:
        self.config = new_config

    def update_name(self, new_name: str) -> None:
        self.name = new_name

    def enable(self) -> None:
        self.is_enabled = True

    def disable(self) -> None:
        self.is_enabled = False