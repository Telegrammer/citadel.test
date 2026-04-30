from datetime import datetime
from dataclasses import dataclass

from ..base import Entity
from ..user import UserId
from .ids import VirtualMachineId
from .enums import ConnectionProtocol


@dataclass(eq=False)
class VirtualMachine(Entity[VirtualMachineId]):
    name: str
    host: str
    port: int
    protocol: ConnectionProtocol
    is_active: bool
    current_user_id: UserId | None
    last_used_at: datetime | None
