from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class ServerStatus(str, Enum):
    active = "active"
    maintenance = "maintenance"
    offline = "offline"


class LoadBalancerStatus(BaseModel):
    module: str
    status: str
    server_count: int
    placement_count: int
    capabilities: list[str]


class ServerCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=128)
    host: str = Field(..., min_length=2, max_length=255)
    port: int = Field(..., ge=1, le=65535)
    protocol: str = Field(default="http", pattern="^https?$")
    status: ServerStatus = ServerStatus.active
    weight: int = Field(default=1, ge=1, le=100)
    max_modules: int = Field(default=8, ge=1, le=200)
    capabilities: list[str] = Field(default_factory=list)
    rules: dict[str, Any] = Field(default_factory=dict)
    notes: str | None = None


class ServerBulkCreate(BaseModel):
    servers: list[ServerCreate]


class ServerRead(ServerCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class ModulePlacementCreate(BaseModel):
    module_name: str = Field(..., min_length=2, max_length=128)
    server_id: int = Field(..., ge=1)
    route_prefix: str = Field(..., min_length=1, max_length=128)
    priority: int = Field(default=1, ge=1, le=100)
    enabled: bool = True
    health_path: str = Field(default="/health", min_length=1, max_length=128)
    load_score: float = Field(default=0.0, ge=0.0, le=100.0)


class ModulePlacementRead(ModulePlacementCreate):
    id: int
    created_at: datetime
    server: ServerRead | None = None

    class Config:
        from_attributes = True


class RoutingTarget(BaseModel):
    module_name: str
    server_id: int
    server_name: str
    base_url: str
    route_prefix: str
    priority: int
    load_score: float


class RoutingPlan(BaseModel):
    module_name: str
    targets: list[RoutingTarget]


class ModuleServerPolicyRead(BaseModel):
    module_group: str
    preferred_servers: list[str]
    capabilities: list[str]
    notes: str


class CodeLocationPolicyRead(BaseModel):
    code_group: str
    github_scope: str
    path_hint: str
    owns: list[str]
    notes: str


class ServerPreset(BaseModel):
    name: str
    provider: str
    host: str
    port: int
    protocol: str
    capabilities: list[str]
    notes: str


class GitStatusResponse(BaseModel):
    branch: str
    clean: bool
    changes: list[str]


class GitCommitRequest(BaseModel):
    message: str = Field(default="auto: nesla os update", min_length=3, max_length=200)
    include_all: bool = True
    push: bool = False


class GitCommitResponse(BaseModel):
    committed: bool
    commit_hash: str | None = None
    message: str
    pushed: bool = False
    output: str


class LlmTaskRequest(BaseModel):
    task_id: str = Field(..., min_length=2, max_length=128)
    prompt: str = Field(..., min_length=1, max_length=8000)
    local_context: dict[str, Any] = Field(default_factory=dict)


class LlmTaskResponse(BaseModel):
    task_id: str
    status: str
    assistant_message: str
    next_action: str
