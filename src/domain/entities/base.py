from dataclasses import dataclass
from domain.value_objects import Id


@dataclass(eq=False)
class Entity[idT: Id]:

    id: idT

    def __eq__(self, other: object) -> bool:

        if not isinstance(other, Entity):
            return NotImplemented
        if type(self) is not type(other):
            return NotImplemented
        return self.id == other.id
