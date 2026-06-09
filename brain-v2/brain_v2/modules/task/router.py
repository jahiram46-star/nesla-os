from fastapi import APIRouter, Depends, HTTPException
from brain_v2.modules.task.schemas import ( # No change needed here, just for context
    TaskRequest, TaskResult, TaskStatusResponse, TaskUpdate, TaskListResponse, TaskStatus
)
from brain_v2.modules.task.service import TaskEngineService
from brain_v2.modules.task.deps import get_task_service

router = APIRouter(prefix="/tasks", tags=["task-engine"])

@router.get("/status", response_model=TaskStatusResponse)
async def get_status(service: TaskEngineService = Depends(get_task_service)):
    return await service.status()

@router.post("/initialize", response_model=TaskListResponse)
async def initialize_tasks(
    request: TaskRequest, 
    service: TaskEngineService = Depends(get_task_service)
):
    tasks = await service.create_tasks_from_plan(request)
    return TaskListResponse(
        tasks=tasks,
        context_id=request.context_id,
        total_count=len(tasks)
    )