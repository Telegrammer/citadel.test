from datetime import datetime
from dataclasses import dataclass

from domain.value_objects import EmailAddress

from ..base import Entity
from .ids import UserId


@dataclass
class ActivationKey:
    lookup: str
    value: bytes
    expire_at: datetime | None


@dataclass(eq=False)
class User(Entity[UserId]):
    created_at: datetime
    updated_at: datetime

    email: EmailAddress
    password: bytes
    activation_key: ActivationKey | None

    is_active: bool
    is_admin: bool = False
