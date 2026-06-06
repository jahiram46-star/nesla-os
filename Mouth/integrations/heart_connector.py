from typing import Any, Dict, Optional

from Mouth.core.delivery_profile_builder import DEFAULT_STYLE_VALUES


class HeartConnector:
    """Connector for reading Heart V2 style profiles from the Heart persistence layer."""

    def __init__(self, memory: Optional[Any] = None) -> None:
        self.memory = memory if memory is not None else self._load_memory()

    def _load_memory(self) -> Any:
        from Heart.memory.heart_memory import HeartMemory

        return HeartMemory()

    def get_style_profile(self, user_id: str) -> Dict[str, Any]:
        voice_profile = self.memory.get_or_create_voice_profile(user_id)
        raw_profile = {
            "speed": voice_profile.average_speed,
            "pitch": voice_profile.average_pitch,
            "pause": voice_profile.average_pause,
            "energy": voice_profile.average_energy,
        }
        return self._validate_style_profile(raw_profile)

    def _validate_style_profile(self, style_profile: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "speed": self._validate_speed(style_profile.get("speed")),
            "pitch": self._validate_text(style_profile.get("pitch"), DEFAULT_STYLE_VALUES["pitch"]),
            "pause": self._validate_text(style_profile.get("pause"), DEFAULT_STYLE_VALUES["pause"]),
            "energy": self._validate_text(style_profile.get("energy"), DEFAULT_STYLE_VALUES["energy"]),
        }

    def _validate_speed(self, value: Any) -> Any:
        if isinstance(value, (int, float)):
            return float(value)
        if isinstance(value, str) and value.strip():
            return value.strip()
        return DEFAULT_STYLE_VALUES["speed"]

    @staticmethod
    def _validate_text(value: Any, default: str) -> str:
        if isinstance(value, str) and value.strip():
            return value.strip()
        return default
