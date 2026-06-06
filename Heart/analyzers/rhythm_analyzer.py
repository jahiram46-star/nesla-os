from typing import Dict


class RhythmAnalyzer:
    """Analyze timing features to determine rhythm patterns."""

    def analyze(self, voice_payload: Dict[str, object]) -> str:
        speed = voice_payload.get("speed")
        if isinstance(speed, (int, float)):
            if speed >= 1.5:
                return "fast"
            if speed <= 0.7:
                return "slow"
            return "medium"

        if any(word in str(voice_payload.get("transcript", "")).lower() for word in ["quickly", "fast", "speed"]):
            return "fast"
        if any(word in str(voice_payload.get("transcript", "")).lower() for word in ["slow", "calmly", "quietly"]):
            return "slow"
        return "medium"
