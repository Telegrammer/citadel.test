from faststream.redis import RedisBroker
from redis.asyncio import Redis


class RedisHelper:
    def __init__(self, url: str):
        self.client = Redis.from_url(url)
        self.broker = RedisBroker(url)

    async def close(self) -> None:
        await self.broker.stop()
        await self.client.aclose()
