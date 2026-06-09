from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class ExecutionStep(BaseModel):
    id: str
    title: str
    description: str
    dependencies: List[str] = []
    required_resources: List[str] = []
    estimated_duration: str = "1m"

class Milestone(BaseModel):
    title: str
    success_criteria: List[str]

class PlanResult(BaseModel):
    goal: str
    milestones: List[Milestone]
    execution_steps: List[ExecutionStep]
    dependencies: List[str] = []
    required_resources: List[str] = []
    estimated_timeline: str
    risk_mitigation_plan: Dict[str, Any] = {}
    success_criteria: List[str]

class PlanRequest(BaseModel):
    decision_result: Any
    context_id: str