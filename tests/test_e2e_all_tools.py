"""
E2E verification for the canonical arifOS MCP tool surface.

Covers:
- 5-organ tools: init_session, agi_cognition, asi_empathy, apex_verdict, vault_seal
- 4 utility tools: search, fetch, analyze, system_audit
"""

from __future__ import annotations

import pytest

from aaa_mcp.server import (
    agi_cognition,
    analyze,
    apex_verdict,
    asi_empathy,
    fetch,
    init_session,
    search,
    system_audit,
    vault_seal,
)


@pytest.mark.anyio
async def test_all_tools() -> None:
    print("=" * 72)
    print("arifOS E2E Tool Verification (Canonical 9 tools)")
    print("=" * 72)

    query = "Should arifOS enable autonomous policy updates without human sign-off?"
    results: dict[str, dict] = {}

    # 1) init_session
    print("\n--- 1. init_session ---")
    init_result = await init_session.fn(query=query, actor_id="test_e2e")
    print(f"  verdict={init_result.get('verdict')} session_id={init_result.get('session_id')}")
    assert isinstance(init_result, dict)
    assert "verdict" in init_result
    results["init_session"] = init_result

    session_id = init_result.get("session_id") or "test_session_fallback"

    # 2) agi_cognition
    print("\n--- 2. agi_cognition ---")
    agi_result = await agi_cognition.fn(query=query, session_id=session_id)
    print(f"  verdict={agi_result.get('verdict')} stage={agi_result.get('stage')}")
    assert isinstance(agi_result, dict)
    assert "verdict" in agi_result
    results["agi_cognition"] = agi_result

    # 3) asi_empathy
    print("\n--- 3. asi_empathy ---")
    asi_result = await asi_empathy.fn(query=query, session_id=session_id)
    print(f"  verdict={asi_result.get('verdict')} stage={asi_result.get('stage')}")
    assert isinstance(asi_result, dict)
    assert "verdict" in asi_result
    results["asi_empathy"] = asi_result

    # 4) apex_verdict
    print("\n--- 4. apex_verdict ---")
    apex_result = await apex_verdict.fn(
        session_id=session_id,
        query=query,
        implementation_details={"source": "tests/test_e2e_all_tools.py"},
        proposed_verdict="SEAL",
        human_approve=False,
    )
    print(f"  verdict={apex_result.get('verdict')} authority={apex_result.get('authority')}")
    assert isinstance(apex_result, dict)
    assert "verdict" in apex_result
    results["apex_verdict"] = apex_result

    # 5) vault_seal
    print("\n--- 5. vault_seal ---")
    vault_result = await vault_seal.fn(
        session_id=session_id,
        summary="Canonical tool E2E test seal entry",
        verdict=apex_result.get("verdict", "SEAL"),
    )
    print(f"  verdict={vault_result.get('verdict')} stage={vault_result.get('stage')}")
    assert isinstance(vault_result, dict)
    assert "verdict" in vault_result
    results["vault_seal"] = vault_result

    # 6) analyze
    print("\n--- 6. analyze ---")
    analyze_result = await analyze.fn(
        data={"init": init_result.get("verdict"), "apex": apex_result.get("verdict")},
        analysis_type="structure",
    )
    print(f"  verdict={analyze_result.get('verdict')} depth={analyze_result.get('depth')}")
    assert isinstance(analyze_result, dict)
    assert "verdict" in analyze_result
    results["analyze"] = analyze_result

    # 7) system_audit
    print("\n--- 7. system_audit ---")
    audit_result = await system_audit.fn(audit_scope="quick", verify_floors=True)
    print(f"  verdict={audit_result.get('verdict')} scope={audit_result.get('scope')}")
    assert isinstance(audit_result, dict)
    assert "verdict" in audit_result
    results["system_audit"] = audit_result

    # 8) search
    print("\n--- 8. search ---")
    search_result = await search.fn("arifOS constitutional governance")
    ids = search_result.get("ids", [])
    print(f"  ids={len(ids)}")
    assert isinstance(search_result, dict)
    assert "ids" in search_result
    results["search"] = search_result

    # 9) fetch
    print("\n--- 9. fetch ---")
    fetch_id = ids[0] if ids else "https://example.invalid/not-found"
    fetch_result = await fetch.fn(fetch_id)
    print(f"  has_error={'error' in fetch_result} id={fetch_result.get('id', 'N/A')}")
    assert isinstance(fetch_result, dict)
    assert ("id" in fetch_result) or ("error" in fetch_result)
    results["fetch"] = fetch_result

    print("\n" + "=" * 72)
    print(f"E2E verification complete. Steps executed: {len(results)}")
    print("=" * 72)
