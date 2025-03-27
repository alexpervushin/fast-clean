from dataclasses import dataclass


@dataclass
class CreateUserInputDTO:
    name: str
    email: str
    password: str

@dataclass
class UpdateUserInputDTO:
    name: str
    email: str

@dataclass
class UpdateUserOutputDTO:
    name: str
    email: str