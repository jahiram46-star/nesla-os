from fastapi import FastAPI
from brain_v2.core.config import settings
from brain_v2.core.lifespan import lifespan
from brain_v2.api.router import api_router

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        description=settings.DESCRIPTION,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    # Include the main API router
    app.include_router(api_router)

    return app