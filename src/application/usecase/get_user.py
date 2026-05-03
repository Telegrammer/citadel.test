from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


from domain.entities.user import User, UserId

from application.exceptions import UserNotFoundError
from application.ports.gateways import UserQueryGateway


@dataclass
class GetUserRequest:
    user_id: UserId

    @classmethod
    def from_primitives(cls, user_id: UUID) -> "GetUserRequest":
        return cls(user_id=UserId(user_id))


@dataclass
class GetUserResponse:
    email: str
    created_at: datetime
    is_admin: bool

    @classmethod
    def from_entity(cls, user: User) -> "GetUserResponse":
        return cls(
            user.email.value,
            user.created_at,
            user.is_admin,
        )


class GetUserUsecase:
    def __init__(self, user_queries: UserQueryGateway):
        self._user_queries = user_queries

    async def __call__(self, request: GetUserRequest) -> GetUserResponse:
        found_user: User | None = await self._user_queries.by_id(request.user_id)

        if not found_user or not found_user.is_active:
            raise UserNotFoundError(
                "Пользователь не найден", "Пользователя не существует"
            )

        return GetUserResponse.from_entity(found_user)
