from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class Severity(str, Enum):
    info = "info"
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class HealthStatus(str, Enum):
    healthy = "healthy"
    degraded = "degraded"
    unhealthy = "unhealthy"
    critical = "critical"


class ComponentStatus(str, Enum):
    online = "online"
    degraded = "degraded"
    failed = "failed"


class SssV2Status(BaseModel):
    module: str
    status: str
    responsibilities: list[str]
    telephony_provider_configured: bool


class SecuritySignalCreate(BaseModel):
    source: str
    signal_type: str
    severity: Severity
    title: str
    description: str
    details: Dict[str, Any] = Field(default_factory=dict)


class SecuritySignalRead(SecuritySignalCreate):
    id: int
    detected_at: datetime

    class Config:
        from_attributes = True


class ProjectHealthSnapshotCreate(BaseModel):
    project_name: str
    component: str
    status: HealthStatus
    health_score: float = Field(..., ge=0, le=100)
    summary: str
    metrics: Dict[str, Any] = Field(default_factory=dict)


class ProjectHealthSnapshotRead(ProjectHealthSnapshotCreate):
    id: int
    observed_at: datetime

    class Config:
        from_attributes = True


class ComponentHealthCheckCreate(BaseModel):
    component: str
    status: ComponentStatus
    response_time_ms: Optional[float] = Field(None, ge=0)
    message: str
    details: Dict[str, Any] = Field(default_factory=dict)


class ComponentHealthCheckRead(ComponentHealthCheckCreate):
    id: int
    checked_at: datetime

    class Config:
        from_attributes = True


class ThreatAssessment(BaseModel):
    category: str
    severity: Severity
    title: str
    description: str
    create_incident: bool = True


class IncidentRead(BaseModel):
    id: int
    source_type: str
    source_id: int
    category: str
    severity: Severity
    status: str
    title: str
    description: str
    requires_admin_alert: bool
    requires_ivr_call: bool
    created_at: datetime

    class Config:
        from_attributes = True


class AdminAlertRead(BaseModel):
    id: int
    incident_id: int
    severity: Severity
    title: str
    message: str
    status: str
    provider_reference: Optional[str]
    created_at: datetime
    acknowledged_at: Optional[datetime]

    class Config:
        from_attributes = True


class IvrCallWorkflowRead(BaseModel):
    id: int
    incident_id: int
    priority: str
    recipient_group: str
    message: str
    status: str
    provider: Optional[str]
    provider_reference: Optional[str]
    created_at: datetime
    started_at: Optional[datetime]
    completed_at: Optional[datetime]

    class Config:
        from_attributes = True


class SecurityMonitoringResult(BaseModel):
    signal: SecuritySignalRead
    incident: Optional[IncidentRead]
    admin_alert: Optional[AdminAlertRead]
    ivr_workflow: Optional[IvrCallWorkflowRead]


class ProjectHealthMonitoringResult(BaseModel):
    snapshot: ProjectHealthSnapshotRead
    incident: Optional[IncidentRead]
    admin_alert: Optional[AdminAlertRead]
    ivr_workflow: Optional[IvrCallWorkflowRead]


class ComponentMonitoringResult(BaseModel):
    check: ComponentHealthCheckRead
    failure_detected: bool
    incident: Optional[IncidentRead]
    admin_alert: Optional[AdminAlertRead]


class AdminAlertDispatch(BaseModel):
    incident_id: int
    severity: Severity
    title: str
    message: str


class IvrCallDispatch(BaseModel):
    incident_id: int
    priority: str
    recipient_group: str
    message: str
