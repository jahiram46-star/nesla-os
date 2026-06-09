import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, JSON, DateTime
from brain_v2.db.base import Base

class DecisionLog(Base):
    __tablename__ = "decision_logs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    context_id = Column(String, index=True, nullable=False)
    selected_action = Column(String, nullable=False)
    decision_reason = Column(String)
    confidence_score = Column(Float, default=0.0)
    priority_score = Column(Float, default=0.0)
    
    # Store full result and metadata as JSON for future learning/auditing
    result_data = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<DecisionLog(id={self.id}, action={self.selected_action})>"