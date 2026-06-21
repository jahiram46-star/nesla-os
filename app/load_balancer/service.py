from dataclasses import dataclass
import subprocess

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.llm_client import OpenRouterFallbackClient
from app.load_balancer.models import LoadBalancerServer, ModulePlacement
from app.load_balancer.schemas import (
    LoadBalancerStatus,
    GitCommitRequest,
    GitCommitResponse,
    GitStatusResponse,
    LlmTaskRequest,
    LlmTaskResponse,
    ModulePlacementCreate,
    ModulePlacementRead,
    RoutingPlan,
    RoutingTarget,
    ServerBulkCreate,
    ServerCreate,
    ServerPreset,
    ServerRead,
)


@dataclass(frozen=True)
class LoadBalancerCapability:
    key: str
    description: str


@dataclass(frozen=True)
class ModuleServerPolicy:
    module_group: str
    preferred_servers: list[str]
    capabilities: list[str]
    notes: str


@dataclass(frozen=True)
class CodeLocationPolicy:
    code_group: str
    github_scope: str
    path_hint: str
    owns: list[str]
    notes: str


class LoadBalancingRuleEngine:
    """Small rule/tool layer that can later be replaced by a smarter scheduler."""

    capabilities = [
        LoadBalancerCapability("server_registry", "Add and list expandable backend servers."),
        LoadBalancerCapability("module_placement", "Assign NESLA modules to selected servers."),
        LoadBalancerCapability("weighted_routing", "Prefer higher weight servers when priorities match."),
        LoadBalancerCapability("health_aware_routing", "Ignore offline or maintenance servers."),
        LoadBalancerCapability("llm_ready_policy", "Reserved hook for future LLM-assisted routing policy."),
    ]

    module_policies = [
        ModuleServerPolicy(
            module_group="brain_heart",
            preferred_servers=["firebase", "huggingface"],
            capabilities=["inference", "orchestration", "model_calls"],
            notes="Brain and Heart should stay model-facing and backend-friendly.",
        ),
        ModuleServerPolicy(
            module_group="mouth_eyes",
            preferred_servers=["firebase", "huggingface", "vercel_ui"],
            capabilities=["multimodal", "ui_bridge", "content_generation"],
            notes="Mouth and Eyes can use UI-connected and model-backed services.",
        ),
        ModuleServerPolicy(
            module_group="sss",
            preferred_servers=["dedicated_backend"],
            capabilities=["security", "monitoring", "incident_response"],
            notes="SSS should live on its own backend server for isolation.",
        ),
        ModuleServerPolicy(
            module_group="llm_admin",
            preferred_servers=["dedicated_backend"],
            capabilities=["agent_orchestration", "browser_automation", "deploy"],
            notes="LLM admin should stay on a dedicated backend server.",
        ),
        ModuleServerPolicy(
            module_group="ui",
            preferred_servers=["vercel_ui", "frontend_static"],
            capabilities=["dashboard", "admin_panel", "web_ui"],
            notes="UI services should stay separate from backend services.",
        ),
    ]

    code_location_policies = [
        CodeLocationPolicy(
            code_group="frontend",
            github_scope="frontend repo",
            path_hint="nesla_admin_ui/**",
            owns=["Flutter admin UI", "web UI", "dashboard screens", "widgets", "theme"],
            notes="UI/client code should live in the frontend repo and frontend folders.",
        ),
        CodeLocationPolicy(
            code_group="backend",
            github_scope="backend repo",
            path_hint="app/**, tests/**, requirements.txt",
            owns=["FastAPI APIs", "LLM orchestration", "load balancer", "SSS", "Brain", "Heart", "Mouth", "Eyes"],
            notes="Service/API/agent code should live in the backend repo and app folder.",
        ),
        CodeLocationPolicy(
            code_group="shared_contracts",
            github_scope="shared contract boundary",
            path_hint="OpenAPI / schema contracts",
            owns=["request/response models", "API route contracts", "shared enums"],
            notes="Keep API contracts consistent between frontend and backend.",
        ),
    ]

    def ordered_targets(
        self,
        module_name: str,
        servers: list[LoadBalancerServer],
        placements: list[ModulePlacement],
    ) -> RoutingPlan:
        servers_by_id = {server.id: server for server in servers if server.status == "active"}
        targets: list[RoutingTarget] = []

        for placement in placements:
            server = servers_by_id.get(placement.server_id)
            if server is None or not placement.enabled:
                continue

            targets.append(
                RoutingTarget(
                    module_name=module_name,
                    server_id=server.id,
                    server_name=server.name,
                    base_url=f"{server.protocol}://{server.host}:{server.port}",
                    route_prefix=placement.route_prefix,
                    priority=placement.priority,
                    load_score=placement.load_score,
                )
            )

        targets.sort(key=lambda item: (item.priority, item.load_score, -servers_by_id[item.server_id].weight))
        preferred = self._preferred_server_names(module_name)
        if preferred:
            targets.sort(
                key=lambda item: (
                    0 if item.server_name in preferred else 1,
                    item.priority,
                    item.load_score,
                    -servers_by_id[item.server_id].weight,
                )
            )
        return RoutingPlan(module_name=module_name, targets=targets)

    def ai_routing_hint(self, module_name: str, servers: list[LoadBalancerServer], placements: list[ModulePlacement]) -> str | None:
        prompt = (
            "Suggest a safe NESLA routing preference for this module.\n"
            f"Module: {module_name}\n"
            f"Servers: {[server.name for server in servers]}\n"
            f"Placements: {[f'{p.module_name}->{p.route_prefix}@{p.server_id}' for p in placements]}\n"
            "Return a short preference list and a one-line reason."
        )
        try:
            result = OpenRouterFallbackClient().generate(
                prompt=prompt,
                system_prompt="You are a routing assistant for NESLA OS. Keep answers short and operational.",
                context={"module_name": module_name},
            )
            return result.content
        except Exception:
            return None

    def policy_for(self, module_name: str) -> ModuleServerPolicy | None:
        group = self._module_group(module_name)
        return next((policy for policy in self.module_policies if policy.module_group == group), None)

    def recommended_server_names(self, module_name: str) -> list[str]:
        policy = self.policy_for(module_name)
        return policy.preferred_servers if policy else []

    def recommended_code_location(self, code_group: str) -> CodeLocationPolicy | None:
        normalized = code_group.lower().strip()
        return next((policy for policy in self.code_location_policies if policy.code_group == normalized), None)

    def policy_cards(self) -> list[ModuleServerPolicy]:
        return list(self.module_policies)

    def code_location_cards(self) -> list[CodeLocationPolicy]:
        return list(self.code_location_policies)

    @staticmethod
    def _module_group(module_name: str) -> str:
        normalized = module_name.lower().strip()
        if normalized in {"brain", "heart"}:
            return "brain_heart"
        if normalized in {"mouth", "eyes"}:
            return "mouth_eyes"
        if normalized == "sss":
            return "sss"
        if "llm" in normalized or "admin" in normalized:
            return "llm_admin"
        if "ui" in normalized or "web" in normalized:
            return "ui"
        return "unknown"

    def _preferred_server_names(self, module_name: str) -> list[str]:
        policy = self.policy_for(module_name)
        return policy.preferred_servers if policy else []


