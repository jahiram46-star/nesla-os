from app.eyes.schemas import AnalyzeResponse, CapabilitiesResponse


def analyze_image(image_name: str) -> AnalyzeResponse:
    # Placeholder: just acknowledge receipt
    return AnalyzeResponse(status="received", message="Eyes V1 ready for image analysis")


def get_capabilities() -> CapabilitiesResponse:
    # Foundation V1: no capabilities yet
    return CapabilitiesResponse(ocr=False, image_understanding=False, document_reading=False, face_detection=False)
