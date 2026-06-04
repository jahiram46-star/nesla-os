from pydantic import BaseModel


class AnalyzeRequest(BaseModel):
    message: str


class AnalyzeResponse(BaseModel):
    emotion: str
    intent: str
    priority: str


class StatusResponse(BaseModel):
    module: str
    status: str
