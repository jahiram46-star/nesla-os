import pytest
from unittest.mock import MagicMock, AsyncMock
from brain_v2.modules.mrm_connector.service import MRMConnectorService
from brain_v2.modules.mrm_connector.schemas import FileRequest, TerminalRequest, GitRequest

@pytest.fixture
def mock_engines_for_mrm():
    # K, M, R, D, P, T, Proj, Exec, Learn
    engines = [MagicMock() for _ in range(9)]
    # Mock the execution engine's run_command for terminal tests
    engines[7].run_command = AsyncMock(return_value=MagicMock(
        execution_status="completed", logs=["mocked output"], errors=[]
    ))
    return engines

@pytest.mark.asyncio
async def test_mrm_file_operation(mock_engines_for_mrm):
    service = MRMConnectorService(*mock_engines_for_mrm)
    request = FileRequest(
        workspace_id="ws_1", project_id="proj_1", context_id="ctx_1",
        path="/src/main.py", op_type="write", content="print('hello')"
    )
    result = await service.handle_file_op(request)
    assert result.status == "success"
    assert result.file_operations[0]["op"] == "write"

@pytest.mark.asyncio
async def test_mrm_terminal_execution(mock_engines_for_mrm):
    service = MRMConnectorService(*mock_engines_for_mrm)
    request = TerminalRequest(
        workspace_id="ws_1", project_id="proj_1", context_id="ctx_1",
        command="ls -la", work_dir="/tmp"
    )
    result = await service.execute_terminal(request)
    assert result.status == "completed"
    assert "mocked output" in result.terminal_operations[0]["output"]

@pytest.mark.asyncio
async def test_mrm_git_operation(mock_engines_for_mrm):
    service = MRMConnectorService(*mock_engines_for_mrm)
    request = GitRequest(workspace_id="ws_1", project_id="proj_1", context_id="ctx_1", action="status")
    result = await service.handle_git(request)
    assert result.status == "success"
    assert result.git_operations[0]["action"] == "status"