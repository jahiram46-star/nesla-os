from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from brain_v2.db.session import get_db
from brain_v2.dependencies import (
    get_knowledge_service, get_memory_service, get_reasoning_service, get_decision_service, get_planning_service
)
from brain_v2.modules.task.service import TaskEngineService
from brain_v2.modules.knowledge.service import KnowledgeEngineService
from brain_v2.modules.memory.service import MemoryEngineService
from brain_v2.modules.reasoning.service import ReasoningEngineService
from brain_v2.modules.decision.service import DecisionEngineService
from brain_v2.modules.planning.service import PlanningEngineService

async def get_task_service(
    db: AsyncSession = Depends(get_db),
    knowledge: KnowledgeEngineService = Depends(get_knowledge_service),
    memory: MemoryEngineService = Depends(get_memory_service),
    reasoning: ReasoningEngineService = Depends(get_reasoning_service),
    decision: DecisionEngineService = Depends(get_decision_service),
    planning: PlanningEngineService = Depends(get_planning_service)
) -> TaskEngineService:
    """
    Dependency provider for TaskEngineService.
    """
    return TaskEngineService(
        knowledge=knowledge,
        memory=memory,
        reasoning=reasoning,
        decision=decision,
        planning=planning,
        db_session=db
    )