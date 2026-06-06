from sqlalchemy.orm import Session

from app.sss_v2.models import AdminAlert, Incident


class AlertManager:
    """Creates Admin Panel alert records for SSS V2 incidents."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def create_for_incident(self, incident: Incident) -> AdminAlert:
        alert = AdminAlert(
            incident_id=incident.id,
            severity=incident.severity,
            title=incident.title,
            message=incident.description,
            status="pending",
        )
        self.db.add(alert)
        self.db.flush()
        return alert
