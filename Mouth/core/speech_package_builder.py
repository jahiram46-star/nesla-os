from typing import Any, Dict


def build_speech_package(delivery_profile: Dict[str, Any]) -> Dict[str, Any]:
    """Create the final speech package from the merged delivery profile."""
    return {
        "response_text": delivery_profile["response_text"],
        "speed": delivery_profile["speed"],
        "pitch": delivery_profile["pitch"],
        "pause": delivery_profile["pause"],
        "energy": delivery_profile["energy"],
    }
