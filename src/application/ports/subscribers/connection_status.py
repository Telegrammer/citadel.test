from collections.abc import AsyncIterator
from typing import Protocol

from application.events import ConnectionStatusUpdated
from domain.entities.user import UserId


class ConnectionStatusSubscriber(Protocol):
    def listen(self, user_id: UserId) -> AsyncIterator[ConnectionStatusUpdated]: ...
