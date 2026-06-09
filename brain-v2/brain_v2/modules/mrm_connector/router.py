from fastapi import APIRouter, Depends

from brain_v2.modules.mrm_connector.schemas import (
    MRMConnectorStatusResponse, MRMConnectorResult, FileRequest, TerminalRequest, GitRequest
)
from brain_v2.modules.mrm_connector.service import MRMConnectorService
from brain_v2.dependencies import get_mrm_connector_service

router = APIRouter(prefix="/mrm", tags=["mrm-connector"])

@router.get("/status", response_model=MRMConnectorStatusResponse)
async def get_status(service: MRMConnectorService = Depends(get_mrm_connector_service)):
    return await service.status()

@router.post("/file", response_model=MRMConnectorResult)
async def file_operation(
    request: FileRequest, 
    service: MRMConnectorService = Depends(get_mrm_connector_service)
):
    return await service.handle_file_op(request)

@router.post("/terminal", response_model=MRMConnectorResult)
async def terminal_command(
    request: TerminalRequest, 
    service: MRMConnectorService = Depends(get_mrm_connector_service)
):
    return await service.execute_terminal(request)

@router.post("/git", response_model=MRMConnectorResult)
async def git_operation(
    request: GitRequest, 
    service: MRMConnectorService = Depends(get_mrm_connector_service)
):
    return await service.handle_git(request)
