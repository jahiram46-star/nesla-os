from dataclasses import dataclass
from typing import Any

from app.llm.browser_control import BrowserAutomationService


@dataclass(frozen=True)
class BrowserConsoleTarget:
    key: str
    label: str
    url: str
    purpose: str


class AccessBrowserCapability:
    """Rule/tool capability for future LLM-controlled browser work.

    This file intentionally does not launch Chrome yet. It describes the
    permission boundary and the exact integration points where Chrome APIs and
    server console URLs can be added later.
    """

    name = "access_browser"
    description = "Open approved server consoles and help the LLM perform guided admin tasks."

    rules = [
        "Only open URLs listed in approved_console_targets.",
        "Never submit credentials, API keys, billing changes, deletes, or deploy actions without explicit user confirmation.",
        "Read dashboard state first, then explain the next action before acting.",
        "Keep browser task context stateless on the backend; store user/task memory in browser IndexedDB.",
        "Prefer console health/status pages before deployment or destructive actions.",
    ]

    tool_capabilities = [
        "open_console_url",
        "read_visible_page_state",
        "click_safe_navigation",
        "type_non_secret_form_value",
        "report_required_user_confirmation",
    ]

    approved_console_targets = [
        BrowserConsoleTarget(
            key="firebase_console",
            label="Firebase Console",
            url="https://console.firebase.google.com/",
            purpose="Manage Firebase projects, Functions, Hosting, and app SDK config.",
        ),
        BrowserConsoleTarget(
            key="github_actions",
            label="GitHub Actions",
            url="https://github.com/",
            purpose="Open repository actions, commits, deployments, and workflow runs.",
        ),
        BrowserConsoleTarget(
            key="google_cloud_run",
            label="Google Cloud Run",
            url="https://console.cloud.google.com/run",
            purpose="Manage Cloud Run services for server deployments.",
        ),
        BrowserConsoleTarget(
            key="render_dashboard",
            label="Render Dashboard",
            url="https://dashboard.render.com/",
            purpose="Manage small/free app services.",
        ),
    ]

    def manifest(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "rules": self.rules,
            "tool_capabilities": self.tool_capabilities,
            "approved_console_targets": [target.__dict__ for target in self.approved_console_targets],
            "chrome_api_hook": self.chrome_api_hook_note(),
        }

    @staticmethod
    def chrome_api_hook_note() -> str:
        return (
            "CHROME API HOOK: Add Chrome DevTools Protocol, extension API, "
            "or Playwright bridge here after you provide credentials/allowed URLs. "
            "SERVER CONSOLE URL HOOK: Add more approved console URLs above only."
        )

    def build_open_request(self, target_key: str) -> dict[str, Any]:
        target = next((item for item in self.approved_console_targets if item.key == target_key), None)
        if target is None:
            return {
                "allowed": False,
                "reason": "Target is not in approved_console_targets.",
            }

        result = BrowserAutomationService().open_target(target.__dict__)
        return {
            "allowed": result.allowed,
            "action": result.action,
            "target": result.target,
            "status": result.status,
        }
