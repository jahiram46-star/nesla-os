from typing import List, Optional
from pydantic import BaseModel

class DecisionResult(BaseModel):
    selected_action: str
    decision_reason: str
    confidence_score: float
    priority_score: float
    risks: List[str] = []
    dependencies: List[str] = []
    required_resources: List[str] = []
    recommended_next_steps: List[str] = []

class DecisionRequest(BaseModel):
    query: str
    context_id: str
    options: Optional[List[str]] = None