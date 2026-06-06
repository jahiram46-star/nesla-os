import re
from typing import Any, Dict, Optional

from Heart.core.heart_core import HeartCore
from app.mouth.schemas import RespondResponse


_GREETINGS = {
    "bn": "আসসালামু আলাইকুম",
    "en": "Hello",
    "hi": "नमस्ते",
    "ar": "السلام عليكم",
}

_DEFAULT_RESPONSES = {
    "bn": "আপনার বার্তা প্রাপ্ত হয়েছে",
    "en": "I received your message",
    "hi": "आपका संदेश प्राप्त हुआ",
    "ar": "تم استلام رسالتك",
}

heart_core = HeartCore()


def respond(message: str, language: str) -> RespondResponse:
    lang = (language or "").lower()
    if lang not in _GREETINGS:
        lang = "en"

    text = (message or "").strip().lower()

    # greeting detection
    if re.search(r"\b(hello|hi|hey|salam|assalam|আসসালাম)\b", text):
        return RespondResponse(response=_GREETINGS.get(lang, _GREETINGS["en"]))

    # basic thanks
    if re.search(r"\b(thank|thanks|dhonnobad|ধন্যবাদ)\b", text):
        if lang == "bn":
            return RespondResponse(response="ধন্যবাদ")
        if lang == "hi":
            return RespondResponse(response="धन्यवाद")
        if lang == "ar":
            return RespondResponse(response="شكرا")
        return RespondResponse(response="Thanks")

    # fallback
    return RespondResponse(response=_DEFAULT_RESPONSES.get(lang, _DEFAULT_RESPONSES["en"]))


def analyze_voice_style(
    user_id: str,
    transcript: str,
    speed: Optional[float] = None,
    pitch: Optional[str] = None,
    pause: Optional[str] = None,
    energy: Optional[str] = None,
) -> Dict[str, Any]:
    voice_payload = {
        "transcript": transcript,
        "speed": speed,
        "pitch": pitch,
        "pause": pause,
        "energy": energy,
    }
    result = heart_core.process_voice(user_id=user_id, original_voice=voice_payload)
    return result.get("style_profile", {})
