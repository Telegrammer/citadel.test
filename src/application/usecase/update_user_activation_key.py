from dataclasses import dataclass
from datetime import datetime

from application.ports.clock import Clock
from application.ports.gateways.user import UserCommandGateway
from domain.entities.user import User
from application.services import CurrentUserService
from domain.services.user import UserService


@dataclass
class UpdateUserActivationKeyResponse:
    email: str
    activation_key: str
    expire_at: datetime | None

    @classmethod
    def from_entity(
        cls, user: User, activation_key: str
    ) -> "UpdateUserActivationKeyResponse":
        return cls(
            email=user.email.value,
            activation_key=activation_key,
            expire_at=user.activation_key.expire_at if user.activation_key else None,
        )


class UpdateUserActivationKeyUsecase:
    def __init__(
        self,
        clock: Clock,
        current_user: CurrentUserService,
        user_service: UserService,
        user_commands: UserCommandGateway,
    ):
        self._clock = clock
        self._current_user = current_user
        self._user_service = user_service
        self._user_commands = user_commands

    async def __call__(self) -> UpdateUserActivationKeyResponse:
        now: datetime = self._clock.now()

        current_user: User = await self._current_user()

        response_key, new_activation_key = self._user_service.generate_activation_key(now)
        current_user = self._user_service.update_activation_key(
            current_user, now, new_activation_key
        )

        await self._user_commands.update(current_user)
        return UpdateUserActivationKeyResponse.from_entity(current_user, response_key)
