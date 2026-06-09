from dataclasses import dataclass

from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from brain_v2.core.config import Settings


@dataclass(slots=True)
class AppContainer:
    settings: Settings
    redis: Redis
    session_factory: async_sessionmaker[AsyncSession]
