from typing import Any, Dict

from .delivery_profile_builder import build_delivery_profile
from .speech_package_builder import build_speech_package


def create_final_speech_package(brain_response: str, style_profile: Dict[str, Any]) -> Dict[str, Any]:
    """Produce the final delivery package without changing brain output."""
    delivery_profile = build_delivery_profile(brain_response=brain_response, style_profile=style_profile)
    return build_speech_package(delivery_profile=delivery_profile)
