from datetime import datetime

from pydantic import BaseModel


class MemoryCreate(BaseModel):
    user_message: str
    ai_response: str


class MemoryRead(BaseModel):
    id: int
    user_message: str
    ai_response: str
    created_at: datetime

    class Config:
        from_attributes = True
