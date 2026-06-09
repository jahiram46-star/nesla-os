from fastapi import APIRouter, Depends
from brain_v2.modules.reasoning.schemas import ReasoningRequest, ReasoningResult, ReasoningStatusResponse
from brain_v2.modules.reasoning.service import ReasoningEngineService
from brain_v2.modules.knowledge.service import KnowledgeEngineService
from brain_v2.dependencies import get_reasoning_service

router = APIRouter(prefix="/reasoning", tags=["reasoning-engine"])

@router.get("/status", response_model=ReasoningStatusResponse)
async def get_status(service: ReasoningEngineService = Depends(get_reasoning_service)):
    return await service.status()

@router.post("/process", response_model=ReasoningResult)
async def process_reasoning(
    request: ReasoningRequest, 
    service: ReasoningEngineService = Depends(get_reasoning_service)
):
    return await service.reason(request)