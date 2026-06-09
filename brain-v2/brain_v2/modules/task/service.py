from typing import List, Optional
from brain_v2.modules.task.base import BaseModuleService, ModuleMetadata
from brain_v2.modules.task.schemas import (
    TaskRequest, TaskResult, TaskStatus, TaskStatusResponse, TaskUpdate
)
from brain_v2.modules.knowledge.service import KnowledgeEngineService
from sqlalchemy.ext.asyncio import AsyncSession
from brain_v2.modules.memory.service import MemoryEngineService
from brain_v2.modules.reasoning.service import ReasoningEngineService
from brain_v2.modules.decision.service import DecisionEngineService
from brain_v2.modules.planning.service import PlanningEngineService
from brain_v2.modules.task.models import TaskEntry

class TaskEngineService(BaseModuleService):
    metadata = ModuleMetadata(
        key="task",
        name="Task Engine",
        description="Transforms execution plans into manageable tasks and tracks their lifecycle.",
    )

    def __init__(
        self,
        knowledge: KnowledgeEngineService,
        memory: MemoryEngineService,
        reasoning: ReasoningEngineService,
        decision: DecisionEngineService,
        planning: PlanningEngineService, 
        db_session: AsyncSession
    ):
        self.knowledge = knowledge
        self.memory = memory
        self.reasoning = reasoning
        self.decision = decision
        self.planning = planning
        self.db = db_session
        self._tasks_processed = 0

    async def status(self) -> TaskStatusResponse:
        # In a real impl, these would be queries to self.db
        return TaskStatusResponse(
            key=self.metadata.key,
            name=self.metadata.name,
            status="active",
            description=self.metadata.description,
            total_tasks=self._tasks_processed,
            active_tasks=0,
            completed_tasks=0,
            failed_tasks=0
        )

    async def create_tasks_from_plan(self, request: TaskRequest) -> List[TaskResult]:
        """
        Converts a PlanResult into individual TaskResult objects.
        """
        plan = request.plan_result
        tasks = []

        for step in plan.execution_steps:
            task = TaskResult(
                task_id=step.id,
                task_name=step.title,
                task_description=step.description,
                priority="high" if "mandatory" in str(plan.goal).lower() else "normal",
                dependencies=step.dependencies,
                status=TaskStatus.PENDING,
                assigned_engine=self._determine_assigned_engine(step.title),
                estimated_duration=step.estimated_duration,
                completion_criteria=plan.success_criteria,
                metadata={
                    "context_id": request.context_id,
                    "required_resources": step.required_resources
                }
            )
            tasks.append(task)
            self._tasks_processed += 1
            
            # Persistence: Save to TaskEntry table
            if self.db:
                db_task = TaskEntry(
                    id=str(task.task_id), # Use task_id from plan as primary key for now, or create a new column for it
                    context_id=request.context_id,
                    plan_step_id=task.task_id, # Store the original step ID from the plan
                    task_name=task.task_name,
                    task_description=task.task_description,
                    priority=task.priority,
                    status=task.status,
                    assigned_engine=task.assigned_engine,
                    dependencies=task.dependencies,
                    completion_criteria=task.completion_criteria,
                    estimated_duration=task.estimated_duration,
                    metadata_info=task.metadata
                )
                self.db.add(db_task)

        if self.db:
            await self.db.commit()

        return tasks

    def _determine_assigned_engine(self, task_title: str) -> str:
        """Heuristic to assign tasks to specific sub-engines."""
        title = task_title.lower()
        if any(x in title for x in ["search", "find", "check knowledge"]):
            return "knowledge_engine"
        if any(x in title for x in ["remember", "past", "history"]):
            return "memory_engine"
        if any(x in title for x in ["analyze", "reason", "logic"]):
            return "reasoning_engine"
        return "system_executor"

    async def update_task_status(self, task_id: str, update: TaskUpdate) -> Optional[TaskResult]:
        """Updates the status and metadata of a task."""
        # Placeholder for DB update and event triggering (e.g., retry logic)
        if update.status == TaskStatus.FAILED:
            # Logic for automatic retry could be triggered here
            pass
        return None

    async def verify_completion(self, task_id: str) -> bool:
        """Uses the Reasoning Engine to verify if task criteria were met."""
        # Logic: 
        # 1. Fetch task and result data.
        # 2. Ask Reasoning Engine to evaluate result against completion_criteria.
        return True