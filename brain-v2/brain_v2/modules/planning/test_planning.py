import pytest
from unittest.mock import MagicMock
from brain_v2.modules.planning.service import PlanningEngineService
from brain_v2.modules.planning.schemas import PlanRequest
from brain_v2.modules.decision.schemas import DecisionResult

@pytest.fixture
def mock_services():
    return MagicMock(), MagicMock(), MagicMock(), MagicMock()

@pytest.mark.asyncio
async def test_plan_generation_flow(mock_services):
    k, m, r, d = mock_services
    service = PlanningEngineService(k, m, r, d)
    
    # Mock decision result
    decision = DecisionResult(
        selected_action="DEPLOY_UPDATE",
        decision_reason="Requirement met.",
        confidence_score=0.9,
        priority_score=0.8,
        risks=["Downtime"],
        dependencies=["Docker"],
        required_resources=["Root"],
        recommended_next_steps=[]
    )
    
    request = PlanRequest(
        decision_result=decision,
        context_id="ctx_999"
    )
    
    plan = await service.generate_plan(request)
    
    assert plan.goal == "Execute DEPLOY_UPDATE effectively."
    assert len(plan.execution_steps) == 3
    assert plan.execution_steps[0].id == "step_1"
    assert "Downtime" in plan.risk_mitigation_plan
    
    status = await service.status()
    assert status.plans_generated == 1