import pytest
from unittest.mock import MagicMock, AsyncMock
from brain_v2.modules.execution.service import ExecutionEngineService
from brain_v2.modules.execution.schemas import TaskExecutionRequest, CommandExecutionRequest

@pytest.fixture
def mock_engines():
    # Knowledge, Memory, Reasoning, Decision, Planning, Task, Project
    return [MagicMock() for _ in range(7)]

@pytest.mark.asyncio
async def test_task_execution_flow(mock_engines):
    k, m, r, d, p, t, proj = mock_engines
    service = ExecutionEngineService(k, m, r, d, p, t, proj)
    
    # Mock reasoning for validation (if execute_task used it)
    # r.reason = AsyncMock()
    # r.reason.return_value.understanding = "Validation Passed"

    request = TaskExecutionRequest(
        task_id="TASK_001",
        context_id="CTX_TEST",
        parameters={"action": "clean"}
    )
    
    result = await service.execute_task(request)
    
    assert result.execution_status == "completed"
    assert "Task_001 completed successfully" in result.output["message"]
    # assert result.validation_result["valid"] is True # Not implemented in current mock

@pytest.mark.asyncio
async def test_command_execution(mock_engines):
    service = ExecutionEngineService(*mock_engines)
    
    # Test a simple 'echo' command
    request = CommandExecutionRequest(command="echo", args=["hello"], context_id="ctx_1")
    result = await service.run_command(request)
    
    assert result.execution_status == "completed"
    assert "hello" in result.logs[0]