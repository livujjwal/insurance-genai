from datetime import UTC, datetime
from typing import Any

import redis.asyncio as aioredis
from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_redis
from app.core.config import get_settings

router = APIRouter(prefix="/health", tags=["Health"])
settings = get_settings()


@router.get("", response_model=dict[str, Any])
async def health_check(
    db: AsyncSession = Depends(get_db),
    redis: aioredis.Redis = Depends(get_redis),
) -> dict[str, Any]:
    """Comprehensive health check checking PostgreSQL and Redis."""
    db_status = "healthy"
    try:
        await db.execute(text("SELECT 1"))
    except Exception as exc:
        db_status = f"unhealthy: {str(exc)}"

    redis_status = "healthy"
    try:
        await redis.ping()
    except Exception as exc:
        redis_status = f"unhealthy: {str(exc)}"

    all_healthy = db_status == "healthy" and redis_status == "healthy"

    return {
        "status": "healthy" if all_healthy else "degraded",
        "timestamp": datetime.now(UTC).isoformat(),
        "environment": settings.ENVIRONMENT,
        "app": settings.APP_NAME,
        "services": {
            "database": db_status,
            "redis": redis_status,
        },
    }
