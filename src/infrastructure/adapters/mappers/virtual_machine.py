from domain.entities.user import UserId
from domain.entities.virtual_machine import VirtualMachine, VirtualMachineId
from infrastructure.models.sqlalchemy import VirtualMachine as ORMVirtualMachine


class SQLAlchemyVirtualMachineMapper:
    def __init__(self) -> None:
        self._source_dtos: dict[VirtualMachineId, ORMVirtualMachine] = {}

    def to_dto(self, domain: VirtualMachine) -> ORMVirtualMachine:
        dto = self._source_dtos.get(domain.id)

        if dto is None:
            dto = ORMVirtualMachine(id=domain.id.value)

        dto.name = domain.name
        dto.host = domain.host
        dto.port = domain.port
        dto.protocol = domain.protocol
        dto.is_active = domain.is_active
        dto.current_user_id = (
            domain.current_user_id.value if domain.current_user_id else None
        )
        dto.last_used_at = domain.last_used_at

        return dto

    def to_domain(self, dto: ORMVirtualMachine) -> VirtualMachine:
        domain = VirtualMachine(
            id=VirtualMachineId(dto.id),
            name=dto.name,
            host=dto.host,
            port=dto.port,
            protocol=dto.protocol,
            is_active=dto.is_active,
            current_user_id=UserId(dto.current_user_id) if dto.current_user_id else None,
            last_used_at=dto.last_used_at,
        )
        self._source_dtos[domain.id] = dto
        return domain
