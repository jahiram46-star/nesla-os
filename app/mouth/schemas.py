from typing import Optional

from pydantic import BaseModel


class RespondRequest(BaseModel):
    message: str
    language: str


class RespondResponse(BaseModel):
    response: str


class VoiceProfileRequest(BaseModel):
    user_id: str
    transcript: str
    speed: Optional[float] = None
    pitch: Optional[str] = None
    pause: Optional[str] = None
    energy: Optional[str] = None


class StyleProfile(BaseModel):
    speed: float
    pitch: str
    pause: str
    energy: str


class VoiceProfileResponse(BaseModel):
    style_profile: StyleProfile


class StatusResponse(BaseModel):
    module: str
    status: str
