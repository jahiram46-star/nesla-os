import pytest
from brain_v2.modules.memory.service import MemoryEngineService
from brain_v2.modules.memory.schemas import MemoryCreate, MemoryType

@pytest.mark.asyncio
async def test_memory_service_status():
    service = MemoryEngineService()
    status = await service.status()
    assert status.key == "memory"
    assert status.status == "active"

@pytest.mark.asyncio
async def test_memory_type_validation():
    # Ensure Pydantic catches invalid memory types
    with pytest.raises(ValueError):
        MemoryCreate(
            memory_type="invalid_type",
            context_id="user_123",
            content="some data"
        )