from dataclasses import dataclass
from datetime import timedelta, datetime


from domain.ports import Hasher
from domain.value_objects import EmailAddress, Password
from domain.entities.user import UserId, User
from application.ports.gateways import UserQueryGateway
from application.ports import Clock
from application.exceptions import UserNotFoundError


@dataclass
class LoginUserRequest:
    email: EmailAddress
    password: Password

    @classmethod
    def from_primitives(cls, email: str, password: str) -> "LoginUserRequest":
        return cls(email=EmailAddress(email), password=Password(password))


@dataclass
class LoginUserResponse:
    id: UserId
    login_at: datetime
    duration: timedelta

    @classmethod
    def from_entity(
        cls, user: User, now: datetime, duration: timedelta
    ) -> "LoginUserResponse":
        return cls(
            id=user.id,
            login_at=now,
            duration=duration,
        )


class LoginUserUsecase:
    def __init__(
        self,
        hasher: Hasher,
        dummy_hash: bytes,
        clock: Clock,
        user_queries: UserQueryGateway,
        login_duration: timedelta,
    ):
        self._hasher = hasher
        self._dummy_hash = dummy_hash
        self._clock = clock
        self._user_queries = user_queries
        self._login_duration = login_duration

    async def __call__(self, request: LoginUserRequest) -> LoginUserResponse:
        now: datetime = self._clock.now()
        user = await self._user_queries.by_email(request.email)

        hashed = user.password if user and user.is_active else self._dummy_hash

        if not self._hasher.is_equal(request.password.value, hashed):
            raise UserNotFoundError(
                "Пользователь не найден", "Неверный логин или пароль"
            )

        if user is None or not user.is_active:
            raise UserNotFoundError(
                "Пользователь не найден", "Пользователя не существует"
            )

        return LoginUserResponse.from_entity(user, now, self._login_duration)
