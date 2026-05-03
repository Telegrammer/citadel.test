from typing import Protocol


class Hasher(Protocol):
    def hash(self, raw_value: str) -> bytes:
        raise NotImplementedError

    def is_equal(self, raw_value: str, value_hash: bytes) -> bool:
        raise NotImplementedError
