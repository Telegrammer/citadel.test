from datetime import datetime
from secrets import token_urlsafe

from domain.entities.user import ActivationKey
from domain.ports import Hasher


class SecretsActivationKeyGenerator:
    def __init__(self, hasher: Hasher, token_bytes: int = 32):
        self._hasher = hasher
        self._token_bytes = token_bytes

    def __call__(self, expiration_time: datetime | None) -> tuple[str, ActivationKey]:
        lookup = token_urlsafe(16)
        secret = token_urlsafe(self._token_bytes)
        raw_key = f"{lookup}.{secret}"

        return (
            raw_key,
            ActivationKey(
                lookup=lookup,
                value=self._hasher.hash(secret),
                expire_at=expiration_time,
            ),
        )
