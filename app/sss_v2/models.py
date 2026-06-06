from sqlalchemy import Boolean, Column, DateTime, Float, Integer, JSON, String, Text, func

from app.db.database import Base


class SecuritySignal(Base):
    __tablename__ = "sss_v2_security_signals"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String(length=128), nullable=False, index=True)
    signal_type = Column(String(length=128), nullable=False, index=True)
    severity = Column(String(length=32), nullable=False, index=True)
    title = Column(String(length=255), nullable=False)
    description = Column(Text, nullable=False)
    details = Column(JSON, nullable=False, default=dict)
    detected_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class ProjectHealthSnapshot(Base):
    __tablename__ = "sss_v2_project_health_snapshots"

    id = Column(Integer, primary_key=True, index=True)
    project_name = Column(String(length=128), nullable=False, index=True)
    component = Column(String(length=128), nullable=False, index=True)
    status = Column(String(length=32), nullable=False, index=True)
    health_score = Column(Float, nullable=False)
    summary = Column(Text, nullable=False)
    metrics = Column(JSON, nullable=False, default=dict)
    observed_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class ComponentHealthCheck(Base):
    __tablename__ = "sss_v2_component_health_checks"

    id = Column(Integer, primary_key=True, index=True)
    component = Column(String(length=128), nullable=False, index=True)
    status = Column(String(length=32), nullable=False, index=True)
    response_time_ms = Column(Float, nullable=True)
    message = Column(Text, nullable=False)
    details = Column(JSON, nullable=False, default=dict)
    checked_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class Incident(Base):
    __tablename__ = "sss_v2_incidents"

    id = Column(Integer, primary_key=True, index=True)
    source_type = Column(String(length=32), nullable=False)
    source_id = Column(Integer, nullable=False, index=True)
    category = Column(String(length=128), nullable=False, index=True)
    severity = Column(String(length=32), nullable=False, index=True)
    status = Column(String(length=32), nullable=False, default="open", index=True)
    title = Column(String(length=255), nullable=False)
    description = Column(Text, nullable=False)
    requires_admin_alert = Column(Boolean, nullable=False, default=False)
    requires_ivr_call = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class AdminAlert(Base):
    __tablename__ = "sss_v2_admin_alerts"

    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(Integer, nullable=False, index=True)
    severity = Column(String(length=32), nullable=False, index=True)
    title = Column(String(length=255), nullable=False)
    message = Column(Text, nullable=False)
    status = Column(String(length=32), nullable=False, default="pending", index=True)
    provider_reference = Column(String(length=255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    acknowledged_at = Column(DateTime(timezone=True), nullable=True)


class IvrCallWorkflow(Base):
    __tablename__ = "sss_v2_ivr_call_workflows"

    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(Integer, nullable=False, index=True)
    priority = Column(String(length=32), nullable=False, default="critical")
    recipient_group = Column(String(length=128), nullable=False, default="administrators")
    message = Column(Text, nullable=False)
    status = Column(String(length=32), nullable=False, default="queued", index=True)
    provider = Column(String(length=128), nullable=True)
    provider_reference = Column(String(length=255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
