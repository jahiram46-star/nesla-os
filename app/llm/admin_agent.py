import base64
import json
from datetime import datetime, timezone
from typing import Any, Literal

from pydantic import BaseModel, Field

from app.llm.access_browser import AccessBrowserCapability
from app.llm.deploy import DeployRequest, DeployService
from app.load_balancer.schemas import GitCommitRequest, ServerCreate, ServerBulkCreate
from app.db import SessionLocal
from app.load_balancer.service import GitAutomationService, LoadBalancerService


class AgentTaskRequest(BaseModel):
    task_id: str = Field(..., min_length=2, max_length=128)
    prompt: str = Field(..., min_length=1, max_length=8000)
    local_context: dict[str, Any] = Field(default_factory=dict)
    auto_execute_safe_actions: bool = True


class AgentAction(BaseModel):
    key: str
    title: str
    risk: Literal["safe", "confirmation_required"]
    tool: str
    payload: dict[str, Any] = Field(default_factory=dict)
    status: str = "planned"


class AgentTaskResponse(BaseModel):
    task_id: str
    status: str
    assistant_message: str
    actions: list[AgentAction]
    confirmation_token: str | None = None
    next_action: str


class AgentConfirmRequest(BaseModel):
    confirmation_token: str
    approved: bool


class AgentConfirmResponse(BaseModel):
    status: str
    assistant_message: str
    executed_actions: list[AgentAction]
    output: dict[str, Any] = Field(default_factory=dict)


class AgentServerPayload(BaseModel):
    name: str = Field(..., min_length=2, max_length=128)
    host: str = Field(..., min_length=2, max_length=255)
    port: int = Field(..., ge=1, le=65535)
    protocol: str = Field(default="http")
    weight: int = Field(default=1, ge=1, le=100)
    max_modules: int = Field(default=8, ge=1, le=200)
    capabilities: list[str] = Field(default_factory=list)
    notes: str | None = None


class AgentBulkServersPayload(BaseModel):
    servers: list[AgentServerPayload] = Field(default_factory=list)


