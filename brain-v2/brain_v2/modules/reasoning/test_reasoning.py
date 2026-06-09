import pytest
from unittest.mock import AsyncMock, MagicMock
from brain_v2.modules.reasoning.service import ReasoningEngineService
from brain_v2.modules.reasoning.schemas import ReasoningRequest

@pytest.mark.asyncio
async def test_reasoning_logic_flow():
    # Mock Dependencies
    mock_k = MagicMock()
    mock_k.search = AsyncMock()
    mock_k.search.return_value.results = []
    
    mock_m = MagicMock()
    mock_m.get_context = AsyncMock()
    mock_m.get_context.return_value.context_string = "Test context"

    service = ReasoningEngineService(mock_k, mock_m)
    
    request = ReasoningRequest(
        query="How do I setup Nesla OS?",
        context_id="session_123",
        depth=1
    )
    
    result = await service.reason(request)
    
    assert result.understanding is not None
    assert len(result.steps) > 0
    assert "Test context" in result.context_summary