from typing import Protocol
from uuid import UUID


class IdGeneratorProtocol(Protocol):
    def generate_id(self) -> UUID: ...