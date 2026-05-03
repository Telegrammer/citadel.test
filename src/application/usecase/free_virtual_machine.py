from collections.abc import Sequence
from dataclasses import dataclass

from application.exceptions.base import AccessDeniedError
from application.ports.gateways.virtual_machine import VirtualMachineCommandGateway
from application.services.current_user import CurrentUserService
from domain.entities.user import UserId


@dataclass(frozen=True)
class FreeVirtualMachineResponse:
    freed_user_ids: Sequence[UserId]


class FreeVirtualMachineUsecase:
    def __init__(
        self,
        current_user: CurrentUserService,
        virtual_machine_commands: VirtualMachineCommandGateway,
    ):
        self._current_user = current_user
        self._virtual_machine_commands = virtual_machine_commands

    async def __call__(self) -> FreeVirtualMachineResponse:
        current_user = await self._current_user()

        if not current_user.is_admin:
            raise AccessDeniedError(
                "Ошибка доступа", "Машины может освободить только администратор"
            )

        freed_user_ids = tuple(
            await self._virtual_machine_commands.release_all_assigned()
        )

        return FreeVirtualMachineResponse(freed_user_ids=freed_user_ids)
