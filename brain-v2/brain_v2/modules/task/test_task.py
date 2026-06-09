import pytest
from unittest.mock import MagicMock
from brain_v2.modules.task.service import TaskEngineService
from brain_v2.modules.task.schemas import TaskRequest, TaskStatus
from brain_v2.modules.planning.schemas import PlanResult, ExecutionStep, Milestone

@pytest.fixture
def mock_engines():
    return MagicMock(), MagicMock(), MagicMock(), MagicMock(), MagicMock()

@pytest.mark.asyncio
async def test_task_creation_from_plan(mock_engines):
    k, m, r, d, p = mock_engines
    service = TaskEngineService(k, m, r, d, p)
    
    # Create a mock PlanResult
    plan = PlanResult(
        goal="Update system security",
        milestones=[Milestone(title="Check", success_criteria=["Done"])],
        execution_steps=[
            ExecutionStep(
                id="step_alpha",
                title="Check Knowledge Base",
                description="Search for security patches",
                dependencies=[],
                estimated_duration="1m"
            )
        ],
        dependencies=[],
        required_resources=[],
        estimated_timeline="1m",
        risk_mitigation_plan={},
        success_criteria=["Patches found"]
    )
    
    request = TaskRequest(
        plan_result=plan,
        context_id="test_ctx"
    )
    
    tasks = await service.create_tasks_from_plan(request)
    
    assert len(tasks) == 1
    assert tasks[0].task_id == "step_alpha"
    assert tasks[0].status == TaskStatus.PENDING
    # Check engine assignment heuristic
    assert tasks[0].assigned_engine == "knowledge_engine"
    
    status = await service.status()
    assert status.total_tasks == 1