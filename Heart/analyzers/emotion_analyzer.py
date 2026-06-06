from typing import Dict


class EmotionAnalyzer:
    """Analyze incoming voice metadata to identify emotion patterns."""

    def analyze(self, voice_payload: Dict[str, object]) -> str:
        transcript = str(voice_payload.get("transcript", "")).lower()
        if any(word in transcript for word in ["happy", "joy", "excited"]):
            return "happy"
        if any(word in transcript for word in ["sad", "upset", "down"]):
            return "sad"
        if any(word in transcript for word in ["calm", "relaxed", "peaceful"]):
            return "calm"
        if any(word in transcript for word in ["angry", "mad", "frustrated"]):
            return "angry"
        if any(word in transcript for word in ["wow", "great", "amazing"]):
            return "excited"
        return "neutral"
