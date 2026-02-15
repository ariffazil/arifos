from __future__ import annotations

from aclip_cai.console_tools import cost_estimator, forge_guard


async def test_cost_estimator_thermodynamic_output() -> None:
    result = await cost_estimator(
        action_description="heavy refactor migration",
        estimated_cpu_percent=85,
        estimated_ram_mb=4096,
        estimated_io_mb=1024,
        operation_type="compute",
        compute_seconds=600,
    )

    assert result.status == "ok"
    thermo = result.data["thermodynamic"]
    assert 0.0 <= thermo["cost_score"] <= 1.0
    assert thermo["risk_band"] in {"green", "amber", "red"}


async def test_forge_guard_cost_threshold_sabar() -> None:
    result = await forge_guard(
        check_system_health=False,
        cost_score_threshold=0.5,
        cost_score_to_check=0.9,
        action="deploy",
        target="service/api",
        session_id="s1",
    )

    assert result.status == "ok"
    assert result.data["gate"] == "SABAR"
    assert result.data["can_proceed"] is False
    assert result.data["reason_code"] == "COST_THRESHOLD_EXCEEDED"


async def test_forge_guard_forbidden_pattern_void_local() -> None:
    result = await forge_guard(
        check_system_health=False,
        action="execute",
        target="rm -rf /",
        session_id="s2",
    )

    assert result.status == "ok"
    assert result.data["gate"] == "VOID_LOCAL"
    assert result.data["can_proceed"] is False
    assert result.data["danger_detected"] is True
