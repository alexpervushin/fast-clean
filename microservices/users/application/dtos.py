from dataclasses import dataclass
from typing import Optional


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