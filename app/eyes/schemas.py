from pydantic import BaseModel


class StatusResponse(BaseModel):
    module: str
    status: str


class AnalyzeRequest(BaseModel):
    image_name: str


class AnalyzeResponse(BaseModel):
    status: str
    message: str


class CapabilitiesResponse(BaseModel):
    ocr: bool
    image_understanding: bool
    document_reading: bool
    face_detection: bool
