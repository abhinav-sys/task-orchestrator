"""Rate limiting middleware."""

import time
from typing import Callable

from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from app.infrastructure.cache.cache_service import CacheService


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Rate limiting middleware."""

    def __init__(
        self,
        app: Callable,
        requests_per_minute: int = 100,
        enabled: bool = True,
    ) -> None:
        """Initialize rate limiter."""
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.enabled = enabled
        self.cache_service = CacheService()

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request with rate limiting."""
        if not self.enabled:
            return await call_next(request)

        # Skip rate limiting for health checks
        if request.url.path.startswith("/api/v1/health"):
            return await call_next(request)

        # Get client identifier
        client_id = request.client.host if request.client else "unknown"

        # Check rate limit
        key = f"rate_limit:{client_id}"
        current = await self.cache_service.get(key)

        if current is None:
            await self.cache_service.set(key, 1, expire=60)
        elif int(current) >= self.requests_per_minute:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded. Please try again later.",
            )
        else:
            await self.cache_service.increment(key)

        return await call_next(request)

