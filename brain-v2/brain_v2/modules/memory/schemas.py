from enum import Enum
from typing import Any, Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from brain_v2.schemas.module import ModuleStatusResponse

class MemoryType(str, Enum):
    USER = "user"
    PROJECT = "project"
    TASK = "task"
    SESSION = "session"
    KNOWLEDGE = "knowledge"
    SYSTEM = "system"

class MemoryBase(BaseModel):
    memory_type: MemoryType
    context_id: str
    key: Optional[str] = None
    content: str
    metadata: Dict[str, Any] = Field(default_factory=dict)

class MemoryCreate(MemoryBase):
    pass

class MemoryUpdate(BaseModel):
    content: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class MemoryRead(MemoryBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class MemorySearchRequest(BaseModel):
    query: str
    memory_type: Optional[MemoryType] = None
    context_id: Optional[str] = None
    limit: int = 10

class MemoryStatusResponse(ModuleStatusResponse):
    total_entries: int
    active_sessions: int
    storage_backend: str

class MemoryContextResponse(BaseModel):
    context_string: str
    memories: List[MemoryRead]