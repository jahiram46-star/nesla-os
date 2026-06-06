
class ConfidenceManager:
    """Estimate confidence based on the number of collected voice samples."""

    @staticmethod
    def estimate_confidence(sample_count: int) -> float:
        if sample_count <= 0:
            return 0.0
        if sample_count < 10:
            return 5.0 * sample_count
        if sample_count < 100:
            return 25.0 + (sample_count - 10) * 0.5
        if sample_count < 1000:
            return 70.0 + (sample_count - 100) * 0.027
        return 95.0
