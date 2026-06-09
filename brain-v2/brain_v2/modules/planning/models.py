import uuid
from datetime import datetime
from sqlalchemy import Column, String, JSON, DateTime, Text
from brain_v2.db.base import Base

class PlanRecord(Base):
    __tablename__ = "plan_records"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    context_id = Column(String, index=True, nullable=False)
    goal = Column(Text, nullable=False)
    
    # Store the entire PlanResult as JSON for auditability
    plan_data = Column(JSON, nullable=False)
    
    status = Column(String, default="draft")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<PlanRecord(id={self.id}, goal={self.goal[:30]}...)>"