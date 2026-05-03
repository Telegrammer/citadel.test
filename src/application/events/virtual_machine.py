from dataclasses import dataclass
from enum import StrEnum

from domain.entities.user import UserId
from domain.entities.virtual_machine import ConnectionProtocol


class ConnectionStatus(StrEnum):
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    HEARTBEAT = "heartbeat"


@dataclass(frozen=True)
class ConnectionStatusUpdated:
    user_id: UserId
    status: ConnectionStatus
    host: str | None = None
    port: int | None = None
    protocol: ConnectionProtocol | None = None


@dataclass(frozen=True)
class VirtualMachineClaimed:
    user_id: UserId
    host: str
    port: int
    protocol: ConnectionProtocol


@dataclass(frozen=True)
class VirtualMachineFreed:
    user_id: UserId
