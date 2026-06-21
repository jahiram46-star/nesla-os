from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.core.env_manager import ALLOWED_KEYS, EnvManager

router = APIRouter(prefix="/admin", tags=["admin"])


class EnvUpdateRequest(BaseModel):
    openrouter_api_key: str | None = None
    openrouter_base_url: str | None = None
    openrouter_model_ids: str | None = Field(default=None, description="Comma-separated model ids")
    openrouter_fallback_model_ids: str | None = Field(default=None, description="Comma-separated fallback model ids")
    openrouter_app_name: str | None = None
    openrouter_referer: str | None = None
    openrouter_timeout_seconds: str | None = None

    def to_env_updates(self) -> dict[str, str]:
        mapping = {
            "OPENROUTER_API_KEY": self.openrouter_api_key,
            "OPENROUTER_BASE_URL": self.openrouter_base_url,
            "OPENROUTER_MODEL_IDS": self.openrouter_model_ids,
            "OPENROUTER_FALLBACK_MODEL_IDS": self.openrouter_fallback_model_ids,
            "OPENROUTER_APP_NAME": self.openrouter_app_name,
            "OPENROUTER_REFERER": self.openrouter_referer,
            "OPENROUTER_TIMEOUT_SECONDS": self.openrouter_timeout_seconds,
        }
        return {key: value for key, value in mapping.items() if value is not None}


@router.get("/env")
def read_env() -> dict[str, str]:
    env = EnvManager().read()
    return {key: env.get(key, "") for key in ALLOWED_KEYS}


@router.put("/env")
def update_env(payload: EnvUpdateRequest) -> dict[str, str]:
    updated = EnvManager().write(payload.to_env_updates())
    return {key: updated.get(key, "") for key in ALLOWED_KEYS}
