from typing import List, Any
from brain_v2.services.base import BaseModuleService, ModuleMetadata
from brain_v2.schemas.module import ModuleStatusResponse
from brain_v2.modules.memory.schemas import MemoryCreate, MemoryRead, MemoryType, MemoryContextResponse, MemoryStatusResponse # Keep MemoryStatusResponse
from brain_v2.modules.memory.repository import MemoryRepository
from sqlalchemy.ext.asyncio import AsyncSession

class MemoryEngineService(BaseModuleService):
    metadata = ModuleMetadata(
        key="memory",
        name="Memory Engine",
        description="Handles short-term and long-term context storage and recall.",
    )
    
    def __init__(self, db_session: Optional[AsyncSession] = None):
        self.repository = MemoryRepository(db_session) if db_session else None

    async def status(self) -> MemoryStatusResponse:
        return ModuleStatusResponse(
            key=self.metadata.key,
            name=self.metadata.name,
            status="active",
            description=self.metadata.description
        )
            total_entries=await self.get_total_entries() if self.repository else 0,
            active_sessions=1, # Mock value
            storage_backend="PostgreSQL" # Mock value
        )
    async def store_memory(self, memory: MemoryCreate) -> MemoryRead:
        if not self.repository:
            raise RuntimeError("MemoryEngineService not initialized with a database session.")
        db_memory = await self.repository.create(memory)
        return MemoryRead.from_orm(db_memory)

    async def store(self, key: str, value: any):
        return True
    async def get_context(self, context_id: str, memory_type: Optional[MemoryType] = None) -> MemoryContextResponse:
        if not self.repository:
            raise RuntimeError("MemoryEngineService not initialized with a database session.")
        
        # For simplicity, fetching all memories for the context_id
        # In a real scenario, this would involve more sophisticated context retrieval
        memories = await self.repository.get_by_context_id(context_id, memory_type)
        
        context_string = "\n".join([f"[{m.memory_type.value}] {m.content}" for m in memories])
        
        return MemoryContextResponse(
            context_string=context_string,
            memories=[MemoryRead.from_orm(m) for m in memories]
        )

    async def search_memories(self, query: str, memory_type: Optional[MemoryType] = None, context_id: Optional[str] = None, limit: int = 10) -> List[MemoryRead]:
        if not self.repository:
            raise RuntimeError("MemoryEngineService not initialized with a database session.")
        
        db_memories = await self.repository.search(query, memory_type, context_id, limit)
        return [MemoryRead.from_orm(m) for m in db_memories]

    async def forget(self, memory_id: str) -> bool:
        if not self.repository:
            raise RuntimeError("MemoryEngineService not initialized with a database session.")
        return await self.repository.delete(memory_id)

    async def get_total_entries(self) -> int:
        return await self.repository.count_all() if self.repository else 0