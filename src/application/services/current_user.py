from application.exceptions.base import CurrentUserDontAssignError
from application.exceptions.user import CurrentUserNotFound
from application.ports.gateways.user import UserQueryGateway
from domain.entities.user import UserId, User


class CurrentUserService:
    def __init__(self, gateway: UserQueryGateway):
        self._id: UserId | None = None
        self._user: User | None = None
        self._gateway: UserQueryGateway = gateway

    def set_user(self, user_id: UserId) -> None:
        self._id = user_id

    async def __call__(self) -> User:
        if self._user:
            return self._user
        if not self._id:
            raise CurrentUserDontAssignError(
                "Текущий пользователь не объявлен",
                "Id текущего пользователя не объявлен",
            )
        self._user = await self._gateway.by_id(self._id)
        if not self._user or not self._user.is_active:
            raise CurrentUserNotFound(
                "Текущий пользователь не найден",
                "Пользователя не существует",
            )
        return self._user
