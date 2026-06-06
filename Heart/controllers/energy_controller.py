

class EnergyController:
    """Choose energy delivery for Mouth based on learned style, emotion, and tone."""

    def select_energy(self, learned_energy: str, emotion: str, tone: str) -> str:
        if learned_energy in {"low", "medium", "high"}:
            return learned_energy
        if emotion in ["excited", "happy"]:
            return "high"
        if emotion in ["sad", "calm"]:
            return "low"
        if tone == "professional":
            return "medium"
        return "medium"
