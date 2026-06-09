from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI
from redis.asyncio import Redis

from brain_v2.core.bootstrap import bootstrap_application
from brain_v2.core.container import AppContainer
from brain_v2.core.config import get_settings
from brain_v2.db.session import create_session_factory, create_sqlalchemy_engine

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = getattr(app.state, "settings", get_settings())
    engine = create_sqlalchemy_engine(settings.database_url)
    session_factory = create_session_factory(engine)
    redis = Redis.from_url(settings.redis_url, decode_responses=True)

    app.state.container = AppContainer(
        settings=settings,
        redis=redis,
        session_factory=session_factory,
    )

    await bootstrap_application(settings, redis)
    yield

    logger.info("Shutting down Brain V2")
    await redis.aclose()
    await engine.dispose()
