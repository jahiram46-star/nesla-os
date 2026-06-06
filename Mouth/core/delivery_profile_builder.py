from typing import Any, Dict


DEFAULT_STYLE_VALUES = {
    "speed": "normal",
    "pitch": "medium",
    "pause": "normal",
    "energy": "normal",
}


def build_delivery_profile(brain_response: str, style_profile: Dict[str, Any]) -> Dict[str, Any]:
    """Combine brain response text and Heart V2 style profile into a delivery profile."""
    if not isinstance(style_profile, dict):
        style_profile = {}

    return {
        "response_text": brain_response,
        "speed": style_profile.get("speed", DEFAULT_STYLE_VALUES["speed"]),
        "pitch": style_profile.get("pitch", DEFAULT_STYLE_VALUES["pitch"]),
        "pause": style_profile.get("pause", DEFAULT_STYLE_VALUES["pause"]),
        "energy": style_profile.get("energy", DEFAULT_STYLE_VALUES["energy"]),
    }
