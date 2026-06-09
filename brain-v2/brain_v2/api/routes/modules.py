from fastapi import APIRouter

from brain_v2.modules.registry import MODULE_SERVICES
from brain_v2.schemas.module import ModuleStatusResponse

router = APIRouter(prefix="/modules", tags=["modules"])


@router.get("", response_model=list[ModuleStatusResponse])
async def list_modules() -> list[ModuleStatusResponse]:
    return [await service.status() for service in MODULE_SERVICES]
