from fastapi import APIRouter, Depends, HTTPException
from brain_v2.modules.decision.schemas import DecisionRequest, DecisionResult, DecisionStatusResponse
from brain_v2.modules.decision.service import DecisionEngineService
from brain_v2.modules.knowledge.service import KnowledgeEngineService
from brain_v2.dependencies import get_decision_service

router = APIRouter(prefix="/decision", tags=["decision-engine"])

@router.get("/status", response_model=DecisionStatusResponse)
async def get_status(service: DecisionEngineService = Depends(get_decision_service)):
    return await service.status()

@router.post("/evaluate", response_model=DecisionResult)
async def evaluate_decision(
    request: DecisionRequest, 
    service: DecisionEngineService = Depends(get_decision_service)
):
    if not request.context_id:
        raise HTTPException(status_code=400, detail="context_id is required for decision tracking.")
    return await service.decide(request)