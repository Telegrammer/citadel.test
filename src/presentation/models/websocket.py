from enum import StrEnum
from typing import Literal
from uuid import UUID

from pydantic import BaseModel

from application.events import ConnectionStatus, ConnectionStatusUpdated
from domain.entities.virtual_machine import ConnectionProtocol


class WebSocketErrorCode(StrEnum):
    UNAUTHORIZED = "unauthorized"
    FORBIDDEN = "forbidden"


class ConnectionStatusMessage(BaseModel):
    status: ConnectionStatus
    user_id: UUID
    host: str | None = None
    port: int | None = None
    protocol: ConnectionProtocol | None = None

    @classmethod
    def from_event(cls, event: ConnectionStatusUpdated) -> "ConnectionStatusMessage":
        return cls(
            status=event.status,
            user_id=event.user_id.value,
            host=event.host,
            port=event.port,
            protocol=event.protocol,
        )


class WebSocketErrorMessage(BaseModel):
    status: Literal["error"] = "error"
    code: WebSocketErrorCode
    detail: str | None = None
