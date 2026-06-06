from typing import Optional

from sqlalchemy.orm import Session

from app.sss_v2.models import AdminAlert, ComponentHealthCheck, Incident
from app.sss_v2.schemas import (
    ComponentHealthCheckCreate,
    ComponentMonitoringResult,
    ComponentStatus,
)
from app.sss_v2.services.alert_manager import AlertManager


class ComponentMonitorService:
    """Monitors reported NESLA OS component health without invoking component logic."""

    def __init__(self, db: Session, alert_manager: Optional[AlertManager] = None) -> None:
        self.db = db
        self.alert_manager = alert_manager or AlertManager(db)

    def record_check(self, payload: ComponentHealthCheckCreate) -> ComponentMonitoringResult:
        check = ComponentHealthCheck(**payload.dict())
        self.db.add(check)
        self.db.flush()

        failure_detected = payload.status == ComponentStatus.failed
        incident = alert = None
        if failure_detected:
            incident = self._create_failure_incident(check)
            alert = self.alert_manager.create_for_incident(incident)

        self.db.commit()
        self.db.refresh(check)
        if incident is not None:
            self.db.refresh(incident)
        if alert is not None:
            self.db.refresh(alert)

        return ComponentMonitoringResult(
            check=check,
            failure_detected=failure_detected,
            incident=incident,
            admin_alert=alert,
        )

    def latest_checks(self) -> list[ComponentHealthCheck]:
        checks = (
            self.db.query(ComponentHealthCheck)
            .order_by(ComponentHealthCheck.checked_at.desc(), ComponentHealthCheck.id.desc())
            .all()
        )
        latest_by_component: dict[str, ComponentHealthCheck] = {}
        for check in checks:
            latest_by_component.setdefault(check.component, check)
        return list(latest_by_component.values())

    def _create_failure_incident(self, check: ComponentHealthCheck) -> Incident:
        incident = Incident(
            source_type="component_monitor",
            source_id=check.id,
            category="component_failure",
            severity="critical",
            status="open",
            title=f"{check.component} component failure",
            description=check.message,
            requires_admin_alert=True,
            requires_ivr_call=False,
        )
        self.db.add(incident)
        self.db.flush()
        return incident
