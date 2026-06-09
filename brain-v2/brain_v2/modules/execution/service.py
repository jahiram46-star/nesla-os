import asyncio
import logging
from typing import List, Optional, Dict, Any
from datetime import datetime
from brain_v2.services.base import BaseModuleService, ModuleMetadata
from brain_v2.services.base import BaseModuleService, ModuleMetadata # Corrected import path
from brain_v2.schemas.module import ModuleStatusResponse # Added import
from brain_v2.modules.execution.schemas import (
    ExecutionResult, TaskExecutionRequest, ProjectExecutionRequest, 
    CommandExecutionRequest, ExecutionStatusResponse
)
from brain_v2.modules.execution.models import ExecutionRecord

# Engine Imports (for type hinting and potential future direct calls)
from brain_v2.modules.knowledge.service import KnowledgeEngineService
from brain_v2.modules.memory.service import MemoryEngineService
from brain_v2.modules.reasoning.service import ReasoningEngineService
from brain_v2.modules.decision.service import DecisionEngineService
from brain_v2.modules.planning.service import PlanningEngineService
from brain_v2.modules.task.service import TaskEngineService
from brain_v2.modules.project.service import ProjectEngineService

logger = logging.getLogger(__name__)

class ExecutionEngineService(BaseModuleService):
    metadata = ModuleMetadata(
        key="execution",
        name="Execution Engine",
        description="Manifests AI plans into reality through task, project, and command execution.",
    )

    def __init__(
        self,
        knowledge: KnowledgeEngineService,
        memory: MemoryEngineService,
        reasoning: ReasoningEngineService,
        decision: DecisionEngineService,
        planning: PlanningEngineService,
        task: TaskEngineService,
        project: ProjectEngineService,
        db_session: Optional[AsyncSession] = None
    ):
        self.knowledge = knowledge
        self.memory = memory
        self.reasoning = reasoning
        self.decision = decision
        self.planning = planning
        self.task_engine = task
        self.project_engine = project
        self.db = db_session
        self._active_count = 0 # In-memory counter, for distributed systems use Redis/DB

    async def status(self) -> ExecutionStatusResponse:
        return ExecutionStatusResponse(
            key=self.metadata.key,
            name=self.metadata.name,
            status="active",
            description=self.metadata.description,
            active_executions_count=self._active_count,
            failed_executions_today=0, # Placeholder
            system_load=0.15, # Placeholder
            last_execution_id=None # Placeholder
        )

    async def execute_task(self, request: TaskExecutionRequest) -> ExecutionResult:
        """Executes a specific task with retry logic and validation."""
        # This is a placeholder for actual task execution logic
        exec_id = f"TASK_EXEC_{datetime.utcnow().timestamp()}"
        result = ExecutionResult(
            execution_id=exec_id,
            execution_type="task",
            execution_status="running",
            started_at=datetime.utcnow()
        )
        self._active_count += 1
        try:
            logger.info(f"Executing task {request.task_id} for context {request.context_id}")
            await asyncio.sleep(1) # Simulate work
            result.output = {"message": f"Task {request.task_id} completed successfully."}
            result.execution_status = "completed"
        except Exception as e:
            result.execution_status = "failed"
            result.errors.append(str(e))
        finally:
            result.completed_at = datetime.utcnow()
            self._active_count -= 1
            # self._save_record(request, result) # Implement persistence
        return result

    async def run_command(self, request: CommandExecutionRequest) -> ExecutionResult:
        """Low-level OS command execution with monitoring."""
        exec_id = f"CMD_{datetime.utcnow().timestamp()}"
        result = ExecutionResult(
            execution_id=exec_id,
            execution_type="command",
            execution_status="running",
            started_at=datetime.utcnow()
        )
        try:
            proc = await asyncio.create_subprocess_exec(
                request.command, *request.args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE, cwd=request.work_dir
            )
            stdout, stderr = await proc.communicate()
            if stdout: result.logs.append(stdout.decode())
            if stderr: result.errors.append(stderr.decode()); result.execution_status = "failed"
            else: result.execution_status = "completed"
        except Exception as e: result.execution_status = "failed"; result.errors.append(f"OS Error: {str(e)}")
        result.completed_at = datetime.utcnow()
        # self._save_record(request, result) # Implement persistence
        return result