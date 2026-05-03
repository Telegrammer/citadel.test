from dataclasses import dataclass
from datetime import datetime

from domain.value_objects import EmailAddress, Password
from domain.entities.user import User, UserId
from domain.services import UserService

from application.ports.gateways import UserCommandGateway
from application.ports import Clock


@dataclass
class RegisterUserRequest:
    email: EmailAddress
    password: Password

    @classmethod
    def from_primitives(cls, email: str, password: str) -> "RegisterUserRequest":
        return cls(email=EmailAddress(email), password=Password(password))


@dataclass
class RegisterUserResponse:
    id: UserId
    email: EmailAddress
    activation_key: str
    expire_at: datetime | None

    @classmethod
    def from_entity(cls, user: User, activation_key: str) -> "RegisterUserResponse":
        return cls(
            id=user.id,
            email=user.email,
            activation_key=activation_key,
            expire_at=user.activation_key.expire_at if user.activation_key else None,
        )


class RegisterUserUsecase:
    def __init__(
        self, clock: Clock, user_service: UserService, user_commands: UserCommandGateway
    ):
        self._clock = clock
        self._user_service = user_service
        self._user_commands = user_commands

    async def __call__(self, request: RegisterUserRequest) -> RegisterUserResponse:
        now = self._clock.now()

        new_user: User = self._user_service.create(request.email, request.password, now)
        response_key, activation_key = self._user_service.generate_activation_key(now)
        new_user = self._user_service.update_activation_key(new_user, now, activation_key)

        await self._user_commands.add(new_user)
        return RegisterUserResponse.from_entity(new_user, response_key)
