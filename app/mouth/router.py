from fastapi import APIRouter
from app.mouth.schemas import RespondRequest, RespondResponse, StatusResponse
from app.mouth.service import respond

router = APIRouter(prefix="/mouth", tags=["mouth"])


@router.post("/respond", response_model=RespondResponse)
def respond_endpoint(req: RespondRequest) -> RespondResponse:
    return respond(req.message, req.language)


@router.get("/status", response_model=StatusResponse)
def status() -> StatusResponse:
    return StatusResponse(module="Mouth", status="active")
