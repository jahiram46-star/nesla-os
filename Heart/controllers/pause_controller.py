

class PauseController:
    """Choose pause patterns for Mouth based on learned style and rhythm."""

    def select_pause(self, learned_pause: str, rhythm: str) -> str:
        if learned_pause in {"low", "medium", "high"}:
            return learned_pause
        if rhythm == "fast":
            return "low"
        if rhythm == "slow":
            return "high"
        return "medium"
