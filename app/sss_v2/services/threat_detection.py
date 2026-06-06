from app.sss_v2.interfaces import ThreatDetector
from app.sss_v2.schemas import SecuritySignalCreate, ThreatAssessment


class FoundationThreatDetector(ThreatDetector):
    """Foundation detector that normalizes upstream security findings.

    A future AI detector can replace this implementation through ThreatDetector
    without changing monitoring, incident, alert, or IVR orchestration.
    """

    def assess(self, signal: SecuritySignalCreate) -> ThreatAssessment:
        return ThreatAssessment(
            category=signal.signal_type,
            severity=signal.severity,
            title=signal.title,
            description=signal.description,
            create_incident=True,
        )
