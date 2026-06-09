from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field
from brain_v2.schemas.module import ModuleStatusResponse

class LearningResult(BaseModel):
    learning_id: str
    source_type: str
    source_reference: str
    lessons_learned: List[str] = Field(default_factory=list)
    detected_patterns: List[str] = Field(default_factory=list)
    success_factors: List[str] = Field(default_factory=list)
    failure_factors: List[str] = Field(default_factory=list)
    improvement_recommendations: List[str] = Field(default_factory=list)
    confidence_score: float
    processed_at: datetime = Field(default_factory=datetime.utcnow)

class LearningRequest(BaseModel):
    source_id: str
    source_type: str  # execution, project, decision
    context_id: str
    analysis_depth: str = "standard"  # standard, deep, forensic
    include_historical_context: bool = True

class FeedbackRequest(BaseModel):
    source_id: str
    rating: int  # 1-5
    comment: Optional[str] = None
    correction_details: Optional[Dict[str, Any]] = None

class LearningStatusResponse(ModuleStatusResponse):
    total_lessons_learned: int
    active_learning_pipelines: int
    last_optimized_at: Optional[datetime] = None
    system_improvement_index: float # 0.0 to 1.0