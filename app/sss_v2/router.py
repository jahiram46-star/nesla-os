from typing import Generator

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.sss_v2.models import AdminAlert, ComponentHealthCheck, Incident, IvrCallWorkflow
from app.sss_v2.schemas import (
    AdminAlertRead,
    ComponentHealthCheckCreate,
    ComponentHealthCheckRead,
    ComponentMonitoringResult,
    IncidentRead,
    IvrCallWorkflowRead,
    ProjectHealthMonitoringResult,
    ProjectHealthSnapshotCreate,
    SecurityMonitoringResult,
    SecuritySignalCreate,
    SssV2Status,
)
from app.sss_v2.services import ComponentMonitorService, FoundationThreatDetector, SssV2MonitoringService

router = APIRouter(prefix="/sss/v2", tags=["sss_v2"])


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_monitoring_service(db: Session = Depends(get_db)) -> SssV2MonitoringService:
    return SssV2MonitoringService(db=db, threat_detector=FoundationThreatDetector())


def get_component_monitor(db: Session = Depends(get_db)) -> ComponentMonitorService:
    return ComponentMonitorService(db=db)


@router.get("/status", response_model=SssV2Status)
def status() -> SssV2Status:
    return SssV2Status(
        module="SSS V2",
        status="active",
        responsibilities=[
            "security_monitoring",
            "threat_detection",
            "project_health_monitoring",
            "admin_alert_generation",
            "incident_logging",
            "ivr_calling_workflow",
        ],
        telephony_provider_configured=False,
    )


@router.post("/security/signals", response_model=SecurityMonitoringResult, status_code=201)
def ingest_security_signal(
    payload: SecuritySignalCreate,
    service: SssV2MonitoringService = Depends(get_monitoring_service),
) -> SecurityMonitoringResult:
    return service.ingest_security_signal(payload)


@router.post("/health/snapshots", response_model=ProjectHealthMonitoringResult, status_code=201)
def ingest_project_health(
    payload: ProjectHealthSnapshotCreate,
    service: SssV2MonitoringService = Depends(get_monitoring_service),
) -> ProjectHealthMonitoringResult:
    return service.ingest_project_health(payload)


@router.post("/components/checks", response_model=ComponentMonitoringResult, status_code=201)
def record_component_check(
    payload: ComponentHealthCheckCreate,
    service: ComponentMonitorService = Depends(get_component_monitor),
) -> ComponentMonitoringResult:
    return service.record_check(payload)


@router.get("/components/status", response_model=list[ComponentHealthCheckRead])
def list_component_statuses(
    service: ComponentMonitorService = Depends(get_component_monitor),
) -> list[ComponentHealthCheck]:
    return service.latest_checks()


@router.get("/incidents", response_model=list[IncidentRead])
def list_incidents(db: Session = Depends(get_db)) -> list[Incident]:
    return db.query(Incident).order_by(Incident.created_at.desc()).all()


@router.get("/alerts", response_model=list[AdminAlertRead])
def list_admin_alerts(db: Session = Depends(get_db)) -> list[AdminAlert]:
    return db.query(AdminAlert).order_by(AdminAlert.created_at.desc()).all()


@router.get("/ivr-workflows", response_model=list[IvrCallWorkflowRead])
def list_ivr_workflows(db: Session = Depends(get_db)) -> list[IvrCallWorkflow]:
    return db.query(IvrCallWorkflow).order_by(IvrCallWorkflow.created_at.desc()).all()
