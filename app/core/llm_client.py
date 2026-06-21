import os
from dataclasses import dataclass
from typing import Any

import requests

from app.core.env_manager import EnvManager


@dataclass(frozen=True)
class LlmGenerationResult:
    model: str
    content: str
    raw: dict[str, Any]


class OpenRouterFallbackClient:
    def __init__(self) -> None:
        env = EnvManager().read()
        self.api_key = env.get("OPENROUTER_API_KEY", os.environ.get("OPENROUTER_API_KEY", "")).strip()
        self.base_url = env.get("OPENROUTER_BASE_URL", os.environ.get("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")).rstrip("/")
        self.app_name = env.get("OPENROUTER_APP_NAME", os.environ.get("OPENROUTER_APP_NAME", "NESLA OS"))
        self.referer = env.get("OPENROUTER_REFERER", os.environ.get("OPENROUTER_REFERER", "http://localhost:8000"))
        self.timeout_seconds = int(env.get("OPENROUTER_TIMEOUT_SECONDS", os.environ.get("OPENROUTER_TIMEOUT_SECONDS", "60")))
        self.models = self._load_models(env)
        self.fallback_models = self._load_fallback_models(env)

    def generate(self, prompt: str, system_prompt: str = "", context: dict[str, Any] | None = None) -> LlmGenerationResult:
        if not self.api_key:
            raise RuntimeError("OPENROUTER_API_KEY is not configured.")

        payload = {
            "model": None,
            "messages": self._build_messages(prompt, system_prompt, context or {}),
            "temperature": 0.2,
        }

        last_error: str | None = None
        for model in self._candidate_models():
            payload["model"] = model
            try:
                response = requests.post(
                    f"{self.base_url}/chat/completions",
                    headers=self._headers(),
                    json=payload,
                    timeout=self.timeout_seconds,
                )
                if response.status_code >= 400:
                    last_error = f"{model}: {response.status_code} {response.text.strip()}"
                    continue

                data = response.json()
                content = self._extract_content(data)
                if content:
                    return LlmGenerationResult(model=model, content=content, raw=data)

                last_error = f"{model}: empty completion"
            except requests.RequestException as exc:
                last_error = f"{model}: {exc}"

        raise RuntimeError(last_error or "OpenRouter request failed.")

    def _candidate_models(self) -> list[str]:
        seen: set[str] = set()
        ordered: list[str] = []
        for model in [*self.models, *self.fallback_models]:
            candidate = model.strip()
            if candidate and candidate not in seen:
                seen.add(candidate)
                ordered.append(candidate)
        return ordered

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": self.referer,
            "X-Title": self.app_name,
            "Content-Type": "application/json",
        }

    @staticmethod
    def _build_messages(prompt: str, system_prompt: str, context: dict[str, Any]) -> list[dict[str, str]]:
        messages: list[dict[str, str]] = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        if context:
            messages.append({"role": "system", "content": f"Context: {context}"})
        messages.append({"role": "user", "content": prompt})
        return messages

    @staticmethod
    def _extract_content(payload: dict[str, Any]) -> str:
        choices = payload.get("choices", [])
        if not choices:
            return ""
        message = choices[0].get("message", {})
        return str(message.get("content", "")).strip()

    @staticmethod
    def _load_models(env: dict[str, str]) -> list[str]:
        raw = env.get("OPENROUTER_MODEL_IDS", os.environ.get("OPENROUTER_MODEL_IDS", ""))
        return [item.strip() for item in raw.split(",") if item.strip()]

    @staticmethod
    def _load_fallback_models(env: dict[str, str]) -> list[str]:
        raw = env.get("OPENROUTER_FALLBACK_MODEL_IDS", os.environ.get("OPENROUTER_FALLBACK_MODEL_IDS", ""))
        return [item.strip() for item in raw.split(",") if item.strip()]
