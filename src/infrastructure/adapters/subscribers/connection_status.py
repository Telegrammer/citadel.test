import json
from collections.abc import AsyncIterator
from uuid import UUID

from redis.asyncio import Redis

from application.events import ConnectionStatus, ConnectionStatusUpdated
from application.ports import ConnectionStatusSubscriber
from domain.entities.user import UserId
from domain.entities.virtual_machine import ConnectionProtocol
from infrastructure.adapters.connection_status_channel import connection_status_channel


HEARTBEAT_INTERVAL_SECONDS = 5.0


class RedisConnectionStatusSubscriber(ConnectionStatusSubscriber):
    def __init__(self, redis: Redis):
        self._redis = redis

    async def listen(self, user_id: UserId) -> AsyncIterator[ConnectionStatusUpdated]:
        pubsub = self._redis.pubsub()
        await pubsub.subscribe(connection_status_channel(user_id))

        try:
            yield ConnectionStatusUpdated(
                user_id=user_id,
                status=ConnectionStatus.CONNECTED,
            )
            while True:
                message = await pubsub.get_message(
                    ignore_subscribe_messages=True,
                    timeout=HEARTBEAT_INTERVAL_SECONDS,
                )
                if message is None:
                    yield ConnectionStatusUpdated(
                        user_id=user_id,
                        status=ConnectionStatus.HEARTBEAT,
                    )
                    continue

                yield self._deserialize(message["data"])
        finally:
            await pubsub.unsubscribe(connection_status_channel(user_id))
            await pubsub.aclose()

    def _deserialize(self, data: bytes | str) -> ConnectionStatusUpdated:
        raw_payload = data.decode() if isinstance(data, bytes) else data
        payload = json.loads(raw_payload)

        return ConnectionStatusUpdated(
            user_id=UserId(UUID(payload["user_id"])),
            status=ConnectionStatus(payload["status"]),
            host=payload.get("host"),
            port=payload.get("port"),
            protocol=(
                ConnectionProtocol(payload["protocol"])
                if payload.get("protocol")
                else None
            ),
        )
