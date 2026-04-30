from dataclasses import replace
from datetime import datetime

from domain.entities.virtual_machine import ConnectionProtocol, VirtualMachine
from domain.entities.user import User


class VirtualMachineService:
    def __init__(self):
        self._id_generator = None

    def create(self, name: str, host: str, port: int, protocol: ConnectionProtocol):

        return VirtualMachine(
            id=self._id_generator(),
            name=name,
            host=host,
            port=port,
            protocol=protocol,
            is_active=False,
            current_user_id=None,
            last_used_at=None,
        )

    def assign_user(
        self, virtual_machine: VirtualMachine, user: User, now: datetime
    ) -> VirtualMachine:
        return replace(
            virtual_machine,
            current_user_id=user.id,
            last_used_at=now,
        )

    def free(self, virtual_machine: VirtualMachine) -> VirtualMachine:
        return replace(virtual_machine, current_user_id=None)

    def activate(self, virtual_machine: VirtualMachine) -> VirtualMachine:
        return replace(virtual_machine, is_active=True)

    def deactivate(self, virtual_machine: VirtualMachine) -> VirtualMachine:
        return replace(virtual_machine, is_active=False)
