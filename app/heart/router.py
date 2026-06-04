from fastapi import APIRouter
from app.heart.schemas import AnalyzeRequest, AnalyzeResponse, StatusResponse
from app.heart.service import analyze_message

router = APIRouter(prefix="/heart", tags=["heart"])


@router.post("/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest) -> AnalyzeResponse:
    return analyze_message(request.message)


@router.get("/status", response_model=StatusResponse)
def status() -> StatusResponse:
    return StatusResponse(module="Heart", status="active")
