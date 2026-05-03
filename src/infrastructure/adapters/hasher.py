from domain.ports import Hasher
from passlib.context import CryptContext


class BcryptHasher(Hasher):
    def __init__(self):
        self._context: CryptContext = CryptContext(schemes=["bcrypt"])

    def hash(self, raw_value: str) -> bytes:
        return bytes(self._context.hash(raw_value), encoding="utf-8")

    def is_equal(self, raw_value: str, value_hash: bytes) -> bool:
        return self._context.verify(raw_value, value_hash.decode("utf-8"))
