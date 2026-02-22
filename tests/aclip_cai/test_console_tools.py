"""
ACLIP_CAI Tests
================

Unit tests for the 9-Tool Nervous System.
"""

import pytest
import asyncio
from pathlib import Path
from unittest.mock import patch, MagicMock

# Import all tools
import sys
from pathlib import Path

# Add project root to sys.path to resolve 'aclip_cai'
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from aclip_cai.console_tools import (
    system_health,
    process_list,
    fs_inspect,
    log_tail,
    net_status,
    config_flags,
    cost_estimator,
    forge_guard,
)

# =============================================================================
# Tool 1: system_health
# =============================================================================


@pytest.mark.asyncio
async def test_system_health_basic():
    """Test basic system health retrieval."""
    result = await system_health()

    assert result.tool == "system_health"
    assert result.status == "ok"
    assert result.data is not None
    assert "cpu" in result.data
    assert "memory" in result.data
    assert "disk" in result.data
    assert result.latency_ms > 0


@pytest.mark.asyncio
async def test_system_health_with_swap():
    """Test system health with swap info."""
    result = await system_health(include_swap=True)

    assert result.status == "ok"
    assert "swap" in result.data.get("memory", {})


@pytest.mark.asyncio
async def test_system_health_no_swap():
    """Test system health without swap info."""
    result = await system_health(include_swap=False)

    assert result.status == "ok"
    assert "swap" not in result.data.get("memory", {})


# =============================================================================
# Tool 2: process_list
# =============================================================================


@pytest.mark.asyncio
async def test_process_list_basic():
    """Test basic process listing."""
    result = await process_list(limit=10)

    assert result.tool == "process_list"
    assert result.status == "ok"
    assert "processes" in result.data
    assert isinstance(result.data["processes"], list)
    assert result.data["total_count"] <= 10


@pytest.mark.asyncio
async def test_process_list_filter():
    """Test process filtering."""
    result = await process_list(filter_name="python", limit=5)

    assert result.status == "ok"
    for proc in result.data.get("processes", []):
        assert "python" in proc.get("name", "").lower()


@pytest.mark.asyncio
async def test_process_list_cpu_threshold():
    """Test CPU threshold filtering."""
    result = await process_list(min_cpu_percent=0.1, limit=20)

    assert result.status == "ok"
    for proc in result.data.get("processes", []):
        assert proc.get("cpu_percent", 0) >= 0.1


# =============================================================================
# Tool 3: fs_inspect
# =============================================================================


@pytest.mark.asyncio
async def test_fs_inspect_directory(tmp_path):
    """Test filesystem directory inspection."""
    # Create a dummy directory and file
    d = tmp_path / "sub"
    d.mkdir()
    f = d / "test.txt"
    f.write_text("content")

    result = await fs_inspect(path=str(tmp_path), max_depth=1)

    assert result.tool == "fs_inspect"
    assert result.status == "ok"
    assert result.data.get("root") == str(tmp_path)
    assert "directories" in result.data
    assert "files" in result.data
    assert len(result.data["directories"]) > 0
    assert result.data["directories"][0]["path"] == str(d)


@pytest.mark.asyncio
async def test_fs_inspect_pattern(tmp_path):
    """Test filesystem pattern filtering."""
    # Create some dummy files
    (tmp_path / "a.py").touch()
    (tmp_path / "b.txt").touch()
    (tmp_path / "c.py").touch()

    result = await fs_inspect(path=str(tmp_path), pattern="*.py", max_depth=1, max_files=10)

    assert result.status == "ok"
    assert len(result.data.get("files", [])) == 2
    for f in result.data.get("files", []):
        assert f.get("path", "").endswith(".py")


@pytest.mark.asyncio
async def test_fs_inspect_nonexistent():
    """Test filesystem inspection of non-existent path."""
    result = await fs_inspect(path="/nonexistent/path/xyz")

    assert result.status == "error"
    assert result.error is not None


# =============================================================================
# Tool 4: log_tail
# =============================================================================


@pytest.mark.asyncio
async def test_log_tail_basic(tmp_path):
    """Test basic log tail functionality."""
    # Use a file we know exists
    test_log = tmp_path / "test.log"
    test_log.write_text("line 1\nline 2\n")

    result = await log_tail(log_path=str(test_log), lines=10)

    assert result.tool == "log_tail"
    assert result.status == "ok"
    assert "entries" in result.data
    assert result.data.get("lines_requested") == 10
    assert result.data.get("lines_returned") == 2


@pytest.mark.asyncio
async def test_log_tail_nonexistent():
    """Test log tail on non-existent file."""
    result = await log_tail(log_path="/nonexistent/log/file.log", lines=10)

    assert result.status == "error"
    assert "not found" in (result.error or "").lower() or "Log file" in (result.error or "")


@pytest.mark.asyncio
async def test_log_tail_grep(tmp_path):
    """Test log tail with grep filter."""
    test_log = tmp_path / "test.log"
    test_log.write_text("apple\nbanana\napple pie\n")

    result = await log_tail(log_path=str(test_log), lines=100, grep_pattern="apple")

    assert result.status == "ok"
    assert result.data.get("lines_returned") == 2


# =============================================================================
# Tool 5: net_status
# =============================================================================


@pytest.mark.asyncio
async def test_net_status_basic():
    """Test basic network status."""
    result = await net_status()

    assert result.tool == "net_status"
    assert result.status == "ok"
    assert "interfaces" in result.data


