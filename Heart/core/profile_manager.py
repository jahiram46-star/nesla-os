from dataclasses import dataclass
from typing import Optional

from Heart.composer.voice_style_composer import VoiceStyleProfile
from Heart.learner.confidence_manager import ConfidenceManager


@dataclass
class VoiceProfile:
    user_id: str
    average_speed: float = 1.0
    average_pitch: str = "medium"
    average_pause: str = "low"
    average_energy: str = "medium"
    confidence_score: float = 0.0
    sample_count: int = 0


class VoiceProfileManager:
    """Manage voice profile aggregation and confidence updates."""

    def update_profile(
        self,
        user_id: str,
        base_profile: "VoiceProfile",
        new_style: VoiceStyleProfile,
        sample_count: int,
    ) -> "VoiceProfile":
        next_count = sample_count
        updated_speed = self._average(
            base_profile.average_speed,
            new_style.speed,
            base_profile.sample_count,
        )

        return VoiceProfile(
            user_id=user_id,
            average_speed=updated_speed,
            average_pitch=new_style.pitch,
            average_pause=new_style.pause,
            average_energy=new_style.energy,
            confidence_score=ConfidenceManager.estimate_confidence(next_count),
            sample_count=next_count,
        )

    @staticmethod
    def _average(current_value: float, new_value: float, count: int) -> float:
        if count <= 0:
            return new_value
        return (current_value * count + new_value) / (count + 1)
