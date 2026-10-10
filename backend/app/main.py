import time
import uuid
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from app.api.v1.health import router as health_router
from app.cache.redis_client import close_redis, get_redis_client
from app.core.config import get_settings
from app.core.exceptions import register_exception_handlers
from app.core.logging import request_id_ctx_var, setup_logging

settings = get_settings()


class RequestIDMiddleware(BaseHTTPMiddleware):
    """Middleware to set and propagate X-Request-ID in context and headers."""

    async def dispatch(self, request: Request, call_next):
        req_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        token = request_id_ctx_var.set(req_id)
        start_time = time.perf_counter()
        try:
            response = await call_next(request)
            process_time = time.perf_counter() - start_time
            response.headers["X-Request-ID"] = req_id
            response.headers["X-Process-Time"] = f"{process_time:.4f}s"
            return response
        finally:
            request_id_ctx_var.reset(token)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """App lifespan context manager for startup and graceful shutdown."""
    setup_logging(level="DEBUG" if settings.DEBUG else "INFO")
    # Verify/initialize redis pool on startup
    try:
        redis = await get_redis_client()
        await redis.ping()
    except Exception:
        pass

    yield

    # Teardown
    await close_redis()


def create_app() -> FastAPI:
    """FastAPI application factory."""
    app = FastAPI(
        title=settings.APP_NAME,
        version="0.1.0",
        description="Production-grade AI assistant for insurance claims and policy intelligence.",
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    # Middleware
    app.add_middleware(RequestIDMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["X-Request-ID", "X-Process-Time"],
    )

    # Exception Handlers
    register_exception_handlers(app)

    # API Routers
    app.include_router(health_router, prefix=settings.API_V1_STR)

    @app.get("/")
    async def root():
        return {
            "name": settings.APP_NAME,
            "version": "0.1.0",
            "environment": settings.ENVIRONMENT,
            "docs": "/docs",
            "health": f"{settings.API_V1_STR}/health",
        }

    return app


app = create_app()
