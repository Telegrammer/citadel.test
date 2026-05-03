from dataclasses import dataclass


@dataclass(frozen=True, eq=False)
class Id[T]:

    value: T

    def __eq__(self, other: object) -> bool:

        if not isinstance(other, Id):
            return NotImplemented
        if type(self) is not type(other):
            return NotImplemented
        return self.value == other.value

    def __hash__(self) -> int:
        return hash(self.value)
