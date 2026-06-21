from __future__ import annotations

from pathlib import Path


ALLOWED_KEYS = [
    "OPENROUTER_API_KEY",
    "OPENROUTER_BASE_URL",
    "OPENROUTER_MODEL_IDS",
    "OPENROUTER_FALLBACK_MODEL_IDS",
    "OPENROUTER_APP_NAME",
    "OPENROUTER_REFERER",
    "OPENROUTER_TIMEOUT_SECONDS",
]


class EnvManager:
    def __init__(self, env_path: str | Path = ".env") -> None:
        self.env_path = Path(env_path)

    def read(self) -> dict[str, str]:
        data: dict[str, str] = {}
        if not self.env_path.exists():
            return data

        for raw_line in self.env_path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            if key in ALLOWED_KEYS:
                data[key] = value.strip().strip('"').strip("'")
        return data

    def write(self, updates: dict[str, str]) -> dict[str, str]:
        existing = self.read()
        merged = {**existing}
        for key, value in updates.items():
            if key in ALLOWED_KEYS:
                merged[key] = str(value)

        lines: list[str] = []
        if self.env_path.exists():
            original = self.env_path.read_text(encoding="utf-8").splitlines()
        else:
            original = []

        written_keys: set[str] = set()
        for raw_line in original:
            stripped = raw_line.strip()
            if not stripped or stripped.startswith("#") or "=" not in raw_line:
                lines.append(raw_line)
                continue
            key, _ = raw_line.split("=", 1)
            normalized_key = key.strip()
            if normalized_key in ALLOWED_KEYS:
                lines.append(f"{normalized_key}={merged.get(normalized_key, '')}")
                written_keys.add(normalized_key)
            else:
                lines.append(raw_line)

        for key in ALLOWED_KEYS:
            if key in merged and key not in written_keys:
                lines.append(f"{key}={merged[key]}")

        self.env_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
        return merged
