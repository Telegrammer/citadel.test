from datetime import datetime
from dataclasses import dataclass

from domain.value_objects import EmailAddress

from ..base import Entity
from .ids import UserId


@dataclass
class ActivationKey:
    value: str
    expire_at: datetime | None


@dataclass(eq=False)
class User(Entity[UserId]):
    created_at: datetime
    updated_at: datetime

    login: EmailAddress
    password_hash: bytes
    activation_key: ActivationKey

    is_active: bool
    is_admin: bool = False
