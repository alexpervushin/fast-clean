from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from microservices.shared.infrastructure.database.orm import BaseModel


class UserModel(BaseModel):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)