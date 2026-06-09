import pytest
from unittest.mock import MagicMock, AsyncMock
from brain_v2.modules.learning.service import LearningEngineService
from brain_v2.modules.learning.schemas import LearningRequest, FeedbackRequest

@pytest.fixture
def mock_engines_for_learning():
    # K, M, R, D, P, T, Proj, Exec
    return [MagicMock() for _ in range(8)]

@pytest.mark.asyncio
async def test_learning_from_execution(mock_engines_for_learning):
    service = LearningEngineService(*mock_engines_for_learning)
    request = LearningRequest(
        source_id="exec_123", source_type="execution", context_id="ctx_learn"
    )
    result = await service.learn_from_execution(request)
    assert result.learning_id is not None
    assert result.source_type == "execution"
    assert result.confidence_score > 0
    assert len(result.lessons_learned) > 0

@pytest.mark.asyncio
async def test_learning_process_feedback(mock_engines_for_learning):
    service = LearningEngineService(*mock_engines_for_learning)
    request = FeedbackRequest(
        source_id="decision_456", rating=5, comment="Excellent decision!"
    )
    result = await service.process_user_feedback(request)
    assert result["status"] == "feedback_integrated"