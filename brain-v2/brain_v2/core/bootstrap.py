import logging

from redis.asyncio import Redis

from brain_v2.core.config import Settings

logger = logging.getLogger(__name__)


async def bootstrap_application(settings: Settings, redis: Redis) -> None:
    logger.info("Bootstrapping Brain V2")
    await redis.ping()
    logger.info("Brain V2 bootstrap completed")
