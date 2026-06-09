from enum import Enum
from typing import List, Optional, Dict, Any # No change needed here, just for context
from pydantic import BaseModel, Field
from brain_v2.schemas.module import ModuleStatusResponse
from brain_v2.modules.planning.schemas import PlanResult

class TaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    RETRYING = "retrying"
    CANCELLED = "cancelled"

class TaskResult(BaseModel):
    task_id: str
    task_name: str
    task_description: str
    priority: str
    dependencies: List[str]
    status: TaskStatus
    assigned_engine: str
    estimated_duration: str
    completion_criteria: List[str]
    metadata: Dict[str, Any] = Field(default_factory=dict)

class TaskRequest(BaseModel):
    plan_result: PlanResult
    context_id: str
    user_id: Optional[str] = None

class TaskUpdate(BaseModel):
    status: Optional[TaskStatus] = None
    progress: Optional[float] = None
    result_data: Optional[Dict[str, Any]] = None

class TaskStatusResponse(ModuleStatusResponse):
    total_tasks: int
    active_tasks: int
    completed_tasks: int
    failed_tasks: int

class TaskListResponse(BaseModel):
    tasks: List[TaskResult]
    context_id: str
    total_count: int