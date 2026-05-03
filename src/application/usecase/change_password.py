from dataclasses import dataclass
from datetime import datetime

from domain.value_objects import Password
from domain.entities.user import User
from domain.services import UserService
from application.ports.gateways import UserCommandGateway
from application.ports import Clock
from application.services import CurrentUserService


@dataclass
class ChangeUserPasswordRequest:
    current_password: Password
    new_password: Password

    @classmethod
    def from_primitives(
        cls, current_password: str, new_password: str
    ) -> "ChangeUserPasswordRequest":
        return cls(
            current_password=Password(current_password),
            new_password=Password(new_password),
        )


class LoginUserUsecase:
    def __init__(
        self,
        clock: Clock,
        user_commands: UserCommandGateway,
        user_service: UserService,
        current_user: CurrentUserService,
    ):
        self._clock = clock
        self._user_commands = user_commands
        self._user_service = user_service
        self._current_user = current_user

    async def __call__(self, request: ChangeUserPasswordRequest) -> None:
        now: datetime = self._clock.now()
        current_user: User = await self._current_user()

        current_user = self._user_service.change_password(
            user=current_user,
            now=now,
            old_password=request.current_password,
            new_password=request.new_password,
        )

        await self._user_commands.update(current_user)
