import uuid
from datetime import datetime
from sqlalchemy import Column, String, JSON, DateTime
from brain_v2.db.base import Base

class MRMSession(Base):
    __tablename__ = "mrm_sessions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    workspace_id = Column(String, index=True, nullable=False)
    project_id = Column(String, nullable=True)
    operation_history = Column(JSON, default=[])
    current_context_id = Column(String, nullable=True)
    status = Column(String, default="active")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)