from uuid import UUID, uuid4

from services.shared.domain.id_generator import IdGeneratorProtocol


class UuidGenerator(IdGeneratorProtocol):
    def generate_id(self) -> UUID:
        return uuid4()