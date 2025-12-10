"""Redis client configuration."""

import redis.asyncio as aioredis
from redis.asyncio import Redis

from app.config import settings


class RedisClient:
    """Redis client singleton."""

    _instance: Redis | None = None
    _cache_instance: Redis | None = None

    @classmethod
    async def get_client(cls) -> Redis:
        """Get Redis client instance."""
        if cls._instance is None:
            cls._instance = await aioredis.from_url(
                settings.redis_url,
                encoding="utf-8",
                decode_responses=True,
            )
        return cls._instance

    @classmethod
    async def get_cache_client(cls) -> Redis:
        """Get Redis cache client instance."""
        if cls._cache_instance is None:
            cls._cache_instance = await aioredis.from_url(
                settings.redis_cache_url,
                encoding="utf-8",
                decode_responses=True,
            )
        return cls._cache_instance

    @classmethod
    async def close(cls) -> None:
        """Close Redis connections."""
        if cls._instance:
            await cls._instance.close()
            cls._instance = None
        if cls._cache_instance:
            await cls._cache_instance.close()
            cls._cache_instance = None


