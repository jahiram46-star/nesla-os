import pytest
from unittest.mock import MagicMock, AsyncMock
from brain_v2.modules.project.service import ProjectEngineService
from brain_v2.modules.project.schemas import ProjectAnalysisRequest, ProjectLifecycleRequest

@pytest.fixture
def mock_engines():
    # K, M, R, D, P, T
    return [MagicMock() for _ in range(6)] 

@pytest.mark.asyncio
async def test_project_analysis_flow(mock_engines):
    k, m, r, d, p, t = mock_engines
    service = ProjectEngineService(k, m, r, d, p, t)
    
    # Mock reasoning for analysis
    r.reason = AsyncMock()
    r.reason.return_value = MagicMock(
        understanding="This is a Python web project using FastAPI.",
        dependencies=["fastapi", "pydantic"],
        recommended_actions=["Ensure all dependencies are up-to-date."],
        metadata={"language": "Python"}
    )

    # Mock DB session
    service.db = MagicMock()
    service.db.query.return_value.filter_by.return_value.first.return_value = None # No existing project
    service.db.add = MagicMock()
    service.db.commit = MagicMock()

    request = ProjectAnalysisRequest(
        path="/mock/project",
        context_id="ctx_123"
    )
    
    result = await service.analyze_project(request)
    
    assert result.health_status == "HEALTHY"
    assert "fastapi" in result.dependencies
    service.db.add.assert_called_once()
    service.db.commit.assert_called_once()

@pytest.mark.asyncio
async def test_project_lifecycle_management(mock_engines):
    service = ProjectEngineService(*mock_engines)
    request = ProjectLifecycleRequest(
        project_id="PROJ_001",
        action="build",
        context_id="ctx_123",
        parameters={"target": "debug"}
    )
    result = await service.manage_lifecycle(request)
    assert result["status"] == "initiated"
    assert result["action"] == "build"