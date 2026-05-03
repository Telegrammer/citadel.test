import json

from redis.asyncio import Redis

from application.events import (
    ConnectionStatus,
    ConnectionStatusUpdated,
    VirtualMachineClaimed,
    VirtualMachineFreed,
)
from application.ports.notifiers import (
    VirtualMachineClaimedNotifier,
    VirtualMachineFreedNotifier,
)
from infrastructure.adapters.connection_status_channel import connection_status_channel


def serialize_connection_status(event: ConnectionStatusUpdated) -> str:
    payload = {
        "status": event.status.value,
        "user_id": str(event.user_id.value),
        "host": event.host,
        "port": event.port,
        "protocol": event.protocol.value if event.protocol else None,
    }
    return json.dumps(
        {key: value for key, value in payload.items() if value is not None},
        ensure_ascii=False,
    )


class RedisVirtualMachineClaimedNotifier(VirtualMachineClaimedNotifier):
    def __init__(self, redis: Redis):
        self._redis = redis

    async def notify(self, event: VirtualMachineClaimed) -> bool:
        status = ConnectionStatusUpdated(
            user_id=event.user_id,
            status=ConnectionStatus.CONNECTED,
            host=event.host,
            port=event.port,
            protocol=event.protocol,
        )
        await self._redis.publish(
            connection_status_channel(event.user_id),
            serialize_connection_status(status),
        )
        return True


class RedisVirtualMachineFreedNotifier(VirtualMachineFreedNotifier):
    def __init__(self, redis: Redis):
        self._redis = redis

    async def notify(self, event: VirtualMachineFreed) -> bool:
        status = ConnectionStatusUpdated(
            user_id=event.user_id,
            status=ConnectionStatus.DISCONNECTED,
        )
        await self._redis.publish(
            connection_status_channel(event.user_id),
            serialize_connection_status(status),
        )
        return True
