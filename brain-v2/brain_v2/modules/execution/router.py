from fastapi import APIRouter, Depends

from brain_v2.modules.execution.schemas import (
    ExecutionStatusResponse, ExecutionResult, TaskExecutionRequest, 
    CommandExecutionRequest
)
from brain_v2.modules.execution.service import ExecutionEngineService
from brain_v2.dependencies import get_execution_service

router = APIRouter(prefix="/execution", tags=["execution-engine"])

@router.get("/status", response_model=ExecutionStatusResponse)
async def get_status(service: ExecutionEngineService = Depends(get_execution_service)):
    return await service.status()

@router.post("/task", response_model=ExecutionResult)
async def execute_task(
    request: TaskExecutionRequest, 
    service: ExecutionEngineService = Depends(get_execution_service)
):
    return await service.execute_task(request)

@router.post("/command", response_model=ExecutionResult)
async def run_command(
    request: CommandExecutionRequest, 
    service: ExecutionEngineService = Depends(get_execution_service)
):
    return await service.run_command(request)
