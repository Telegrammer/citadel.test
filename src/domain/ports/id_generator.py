from typing import Protocol
from domain.value_objects import Id


class IdGenerator[idT: Id](Protocol):
    """Define a contract for generating entity identifiers."""

    def __call__(self) -> idT:
        raise NotImplementedError
