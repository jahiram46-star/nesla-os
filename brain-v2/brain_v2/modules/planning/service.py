from typing import List
from brain_v2.services.base import BaseModuleService, ModuleMetadata
from brain_v2.services.base import BaseModuleService, ModuleMetadata # Corrected import path
from brain_v2.modules.planning.schemas import (
    PlanRequest, PlanResult, PlanningStatusResponse, 
    ExecutionStep, Milestone
)
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession # Changed to AsyncSession
from brain_v2.modules.knowledge.service import KnowledgeEngineService
from brain_v2.modules.memory.service import MemoryEngineService
from brain_v2.modules.reasoning.service import ReasoningEngineService
from brain_v2.modules.decision.service import DecisionEngineService
from brain_v2.modules.planning.models import PlanRecord

class PlanningEngineService(BaseModuleService):
    metadata = ModuleMetadata(
        key="planning",
        name="Planning Engine",
        description="Transforms intelligent decisions into actionable multi-step execution plans.",
    )

    def __init__(
        self,
        knowledge: KnowledgeEngineService,
        memory: MemoryEngineService,
        reasoning: ReasoningEngineService,
        decision: DecisionEngineService,
        db_session: AsyncSession
    ):
        self.knowledge = knowledge
        self.memory = memory
        self.reasoning = reasoning
        self.decision = decision
        self.db = db_session
        self._plans_generated = 0

    async def status(self) -> PlanningStatusResponse:
        return PlanningStatusResponse(
            key=self.metadata.key,
            name=self.metadata.name,
            status="active",
            description=self.metadata.description,
            active_plans=0,
            plans_generated=self._plans_generated,
            supported_frameworks=["StepDecomposition", "DependencyMapping"]
        )

    async def generate_plan(self, request: PlanRequest) -> PlanResult:
        """
        Orchestrates Knowledge, Memory, and Decision results to build a structured plan.
        """
        decision = request.decision_result
        
        # 1. Strategic Breakdown
        # Consult knowledge for technical best practices if applicable
        # (Simulated search based on selected action)
        knowledge_ctx = await self.knowledge.search(decision.selected_action, limit=2)
        
        # 2. Task Breakdown (Pipeline logic)
        steps = self._decompose_action_to_steps(decision.selected_action, decision.dependencies)
        
        # 3. Milestone Generation
        milestones = [
            Milestone(
                title="Prerequisites Alignment",
                success_criteria=["Resources verified", "Dependencies mapped"]
            ),
            Milestone(
                title="Primary Execution",
                success_criteria=["Main action completed successfully"]
            )
        ]

        # 4. Risk Mitigation
        mitigation = {risk: f"Pre-check validation for {risk}" for risk in decision.risks}

        plan = PlanResult(
            goal=f"Execute {decision.selected_action} effectively.",
            milestones=milestones,
            execution_steps=steps,
            dependencies=decision.dependencies,
            required_resources=decision.required_resources,
            estimated_timeline="Short-term (Immediate Execution)",
            risk_mitigation_plan=mitigation,
            success_criteria=["Step execution without critical failures", "Goal alignment verified"],
            metadata={
                "confidence": decision.confidence_score,
                "context_id": request.context_id
            }
        )

        # Persistence: Save to PlanRecord
        if self.db:
            db_plan = PlanRecord(
                context_id=request.context_id,
                goal=plan.goal,
                plan_data=plan.dict(),
                status="active"
            )
            self.db.add(db_plan)
            self.db.commit()
            self.db.add(db_plan) # type: ignore
            await self.db.commit() # type: ignore

        self._plans_generated += 1
        return plan

    def _decompose_action_to_steps(self, action: str, deps: List[str]) -> List[ExecutionStep]:
        """Logic to turn a high-level action into individual steps."""
        # In production, this would use the Reasoning Engine's decomposition capabilities
        return [
            ExecutionStep(
                id="step_1",
                title="Environment Setup",
                description=f"Validate dependencies: {', '.join(deps)}",
                estimated_duration="2m"
            ),
            ExecutionStep(
                id="step_2",
                title="Action Trigger",
                description=f"Execute the core logic for {action}",
                dependencies=["step_1"],
                estimated_duration="5m"
            ),
            ExecutionStep(
                id="step_3",
                title="Verification",
                description="Post-action health check",
                dependencies=["step_2"],
                estimated_duration="1m"
            )
        ]