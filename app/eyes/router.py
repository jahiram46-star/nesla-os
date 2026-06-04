from fastapi import APIRouter
from app.eyes.schemas import StatusResponse, AnalyzeRequest, AnalyzeResponse, CapabilitiesResponse
from app.eyes.service import analyze_image, get_capabilities

router = APIRouter(prefix="/eyes", tags=["eyes"])


@router.get("/status", response_model=StatusResponse)
def status() -> StatusResponse:
    return StatusResponse(module="Eyes", status="active")


@router.post("/analyze", response_model=AnalyzeResponse)
def analyze(req: AnalyzeRequest) -> AnalyzeResponse:
    return analyze_image(req.image_name)


@router.get("/capabilities", response_model=CapabilitiesResponse)
def capabilities() -> CapabilitiesResponse:
    return get_capabilities()
