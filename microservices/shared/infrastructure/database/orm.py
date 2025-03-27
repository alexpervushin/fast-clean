import uuid

from sqlalchemy import UUID as UUID_SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class BaseModel(DeclarativeBase):
    id: Mapped[uuid.UUID] = mapped_column(
        UUID_SQLAlchemy(as_uuid=True),
        primary_key=True,
        nullable=False,
    )