from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel, Field

from Heart.core.heart_core import HeartCore

router = APIRouter(prefix="/heart/v2", tags=["heart_v2"])
heart_core = HeartCore()


class HeartInput(BaseModel):
    user_id: str = Field(..., description="Unique end-user identifier")
    transcript: str = Field(..., description="Transcribed user speech")
    speed: Optional[float] = Field(None, description="Measured speaking speed")
    pitch: Optional[str] = Field(None, description="Measured speaking pitch")
    pause: Optional[str] = Field(None, description="Measured speaking pause style")
    energy: Optional[str] = Field(None, description="Measured speaking energy")


class StyleProfile(BaseModel):
    speed: float
    pitch: str
    pause: str
    energy: str


class HeartOutput(BaseModel):
    style_profile: StyleProfile


class StatusResponse(BaseModel):
    module: str
    status: str


@router.post("/profile", response_model=HeartOutput)
def analyze_voice_profile(payload: HeartInput) -> HeartOutput:
    result = heart_core.process_voice(user_id=payload.user_id, original_voice=payload.dict())
    return HeartOutput(style_profile=result["style_profile"])


@router.get("/status", response_model=StatusResponse)
def status() -> StatusResponse:
    return StatusResponse(module="Heart V2", status="active")
