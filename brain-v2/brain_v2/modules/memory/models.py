import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, JSON, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from brain_v2.db.base import Base # Assuming Base is defined in core db
from brain_v2.modules.memory.schemas import MemoryType

class MemoryEntry(Base):
    __tablename__ = "memory_entries"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    memory_type = Column(SQLEnum(MemoryType), nullable=False, index=True)
    context_id = Column(String, nullable=False, index=True)
    key = Column(String, nullable=True, index=True)
    content = Column(Text, nullable=False)
    metadata = Column(JSON, default={})
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<MemoryEntry(id={self.id}, type={self.memory_type}, key={self.key})>"