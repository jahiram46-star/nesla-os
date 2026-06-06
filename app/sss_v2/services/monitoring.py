from typing import Optional

from sqlalchemy.orm import Session

from app.sss_v2.interfaces import ThreatDetector
from app.sss_v2.models import (
    AdminAlert,
    Incident,
    IvrCallWorkflow,
    ProjectHealthSnapshot,
    SecuritySignal,
)
from app.sss_v2.schemas import (
    HealthStatus,
    ProjectHealthMonitoringResult,
    ProjectHealthSnapshotCreate,
    SecurityMonitoringResult,
    SecuritySignalCreate,
    Severity,
    ThreatAssessment,
)


class SssV2MonitoringService:
    """Orchestrates monitoring, incidents, admin alerts, and IVR queueing."""

    def __init__(self, db: Session, threat_detector: ThreatDetector) -> None:
        self.db = db
        self.threat_detector = threat_detector

    def ingest_security_signal(self, payload: SecuritySignalCreate) -> SecurityMonitoringResult:
        signal = SecuritySignal(**payload.dict())
        self.db.add(signal)
        self.db.flush()

        assessment = self.threat_detector.assess(payload)
        incident, alert, ivr = self._create_response(
            source_type="security_signal",
            source_id=signal.id,
            assessment=assessment,
        )
        self.db.commit()
        self._refresh(signal, incident, alert, ivr)

        return SecurityMonitoringResult(
            signal=signal,
            incident=incident,
            admin_alert=alert,
            ivr_workflow=ivr,
        )

    def ingest_project_health(
        self,
        payload: ProjectHealthSnapshotCreate,
    ) -> ProjectHealthMonitoringResult:
        snapshot = ProjectHealthSnapshot(**payload.dict())
        self.db.add(snapshot)
        self.db.flush()

        assessment = self._assess_project_health(payload)
        incident = alert = ivr = None
        if assessment is not None:
            incident, alert, ivr = self._create_response(
                source_type="project_health",
                source_id=snapshot.id,
                assessment=assessment,
            )

        self.db.commit()
        self._refresh(snapshot, incident, alert, ivr)
        return ProjectHealthMonitoringResult(
            snapshot=snapshot,
            incident=incident,
            admin_alert=alert,
            ivr_workflow=ivr,
        )

    def _create_response(
        self,
        source_type: str,
        source_id: int,
        assessment: ThreatAssessment,
    ) -> tuple[Optional[Incident], Optional[AdminAlert], Optional[IvrCallWorkflow]]:
        if not assessment.create_incident:
            return None, None, None

        is_critical = assessment.severity == Severity.critical
        incident = Incident(
            source_type=source_type,
            source_id=source_id,
            category=assessment.category,
            severity=assessment.severity.value,
            title=assessment.title,
            description=assessment.description,
            requires_admin_alert=is_critical,
            requires_ivr_call=is_critical,
        )
        self.db.add(incident)
        self.db.flush()

        if not is_critical:
            return incident, None, None

        alert = AdminAlert(
            incident_id=incident.id,
            severity=assessment.severity.value,
            title=assessment.title,
            message=assessment.description,
            status="pending",
        )
        ivr = IvrCallWorkflow(
            incident_id=incident.id,
            priority="critical",
            recipient_group="administrators",
            message=assessment.description,
            status="queued",
        )
        self.db.add_all([alert, ivr])
        return incident, alert, ivr

    @staticmethod
    def _assess_project_health(
        payload: ProjectHealthSnapshotCreate,
    ) -> Optional[ThreatAssessment]:
        if payload.status == HealthStatus.healthy:
            return None

        severity = Severity.critical if payload.status == HealthStatus.critical else Severity.high
        return ThreatAssessment(
            category="project_health",
            severity=severity,
            title=f"{payload.project_name}/{payload.component} health is {payload.status.value}",
            description=payload.summary,
        )

    def _refresh(self, *records: object) -> None:
        for record in records:
            if record is not None:
                self.db.refresh(record)
