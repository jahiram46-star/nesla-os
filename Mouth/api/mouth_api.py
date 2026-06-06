from typing import Any, Dict, Union

from fastapi import APIRouter
from pydantic import BaseModel, Field

from Mouth.core.mouth_controller import create_final_speech_package
from Mouth.integrations.heart_connector import HeartConnector

router = APIRouter(prefix="/mouth/v2", tags=["mouth_v2"])
heart_connector = HeartConnector()


class MouthV2Request(BaseModel):
    user_id: str = Field(..., description="Unique end-user identifier")
    brain_response: str = Field(..., description="Response text from Brain")


class FinalSpeechPackage(BaseModel):
    response_text: str
    speed: Union[float, str]
    pitch: str
    pause: str
    energy: str


@router.post("/package", response_model=FinalSpeechPackage)
def build_package(payload: MouthV2Request) -> FinalSpeechPackage:
    style_profile: Dict[str, Any] = heart_connector.get_style_profile(payload.user_id)
    final_package: Dict[str, Any] = create_final_speech_package(
        brain_response=payload.brain_response,
        style_profile=style_profile,
    )
    return FinalSpeechPackage(**final_package)


@router.get("/status")
def status() -> Dict[str, str]:
    return {"module": "Mouth V2", "status": "active"}
