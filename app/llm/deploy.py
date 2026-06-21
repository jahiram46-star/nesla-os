import os
import subprocess
from dataclasses import dataclass
from typing import Any, Literal

from fastapi import HTTPException
from pydantic import BaseModel, Field


class DeployRequest(BaseModel):
    provider: Literal["command", "firebase", "cloud_run", "render_hook"] = "command"
    target: str = Field(..., min_length=2, max_length=128)
    dry_run: bool = True
    command: list[str] = Field(default_factory=list)
    env: dict[str, str] = Field(default_factory=dict)
    cwd: str | None = None
    timeout_seconds: int = Field(default=900, ge=1, le=7200)
    confirm: bool = False


class DeployResponse(BaseModel):
    provider: str
    target: str
    status: str
    dry_run: bool
    command: list[str]
    output: str
    details: dict[str, Any] = Field(default_factory=dict)


@dataclass
class DeployPlan:
    provider: str
    target: str
    command: list[str]
    details: dict[str, Any]


class DeployService:
    def prepare(self, request: DeployRequest) -> DeployPlan:
        if request.provider == "firebase":
            project_id = os.environ.get("FIREBASE_PROJECT_ID", "")
            command = self._firebase_command(request.target, project_id)
            if project_id:
                command.extend(["--project", project_id])
            return DeployPlan(request.provider, request.target, command, {"project_id": project_id})

        if request.provider == "cloud_run":
            region = os.environ.get("CLOUD_RUN_REGION", "us-central1")
            service = os.environ.get("CLOUD_RUN_SERVICE", request.target)
            image = os.environ.get("CLOUD_RUN_IMAGE", "")
            command = self._cloud_run_command(service, region, image)
            if image:
                command.extend(["--image", image])
            return DeployPlan(request.provider, request.target, command, {"region": region, "service": service, "image": image})

        if request.provider == "render_hook":
            hook = os.environ.get("RENDER_DEPLOY_HOOK_URL", "")
            if not hook:
                raise HTTPException(status_code=400, detail="RENDER_DEPLOY_HOOK_URL is not configured.")
            return DeployPlan(
                request.provider,
                request.target,
                [
                    "curl",
                    "-X",
                    "POST",
                    hook,
                    "-H",
                    "Content-Type: application/json",
                    "-d",
                    '{"service":"%s","target":"%s"}' % (request.target, request.target),
                ],
                {"hook_configured": True},
            )

        if not request.command:
            raise HTTPException(status_code=400, detail="Provide a command for provider=command.")
        return DeployPlan(request.provider, request.target, request.command, {})

    def run(self, request: DeployRequest) -> DeployResponse:
        plan = self.prepare(request)

        if request.dry_run and not request.confirm:
            return DeployResponse(
                provider=plan.provider,
                target=plan.target,
                status="dry_run",
                dry_run=True,
                command=plan.command,
                output="Deployment planned but not executed. Set dry_run=false and confirm=true to run.",
                details=plan.details,
            )

        if plan.provider == "render_hook":
            return DeployResponse(
                provider=plan.provider,
                target=plan.target,
                status="submitted",
                dry_run=False,
                command=plan.command,
                output=self._run(plan.command, request.cwd, request.env, request.timeout_seconds),
                details=plan.details,
            )

        output = self._run(plan.command, request.cwd, request.env, request.timeout_seconds)
        return DeployResponse(
            provider=plan.provider,
            target=plan.target,
            status="completed",
            dry_run=False,
            command=plan.command,
            output=output,
            details=plan.details,
        )

    @staticmethod
    def _firebase_command(target: str, project_id: str) -> list[str]:
        command = ["firebase", "deploy", "--only", target]
        if project_id:
            command.extend(["--project", project_id])
        return command

    @staticmethod
    def _cloud_run_command(service: str, region: str, image: str) -> list[str]:
        command = ["gcloud", "run", "deploy", service, "--region", region, "--platform", "managed"]
        if image:
            command.extend(["--image", image])
        return command

    def _run(self, command: list[str], cwd: str | None, env: dict[str, str], timeout_seconds: int) -> str:
        merged_env = os.environ.copy()
        merged_env.update(env)
        result = subprocess.run(
            command,
            cwd=cwd,
            env=merged_env,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            check=False,
        )
        output = (result.stdout + result.stderr).strip()
        if result.returncode != 0:
            raise HTTPException(status_code=400, detail=output or f"Command failed: {' '.join(command)}")
        return output or "Deployment command completed."
