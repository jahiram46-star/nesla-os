from pydantic import BaseModel


class RespondRequest(BaseModel):
    message: str
    language: str


class RespondResponse(BaseModel):
    response: str


class StatusResponse(BaseModel):
    module: str
    status: str
