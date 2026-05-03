from collections.abc import Sequence
from typing import Protocol

from domain.entities.user import UserId
from domain.entities.virtual_machine import VirtualMachine, VirtualMachineId


class VirtualMachineCommandGateway(Protocol):
    async def add(self, virtual_machine: VirtualMachine) -> None:
        raise NotImplementedError

    async def update(self, virtual_machine: VirtualMachine) -> None:
        raise NotImplementedError

    async def release_all_assigned(self) -> Sequence[UserId]:
        raise NotImplementedError


class VirtualMachineQueryGateway(Protocol):
    async def by_id(
        self, virtual_machine_id: VirtualMachineId
    ) -> VirtualMachine | None:
        raise NotImplementedError

    async def by_availability(self) -> VirtualMachine | None:
        raise NotImplementedError

    async def by_user(self, user_id: UserId) -> VirtualMachine | None:
        raise NotImplementedError
