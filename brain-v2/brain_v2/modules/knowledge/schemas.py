from typing import List, Optional
from pydantic import BaseModel, Field
from brain_v2.schemas.module import ModuleStatusResponse

class KnowledgeDocument(BaseModel):
    id: Optional[str] = None
    title: str
    content: str
    metadata: dict = Field(default_factory=dict)

class KnowledgeSearchRequest(BaseModel):
    query: str
    limit: int = 5

class KnowledgeSearchResponse(BaseModel):
    results: List[KnowledgeDocument]
    count: int

class KnowledgeIngestResponse(BaseModel):
    success: bool
    processed_files: int
    message: str

class KnowledgeStatusResponse(ModuleStatusResponse):
    document_count: int
    indexing_engine: str
    source_path: str