class LoadBalancerService:
    def __init__(self, db: Session, rule_engine: LoadBalancingRuleEngine | None = None) -> None:
        self.db = db
        self.rule_engine = rule_engine or LoadBalancingRuleEngine()

    def status(self) -> LoadBalancerStatus:
        return LoadBalancerStatus(
            module="Load Balancer",
            status="active",
            server_count=self.db.query(LoadBalancerServer).count(),
            placement_count=self.db.query(ModulePlacement).count(),
            capabilities=[capability.key for capability in self.rule_engine.capabilities],
        )

    def list_servers(self) -> list[LoadBalancerServer]:
        return self.db.query(LoadBalancerServer).order_by(LoadBalancerServer.created_at.desc()).all()

    def create_server(self, payload: ServerCreate) -> LoadBalancerServer:
        existing = self.db.query(LoadBalancerServer).filter(LoadBalancerServer.name == payload.name).first()
        if existing is not None:
            raise HTTPException(status_code=409, detail="Server name already exists.")

        server = LoadBalancerServer(**payload.model_dump())
        self.db.add(server)
        self.db.commit()
        self.db.refresh(server)
        return server

    def create_servers_bulk(self, payload: ServerBulkCreate) -> list[LoadBalancerServer]:
        created: list[LoadBalancerServer] = []
        for server_payload in payload.servers:
            existing = self.db.query(LoadBalancerServer).filter(LoadBalancerServer.name == server_payload.name).first()
            if existing is not None:
                continue
            server = LoadBalancerServer(**server_payload.model_dump())
            self.db.add(server)
            created.append(server)
        self.db.commit()
        for server in created:
            self.db.refresh(server)
        return created

    def firebase_presets(self, project_id: str = "your-project-id") -> list[ServerPreset]:
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
        return [
            ServerPreset(
                name=f"firebase-{region}",
                provider="firebase",
                host=f"{region}-{project_id}.cloudfunctions.net",
                port=443,
                protocol="https",
                capabilities=["llm_pipeline", "tasks", "serverless", region],
                notes="Firebase Functions/Hosting preset. Replace project_id before production use.",
            )
            for region in regions
        ]

    def huggingface_presets(self, space_id: str = "your-username/your-space") -> list[ServerPreset]:
        return [
            ServerPreset(
                name="huggingface-inference",
                provider="huggingface",
                host=f"{space_id}.hf.space",
                port=443,
                protocol="https",
                capabilities=["llm_pipeline", "inference", "model_calls"],
                notes="Hugging Face Space preset. Replace space_id with your real Space or endpoint.",
            ),
            ServerPreset(
                name="huggingface-api",
                provider="huggingface",
                host="api-inference.huggingface.co",
                port=443,
                protocol="https",
                capabilities=["llm_pipeline", "inference", "model_calls", "api"],
                notes="Hugging Face inference API preset.",
            ),
        ]

    def list_placements(self) -> list[ModulePlacementRead]:
        placements = self.db.query(ModulePlacement).order_by(ModulePlacement.created_at.desc()).all()
        servers_by_id = {server.id: server for server in self.list_servers()}
        return [
            ModulePlacementRead.model_validate(placement).model_copy(
                update={"server": ServerRead.model_validate(servers_by_id.get(placement.server_id))}
                if placement.server_id in servers_by_id
                else {"server": None}
            )
            for placement in placements
        ]

    def create_placement(self, payload: ModulePlacementCreate) -> ModulePlacement:
        server = self.db.get(LoadBalancerServer, payload.server_id)
        if server is None:
            raise HTTPException(status_code=404, detail="Server not found.")

        assigned_count = (
            self.db.query(ModulePlacement)
            .filter(ModulePlacement.server_id == payload.server_id, ModulePlacement.enabled.is_(True))
            .count()
        )
        if assigned_count >= server.max_modules:
            raise HTTPException(status_code=400, detail="Server module capacity is full.")

        placement = ModulePlacement(**payload.model_dump())
        self.db.add(placement)
        self.db.commit()
        self.db.refresh(placement)
        return placement

    def routing_plan(self, module_name: str) -> RoutingPlan:
        servers = self.db.query(LoadBalancerServer).all()
        placements = (
            self.db.query(ModulePlacement)
            .filter(ModulePlacement.module_name == module_name)
            .order_by(ModulePlacement.priority.asc(), ModulePlacement.load_score.asc())
            .all()
        )

        # LLM MODULE HOOK:
        # If OpenRouter is configured, ask one model for a routing hint and keep
        # the deterministic rule engine as the final source of truth.
        _ai_hint = self.rule_engine.ai_routing_hint(module_name, servers, placements)

        return self.rule_engine.ordered_targets(module_name, servers, placements)


