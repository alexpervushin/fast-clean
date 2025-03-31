from dataclasses import dataclass
from typing import Optional
from uuid import UUID


@dataclass
class CreateUserInputDTO:
    name: str
    email: str
    password: str

@dataclass
class UpdateUserInputDTO:
    name: Optional[str] = None
    email: Optional[str] = None

@dataclass
class UpdateUserOutputDTO:
    name: str
    email: str

@dataclass
class UserOutputDTO:
    id: UUID
    name: str
    email: str

