from typing import Dict


class ToneAnalyzer:
    """Analyze voice metadata to infer speaking tone."""

    def analyze(self, voice_payload: Dict[str, object]) -> str:
        transcript = str(voice_payload.get("transcript", "")).lower()
        if any(word in transcript for word in ["please", "thank you", "kindly"]):
            return "friendly"
        if any(word in transcript for word in ["sir", "madam", "regards"]):
            return "formal"
        if any(word in transcript for word in ["report", "summary", "analysis"]):
            return "professional"
        return "neutral"
