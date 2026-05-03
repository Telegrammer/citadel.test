from typing import Protocol

from domain.entities.user import User


class UserMapper[dtoT](Protocol):

    def to_dto(self, domain: User) -> dtoT:
        raise NotImplementedError

    def to_domain(self, dto: dtoT) -> User:
        raise NotImplementedError
