from brain_v2.services.base import BaseModuleService, ModuleMetadata # Corrected import path
import logging
from typing import Dict, Any, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from brain_v2.schemas.module import ModuleStatusResponse # Added import
from brain_v2.modules.mrm_connector.schemas import (
    MRMConnectorResult, FileRequest, TerminalRequest, GitRequest, MRMConnectorStatusResponse
)
from brain_v2.modules.mrm_connector.models import MRMSession

# Engine Imports
from brain_v2.modules.knowledge.service import KnowledgeEngineService
from brain_v2.modules.memory.service import MemoryEngineService
from brain_v2.modules.reasoning.service import ReasoningEngineService
from brain_v2.modules.decision.service import DecisionEngineService
from brain_v2.modules.planning.service import PlanningEngineService
from brain_v2.modules.task.service import TaskEngineService
from brain_v2.modules.project.service import ProjectEngineService
from brain_v2.modules.execution.service import ExecutionEngineService
from brain_v2.modules.learning.service import LearningEngineService

logger = logging.getLogger(__name__)


class MRMConnectorService(BaseModuleService):
    metadata = ModuleMetadata(
        key="mrm_connector",
        name="MRM Connector",
        description="Bridges Brain V2 with the MRM VS Code-style development environment.",
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
        execution: ExecutionEngineService,
        learning: LearningEngineService,
        db_session: Optional[AsyncSession] = None
    ):
        self.knowledge = knowledge
        self.memory = memory
        self.reasoning = reasoning
        self.decision = decision
        self.planning = planning
        self.task = task
        self.project_engine = project
        self.execution = execution
        self.learning = learning
        self.db = db_session

    async def status(self) -> MRMConnectorStatusResponse:
        return MRMConnectorStatusResponse(
            key=self.metadata.key,
            name=self.metadata.name,
            status="active",
            description=self.metadata.description,
            active_workspaces=1, # Mock
            total_operations_today=100 # Mock
        )

    async def handle_file_op(self, request: FileRequest) -> MRMConnectorResult:
        """Orchestrates file interactions through Execution Engine."""
        logger.info(f"MRM: File operation {request.op_type} on {request.path}")
        # In a real scenario, this would call the Execution Engine to perform the actual file I/O
        # For now, we'll simulate success.
        op_data = {"op": request.op_type, "path": request.path, "success": True, "timestamp": datetime.utcnow()}
        return MRMConnectorResult(
            workspace_id=request.workspace_id, project_id=request.project_id, file_operations=[op_data], status="success"
        )

    async def execute_terminal(self, request: TerminalRequest) -> MRMConnectorResult:
        """Proxy terminal commands to the Execution Engine."""
        from brain_v2.modules.execution.schemas import CommandExecutionRequest
        exec_req = CommandExecutionRequest(
            command=request.command.split()[0], args=request.command.split()[1:], work_dir=request.work_dir, context_id=request.context_id
        )
        exec_result = await self.execution.run_command(exec_req)
        terminal_op = {
            "command": request.command, "exit_code": 0 if exec_result.execution_status == "completed" else 1,
            "output": exec_result.logs, "errors": exec_result.errors
        }
        return MRMConnectorResult(
            workspace_id=request.workspace_id, terminal_operations=[terminal_op], status=exec_result.execution_status
        )

    async def handle_git(self, request: GitRequest) -> MRMConnectorResult:
        """Handles Git operations via specific CLI execution patterns."""
        logger.info(f"MRM: Git operation {request.action} for project {request.project_id}")
        # This would also call the Execution Engine for git commands
        git_op_data = {"action": request.action, "params": request.params, "result": "mocked_success", "timestamp": datetime.utcnow()}
        return MRMConnectorResult(
            workspace_id=request.workspace_id, project_id=request.project_id, git_operations=[git_op_data], status="success"
        )

    # Placeholder for _save_session_record if needed
    def _save_session_record(self, session_data: Dict[str, Any]):
        if self.db:
            # Logic to save or update MRMSession
            pass
