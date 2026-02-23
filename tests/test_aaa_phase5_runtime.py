"""Phase 5 runtime verification for arifOS AAA MCP.

Validates:
- 000->999 chain is callable through canonical tool names
- governance envelope fields are present on real tool responses
"""

from __future__ import annotations

from arifos_aaa_mcp import server as aaa


def _assert_envelope(payload: dict) -> None:
    assert "axioms_333" in payload
    assert "laws_13" in payload
    assert "apex_dials" in payload
    assert "motto" in payload


async def test_phase5_chain_000_to_999_with_envelopes() -> None:
    init = await aaa.anchor_session(query="Phase 5 verification", actor_id="ops")
    _assert_envelope(init)
    assert "DITEMPA" in init["motto"]["line"]
    session_id = init["data"].get("session_id", "")
    assert session_id

    reason = await aaa.reason_mind(query="verify pipeline", session_id=session_id)
    _assert_envelope(reason)

    heart = await aaa.simulate_heart(query="verify impact", session_id=session_id)
    _assert_envelope(heart)

    critique = await aaa.critique_thought(plan={"query": "verify", "risk": "medium"}, session_id=session_id)
    _assert_envelope(critique)

    judge = await aaa.judge_soul(
        session_id=session_id,
        query="finalize verification",
        agi_result=reason.get("data", {}),
        asi_result=heart.get("data", {}),
        critique_result=critique.get("data", {}),
    )
    _assert_envelope(judge)

    seal = await aaa.seal_vault(session_id=session_id, summary="Phase 5 verified", verdict="SEAL")
    _assert_envelope(seal)
    assert "DITEMPA" in seal["motto"]["line"]


async def test_phase5_auxiliary_tools_have_governed_envelope() -> None:
    tools = [
        await aaa.search_reality(query="arifOS"),
        await aaa.fetch_content(id="https://example.com", max_chars=200),
        await aaa.inspect_file(path=".", depth=1, max_files=10),
        await aaa.audit_rules(audit_scope="quick", verify_floors=True),
        await aaa.check_vital(include_swap=False, include_io=False, include_temp=False),
    ]

    for payload in tools:
        _assert_envelope(payload)
