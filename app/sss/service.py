from typing import Generator

from sqlalchemy.orm import Session

from app.sss.models import SystemEvent
from app.db import SessionLocal
from app.sss.schemas import ModuleStatus, StatusResponse, SystemEventCreate

MONITORED_MODULES = [
    ModuleStatus(name="Brain", status="online"),
    ModuleStatus(name="Memory", status="online"),
    ModuleStatus(name="Knowledge", status="online"),
    ModuleStatus(name="Documents", status="online"),
]


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_system_status() -> StatusResponse:
    return StatusResponse(module="SSS", status="active")


def get_module_statuses() -> list[ModuleStatus]:
    return MONITORED_MODULES


def get_system_events(db: Session) -> list[SystemEvent]:
    return db.query(SystemEvent).order_by(SystemEvent.created_at.desc()).all()


def add_system_event(event: SystemEventCreate, db: Session) -> SystemEvent:
    db_event = SystemEvent(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event
