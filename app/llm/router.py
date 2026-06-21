from fastapi import APIRouter

from pydantic import BaseModel, Field

from app.llm.access_browser import AccessBrowserCapability
from app.llm.browser_control import BrowserAutomationService
from app.llm.admin_agent import (
    AdminAgentEngine,
    AgentConfirmRequest,
    AgentConfirmResponse,
    AgentTaskRequest,
    AgentTaskResponse,
)
from app.llm.deploy import DeployRequest, DeployResponse, DeployService

router = APIRouter(prefix="/llm/browser", tags=["llm_browser"])


class BrowserNavigateRequest(BaseModel):
    url: str = Field(..., min_length=8, max_length=2048)


class BrowserActionRequest(BaseModel):
    url: str = Field(..., min_length=8, max_length=2048)
    selector: str = Field(..., min_length=1, max_length=512)
    text: str | None = Field(default=None, max_length=8000)


@router.get("/manifest")
def browser_manifest() -> dict:
    return AccessBrowserCapability().manifest()


@router.post("/open/{target_key}")
def request_browser_open(target_key: str) -> dict:
    return AccessBrowserCapability().build_open_request(target_key)


@router.post("/navigate")
def browser_navigate(payload: BrowserNavigateRequest) -> dict:
    return BrowserAutomationService().navigate(payload.url)


@router.post("/click")
def browser_click(payload: BrowserActionRequest) -> dict:
    return BrowserAutomationService().click(payload.url, payload.selector)


@router.post("/type")
def browser_type(payload: BrowserActionRequest) -> dict:
    return BrowserAutomationService().type_text(payload.url, payload.selector, payload.text or "")


@router.post("/agent/tasks", response_model=AgentTaskResponse)
def run_admin_agent_task(payload: AgentTaskRequest) -> AgentTaskResponse:
    return AdminAgentEngine().plan(payload)


@router.post("/agent/confirm", response_model=AgentConfirmResponse)
def confirm_admin_agent_actions(payload: AgentConfirmRequest) -> AgentConfirmResponse:
    return AdminAgentEngine().confirm(payload)


@router.post("/deploy/run", response_model=DeployResponse)
def run_deploy(payload: DeployRequest) -> DeployResponse:
    return DeployService().run(payload)
