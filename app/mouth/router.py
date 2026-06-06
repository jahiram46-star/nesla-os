from fastapi import APIRouter
from app.mouth.schemas import (
    RespondRequest,
    RespondResponse,
    StatusResponse,
    VoiceProfileRequest,
    VoiceProfileResponse,
)
from app.mouth.service import analyze_voice_style, respond

router = APIRouter(prefix="/mouth", tags=["mouth"])


@router.post("/respond", response_model=RespondResponse)
def respond_endpoint(req: RespondRequest) -> RespondResponse:
    return respond(req.message, req.language)


@router.post("/voice-style", response_model=VoiceProfileResponse)
def voice_style_endpoint(req: VoiceProfileRequest) -> VoiceProfileResponse:
    style_profile = analyze_voice_style(
        user_id=req.user_id,
        transcript=req.transcript,
        speed=req.speed,
        pitch=req.pitch,
        pause=req.pause,
        energy=req.energy,
    )
    return VoiceProfileResponse(style_profile=style_profile)


@router.get("/status", response_model=StatusResponse)
def status() -> StatusResponse:
    return StatusResponse(module="Mouth", status="active")
