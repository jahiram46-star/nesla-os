from typing import Dict


class PitchController:
    """Choose an appropriate pitch for Mouth based on learned style, tone, and emotion."""

    def select_pitch(self, learned_pitch: str, tone: str, emotion: str) -> str:
        if learned_pitch in {"low", "medium", "high"}:
            return learned_pitch
        if emotion == "excited":
            return "high"
        if emotion == "calm":
            return "low"
        if tone == "formal":
            return "medium"
        return "medium"
