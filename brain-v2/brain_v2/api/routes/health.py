from fastapi import APIRouter, Depends

from brain_v2.api.deps import get_app_settings
from brain_v2.core.config import Settings
from brain_v2.schemas.health import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health(settings: Settings = Depends(get_app_settings)) -> HealthResponse:
    return HealthResponse(
        status="ok",
        service=settings.app_name,
        environment=settings.app_env,
    )
