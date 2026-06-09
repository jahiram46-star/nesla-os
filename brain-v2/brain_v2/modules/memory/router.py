from fastapi import APIRouter, Depends, HTTPException
from brain_v2.modules.memory.schemas import (
    MemoryCreate, MemoryRead, MemoryStatusResponse, 
    MemorySearchRequest, MemoryContextResponse, MemoryType
)
from brain_v2.modules.memory.service import MemoryEngineService # Keep import for type hinting
from brain_v2.dependencies import get_memory_service

router = APIRouter(prefix="/memory", tags=["memory-engine"])

@router.get("/status", response_model=MemoryStatusResponse)
async def get_status(service: MemoryEngineService = Depends(get_memory_service)):
    return await service.status()

@router.post("", response_model=MemoryRead)
async def create_memory(memory: MemoryCreate, service: MemoryEngineService = Depends(get_memory_service)):
    return await service.store_memory(memory)

@router.get("/context/{memory_type}/{context_id}", response_model=MemoryContextResponse)
async def get_context(memory_type: MemoryType, context_id: str, service: MemoryEngineService = Depends(get_memory_service)):
    return await service.get_context(context_id, memory_type)

@router.post("/search", response_model=list[MemoryRead])
async def search_memories(req: MemorySearchRequest, service: MemoryEngineService = Depends(get_memory_service)):
    return await service.search_memories(req.query, req.memory_type)

@router.delete("/{memory_id}")
async def delete_memory(memory_id: str, service: MemoryEngineService = Depends(get_memory_service)):
    return {"success": await service.forget(memory_id)}