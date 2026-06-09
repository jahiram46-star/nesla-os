from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from brain_v2.db.session import get_db

# Import all engine services
from brain_v2.modules.knowledge.service import KnowledgeEngineService
from brain_v2.modules.memory.service import MemoryEngineService
from brain_v2.modules.reasoning.service import ReasoningEngineService
from brain_v2.modules.decision.service import DecisionEngineService
from brain_v2.modules.planning.service import PlanningEngineService
from brain_v2.modules.task.service import TaskEngineService
from brain_v2.modules.project.service import ProjectEngineService
from brain_v2.modules.execution.service import ExecutionEngineService
from brain_v2.modules.learning.service import LearningEngineService
from brain_v2.modules.mrm_connector.service import MRMConnectorService


async def get_knowledge_service() -> KnowledgeEngineService:
    """Dependency provider for KnowledgeEngineService."""
    return KnowledgeEngineService()

async def get_memory_service(db: AsyncSession = Depends(get_db)) -> MemoryEngineService:
    """Dependency provider for MemoryEngineService."""
    return MemoryEngineService(db_session=db)

async def get_reasoning_service(
    knowledge: KnowledgeEngineService = Depends(get_knowledge_service),
    memory: MemoryEngineService = Depends(get_memory_service)
) -> ReasoningEngineService:
    """Dependency provider for ReasoningEngineService."""
    return ReasoningEngineService(knowledge=knowledge, memory=memory)

async def get_decision_service(
    knowledge: KnowledgeEngineService = Depends(get_knowledge_service),
    memory: MemoryEngineService = Depends(get_memory_service),
    reasoning: ReasoningEngineService = Depends(get_reasoning_service)
) -> DecisionEngineService:
    """Dependency provider for DecisionEngineService."""
    return DecisionEngineService(knowledge=knowledge, memory=memory, reasoning=reasoning)

async def get_planning_service(
    knowledge: KnowledgeEngineService = Depends(get_knowledge_service),
    memory: MemoryEngineService = Depends(get_memory_service),
    reasoning: ReasoningEngineService = Depends(get_reasoning_service),
    decision: DecisionEngineService = Depends(get_decision_service)
) -> PlanningEngineService:
    """Dependency provider for PlanningEngineService."""
    return PlanningEngineService(knowledge=knowledge, memory=memory, reasoning=reasoning, decision=decision)

async def get_task_service(
    db: AsyncSession = Depends(get_db),
    knowledge: KnowledgeEngineService = Depends(get_knowledge_service),
    memory: MemoryEngineService = Depends(get_memory_service),
    reasoning: ReasoningEngineService = Depends(get_reasoning_service),
    decision: DecisionEngineService = Depends(get_decision_service),
    planning: PlanningEngineService = Depends(get_planning_service)
) -> TaskEngineService:
    """Dependency provider for TaskEngineService."""
    return TaskEngineService(
        knowledge=knowledge, memory=memory, reasoning=reasoning,
        decision=decision, planning=planning, db_session=db
    )

async def get_project_service(
    db: AsyncSession = Depends(get_db),
    knowledge: KnowledgeEngineService = Depends(get_knowledge_service),
    memory: MemoryEngineService = Depends(get_memory_service),
    reasoning: ReasoningEngineService = Depends(get_reasoning_service),
    decision: DecisionEngineService = Depends(get_decision_service),
    planning: PlanningEngineService = Depends(get_planning_service),
    task: TaskEngineService = Depends(get_task_service)
) -> ProjectEngineService:
    """Dependency provider for ProjectEngineService."""
    return ProjectEngineService(
        knowledge=knowledge, memory=memory, reasoning=reasoning,
        decision=decision, planning=planning, task=task, db_session=db
    )

async def get_execution_service() -> ExecutionEngineService:
    """Dependency provider for ExecutionEngineService."""
    # ExecutionEngineService might have its own dependencies,
    # but for now, we'll assume it can be initialized directly.
    return ExecutionEngineService()

async def get_learning_service(
    knowledge: KnowledgeEngineService = Depends(get_knowledge_service),
    memory: MemoryEngineService = Depends(get_memory_service),
    reasoning: ReasoningEngineService = Depends(get_reasoning_service),
    decision: DecisionEngineService = Depends(get_decision_service),
    planning: PlanningEngineService = Depends(get_planning_service),
    task: TaskEngineService = Depends(get_task_service),
    project: ProjectEngineService = Depends(get_project_service),
    execution: ExecutionEngineService = Depends(get_execution_service),
    db: AsyncSession = Depends(get_db)
) -> LearningEngineService:
    """Dependency provider for LearningEngineService."""
    return LearningEngineService(
        knowledge=knowledge, memory=memory, reasoning=reasoning,
        decision=decision, planning=planning, task=task, project=project,
        execution=execution, db_session=db
    )

async def get_mrm_connector_service(
    knowledge: KnowledgeEngineService = Depends(get_knowledge_service),
    memory: MemoryEngineService = Depends(get_memory_service),
    reasoning: ReasoningEngineService = Depends(get_reasoning_service),
    decision: DecisionEngineService = Depends(get_decision_service),
    planning: PlanningEngineService = Depends(get_planning_service),
    task: TaskEngineService = Depends(get_task_service),
    project: ProjectEngineService = Depends(get_project_service),
    execution: ExecutionEngineService = Depends(get_execution_service),
    learning: LearningEngineService = Depends(get_learning_service)
) -> MRMConnectorService:
    """Dependency provider for MRMConnectorService."""
    return MRMConnectorService(
        knowledge=knowledge, memory=memory, reasoning=reasoning,
        decision=decision, planning=planning, task=task, project=project,
        execution=execution, learning=learning
    )