class GitAutomationService:
    def __init__(self, repo_path: str = ".") -> None:
        self.repo_path = repo_path

    def status(self) -> GitStatusResponse:
        branch = self._run(["git", "branch", "--show-current"]).strip() or "unknown"
        raw_status = self._run(["git", "status", "--short"])
        changes = [line for line in raw_status.splitlines() if line.strip()]
        return GitStatusResponse(branch=branch, clean=len(changes) == 0, changes=changes)

    def commit(self, payload: GitCommitRequest) -> GitCommitResponse:
        if payload.include_all:
            self._run(["git", "add", "-A"])

        status = self.status()
        if status.clean:
            return GitCommitResponse(
                committed=False,
                message="No changes to commit.",
                output="Working tree clean.",
            )

        output = self._run(["git", "commit", "-m", payload.message])
        commit_hash = self._run(["git", "rev-parse", "--short", "HEAD"]).strip()
        pushed = False
        if payload.push:
            output += "\n" + self._run(["git", "push"])
            pushed = True

        return GitCommitResponse(
            committed=True,
            commit_hash=commit_hash,
            message=payload.message,
            pushed=pushed,
            output=output,
        )

    def _run(self, command: list[str]) -> str:
        result = subprocess.run(
            command,
            cwd=self.repo_path,
            check=False,
            capture_output=True,
            text=True,
        )
        output = (result.stdout + result.stderr).strip()
        if result.returncode != 0:
            raise HTTPException(status_code=400, detail=output or f"Command failed: {' '.join(command)}")
        return output


class StatelessLlmPipelineService:
    def run_task(self, payload: LlmTaskRequest) -> LlmTaskResponse:
        server_count = len(payload.local_context.get("servers", []))
        placement_count = len(payload.local_context.get("placements", []))

        # LLM API HOOK:
        # Try OpenRouter models in order. If they all fail, fall back to the
        # local deterministic response so the app keeps working.
        try:
            result = OpenRouterFallbackClient().generate(
                prompt=payload.prompt,
                system_prompt="You are NESLA OS's stateless assistant. Answer briefly and actionably.",
                context=payload.local_context,
            )
            return LlmTaskResponse(
                task_id=payload.task_id,
                status="completed",
                assistant_message=result.content,
                next_action="store_result_in_indexeddb",
            )
        except Exception:
            pass

        return LlmTaskResponse(
            task_id=payload.task_id,
            status="completed",
            assistant_message=(
                "I finished the local pipeline task. "
                f"I received {server_count} servers and {placement_count} module placements from browser IndexedDB. "
                "A real LLM provider can replace this mock response at the hook."
            ),
            next_action="store_result_in_indexeddb",
        )
