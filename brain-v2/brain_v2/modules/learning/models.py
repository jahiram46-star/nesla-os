import uuid
from datetime import datetime
from sqlalchemy import Column, String, JSON, DateTime, Float, Text
from brain_v2.db.base import Base

class LearningRecord(Base):
    __tablename__ = "learning_records"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    source_type = Column(String, nullable=False)  # execution, project, decision, feedback
    source_reference = Column(String, index=True) # ID of the execution/project
    
    lessons_learned = Column(JSON, default=[])
    detected_patterns = Column(JSON, default=[])
    success_factors = Column(JSON, default=[])
    failure_factors = Column(JSON, default=[])
    improvement_recommendations = Column(JSON, default=[])
    
    confidence_score = Column(Float, default=0.0)
    metadata_dump = Column(JSON, default={})
    
    created_at = Column(DateTime, default=datetime.utcnow)
    context_id = Column(String, index=True)

    def __repr__(self):
        return f"<LearningRecord(id={self.id}, source={self.source_type}, confidence={self.confidence_score})>"