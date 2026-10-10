import logging
from collections.abc import Callable
from typing import Any

from arq.connections import RedisSettings

from app.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


async def startup(ctx: Any) -> None:
    logger.info("ARQ Worker started.")


async def shutdown(ctx: Any) -> None:
    logger.info("ARQ Worker stopped.")


class WorkerSettings:
    functions: list[Callable[..., Any]] = []
    on_startup = startup
    on_shutdown = shutdown
    redis_settings = RedisSettings.from_dsn(settings.REDIS_URL)
