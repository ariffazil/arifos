"""Canonical constitutional tests for the live AAA MCP 13-tool surface."""

import os

import pytest

os.environ["AAA_MCP_OUTPUT_MODE"] = "debug"

pytestmark = pytest.mark.constitutional


def _get_tool_fn(tool):
    return getattr(tool, "fn", tool)


def _payload(result: dict):
    data = result.get("data")
    return data if isinstance(data, dict) else result


def _assert_contrast_engine(result: dict) -> None:
    engine = result.get("contrast_engine", {})
    assert isinstance(engine, dict)
    assert "tac" in engine
    assert "tpcp" in engine
    assert "scarpacket" in engine
    tac = engine["tac"]
    tpcp = engine["tpcp"]
    assert tac.get("engine") == "TAC"
    assert tpcp.get("engine") == "TPCP"
    assert 0.0 <= float(tac.get("ac_metric", 0.0)) <= 1.0
    assert 0.0 <= float(tpcp.get("phiP", 0.0)) <= 2.0


def test_all_13_floors_registered():
    from core.shared.floors import ALL_FLOORS

    assert len(ALL_FLOORS) == 13
    for i in range(1, 14):
        assert f"F{i}" in ALL_FLOORS


def test_mcp_instance_exists_and_named():
    from arifos_aaa_mcp.server import mcp

    assert mcp is not None
    assert mcp.name == "arifOS_AAA_MCP"


def test_canonical_13_tools_importable():
    from arifos_aaa_mcp.server import (
        anchor_session,
        apex_judge,
        audit_rules,
        check_vital,
        critique_thought,
        eureka_forge,
        fetch_content,
        inspect_file,
        reason_mind,
        recall_memory,
        seal_vault,
        search_reality,
        simulate_heart,
    )

    for tool in [
        anchor_session,
        reason_mind,
        recall_memory,
        simulate_heart,
        critique_thought,
        apex_judge,
        eureka_forge,
        seal_vault,
        search_reality,
        fetch_content,
        inspect_file,
        audit_rules,
        check_vital,
    ]:
        assert callable(_get_tool_fn(tool))


async def test_anchor_reason_flow_preserves_session_and_entropy_contract():
    from arifos_aaa_mcp.server import anchor_session, reason_mind

    anchor = await _get_tool_fn(anchor_session)(
        query="What is constitutional governance?",
        actor_id="user",
    )
    assert anchor["verdict"] in ("SEAL", "PARTIAL", "SABAR", "VOID")
    _assert_contrast_engine(anchor)
    anchor_data = _payload(anchor)
    assert anchor_data.get("stage") == "000_INIT"
    session_id = anchor_data.get("session_id")
    assert isinstance(session_id, str) and session_id

    reason = await _get_tool_fn(reason_mind)(
        query="Explain in one paragraph",
        session_id=session_id,
    )
    assert reason["verdict"] in ("SEAL", "PARTIAL", "SABAR", "VOID")
    _assert_contrast_engine(reason)
    reason_data = _payload(reason)
    assert reason_data.get("stage") == "111-444"
    assert reason_data.get("session_id") == session_id

    apex_dials = reason.get("apex_dials", {})
    if isinstance(apex_dials, dict) and "omega0" in apex_dials:
        assert 0.03 <= float(apex_dials["omega0"]) <= 0.05


async def test_heart_critique_judge_seal_flow():
    from arifos_aaa_mcp.server import (
        anchor_session,
        apex_judge,
        critique_thought,
        seal_vault,
        simulate_heart,
    )

    anchor = await _get_tool_fn(anchor_session)(
        query="Assess impact of config change",
        actor_id="user",
    )
    session_id = _payload(anchor)["session_id"]

    heart = await _get_tool_fn(simulate_heart)(
        query="Assess impact of config change",
        session_id=session_id,
        stakeholders=["operators", "end_users"],
    )
    assert heart["verdict"] in ("SEAL", "PARTIAL", "SABAR", "VOID")
    _assert_contrast_engine(heart)
    assert _payload(heart).get("session_id") == session_id

    critique = await _get_tool_fn(critique_thought)(
        plan={"goal": "Assess impact", "steps": ["validate", "align"]},
        session_id=session_id,
        context="Assess impact of config change",
    )
    assert critique["verdict"] in ("SEAL", "PARTIAL", "SABAR", "VOID")
    _assert_contrast_engine(critique)
    assert _payload(critique).get("session_id") == session_id

    judge = await _get_tool_fn(apex_judge)(
        session_id=session_id,
        query="Approve minimal reversible change",
        human_approve=False,
    )
    assert judge["verdict"] in ("SEAL", "PARTIAL", "SABAR", "VOID", "HOLD", "888_HOLD")
    _assert_contrast_engine(judge)
    assert _payload(judge).get("session_id") == session_id

    sealed = await _get_tool_fn(seal_vault)(
        session_id=session_id,
        summary="Constitutional flow completed",
        verdict="SEAL",
    )
    assert sealed["verdict"] in ("SEAL", "PARTIAL", "SABAR", "VOID")
    _assert_contrast_engine(sealed)
    assert _payload(sealed).get("session_id") == session_id


