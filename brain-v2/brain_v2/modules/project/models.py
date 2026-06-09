import uuid
from datetime import datetime
from sqlalchemy import Column, String, JSON, DateTime
from brain_v2.db.base import Base

class ProjectRecord(Base):
    __tablename__ = "project_records"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    path = Column(String, nullable=False)
    project_type = Column(String, nullable=True)
    health_status = Column(String, default="UNKNOWN")
    metadata_dump = Column(JSON, default={})
    context_id = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)