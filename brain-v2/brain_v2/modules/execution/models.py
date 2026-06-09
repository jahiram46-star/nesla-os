import uuid
from datetime import datetime
from sqlalchemy import Column, String, JSON, DateTime, Text
from brain_v2.db.base import Base

class ExecutionRecord(Base):
    __tablename__ = "execution_records"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    execution_type = Column(String, nullable=False) # task, project, workflow, command
    status = Column(String, default="queued") # queued, running, completed, failed, rolled_back
    input_params = Column(JSON, default={})
    output_data = Column(JSON, default={})
    logs = Column(Text, default="")
    errors = Column(JSON, default=[])
    validation_result = Column(JSON, default={})
    rollback_status = Column(String, default="none") # none, pending, success, failed
    context_id = Column(String, index=True)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)