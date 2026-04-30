from typing import Protocol


from domain.value_objects import Password


class PasswordHasher(Protocol):
    """Define a contract for generating decrypted version of password"""

    def hash(self, password: Password) -> bytes:
        raise NotImplementedError

    def is_equal(self, password: Password, password_hash: bytes) -> bool:
        raise NotImplementedError
