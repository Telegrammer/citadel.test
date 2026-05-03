from typing import Protocol

from starlette.websockets import WebSocket

from application.events import ConnectionStatusUpdated
from presentation.models import (
    ConnectionStatusMessage,
    WebSocketErrorCode,
    WebSocketErrorMessage,
)
from presentation.ws.codes import WebSocketCloseCode


class ConnectionStatusConnection(Protocol):
    async def accept(self) -> None: ...

    async def send_status(self, event: ConnectionStatusUpdated) -> None: ...

    async def send_error(
        self,
        code: WebSocketErrorCode,
        detail: str | None = None,
    ) -> None: ...

    async def close(self, code: WebSocketCloseCode) -> None: ...


class StarletteConnectionStatusConnection:
    def __init__(self, websocket: WebSocket) -> None:
        self._websocket = websocket

    async def accept(self) -> None:
        await self._websocket.accept()

    async def send_status(self, event: ConnectionStatusUpdated) -> None:
        await self._websocket.send_json(
            ConnectionStatusMessage.from_event(event).model_dump(mode="json")
        )

    async def send_error(
        self,
        code: WebSocketErrorCode,
        detail: str | None = None,
    ) -> None:
        await self._websocket.send_json(
            WebSocketErrorMessage(code=code, detail=detail).model_dump(mode="json")
        )

    async def close(self, code: WebSocketCloseCode) -> None:
        await self._websocket.close(code=code)
