from datetime import datetime
from dataclasses import replace

from domain.value_objects import EmailAddress, Password
from domain.ports import PasswordHasher, IdGenerator, ActivationKeyGenerator
from domain.entities.user import User, UserId
from domain.exceptions import DomainError


class UserService:
    def __init__(
        self,
        id_generator: IdGenerator[UserId],
        hasher: PasswordHasher,
        activation_key_generator: ActivationKeyGenerator,
        activation_key_expirtaion_duration: datetime | None = None,
    ):
        self._id_generator = id_generator
        self._hasher = hasher
        self._activation_key_generator = activation_key_generator
        self._activation_key_expiration_duration = activation_key_expirtaion_duration

    def create(
        self,
        email: EmailAddress,
        password: Password,
        now: datetime,
    ):
        return User(
            id=self._id_generator(),
            created_at=now,
            updated_at=now,
            email=email,
            password=self._hasher.hash(password),
            activation_key=self._activation_key_generator(
                self._activation_key_expiration_duration
            ),
            is_active=True,
        )

    def regenerate_activation_key(self, user: User) -> User:
        return replace(
            user,
            activation_key=self._activation_key_generator(
                self._activation_key_expiration_duration
            ),
        )

    def change_password(
        self, user: User, old_password: Password, new_password: Password
    ) -> User:

        if self._hasher.is_equal(new_password, user.password):
            raise DomainError(
                "Одинаковые пароли", "Новый пароль не может совпадать со старым паролем"
            )

        if not self._hasher.is_equal(old_password, user.password):
            raise DomainError("Неверный пароль", "Введенный пароль неверный")

        return replace(user, password=self._hasher.hash(new_password))
