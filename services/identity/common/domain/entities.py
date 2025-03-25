from dataclasses import dataclass
from services.shared.domain.base_entity import BaseEntity

@dataclass
class User(BaseEntity):
    name: str
    email: str
    hashed_password: str

    def change_name(self, new_name: str) -> None:
        self.name = new_name

    def change_email(self, new_email: str) -> None:
        self.email = new_email