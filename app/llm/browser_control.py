import asyncio
import webbrowser
from dataclasses import dataclass
from typing import Any

from fastapi import HTTPException

try:
    from playwright.sync_api import sync_playwright
except Exception:  # pragma: no cover - optional dependency
    sync_playwright = None


@dataclass(frozen=True)
class BrowserOpenResult:
    allowed: bool
    action: str
    target: dict[str, Any]
    status: str


class BrowserAutomationService:
    def open_target(self, target: dict[str, Any]) -> BrowserOpenResult:
        url = target.get("url")
        if not isinstance(url, str) or not url:
            raise HTTPException(status_code=400, detail="Target URL is missing.")

        if self._try_playwright_open(url):
            return BrowserOpenResult(
                allowed=True,
                action="open_console_url",
                target=target,
                status="opened_with_playwright",
            )

        opened = webbrowser.open_new_tab(url)
        if not opened:
            raise HTTPException(status_code=500, detail="System browser could not be opened.")

        return BrowserOpenResult(
            allowed=True,
            action="open_console_url",
            target=target,
            status="opened_in_system_browser",
        )

    def navigate(self, url: str) -> dict[str, Any]:
        playwright, browser, page, context = self._new_context_page()
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=30000)
            return {
                "status": "navigated",
                "url": page.url,
                "title": page.title(),
            }
        finally:
            context.close()
            browser.close()
            playwright.stop()

    def click(self, url: str, selector: str) -> dict[str, Any]:
        playwright, browser, page, context = self._new_context_page()
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=30000)
            page.click(selector, timeout=30000)
            return {
                "status": "clicked",
                "url": page.url,
                "title": page.title(),
                "selector": selector,
            }
        finally:
            context.close()
            browser.close()
            playwright.stop()

    def type_text(self, url: str, selector: str, text: str) -> dict[str, Any]:
        playwright, browser, page, context = self._new_context_page()
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=30000)
            page.fill(selector, text, timeout=30000)
            return {
                "status": "typed",
                "url": page.url,
                "title": page.title(),
                "selector": selector,
            }
        finally:
            context.close()
            browser.close()
            playwright.stop()

    def _new_context_page(self):
        if sync_playwright is None:
            raise HTTPException(status_code=500, detail="Playwright is not installed. Install playwright and browser binaries.")
        playwright = sync_playwright().start()
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        return playwright, browser, page, context

    def _try_playwright_open(self, url: str) -> bool:
        if sync_playwright is None:
            return False
        try:
            playwright = sync_playwright().start()
            browser = playwright.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, wait_until="domcontentloaded", timeout=30000)
            browser.close()
            playwright.stop()
            return True
        except Exception:
            try:
                playwright.stop()
            except Exception:
                pass
            return False
