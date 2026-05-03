from dishka import Provider, Scope, from_context, provide
from faststream.redis import RedisBroker
from redis.asyncio import Redis

from setup.config import Settings
from setup.redis_helper import RedisHelper


class RedisProvider(Provider):
    scope = Scope.APP

    settings = from_context(Settings)

    @provide
    def provide_redis_helper(self, settings: Settings) -> RedisHelper:
        return RedisHelper(settings.redis.url)

    @provide
    def provide_redis_client(self, redis_helper: RedisHelper) -> Redis:
        return redis_helper.client

    @provide
    def provide_redis_broker(self, redis_helper: RedisHelper) -> RedisBroker:
        return redis_helper.broker
