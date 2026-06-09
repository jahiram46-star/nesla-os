import uuid
from datetime import datetime
from sqlalchemy import Column, String, JSON, DateTime, Text, Float, Enum as SQLEnum
from brain_v2.db.base import Base
from brain_v2.modules.task.schemas import TaskStatus

class TaskEntry(Base):
    __tablename__ = "task_entries"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    context_id = Column(String, index=True, nullable=False) # Context ID from the overall operation
    plan_step_id = Column(String, nullable=False, index=True) # ID from the planning execution step
    task_name = Column(String, nullable=False)
    task_description = Column(Text)
    priority = Column(String, default="normal")
    
    status = Column(SQLEnum(TaskStatus), default=TaskStatus.PENDING)
    progress = Column(Float, default=0.0)
    assigned_engine = Column(String) # Which engine is responsible for executing this task
    
    dependencies = Column(JSON, default=[]) # List of task IDs
    completion_criteria = Column(JSON, default=[])
    estimated_duration = Column(String, nullable=True) # e.g., "1m", "5m"
    result_data = Column(JSON, default={})
    metadata_info = Column(JSON, default={})

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<TaskEntry(id={self.id}, name={self.task_name}, status={self.status})>"