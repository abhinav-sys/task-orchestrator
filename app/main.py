"""FastAPI application entry point."""

from contextlib import asynccontextmanager
import structlog

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.api.v1.routes import auth, tasks, users, health
from app.api.middleware.rate_limiter import RateLimitMiddleware
from app.api.middleware.logging_middleware import LoggingMiddleware
from app.infrastructure.cache.redis_client import RedisClient


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    logger = structlog.get_logger()
    logger.info("application_startup", version=settings.app_version)

    # Initialize Redis connections
    await RedisClient.get_client()
    await RedisClient.get_cache_client()

    yield

    # Shutdown
    logger.info("application_shutdown")
    await RedisClient.close()


# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Production-grade distributed task processing and API platform",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom middleware
app.add_middleware(LoggingMiddleware)
if settings.rate_limit_enabled:
    app.add_middleware(
        RateLimitMiddleware,
        requests_per_minute=settings.rate_limit_requests,
        enabled=settings.rate_limit_enabled,
    )

# Include routers
app.include_router(auth.router, prefix="/api/v1")
app.include_router(tasks.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
app.include_router(health.router, prefix="/api/v1")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Task Orchestrator API",
        "version": settings.app_version,
        "docs": "/docs",
    }