@pytest.mark.asyncio
async def test_net_status_with_ping():
    """Test network status with ping."""
    result = await net_status(target_host="127.0.0.1")

    assert result.status == "ok"
    assert "ping_test" in result.data
    assert result.data["ping_test"]["target"] == "127.0.0.1"


# =============================================================================
# Tool 6: config_flags
# =============================================================================


@pytest.mark.asyncio
async def test_config_flags_env():
    """Test config flags environment inspection."""
    result = await config_flags(env_prefix="PATH")

    assert result.tool == "config_flags"
    assert result.status == "ok"
    assert "environment" in result.data


@pytest.mark.asyncio
async def test_config_flags_file(tmp_path):
    """Test config flags file inspection."""
    p = tmp_path / "pyproject.toml"
    p.write_text("[tool.pytest]\n")

    result = await config_flags(config_path=str(p), env_prefix=None)

    assert result.status == "ok"
    assert "files" in result.data
    assert str(p) in result.data["files"]


@pytest.mark.asyncio
async def test_config_flags_secrets_masked():
    """Test that secrets are masked by default."""
    result = await config_flags(env_prefix="ARIFOS")

    assert result.status == "ok"
    # Check that any value containing 'secret' is masked
    for key, value in result.data.get("environment", {}).items():
        if "secret" in key.lower() or "key" in key.lower():
            assert value == "***masked***" or "***" in str(value)


# =============================================================================
# Tool 8: cost_estimator
# =============================================================================


@pytest.mark.asyncio
async def test_cost_estimator_llm():
    """Test LLM cost estimation."""
    result = await cost_estimator(
        operation_type="llm", token_count=1000, provider="openai", model="gpt-4"
    )

    assert result.tool == "cost_estimator"
    assert result.status == "ok"
    assert "costs" in result.data
    assert result.data["costs"]["llm_cost_usd"] > 0
    assert result.data["costs"]["total_usd"] > 0


@pytest.mark.asyncio
async def test_cost_estimator_storage():
    """Test storage cost estimation."""
    result = await cost_estimator(operation_type="storage", storage_gb=100.0)

    assert result.status == "ok"
    assert result.data["costs"]["storage_cost_usd"] > 0


@pytest.mark.asyncio
async def test_cost_estimator_compute():
    """Test compute cost estimation."""
    result = await cost_estimator(
        operation_type="compute",
        compute_seconds=3600,  # 1 hour
    )

    assert result.status == "ok"
    assert result.data["costs"]["compute_cost_usd"] > 0


# =============================================================================
# Tool 9: forge_guard
# =============================================================================


@pytest.mark.asyncio
async def test_forge_guard_low_risk():
    """Test forge guard with low risk."""
    with patch("aclip_cai.tools.safety_guard.get_system_health") as mock_health:
        mock_health.return_value = {
            "status": "SEAL",
            "cpu": {"percent": 10.0},
            "memory": {"percent": 10.0}
        }
        result = await forge_guard(
            action="read", target="/tmp/test", session_id="test-session", risk_level="low", dry_run=True
        )

    assert result.tool == "forge_guard"
    assert result.status == "ok"
    assert result.data["verdict"] == "SEAL"
    assert result.data["can_proceed"] is True


@pytest.mark.asyncio
async def test_forge_guard_high_risk():
    """Test forge guard with high risk."""
    result = await forge_guard(
        action="delete",
        target="/important/data",
        session_id="test-session",
        risk_level="high",
        dry_run=True,
    )

    assert result.status in ["ok", "error"]  # Constitutional block
    assert result.data["verdict"] == "SABAR"
    assert result.data["can_proceed"] is False  # dry_run=True


@pytest.mark.asyncio
async def test_forge_guard_critical_risk():
    """Test forge guard with critical risk."""
    result = await forge_guard(
        action="deploy",
        target="/production",
        session_id="test-session",
        risk_level="critical",
        dry_run=True,
    )

    assert result.status in ["ok", "error"]
    assert result.data["verdict"] == "SABAR"  # Changed from 888_HOLD
    assert result.data["can_proceed"] is False


@pytest.mark.asyncio
async def test_forge_guard_dangerous_pattern():
    """Test forge guard blocks dangerous patterns."""
    result = await forge_guard(
        action="execute",
        target="rm -rf /",
        session_id="test-session",
        risk_level="low",
        dry_run=True,
    )

    assert result.status in ["ok", "error"]
    assert result.data["verdict"] == "VOID"
    assert result.data["danger_detected"] is True
    assert result.data["can_proceed"] is False


# =============================================================================
# Integration Tests
# =============================================================================


@pytest.mark.asyncio
async def test_all_tools_latency(tmp_path):
    """Test that all tools complete within reasonable time."""
    tools = [
        system_health(),
        process_list(limit=5),
        fs_inspect(path=str(tmp_path), max_depth=1),
        net_status(check_interfaces=True, check_connections=False),
        config_flags(env_prefix="HOME"),
        cost_estimator(operation_type="llm", token_count=1000),
        forge_guard(action="test", target=str(tmp_path), session_id="test", dry_run=True),
    ]

    results = await asyncio.gather(*tools)

    for result in results:
        assert result.latency_ms < 20000, f"{result.tool} took too long: {result.latency_ms}ms"


@pytest.mark.asyncio
async def test_response_format_consistency():
    """Test that all tools return consistent response format."""
    result = await system_health()

    # Check required fields
    assert hasattr(result, "tool")
    assert hasattr(result, "status")
    assert hasattr(result, "timestamp")
    assert hasattr(result, "data")
    assert hasattr(result, "error")
    assert hasattr(result, "latency_ms")

    # Check status values
    assert result.status in ["ok", "error", "warning"]
