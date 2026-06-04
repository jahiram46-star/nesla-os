from fastapi import APIRouter, Depends
from starlette import status
from sqlalchemy.orm import Session

from app.sss.schemas import StatusResponse, ModuleStatus, SystemEventCreate, SystemEventRead
from app.sss.service import get_db, get_system_status, get_module_statuses, get_system_events, add_system_event

router = APIRouter(prefix="/sss", tags=["sss"])


@router.get("/status", response_model=StatusResponse)
def get_status() -> StatusResponse:
    return get_system_status()


@router.get("/modules", response_model=list[ModuleStatus])
def modules() -> list[ModuleStatus]:
    return get_module_statuses()


@router.get("/events", response_model=list[SystemEventRead])
def events(db: Session = Depends(get_db)) -> list[SystemEventRead]:
    return get_system_events(db)


@router.post("/event", response_model=SystemEventRead, status_code=status.HTTP_201_CREATED)
def create_event(event: SystemEventCreate, db: Session = Depends(get_db)) -> SystemEventRead:
    return add_system_event(event, db)
