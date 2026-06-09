from brain_v2.schemas.module import ModuleStatusResponse

from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field

class FileOperation(BaseModel):
    operation: str # read, write, update, delete
    path: str
    content: Optional[str] = None
    success: bool = False
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class MRMConnectorResult(BaseModel):
    workspace_id: str
    project_id: Optional[str] = None
    file_operations: List[Dict[str, Any]] = Field(default_factory=list)
    terminal_operations: List[Dict[str, Any]] = Field(default_factory=list)
    git_operations: List[Dict[str, Any]] = Field(default_factory=list)
    build_operations: List[Dict[str, Any]] = Field(default_factory=list)
    debug_operations: List[Dict[str, Any]] = Field(default_factory=list)
    status: str

class WorkspaceRequest(BaseModel):
    workspace_id: str
    project_id: Optional[str] = None
    context_id: str

class TerminalRequest(WorkspaceRequest):
    command: str
    work_dir: str = "."

class FileRequest(WorkspaceRequest):
    path: str
    content: Optional[str] = None
    op_type: str # read, write, update, delete

class GitRequest(WorkspaceRequest):
    action: str # status, commit, branch, push, pull
    params: Dict[str, Any] = Field(default_factory=dict)

class MRMConnectorStatusResponse(ModuleStatusResponse):
    active_workspaces: int
    total_operations_today: int
