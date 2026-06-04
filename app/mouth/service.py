import re
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
