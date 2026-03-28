import importlib

import pytest

from arifosmcp.core.shared.types import Verdict
from arifosmcp.runtime.models import RuntimeStatus


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("module_path", "func_name", "tool_name", "stage", "mode"),
    [
        (
            "arifosmcp.runtime.megaTools.tool_07_engineering_memory",
            "engineering_memory",
            "engineering_memory",
            "555_MEMORY",
            "engineer",
        ),
        (
            "arifosmcp.runtime.megaTools.tool_09_math_estimator",
            "math_estimator",
            "math_estimator",
            "444_ROUTER",
            "health",
        ),
        (
            "arifosmcp.runtime.megaTools.tool_10_code_engine",
            "code_engine",
            "code_engine",
            "M-3_EXEC",
            "fs",
        ),
    ],
)
async def test_megatool_error_status_overrides_explicit_ok(
    monkeypatch,
    module_path,
    func_name,
    tool_name,
    stage,
    mode,
):
    module = importlib.import_module(module_path)

    async def fake_dispatch(*, mode, payload):
        return {
            "ok": True,
            "tool": tool_name,
            "stage": stage,
            "status": "ERROR",
            "verdict": "VOID",
            "payload": {
                "status": "ERROR",
                "verdict": "VOID",
                "error": "forced regression",
            },
        }

    monkeypatch.setitem(module.HARDENED_DISPATCH_MAP, tool_name, fake_dispatch)

    result = await getattr(module, func_name)(mode=mode, payload={})

    assert result.ok is False
    assert result.status == RuntimeStatus.ERROR
    assert result.verdict == Verdict.VOID


@pytest.mark.asyncio
async def test_megatool_nested_payload_error_also_forces_ok_false(monkeypatch):
    module = importlib.import_module("arifosmcp.runtime.megaTools.tool_07_engineering_memory")

    async def fake_dispatch(*, mode, payload):
        return {
            "ok": True,
            "tool": "engineering_memory",
            "stage": "555_MEMORY",
            "payload": {
                "status": "ERROR",
                "verdict": "VOID",
                "errors": [{"code": "TEST", "message": "nested failure"}],
            },
        }

    monkeypatch.setitem(module.HARDENED_DISPATCH_MAP, "engineering_memory", fake_dispatch)

    result = await module.engineering_memory(mode="engineer", payload={})

    assert result.ok is False
    assert result.status == RuntimeStatus.ERROR
    assert result.verdict == Verdict.VOID
