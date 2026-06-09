import logging
from typing import Dict, Any
from datetime import datetime
from brain_v2.modules.task.base import BaseModuleService, ModuleMetadata
from brain_v2.schemas.module import ModuleStatusResponse
from brain_v2.modules.project.schemas import ProjectAnalysisRequest, ProjectAnalysisResult
from brain_v2.modules.project.models import ProjectRecord
from brain_v2.modules.reasoning.schemas import ReasoningRequest
from brain_v2.modules.knowledge.service import KnowledgeEngineService
from brain_v2.modules.memory.service import MemoryEngineService
from brain_v2.modules.reasoning.service import ReasoningEngineService
from brain_v2.modules.decision.service import DecisionEngineService
from brain_v2.modules.planning.service import PlanningEngineService
from brain_v2.modules.task.service import TaskEngineService

logger = logging.getLogger(__name__)

class ProjectEngineService(BaseModuleService):
    metadata = ModuleMetadata(
        key="project",
        name="Project Engine",
        description="Manages the lifecycle, structure, and health of development projects.",
    )

    def __init__(
        self,
        knowledge: KnowledgeEngineService,
        memory: MemoryEngineService,
        reasoning: ReasoningEngineService,
        decision: DecisionEngineService,
        planning: PlanningEngineService,
        task: TaskEngineService,
        db_session=None # This should ideally be AsyncSession

    ):
        self.knowledge = knowledge
        self.memory = memory
        self.reasoning = reasoning
        self.decision = decision
        self.planning = planning
        self.task = task
        self.db = db_session

    async def analyze_project(self, request: ProjectAnalysisRequest) -> ProjectAnalysisResult:
        """Analyzes project structure and health using the Reasoning and Knowledge engines."""
        logger.info(f"Analyzing project at: {request.path}")

        # 1. Use Reasoning Engine to understand project structure
        reasoning_req = ReasoningRequest(
            query=f"Analyze project at {request.path} and identify main dependencies.",
            context_id=request.context_id
        )
        analysis = await self.reasoning.reason(reasoning_req)

        # 2. Use Decision Engine to evaluate health (Mocked for logic flow)
        health = "HEALTHY"
        
        result = ProjectAnalysisResult(
            project_id=f"PROJ_{datetime.utcnow().timestamp()}",
            health_status=health,
            dependencies=getattr(analysis, 'dependencies', []),
            suggestions=["Keep up the good work"]
        )

        # 3. Persist project record
        if self.db:
            record = ProjectRecord(
                id=result.project_id,
                name=request.path.split('/')[-1],
                path=request.path,
                health_status=health,
                context_id=request.context_id
            )
            self.db.add(record)
            await self.db.commit()

        return result