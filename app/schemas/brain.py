from datetime import datetime

from pydantic import BaseModel


class BrainChat(BaseModel):
    message: str


class BrainAsk(BaseModel):
    message: str


class BrainChatResponse(BaseModel):
    user_message: str
    response: str
    timestamp: datetime

    class Config:
        from_attributes = True


class BrainProcessRequest(BaseModel):
    message: str


class BrainProcessResponse(BaseModel):
    message: str
    emotion: str
    intent: str
    priority: str
    response: str
