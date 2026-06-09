from brain_v2.schemas.module import ModuleStatusResponse

from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field

class ExecutionResult(BaseModel):
    execution_id: str
    execution_type: str
    execution_status: str
    started_at: datetime
    completed_at: Optional[datetime] = None
    output: Dict[str, Any] = Field(default_factory=dict)
    logs: List[str] = Field(default_factory=list)
    errors: List[str] = Field(default_factory=list)
    validation_result: Dict[str, Any] = Field(default_factory=dict)
    rollback_status: str = "none"

class TaskExecutionRequest(BaseModel):
    task_id: str
    context_id: str
    parameters: Dict[str, Any] = Field(default_factory=dict)
    enable_rollback: bool = True
    retry_limit: int = 3

class ProjectExecutionRequest(BaseModel):
    project_id: str
    action_type: str  # build, deploy, test, analyze
    context_id: str
    environment: str = "development"

class CommandExecutionRequest(BaseModel):
    command: str
    args: List[str] = Field(default_factory=list)
    work_dir: Optional[str] = None
    context_id: str

class ExecutionStatusResponse(ModuleStatusResponse):
    active_executions_count: int
    failed_executions_today: int
    system_load: float
    last_execution_id: Optional[str] = None
