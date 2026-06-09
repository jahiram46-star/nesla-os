from fastapi import APIRouter, Depends
from brain_v2.modules.project.schemas import ProjectAnalysisRequest, ProjectAnalysisResult, ProjectLifecycleRequest
from brain_v2.modules.project.service import ProjectEngineService
from brain_v2.schemas.module import ModuleStatusResponse
from brain_v2.dependencies import (
    get_knowledge_service, get_memory_service, get_reasoning_service,
    get_decision_service, get_planning_service, get_task_service,
    get_db, get_project_service
)

router = APIRouter(prefix="/project", tags=["project-engine"])

@router.get("/status", response_model=ModuleStatusResponse)
async def get_status(service: ProjectEngineService = Depends(get_project_service)):
    return await service.status()

@router.post("/analyze", response_model=ProjectAnalysisResult)
async def analyze_project(request: ProjectAnalysisRequest, service: ProjectEngineService = Depends(get_project_service)):
    return await service.analyze_project(request)

@router.get("/{project_id}/status")
async def get_project_status(project_id: str):
    # This would typically fetch from DB or ProjectEngineService
    return {"project_id": project_id, "status": "active", "health": "HEALTHY"}

@router.post("/lifecycle", response_model=Dict[str, Any])
async def manage_project_lifecycle(
    request: ProjectLifecycleRequest,
    service: ProjectEngineService = Depends(get_project_service)
):
    return await service.manage_lifecycle(request)