class AdminAgentEngine:
    """Stateless admin agent for NESLA OS.

    The browser keeps conversation/context in IndexedDB. The backend receives a
    task, prepares actions, and returns a self-contained confirmation token for
    risky work. No chat history is persisted here.
    """

    def plan(self, request: AgentTaskRequest) -> AgentTaskResponse:
        prompt = request.prompt.lower()
        actions: list[AgentAction] = []

        if any(word in prompt for word in ["browser", "chrome", "console", "firebase", "github", "cloud run"]):
            target_key = self._select_console_target(prompt)
            actions.append(
                AgentAction(
                    key="open_console",
                    title=f"Open approved console: {target_key}",
                    risk="confirmation_required",
                    tool="access_browser.open_console_url",
                    payload={"target_key": target_key},
                )
            )

        if any(word in prompt for word in ["deploy", "server deploy", "live", "publish"]):
            actions.append(
                AgentAction(
                    key="prepare_deploy",
                    title="Prepare deployment pipeline",
                    risk="confirmation_required",
                    tool="deploy.prepare_pipeline",
                    payload={
                        "provider": "command",
                        "target": request.local_context.get("deploy_target", "nesla"),
                        "mode": "dry_run",
                        "steps": ["git_status", "build", "upload_or_pull", "run_service", "health_check"],
                        "command": request.local_context.get("deploy_command", []),
                        "cwd": request.local_context.get("deploy_cwd"),
                        "env": request.local_context.get("deploy_env", {}),
                    },
                )
            )

        if "commit" in prompt:
            actions.append(
                AgentAction(
                    key="git_commit",
                    title="Create local git commit",
                    risk="confirmation_required",
                    tool="git.commit",
                    payload={"message": "auto: nesla admin agent update", "push": "push" in prompt},
                )
            )

        if any(word in prompt for word in ["add server", "create server", "new server", "register server"]):
            server_payload = self._build_server_payload(request)
            actions.append(
                AgentAction(
                    key="add_server",
                    title=f"Create server: {server_payload.name}",
                    risk="confirmation_required",
                    tool="load_balancer.create_server",
                    payload=server_payload.model_dump(),
                )
            )

        if any(word in prompt for word in ["brain", "heart", "mouth", "eyes", "sss", "admin llm", "ui server"]):
            recommended = self._recommended_flow(prompt)
            actions.append(
                AgentAction(
                    key="recommend_server_flow",
                    title=f"Recommend server flow: {recommended['module_group']}",
                    risk="safe",
                    tool="load_balancer.recommendation",
                    payload=recommended,
                    status="completed" if request.auto_execute_safe_actions else "planned",
                )
            )

        if any(word in prompt for word in ["frontend", "backend", "github", "repo", "code location", "where code goes"]):
            code_location = self._recommended_code_location(prompt)
            actions.append(
                AgentAction(
                    key="recommend_code_location",
                    title=f"Recommend GitHub code location: {code_location['code_group']}",
                    risk="safe",
                    tool="github.code_location_recommendation",
                    payload=code_location,
                    status="completed" if request.auto_execute_safe_actions else "planned",
                )
            )

        if any(word in prompt for word in ["bulk add", "bulk create", "add presets", "firebase presets"]):
            bulk_payload = self._build_bulk_servers_payload(request)
            actions.append(
                AgentAction(
                    key="bulk_add_servers",
                    title=f"Create {len(bulk_payload.servers)} server presets",
                    risk="confirmation_required",
                    tool="load_balancer.create_servers_bulk",
                    payload=bulk_payload.model_dump(),
                )
            )

        if not actions:
            actions.append(
                AgentAction(
                    key="inspect_context",
                    title="Inspect local dashboard context",
                    risk="safe",
                    tool="context.inspect_indexeddb_snapshot",
                    payload={
                        "server_count": len(request.local_context.get("servers", [])),
                        "placement_count": len(request.local_context.get("placements", [])),
                    },
                    status="completed" if request.auto_execute_safe_actions else "planned",
                )
            )

        risky_actions = [action for action in actions if action.risk == "confirmation_required"]
        token = self._encode_token(risky_actions) if risky_actions else None
        server_count = len(request.local_context.get("servers", []))
        placement_count = len(request.local_context.get("placements", []))
        message = (
            f"I read your browser IndexedDB context: {server_count} servers, "
            f"{placement_count} placements. I prepared {len(actions)} action(s)."
        )
        if risky_actions:
            message += " I need admin confirmation before browser/deploy/git actions."
        else:
            message += " Safe inspection is complete."

        return AgentTaskResponse(
            task_id=request.task_id,
            status="confirmation_required" if risky_actions else "completed",
            assistant_message=message,
            actions=actions,
            confirmation_token=token,
            next_action="confirm_actions" if risky_actions else "store_result_in_indexeddb",
        )

    def confirm(self, request: AgentConfirmRequest) -> AgentConfirmResponse:
        actions = self._decode_token(request.confirmation_token)
        if not request.approved:
            return AgentConfirmResponse(
                status="cancelled",
                assistant_message="Admin cancelled the planned actions.",
                executed_actions=[action.model_copy(update={"status": "cancelled"}) for action in actions],
            )

        executed: list[AgentAction] = []
        output: dict[str, Any] = {}
        for action in actions:
            result = self._execute_action(action)
            executed.append(action.model_copy(update={"status": result.get("status", "completed")}))
            output[action.key] = result

        return AgentConfirmResponse(
            status="completed",
            assistant_message="Confirmed actions completed or prepared at their integration hooks.",
            executed_actions=executed,
            output=output,
        )

    def _execute_action(self, action: AgentAction) -> dict[str, Any]:
        if action.tool == "access_browser.open_console_url":
            return AccessBrowserCapability().build_open_request(action.payload["target_key"])

        if action.tool == "git.commit":
            payload = GitCommitRequest(
                message=action.payload.get("message", "auto: nesla admin agent update"),
                include_all=True,
                push=bool(action.payload.get("push", False)),
            )
            result = GitAutomationService().commit(payload)
            return result.model_dump()

        if action.tool == "load_balancer.create_server":
            db = SessionLocal()
            try:
                result = LoadBalancerService(db).create_server(ServerCreate.model_validate(action.payload))
                return {"status": "created", "server": result.name, "id": result.id}
            finally:
                db.close()

        if action.tool == "load_balancer.create_servers_bulk":
            db = SessionLocal()
            try:
                payload = AgentBulkServersPayload.model_validate(action.payload)
                result = LoadBalancerService(db).create_servers_bulk(
                    ServerBulkCreate(
                        servers=[
                            ServerCreate(
                                name=item.name,
                                host=item.host,
                                port=item.port,
                                protocol=item.protocol,
                                weight=item.weight,
                                max_modules=item.max_modules,
                                capabilities=item.capabilities,
                                notes=item.notes,
                            )
                            for item in payload.servers
                        ]
                    )
                )
                return {"status": "created", "count": len(result), "servers": [server.name for server in result]}
            finally:
                db.close()

        if action.tool == "deploy.prepare_pipeline":
            request = DeployRequest(
                provider=str(action.payload.get("provider", "command")),
                target=str(action.payload.get("target", action.key)),
                dry_run=bool(action.payload.get("mode", "dry_run") == "dry_run"),
                command=list(action.payload.get("command", [])),
                env=dict(action.payload.get("env", {})),
                cwd=action.payload.get("cwd"),
                confirm=True,
            )
            return DeployService().run(request).model_dump()

        return {"status": "skipped", "reason": "Unknown tool."}

    @staticmethod
    def _recommended_flow(prompt: str) -> dict[str, Any]:
        normalized = prompt.lower()
        if any(name in normalized for name in ["brain", "heart"]):
            return {
                "module_group": "brain_heart",
                "preferred_servers": ["firebase", "huggingface"],
                "notes": "Brain and Heart should use Firebase + HuggingFace.",
            }
        if any(name in normalized for name in ["mouth", "eyes"]):
            return {
                "module_group": "mouth_eyes",
                "preferred_servers": ["firebase", "huggingface", "vercel_ui"],
                "notes": "Mouth and Eyes should use Firebase + HuggingFace + Vercel UI server.",
            }
        if "sss" in normalized:
            return {
                "module_group": "sss",
                "preferred_servers": ["dedicated_backend"],
                "notes": "SSS should use a dedicated backend server.",
            }
        if "admin llm" in normalized or "llm admin" in normalized:
            return {
                "module_group": "llm_admin",
                "preferred_servers": ["dedicated_backend"],
                "notes": "LLM admin should use a separate dedicated server.",
            }
        if "ui" in normalized or "web" in normalized:
            return {
                "module_group": "ui",
                "preferred_servers": ["vercel_ui", "frontend_static"],
                "notes": "UI services should stay on UI servers.",
            }
        return {
            "module_group": "unknown",
            "preferred_servers": [],
            "notes": "No explicit module group detected.",
        }

    @staticmethod
    def _recommended_code_location(prompt: str) -> dict[str, Any]:
        normalized = prompt.lower()
        if "frontend" in normalized or "ui" in normalized:
            return {
                "code_group": "frontend",
                "github_scope": "frontend repo",
                "path_hint": "nesla_admin_ui/**",
                "owns": ["Flutter admin UI", "web UI", "dashboard screens", "widgets", "theme"],
                "notes": "Frontend code should live in nesla_admin_ui or the frontend repo.",
            }
        if "backend" in normalized or "server" in normalized:
            return {
                "code_group": "backend",
                "github_scope": "backend repo",
                "path_hint": "app/**, tests/**, requirements.txt",
                "owns": ["FastAPI APIs", "LLM orchestration", "load balancer", "SSS", "Brain", "Heart", "Mouth", "Eyes"],
                "notes": "Backend code should live in app/ and backend repo paths.",
            }
        return {
            "code_group": "shared_contracts",
            "github_scope": "shared contract boundary",
            "path_hint": "OpenAPI / schema contracts",
            "owns": ["request/response models", "API route contracts", "shared enums"],
            "notes": "Shared contracts keep frontend and backend aligned.",
        }

    @staticmethod
    def _select_console_target(prompt: str) -> str:
        if "github" in prompt:
            return "github_actions"
        if "cloud run" in prompt or "google cloud" in prompt:
            return "google_cloud_run"
        if "render" in prompt:
            return "render_dashboard"
        return "firebase_console"

    @staticmethod
    def _encode_token(actions: list[AgentAction]) -> str:
        payload = {
            "created_at": datetime.now(timezone.utc).isoformat(),
            "actions": [action.model_dump() for action in actions],
        }
        raw = json.dumps(payload, separators=(",", ":")).encode("utf-8")
        return base64.urlsafe_b64encode(raw).decode("ascii")

    @staticmethod
    def _decode_token(token: str) -> list[AgentAction]:
        raw = base64.urlsafe_b64decode(token.encode("ascii"))
        payload = json.loads(raw.decode("utf-8"))
        return [AgentAction.model_validate(action) for action in payload.get("actions", [])]

    @staticmethod
    def _build_server_payload(request: AgentTaskRequest) -> AgentServerPayload:
        context = request.local_context
        return AgentServerPayload(
            name=str(context.get("server_name") or "llm-server-1"),
            host=str(context.get("server_host") or "127.0.0.1"),
            port=int(context.get("server_port") or 8001),
            protocol=str(context.get("server_protocol") or "http"),
            weight=int(context.get("server_weight") or 1),
            max_modules=int(context.get("server_max_modules") or 8),
            capabilities=list(context.get("server_capabilities") or ["llm", "browser"]),
            notes=str(context.get("server_notes") or "Created by NESLA LLM agent."),
        )

    @staticmethod
    def _build_bulk_servers_payload(request: AgentTaskRequest) -> AgentBulkServersPayload:
        context = request.local_context
        presets = context.get("server_presets")
        if isinstance(presets, list) and presets:
            servers = [
                AgentServerPayload.model_validate(item if isinstance(item, dict) else {})
                for item in presets
            ]
            return AgentBulkServersPayload(servers=servers)

        project = str(context.get("firebase_project_id") or "your-project-id")
        regions = [
            "us-central1",
            "us-east1",
            "us-west1",
            "europe-west1",
            "europe-west2",
            "asia-south1",
            "asia-east1",
            "asia-northeast1",
            "australia-southeast1",
            "southamerica-east1",
        ]
        servers = [
            AgentServerPayload(
                name=f"firebase-{region}",
                host=f"{region}-{project}.cloudfunctions.net",
                port=443,
                protocol="https",
                capabilities=["llm_pipeline", "tasks", "serverless", region],
                notes="Firebase Functions/Hosting preset generated by NESLA LLM agent.",
            )
            for region in regions
        ]
        return AgentBulkServersPayload(servers=servers)
