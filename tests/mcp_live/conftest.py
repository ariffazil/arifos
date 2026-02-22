import pytest
from pathlib import Path
from rich.console import Console
from aclip_cai.core.kernel import get_kernel

console = Console()

@pytest.fixture(scope="session")
async def kernel():
    """Provides a shared constitutional kernel singleton for test life-cycle."""
    return await get_kernel()

@pytest.fixture(scope="session")
def session_id():
    """Provides a shared session ID for triad and pipeline tests."""
    return "test-session-mcp-live-xyz123"

@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    # Setup test reports path
    config.option.htmlpath = "test-reports/arifos-live-report.html"

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.passed:
        # Extract verdict & thermo from test
        verdict = getattr(item, "verdict", "UNKNOWN (SEAL Expected)")
        thermo = getattr(item, "thermo_snapshot", {})
        floor_summary = getattr(item, "floor_results", {})

        # Import pytest_html here safely
        try:
            import pytest_html
            extra = getattr(report, 'extra', [])
            extra.append(pytest_html.extras.html(
                f"<div style='background:#111;color:#e6c25d;padding:1rem;border-radius:8px;'>"
                f"<strong>Verdict:</strong> {verdict}<br>"
                f"<strong>Genius:</strong> {thermo.get('genius', 'N/A')}<br>"
                f"<strong>ΔS:</strong> {thermo.get('delta_s', 'N/A')}<br>"
                f"<strong>Floors:</strong> {floor_summary}"
                f"</div>"
            ))
            report.extra = extra
        except ImportError:
            pass
