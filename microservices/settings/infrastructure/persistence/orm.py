from sqlalchemy import UUID as UUID_SQLAlchemy
from sqlalchemy import Boolean, Enum, JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from microservices.shared.infrastructure.database.orm import BaseModel
from microservices.settings.domain.value_objects import DataSourceType


class DataSourceModel(BaseModel):
    __tablename__ = "data_sources"

    user_id: Mapped[UUID_SQLAlchemy] = mapped_column(
        UUID_SQLAlchemy(as_uuid=True), nullable=False, index=True
    )
    type: Mapped[DataSourceType] = mapped_column(Enum(DataSourceType), nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    config: Mapped[dict] = mapped_column(JSON, nullable=False, default=lambda: {})
    is_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
