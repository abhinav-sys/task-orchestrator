"""Cache service."""

import json
from typing import Any, Optional

from app.infrastructure.cache.redis_client import RedisClient


class CacheService:
    """Cache service for Redis operations."""

    def __init__(self) -> None:
        """Initialize cache service."""
        self._client: Optional[Any] = None

    async def _get_client(self):
        """Get Redis cache client."""
        if self._client is None:
            self._client = await RedisClient.get_cache_client()
        return self._client

    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        client = await self._get_client()
        value = await client.get(key)
        if value:
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return value
        return None

    async def set(
        self, key: str, value: Any, expire: Optional[int] = None
    ) -> bool:
        """Set value in cache."""
        client = await self._get_client()
        if isinstance(value, (dict, list)):
            value = json.dumps(value)
        return await client.set(key, value, ex=expire)

    async def delete(self, key: str) -> bool:
        """Delete key from cache."""
        client = await self._get_client()
        return bool(await client.delete(key))

    async def exists(self, key: str) -> bool:
        """Check if key exists."""
        client = await self._get_client()
        return bool(await client.exists(key))

    async def increment(self, key: str, amount: int = 1) -> int:
        """Increment key value."""
        client = await self._get_client()
        return await client.incrby(key, amount)

    async def expire(self, key: str, seconds: int) -> bool:
        """Set expiration on key."""
        client = await self._get_client()
        return bool(await client.expire(key, seconds))


