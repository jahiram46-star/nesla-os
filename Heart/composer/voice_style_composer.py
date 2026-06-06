from dataclasses import dataclass
from typing import Dict


@dataclass
class VoiceStyleProfile:
    speed: float
    pitch: str
    pause: str
    energy: str


class VoiceStyleComposer:
    """Compose a delivery style profile for Mouth."""

    def build_style_profile(self, speed: float, pitch: str, pause: str, energy: str) -> VoiceStyleProfile:
        return VoiceStyleProfile(
            speed=max(0.1, float(speed)),
            pitch=self._normalize_pitch(pitch),
            pause=self._normalize_pause(pause),
            energy=self._normalize_energy(energy),
        )

    def serialize(self, profile: VoiceStyleProfile) -> Dict[str, object]:
        return {
            "speed": profile.speed,
            "pitch": profile.pitch,
            "pause": profile.pause,
            "energy": profile.energy,
        }

    @staticmethod
    def _normalize_pitch(value: str) -> str:
        if value and value.lower() in {"low", "medium", "high"}:
            return value.lower()
        return "medium"

    @staticmethod
    def _normalize_pause(value: str) -> str:
        if value and value.lower() in {"low", "medium", "high"}:
            return value.lower()
        return "medium"

    @staticmethod
    def _normalize_energy(value: str) -> str:
        if value and value.lower() in {"low", "medium", "high"}:
            return value.lower()
        return "medium"
