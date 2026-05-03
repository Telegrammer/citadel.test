from dataclasses import dataclass
from datetime import datetime

from domain.entities.virtual_machine import (
    VirtualMachine,
    ConnectionProtocol,
)
from domain.entities.user import UserId
from domain.services import UserService, VirtualMachineService

from application.ports.gateways import (
    VirtualMachineCommandGateway,
    VirtualMachineQueryGateway,
    UserCommandGateway,
)
from application.ports import Clock
from application.exceptions import NoFreeVirtualMachinesError
from application.services import CurrentUserService


@dataclass
class ClaimVirtualMachineRequest:
    activation_key: str

    @classmethod
    def from_primitives(cls, activation_key: str) -> "ClaimVirtualMachineRequest":
        return cls(activation_key=activation_key)


@dataclass
class ClaimVirtualMachineResponse:
    user_id: UserId
    claimed_at: datetime
    host: str
    port: int
    protocol: ConnectionProtocol

    @classmethod
    def from_entity(
        cls, virtual_machine: VirtualMachine, user_id: UserId, claimed_at: datetime
    ) -> "ClaimVirtualMachineResponse":
        return cls(
            user_id=user_id,
            claimed_at=claimed_at,
            host=virtual_machine.host,
            port=virtual_machine.port,
            protocol=virtual_machine.protocol,
        )


class ClaimVirtualMachineUsecase:
    def __init__(
        self,
        clock: Clock,
        current_user: CurrentUserService,
        user_service: UserService,
        virtual_machine_queries: VirtualMachineQueryGateway,
        virtual_machine_service: VirtualMachineService,
        user_commands: UserCommandGateway,
        virtual_machine_commands: VirtualMachineCommandGateway,
    ):
        self._clock = clock
        self._current_user = current_user
        self._user_service = user_service
        self._virtual_machine_queries = virtual_machine_queries
        self._virtual_machine_service = virtual_machine_service
        self._user_commands = user_commands
        self._virtual_machine_commands = virtual_machine_commands

    async def __call__(
        self, request: ClaimVirtualMachineRequest
    ) -> ClaimVirtualMachineResponse:
        now = self._clock.now()
        current_user = await self._current_user()
        current_user = self._user_service.use_activation_key(
            current_user, now, request.activation_key
        )

        last_used_machine: (
            VirtualMachine | None
        ) = await self._virtual_machine_queries.by_user(current_user.id)
        if last_used_machine:
            last_used_machine = self._virtual_machine_service.free(last_used_machine)
            await self._virtual_machine_commands.update(last_used_machine)

        free_machine: (
            VirtualMachine | None
        ) = await self._virtual_machine_queries.by_availability()
        if not free_machine:
            raise NoFreeVirtualMachinesError(
                "Виртуальная машина не найдена",
                "В данный момент все виртуальные машины заняты",
            )
        claimed_machine = self._virtual_machine_service.assign_user(
            free_machine, current_user, now
        )

        await self._user_commands.update(current_user)
        await self._virtual_machine_commands.update(claimed_machine)

        return ClaimVirtualMachineResponse.from_entity(
            claimed_machine,
            current_user.id,
            now,
        )
