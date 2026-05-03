from uuid import uuid4
from domain.entities.user import UserId
from domain.entities.virtual_machine import VirtualMachineId


class Uuid4UserIdGenerator:
    def __call__(self) -> UserId:
        return UserId(uuid4())


class Uuid4VirtualMachineIdGenerator:
    def __call__(self) -> VirtualMachineId:
        return VirtualMachineId(uuid4())
