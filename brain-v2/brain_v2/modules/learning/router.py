from fastapi import APIRouter, Depends
from brain_v2.modules.learning.schemas import (
    LearningStatusResponse, LearningResult, LearningRequest, FeedbackRequest
)
from brain_v2.modules.learning.service import LearningEngineService
from brain_v2.dependencies import get_learning_service

router = APIRouter(prefix="/learning", tags=["learning-engine"])

@router.get("/status", response_model=LearningStatusResponse)
async def get_status(service: LearningEngineService = Depends(get_learning_service)):
    return await service.status()

@router.post("/analyze", response_model=LearningResult)
async def analyze_activity(
    request: LearningRequest, 
    service: LearningEngineService = Depends(get_learning_service)
):
    return await service.learn_from_execution(request)

@router.post("/feedback")
async def submit_feedback(
    request: FeedbackRequest,
    service: LearningEngineService = Depends(get_learning_service)
):
    return await service.process_user_feedback(request)