from collections.abc import AsyncIterator

from fastapi import Request
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from brain_v2.core.config import Settings
from brain_v2.core.container import AppContainer


def get_container(request: Request) -> AppContainer:
    return request.app.state.container


def get_app_settings(request: Request) -> Settings:
    return get_container(request).settings


def get_redis(request: Request) -> Redis:
    return get_container(request).redis


async def get_db_session(request: Request) -> AsyncIterator[AsyncSession]:
    session_factory = get_container(request).session_factory
    async with session_factory() as session:
        yield session
