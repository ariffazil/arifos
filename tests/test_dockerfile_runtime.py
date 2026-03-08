from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_runtime_dockerfile_installs_playwright_browser_deterministically():
    dockerfile = (ROOT / "Dockerfile").read_text(encoding="utf-8")

    assert "ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright" in dockerfile
    assert "python -m playwright install --with-deps chromium" in dockerfile
