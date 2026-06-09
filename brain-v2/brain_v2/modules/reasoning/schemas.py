from typing import List, Optional
from pydantic import BaseModel

class ReasoningRequest(BaseModel):
    query: str
    context_id: str
    depth: int = 1

class ReasoningResult(BaseModel):
    understanding: str
    steps: List[str]
    context_summary: str
    dependencies: List[str] = []
    recommended_actions: List[str] = []