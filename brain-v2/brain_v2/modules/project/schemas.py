from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field

class ProjectAnalysisRequest(BaseModel):
    path: str
    context_id: str
    depth: int = 1

class ProjectAnalysisResult(BaseModel):
    project_id: str
    health_status: str
    dependencies: List[str] = []
    suggestions: List[str] = []
    structure_map: Dict[str, Any] = {}
    analyzed_at: datetime = Field(default_factory=datetime.utcnow)

class ProjectLifecycleRequest(BaseModel):
    project_id: str
    action: str # init, build, test, deploy
    context_id: str
    parameters: Dict[str, Any] = {}