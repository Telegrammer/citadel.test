from datetime import datetime, timedelta
from dataclasses import replace

from domain.value_objects import EmailAddress, Password
from domain.ports import Hasher, IdGenerator, ActivationKeyGenerator
from domain.entities.user import User, UserId, ActivationKey
from domain.exceptions import (
    InvalidNewPasswordError,
    ActivationKeyIsExpiredError,
    InvalidActvationKeyError,
)


class UserService:
    def __init__(
        self,
        id_generator: IdGenerator[UserId],
        hasher: Hasher,
        activation_key_generator: ActivationKeyGenerator,
        activation_key_expiration_duration: timedelta | None = None,
    ):
        self._id_generator = id_generator
        self._hasher = hasher
        self._activation_key_generator = activation_key_generator
        self._activation_key_expiration_duration = activation_key_expiration_duration

    def create(
        self,
        email: EmailAddress,
        password: Password,
        now: datetime | None,
    ) -> User:

        return User(
            id=self._id_generator(),
            created_at=now,
            updated_at=now,
            email=email,
            password=self._hasher.hash(password.value),
            activation_key=None,
            is_active=True,
        )

    def generate_activation_key(self, now: datetime) -> tuple[str, ActivationKey]:

        return self._activation_key_generator(
            now + self._activation_key_expiration_duration
            if self._activation_key_expiration_duration and now
            else None
        )

    def update_activation_key(
        self, user: User, now: datetime, activation_key: ActivationKey
    ) -> User:
        return replace(user, activation_key=activation_key, updated_at=now)

    def use_activation_key(self, user: User, now: datetime, raw_key: str) -> User:

        if user.activation_key is None:
            raise InvalidActvationKeyError(
                "Ключ активации недействителен",
                "Ключ активации у пользователя отсутсвует",
            )

        try:
            raw_lookup, raw_secret = raw_key.split(".", maxsplit=1)
        except ValueError:
            raise InvalidActvationKeyError(
                "Неверный ключ активации",
                "Переданный ключ имеет неверный формат",
            )

        if raw_lookup != user.activation_key.lookup:
            raise InvalidActvationKeyError(
                "Неверный ключ активации",
                "Идентификатор ключа активации не совпадает",
            )

        if not self._hasher.is_equal(raw_secret, user.activation_key.value):
            raise InvalidActvationKeyError(
                "Неверный ключ активации",
                "Переданный ключ не совпдает с текщим ключом пользователя",
            )

        if (
            user.activation_key.expire_at is not None
            and user.activation_key.expire_at < now
        ):
            raise ActivationKeyIsExpiredError(
                "Ключ активации недействителен", "Ключ активации испортился"
            )

        return replace(user, activation_key=None, updated_at=now)

    def change_password(
        self, user: User, now: datetime, old_password: Password, new_password: Password
    ) -> User:

        if self._hasher.is_equal(new_password.value, user.password):
            raise InvalidNewPasswordError(
                "Одинаковые пароли", "Новый пароль не может совпадать со старым паролем"
            )

        if not self._hasher.is_equal(old_password.value, user.password):
            raise InvalidNewPasswordError(
                "Неверный пароль", "Введенный пароль не совпадает с текущем"
            )

        return replace(
            user,
            password=self._hasher.hash(new_password.value),
            updated_at=now,
        )
