from typing import Protocol


from domain.entities.user.ids import UserId
from domain.value_objects import EmailAddress
from domain.entities.user import User


class UserCommandGateway(Protocol):
    async def add(self, user: User) -> None:
        raise NotImplementedError

    async def update(self, user: User) -> None:
        raise NotImplementedError


class UserQueryGateway(Protocol):
    async def by_email(self, email: EmailAddress) -> User | None:
        raise NotImplementedError

    async def by_id(self, user_id: UserId) -> User | None:
        raise NotImplementedError

    async def by_activation_key_lookup(self, lookup: str) -> User | None:
        raise NotImplementedError
