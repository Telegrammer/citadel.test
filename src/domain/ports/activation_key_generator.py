from typing import Protocol
from datetime import datetime
from domain.entities.user import ActivationKey


class ActivationKeyGenerator(Protocol):
    def __call__(
        self, expiration_time: datetime | None
    ) -> tuple[str, ActivationKey]:
        raise NotImplementedError
