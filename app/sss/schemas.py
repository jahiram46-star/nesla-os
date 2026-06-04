from datetime import datetime

from pydantic import BaseModel


class StatusResponse(BaseModel):
    module: str
    status: str


class ModuleStatus(BaseModel):
    name: str
    status: str


class SystemEventCreate(BaseModel):
    module_name: str
    event_type: str
    message: str


class SystemEventRead(BaseModel):
    id: int
    module_name: str
    event_type: str
    message: str
    created_at: datetime

    class Config:
        from_attributes = True
