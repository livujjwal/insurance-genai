import redis.asyncio as aioredis
from fastapi import Request

from app.cache.redis_client import get_redis_client
from app.core.logging import request_id_ctx_var
from app.db.session import get_db

__all__ = ["get_db", "get_redis", "get_current_request_id"]


async def get_redis() -> aioredis.Redis:
    """Dependency that returns the active Redis client."""
    return await get_redis_client()


def get_current_request_id(request: Request) -> str:
    """Dependency returning current correlation request ID."""
    return request_id_ctx_var.get() or request.headers.get("X-Request-ID", "")
