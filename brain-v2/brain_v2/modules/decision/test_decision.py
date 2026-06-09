import pytest
from unittest.mock import MagicMock
from brain_v2.modules.decision.service import DecisionEngineService
from brain_v2.modules.decision.schemas import DecisionRequest
from brain_v2.modules.reasoning.schemas import ReasoningResult, ReasoningRequirement

@pytest.fixture
def mock_engines():
    return MagicMock(), MagicMock(), MagicMock()

@pytest.mark.asyncio
async def test_decision_logic_with_risks(mock_engines):
    k, m, r = mock_engines
    service = DecisionEngineService(k, m, r)
    
    # Create a reasoning result with multiple risks
    reasoning = ReasoningResult(
        context_summary="User wants to restart server.",
        understanding="Restart operation requested.",
        requirements=[ReasoningRequirement(item="Root access", priority="mandatory", source="sys")],
        dependencies=["Service Manager"],
        risks=["Active connections may be dropped", "Data loss risk"],
        steps=[],
        recommended_actions=["RESTART_NOW", "SCHEDULE_RESTART"]
    )
    
    request = DecisionRequest(
        reasoning_result=reasoning,
        user_goals=["Uptime maintenance"],
        context_id="ctx_123"
    )
    
    result = await service.decide(request)
    
    # Check if confidence dropped due to risks (2 risks * 0.15 = 0.3 deduction)
    assert result.confidence_score <= 0.7
    assert result.selected_action == "RESTART_NOW"
    assert "Root access" in result.required_resources

@pytest.mark.asyncio
async def test_decision_status(mock_engines):
    k, m, r = mock_engines
    service = DecisionEngineService(k, m, r)
    
    status = await service.status()
    assert status.key == "decision"
    assert status.status == "active"
    assert status.active_strategy == "WeightedGoalAlignment"