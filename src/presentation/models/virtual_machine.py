from uuid import UUID

from pydantic import BaseModel

from domain.entities.virtual_machine import ConnectionProtocol


class VirtualMachineClaim(BaseModel):
    activation_key: str


class VirtualMachineClaimed(BaseModel):
    user_id: UUID
    host: str
    port: int
    protocol: ConnectionProtocol
    access_token: str
    token_type: str = "Bearer"


class VirtualMachineCreate(BaseModel):
    name: str
    host: str
    port: int
    protocol: str


class VirtualMachineCreated(BaseModel):
    id: UUID
    name: str
    host: str
    port: int
    protocol: ConnectionProtocol
    is_active: bool
