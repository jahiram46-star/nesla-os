from typing import Generator

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.load_balancer.models import LoadBalancerServer, ModulePlacement
from app.load_balancer.schemas import (
    GitCommitRequest,
    GitCommitResponse,
    GitStatusResponse,
    LlmTaskRequest,
    LlmTaskResponse,
    LoadBalancerStatus,
    ModulePlacementCreate,
    ModulePlacementRead,
    CodeLocationPolicyRead,
    ModuleServerPolicyRead,
    RoutingPlan,
    ServerBulkCreate,
    ServerCreate,
    ServerPreset,
    ServerRead,
)
from app.load_balancer.service import GitAutomationService, LoadBalancerService, StatelessLlmPipelineService

router = APIRouter(prefix="/load-balancer", tags=["load_balancer"])


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_service(db: Session = Depends(get_db)) -> LoadBalancerService:
    return LoadBalancerService(db)


@router.get("/status", response_model=LoadBalancerStatus)
def status(service: LoadBalancerService = Depends(get_service)) -> LoadBalancerStatus:
    return service.status()


@router.get("/servers", response_model=list[ServerRead])
def list_servers(service: LoadBalancerService = Depends(get_service)) -> list[LoadBalancerServer]:
    return service.list_servers()


@router.post("/servers", response_model=ServerRead, status_code=201)
def create_server(
    payload: ServerCreate,
    service: LoadBalancerService = Depends(get_service),
) -> LoadBalancerServer:
    return service.create_server(payload)


@router.post("/servers/bulk", response_model=list[ServerRead], status_code=201)
def create_servers_bulk(
    payload: ServerBulkCreate,
    service: LoadBalancerService = Depends(get_service),
) -> list[LoadBalancerServer]:
    return service.create_servers_bulk(payload)


@router.get("/presets/firebase", response_model=list[ServerPreset])
def firebase_presets(
    project_id: str = Query(default="your-project-id", min_length=2),
    service: LoadBalancerService = Depends(get_service),
) -> list[ServerPreset]:
    return service.firebase_presets(project_id)


@router.get("/presets/huggingface", response_model=list[ServerPreset])
def huggingface_presets(
    space_id: str = Query(default="your-username/your-space", min_length=2),
    service: LoadBalancerService = Depends(get_service),
) -> list[ServerPreset]:
    return service.huggingface_presets(space_id)


@router.get("/placements", response_model=list[ModulePlacementRead])
def list_placements(service: LoadBalancerService = Depends(get_service)) -> list[ModulePlacementRead]:
    return service.list_placements()


@router.post("/placements", response_model=ModulePlacementRead, status_code=201)
def create_placement(
    payload: ModulePlacementCreate,
    service: LoadBalancerService = Depends(get_service),
) -> ModulePlacement:
    return service.create_placement(payload)


@router.get("/routing-plan", response_model=RoutingPlan)
def routing_plan(
    module_name: str = Query(..., min_length=2),
    service: LoadBalancerService = Depends(get_service),
) -> RoutingPlan:
    return service.routing_plan(module_name)


@router.get("/policies", response_model=list[ModuleServerPolicyRead])
def policies(service: LoadBalancerService = Depends(get_service)) -> list[ModuleServerPolicyRead]:
    return [
        ModuleServerPolicyRead.model_validate(policy.model_dump())
        for policy in service.rule_engine.policy_cards()
    ]


@router.get("/code-locations", response_model=list[CodeLocationPolicyRead])
def code_locations(service: LoadBalancerService = Depends(get_service)) -> list[CodeLocationPolicyRead]:
    return [
        CodeLocationPolicyRead.model_validate(policy.model_dump())
        for policy in service.rule_engine.code_location_cards()
    ]


@router.get("/git/status", response_model=GitStatusResponse)
def git_status() -> GitStatusResponse:
    return GitAutomationService().status()


@router.post("/git/commit", response_model=GitCommitResponse)
def git_commit(payload: GitCommitRequest) -> GitCommitResponse:
    return GitAutomationService().commit(payload)


@router.post("/llm/tasks", response_model=LlmTaskResponse)
def run_llm_task(payload: LlmTaskRequest) -> LlmTaskResponse:
    return StatelessLlmPipelineService().run_task(payload)
