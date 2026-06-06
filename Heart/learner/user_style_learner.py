from typing import Dict, Any

from Heart.memory.heart_memory import HeartMemory


class UserStyleLearner:
    """Learns user speaking profile data from voice input."""

    def __init__(self) -> None:
        self.memory = HeartMemory()

    def learn(
        self,
        user_id: str,
        voice_payload: Dict[str, Any],
        emotion: str,
        tone: str,
        rhythm: str,
    ) -> Dict[str, Any]:
        """Extract speaking metrics and update historical voice patterns."""
        voice_profile = self.memory.get_or_create_voice_profile(user_id)

        speed = self._extract_speed(voice_payload, voice_profile.average_speed)
        pitch = self._extract_pitch(voice_payload, voice_profile.average_pitch)
        pause = self._extract_pause(voice_payload, voice_profile.average_pause)
        energy = self._extract_energy(voice_payload, voice_profile.average_energy)

        self.memory.record_voice_sample(user_id)
        self.memory.record_emotion(user_id, emotion)
        self.memory.record_tone(user_id, tone)
        self.memory.record_rhythm(user_id, rhythm)

        return {
            "speed": speed,
            "pitch": pitch,
            "pause": pause,
            "energy": energy,
        }

    @staticmethod
    def _extract_speed(voice_payload: Dict[str, Any], fallback_speed: float) -> float:
        speed_value = voice_payload.get("speed")
        try:
            if speed_value is not None:
                return float(speed_value)
        except (ValueError, TypeError):
            pass
        return float(fallback_speed or 1.0)

    @staticmethod
    def _extract_pitch(voice_payload: Dict[str, Any], fallback_pitch: str) -> str:
        pitch = voice_payload.get("pitch")
        if isinstance(pitch, str) and pitch.strip():
            normalized = pitch.strip().lower()
            if normalized in {"low", "medium", "high"}:
                return normalized
        return fallback_pitch

    @staticmethod
    def _extract_pause(voice_payload: Dict[str, Any], fallback_pause: str) -> str:
        pause = voice_payload.get("pause")
        if isinstance(pause, str) and pause.strip():
            normalized = pause.strip().lower()
            if normalized in {"low", "medium", "high"}:
                return normalized
        return fallback_pause

    @staticmethod
    def _extract_energy(voice_payload: Dict[str, Any], fallback_energy: str) -> str:
        energy = voice_payload.get("energy")
        if isinstance(energy, str) and energy.strip():
            normalized = energy.strip().lower()
            if normalized in {"low", "medium", "high"}:
                return normalized
        return fallback_energy
