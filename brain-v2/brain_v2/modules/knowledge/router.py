from fastapi import APIRouter, HTTPException
from brain_v2.modules.knowledge.schemas import (
    KnowledgeStatusResponse, KnowledgeSearchResponse, 
    KnowledgeIngestResponse, KnowledgeSearchRequest
)
from brain_v2.modules.knowledge.service import KnowledgeEngineService # Keep import for type hinting
from brain_v2.dependencies import get_knowledge_service

router = APIRouter(prefix="/knowledge", tags=["knowledge-engine"])

@router.get("/status", response_model=KnowledgeStatusResponse)
async def get_status(service: KnowledgeEngineService = Depends(get_knowledge_service)):
    return await service.status()

@router.post("/ingest", response_model=KnowledgeIngestResponse)
async def ingest_files(service: KnowledgeEngineService = Depends(get_knowledge_service)):
    return await service.ingest_local_files()

@router.post("/search", response_model=KnowledgeSearchResponse)
async def search_knowledge(request: KnowledgeSearchRequest, service: KnowledgeEngineService = Depends(get_knowledge_service)):
    if not request.query:
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    return await service.search(request.query, request.limit)