from typing import Protocol

from domain.entities.virtual_machine import VirtualMachine


class VirtualMachineMapper[dtoT](Protocol):

    def to_dto(self, domain: VirtualMachine) -> dtoT:
        raise NotImplementedError

    def to_domain(self, dto: dtoT) -> VirtualMachine:
        raise NotImplementedError