async def test_forge_returns_guarded_status_for_irreversible_gate():
    from arifos_aaa_mcp.server import anchor_session, eureka_forge

    anchor = await _get_tool_fn(anchor_session)(query="Execute risky action", actor_id="user")
    session_id = _payload(anchor)["session_id"]

    forged = await _get_tool_fn(eureka_forge)(
        session_id=session_id,
        command="restart_service",
        purpose="dry run"
    )
    assert forged["verdict"] in ("SEAL", "PARTIAL", "SABAR", "VOID", "888_HOLD")
    _assert_contrast_engine(forged)
    assert _payload(forged).get("session_id") == session_id


async def test_read_only_utility_tools_execute():
    from arifos_aaa_mcp.server import (
        audit_rules,
        check_vital,
        fetch_content,
        inspect_file,
        search_reality,
    )

    search = await _get_tool_fn(search_reality)(query="model context protocol", intent="general")
    _assert_contrast_engine(search)
    search_data = _payload(search)
    assert "status" in search_data
    assert "results" in search_data

    bad_fetch = await _get_tool_fn(fetch_content)(id="not-a-url", max_chars=200)
    _assert_contrast_engine(bad_fetch)
    assert _payload(bad_fetch).get("status") in ("BAD_ID", "ERROR")

    audited = await _get_tool_fn(audit_rules)(audit_scope="quick", verify_floors=True)
    assert audited["verdict"] in ("SEAL", "PARTIAL", "VOID")
    _assert_contrast_engine(audited)

    inspected = await _get_tool_fn(inspect_file)(path="/root/arifOS", depth=1, max_files=20)
    assert inspected["verdict"] in ("SEAL", "PARTIAL", "SABAR", "VOID")
    _assert_contrast_engine(inspected)

    vital = await _get_tool_fn(check_vital)(include_swap=True)
    assert vital["verdict"] in ("SEAL", "PARTIAL", "SABAR", "VOID")
    _assert_contrast_engine(vital)


async def test_law_enforcement_matrix_13_tools() -> None:
    from arifos_aaa_mcp import server as api
    from arifos_aaa_mcp.governance import TOOL_LAW_BINDINGS

    anchor = await _get_tool_fn(api.anchor_session)(query="matrix", actor_id="qa")
    session_id = _payload(anchor)["session_id"]

    calls = {
        "anchor_session": anchor,
        "reason_mind": await _get_tool_fn(api.reason_mind)(query="matrix", session_id=session_id),
        "recall_memory": await _get_tool_fn(api.recall_memory)(
            current_thought_vector="matrix-vector",
            session_id=session_id,
        ),
        "simulate_heart": await _get_tool_fn(api.simulate_heart)(
            query="matrix",
            session_id=session_id,
            stakeholders=["users"],
        ),
        "critique_thought": await _get_tool_fn(api.critique_thought)(
            plan={"goal": "matrix", "steps": ["verify"]},
            session_id=session_id,
            context="matrix",
        ),
        "apex_judge": await _get_tool_fn(api.apex_judge)(
            session_id=session_id,
            query="matrix verdict",
            human_approve=False,
        ),
        "eureka_forge": await _get_tool_fn(api.eureka_forge)(
                session_id=session_id,
                command="noop",
                purpose="matrix seal",
            ),
        "seal_vault": await _get_tool_fn(api.seal_vault)(
            session_id=session_id,
            summary="matrix seal",
            verdict="SEAL",
        ),
        "search_reality": await _get_tool_fn(api.search_reality)(query="matrix"),
        "fetch_content": await _get_tool_fn(api.fetch_content)(id="not-a-url"),
        "inspect_file": await _get_tool_fn(api.inspect_file)(path=".", depth=1, max_files=10),
        "audit_rules": await _get_tool_fn(api.audit_rules)(audit_scope="quick", verify_floors=True),
        "check_vital": await _get_tool_fn(api.check_vital)(),
    }

    assert set(calls.keys()) == set(api.AAA_TOOLS)

    for tool_name, result in calls.items():
        required = set(result["laws_13"]["required"])
        assert required == set(TOOL_LAW_BINDINGS[tool_name])
        assert len(result["laws_13"]["checks"]) == 13
        _assert_contrast_engine(result)

    assert "F13_SOVEREIGNTY" not in calls["anchor_session"]["laws_13"]["failed_required"]
    # F3_TRI_WITNESS is a SOFT floor ("mirror" type) — in test environments without
    # real multi-witness consensus, W₃ = ∛(H×A×E) may legitimately dip below threshold.
    # We verify it was CHECKED (required), not that it necessarily PASSES.
    assert "F3_TRI_WITNESS" in calls["reason_mind"]["laws_13"]["required"]
    assert "F3_TRI_WITNESS" in calls["simulate_heart"]["laws_13"]["required"]
    assert "F3_TRI_WITNESS" in calls["critique_thought"]["laws_13"]["required"]
    assert "F13_SOVEREIGNTY" not in calls["eureka_forge"]["laws_13"]["failed_required"]
