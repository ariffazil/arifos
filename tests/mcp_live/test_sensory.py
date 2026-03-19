import pytest
from aaa_mcp.server import _analyze, audit_rules, fetch_content, search_reality
from aclip_cai.tools.system_monitor import get_system_health
from aclip_cai.tools.fs_inspector import fs_inspect
from tests.mcp_live.utils.validators import validate_constitutionally


@pytest.mark.asyncio
async def test_search(kernel, session_id):
    result = await search_reality.fn(query="constitutional AI governance", intent="research")
    validate_constitutionally("search", result, kernel)
    assert result is not None


@pytest.mark.asyncio
async def test_fetch(kernel, session_id):
    result = await fetch_content.fn(id="https://modelcontextprotocol.io", max_chars=500)
    validate_constitutionally("fetch", result, kernel)
    assert result is not None


@pytest.mark.asyncio
async def test_analyze(kernel, session_id):
    result = await _analyze(
        data={"session_id": session_id, "verdict": "SEAL", "nested": {"key": "value"}},
        analysis_type="structure",
    )
    validate_constitutionally("analyze", result, kernel)
    assert result is not None


@pytest.mark.asyncio
async def test_system_audit(kernel, session_id):
    result = await audit_rules.fn(audit_scope="quick", verify_floors=True)
    validate_constitutionally("system_audit", result, kernel)
    assert result is not None


@pytest.mark.asyncio
async def test_sense_health():
    # Sync tool
    result = get_system_health()
    assert result is not None
    assert "status" in result


@pytest.mark.asyncio
async def test_sense_fs():
    # Sync tool
    result = fs_inspect(path=".", depth=1)
    assert result is not None
    assert "status" in result
