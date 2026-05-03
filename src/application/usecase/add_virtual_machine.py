from dataclasses import dataclass

from application.exceptions import AccessDeniedError
from application.ports.gateways import VirtualMachineCommandGateway
from application.services import CurrentUserService
from domain.entities.virtual_machine import ConnectionProtocol, VirtualMachine
from domain.exceptions import DomainFieldError
from domain.entities.virtual_machine.ids import VirtualMachineId
from domain.services import VirtualMachineService


@dataclass
class AddVirtualMachineRequest:
    name: str
    host: str
    port: int
    protocol: ConnectionProtocol

    @classmethod
    def from_primitives(
        cls,
        name: str,
        host: str,
        port: int,
        protocol: str,
    ) -> "AddVirtualMachineRequest":
        try:
            proto = ConnectionProtocol(protocol)
        except ValueError as exc:
            raise DomainFieldError(
                code="invalid_protocol",
                field="protocol",
                message=f"Недопустимый протокол: {protocol!r}",
            ) from exc
        return cls(
            name=name,
            host=host,
            port=port,
            protocol=proto,
        )


@dataclass
class AddVirtualMachineResponse:
    id: VirtualMachineId
    name: str
    host: str
    port: int
    protocol: ConnectionProtocol
    is_active: bool

    @classmethod
    def from_entity(
        cls, virtual_machine: VirtualMachine
    ) -> "AddVirtualMachineResponse":
        return cls(
            id=virtual_machine.id,
            name=virtual_machine.name,
            host=virtual_machine.host,
            port=virtual_machine.port,
            protocol=virtual_machine.protocol,
            is_active=virtual_machine.is_active,
        )


class AddVirtualMachineUsecase:
    def __init__(
        self,
        current_user: CurrentUserService,
        virtual_machine_service: VirtualMachineService,
        virtual_machine_commands: VirtualMachineCommandGateway,
    ):
        self._current_user = current_user
        self._virtual_machine_service = virtual_machine_service
        self._virtual_machine_commands = virtual_machine_commands

    async def __call__(
        self, request: AddVirtualMachineRequest
    ) -> AddVirtualMachineResponse:
        current_user = await self._current_user()

        if not current_user.is_admin:
            raise AccessDeniedError(
                "Недостаточно прав",
                "Добавлять виртуальные машины может только администратор",
            )

        virtual_machine = self._virtual_machine_service.create(
            name=request.name,
            host=request.host,
            port=request.port,
            protocol=request.protocol,
        )

        await self._virtual_machine_commands.add(virtual_machine)

        return AddVirtualMachineResponse.from_entity(virtual_machine)
