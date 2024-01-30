from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Annotated, Any, AsyncIterator, cast

from fastapi import Depends, Request
from fastapi_async_safe import async_safe
from loguru import logger
from redis.asyncio import Redis
from starlette.types import ASGIApp

from .exceptions import RedisClientIsNotInitializedException
from .settings import settings


@asynccontextmanager
async def redis_lifespan(_: ASGIApp) -> AsyncIterator[dict[str, Any]]:
    client = Redis.from_url(str(settings.REDIS_DSN))

    logger.info("Connecting to Redis")
    async with client:
        await client.ping()
        yield {"redis": client}
    logger.info("Disconnected from Redis")


async def get_redis_client(request: Request) -> Redis:
    try:
        client = cast(Redis, request.state.redis)
    except AttributeError:
        logger.error("Redis client is not initialized")
        raise RedisClientIsNotInitializedException from None

    return client


@dataclass
@async_safe
class PoolService:
    client: Annotated[Redis, Depends(get_redis_client)]

    async def get_redirect_domain(self, pool_id: str) -> tuple[str, int] | None:
        res = await self.client.zrandmember(pool_id, count=1, withscores=True)

        match res:
            case [domain, weight, *_]:
                return domain.decode(), int(weight)
            case _:
                return None


__all__ = [
    "PoolService",
    "redis_lifespan",
    "get_redis_client",
]
