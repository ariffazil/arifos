#!/usr/bin/env python3
"""
test_all_tools_live.py — Live verbatim test of all arifOS MCP tools.

Tests:
  5 Governance tools: init_session, agi_cognition, asi_empathy, apex_verdict, vault_seal
  4 Utility tools:    search, fetch, analyze, system_audit
  2 Sensory tools:    sense_health, sense_fs  (from aclip_cai)
  9 Triad tools:      triad_anchor, triad_reason, triad_integrate,
                      triad_respond, triad_validate, triad_align,
                      triad_forge, triad_audit, triad_seal
"""

import asyncio
import json
import sys
import traceback

# ── helpers ──────────────────────────────────────────────────────────────────

def banner(title: str) -> None:
    print()
    print("═" * 70)
    print(f"  {title}")
    print("═" * 70)

def section(name: str) -> None:
    print(f"\n{'─' * 70}")
    print(f"  TOOL: {name}")
    print(f"{'─' * 70}")

def show(label: str, result: object) -> None:
    print(f"\n[{label}]")
    try:
        print(json.dumps(result, indent=2, default=str))
    except Exception:
        print(repr(result))

PASS = "✅ PASS"
FAIL = "❌ FAIL"
results: list[tuple[str, str, str]] = []   # (tool, status, note)

def record(tool: str, result: object, *, expect_key: str = "verdict") -> None:
    try:
        if isinstance(result, dict):
            v = result.get(expect_key, result.get("status", "?"))
            note = str(v)
            status = FAIL if str(v).upper() in {"VOID", "ERROR"} else PASS
        else:
            note = repr(result)[:80]
            status = PASS
    except Exception as e:
        note = str(e)
        status = FAIL
    results.append((tool, status, note))
    print(f"\n  → {status}  verdict/status = {note}")


# ── main test coroutine ───────────────────────────────────────────────────────

async def run_all() -> None:
    banner("arifOS MCP — Full Tool Surface Live Test")

    # ── shared session id ────────────────────────────────────────────────────
    SESSION_ID = "test-session-abc123"

    # ════════════════════════════════════════════════════════════════════════
    # BLOCK 1 — 5 Governance Tools  (aaa_mcp/server.py)
    # ════════════════════════════════════════════════════════════════════════
    banner("BLOCK 1 — Governance Tools (5-Organ Trinity)")

    from aaa_mcp.server import (
        _init_session,
        _agi_cognition,
        _asi_empathy,
        _apex_verdict,
        _vault_seal,
        _search,
        _fetch,
        _analyze,
        _system_audit,
    )

    # 1. init_session
    section("init_session")
    try:
        r = await _init_session(
            query="What is the meaning of constitutional AI?",
            actor_id="test_actor",
            mode="conscience",
            grounding_required=True,
            debug=True,
        )
        show("init_session result", r)
        record("init_session", r)
        SESSION_ID = r.get("session_id", SESSION_ID)
        print(f"  → session_id captured: {SESSION_ID}")
    except Exception as e:
        print(f"  EXCEPTION: {e}")
        traceback.print_exc()
        results.append(("init_session", FAIL, str(e)))

    # 2. agi_cognition
    section("agi_cognition")
    try:
        r = await _agi_cognition(
            query="Explain constitutional AI governance in 3 sentences.",
            session_id=SESSION_ID,
            grounding=[{"source": "test", "text": "Constitutional AI aligns AI with human values."}],
            capability_modules=["reasoning", "integration"],
            debug=True,
        )
        show("agi_cognition result", r)
        record("agi_cognition", r)
    except Exception as e:
        print(f"  EXCEPTION: {e}")
        traceback.print_exc()
        results.append(("agi_cognition", FAIL, str(e)))

    # 3. asi_empathy
    section("asi_empathy")
    try:
        r = await _asi_empathy(
            query="Should we deploy this AI system to production?",
            session_id=SESSION_ID,
            stakeholders=["users", "operators", "society"],
            capability_modules=["empathy", "ethics"],
            debug=True,
        )
        show("asi_empathy result", r)
        record("asi_empathy", r)
    except Exception as e:
        print(f"  EXCEPTION: {e}")
        traceback.print_exc()
        results.append(("asi_empathy", FAIL, str(e)))

    # 4. apex_verdict
    section("apex_verdict")
    try:
        r = await _apex_verdict(
            session_id=SESSION_ID,
            query="Final verdict on deploying constitutional AI system.",
            agi_result={"verdict": "SEAL", "stage": "111-444"},
            asi_result={"verdict": "SEAL", "stage": "555-666"},
            proposed_verdict="SEAL",
            human_approve=False,
            debug=True,
        )
        show("apex_verdict result", r)
        record("apex_verdict", r)
    except Exception as e:
        print(f"  EXCEPTION: {e}")
        traceback.print_exc()
        results.append(("apex_verdict", FAIL, str(e)))

    # 5. vault_seal
    section("vault_seal")
    try:
        r = await _vault_seal(
            session_id=SESSION_ID,
            summary="Test session: constitutional AI governance query completed.",
            verdict="SEAL",
        )
        show("vault_seal result", r)
        record("vault_seal", r)
    except Exception as e:
        print(f"  EXCEPTION: {e}")
        traceback.print_exc()
        results.append(("vault_seal", FAIL, str(e)))

    # ════════════════════════════════════════════════════════════════════════
    # BLOCK 2 — 4 Utility Tools
    # ════════════════════════════════════════════════════════════════════════
    banner("BLOCK 2 — Utility Tools (Read-Only)")

    # 6. search
    section("search")
    try:
        r = await _search(query="constitutional AI governance", intent="research")
        show("search result", r)
        record("search", r, expect_key="status")
    except Exception as e:
        print(f"  EXCEPTION: {e}")
        traceback.print_exc()
        results.append(("search", FAIL, str(e)))

    # 7. fetch
    section("fetch")
    try:
        r = await _fetch(id="https://modelcontextprotocol.io", max_chars=500)
        show("fetch result", r)
        record("fetch", r, expect_key="status")
    except Exception as e:
        print(f"  EXCEPTION: {e}")
        traceback.print_exc()
        results.append(("fetch", FAIL, str(e)))

    # 8. analyze
    section("analyze")
    try:
        r = await _analyze(
            data={"session_id": SESSION_ID, "verdict": "SEAL", "nested": {"key": "value"}},
            analysis_type="structure",
        )
        show("analyze result", r)
        record("analyze", r)
    except Exception as e:
        print(f"  EXCEPTION: {e}")
        traceback.print_exc()
        results.append(("analyze", FAIL, str(e)))

    # 9. system_audit
    section("system_audit")
    try:
        r = await _system_audit(audit_scope="quick", verify_floors=True)
        show("system_audit result", r)
        record("system_audit", r)
    except Exception as e:
        print(f"  EXCEPTION: {e}")
        traceback.print_exc()
        results.append(("system_audit", FAIL, str(e)))

    # ════════════════════════════════════════════════════════════════════════
    # BLOCK 3 — aclip_cai Sensory Tools
    # ════════════════════════════════════════════════════════════════════════
    banner("BLOCK 3 — aclip_cai Sensory Tools")

    from aclip_cai.tools.system_monitor import get_system_health
    from aclip_cai.tools.fs_inspector import fs_inspect

    # 10. sense_health
    section("sense_health")
    try:
        r = get_system_health()
        show("sense_health result", r)
        record("sense_health", r, expect_key="status")
    except Exception as e:
        print(f"  EXCEPTION: {e}")
        traceback.print_exc()
        results.append(("sense_health", FAIL, str(e)))

    # 11. sense_fs
    section("sense_fs")
    try:
        r = fs_inspect(path=".", depth=1)
        show("sense_fs result", r)
        record("sense_fs", r, expect_key="status")
    except Exception as e:
        print(f"  EXCEPTION: {e}")
        traceback.print_exc()
        results.append(("sense_fs", FAIL, str(e)))

    # ════════════════════════════════════════════════════════════════════════
    # BLOCK 4 — 9 Triad Tools (raw kernel functions)
    # ════════════════════════════════════════════════════════════════════════
    banner("BLOCK 4 — 9 Triad Kernel Functions (aclip_cai/triad)")

    from aclip_cai.triad import (
        anchor, reason, integrate,
        respond, validate, align,
        forge, audit, seal,
    )

    TRIAD_SID = "triad-test-xyz789"

    # 12. triad_anchor
    section("triad_anchor")
    try:
        r = await anchor(session_id=TRIAD_SID, user_id="triad_tester", context="Testing the triad anchor.")
        show("triad_anchor result", r)
        record("triad_anchor", r)
    except Exception as e:
        print(f"  EXCEPTION: {e}")
        traceback.print_exc()
        results.append(("triad_anchor", FAIL, str(e)))

    # 13. triad_reason
    section("triad_reason")
    try:
        r = await reason(
            session_id=TRIAD_SID,
            hypothesis="Constitutional AI reduces harmful outputs.",
            evidence=["F1 Amanah enforces truthfulness.", "F9 Anti-Hantu blocks deceptive claims."],
        )
        show("triad_reason result", r)
        record("triad_reason", r)
    except Exception as e:
        print(f"  EXCEPTION: {e}")
        traceback.print_exc()
        results.append(("triad_reason", FAIL, str(e)))

    # 14. triad_integrate
    section("triad_integrate")
    try:
        r = await integrate(
            session_id=TRIAD_SID,
            context_bundle={"query": "test", "grounding": {"source": "unit-test"}},
        )
        show("triad_integrate result", r)
        record("triad_integrate", r)
    except Exception as e:
        print(f"  EXCEPTION: {e}")
        traceback.print_exc()
        results.append(("triad_integrate", FAIL, str(e)))

    # 15. triad_respond
    section("triad_respond")
    try:
        r = await respond(
            session_id=TRIAD_SID,
            draft="Draft: Constitutional AI is governed by 13 floors.",
        )
        show("triad_respond result", r)
        record("triad_respond", r)
    except Exception as e:
        print(f"  EXCEPTION: {e}")
        traceback.print_exc()
        results.append(("triad_respond", FAIL, str(e)))

    # 16. triad_validate
    section("triad_validate")
    try:
        r = await validate(session_id=TRIAD_SID, action="Deploy AI system to production.")
        show("triad_validate result", r)
        record("triad_validate", r)
    except Exception as e:
        print(f"  EXCEPTION: {e}")
        traceback.print_exc()
        results.append(("triad_validate", FAIL, str(e)))

    # 17. triad_align
    section("triad_align")
    try:
        r = await align(session_id=TRIAD_SID, action="Align AI outputs with human values.")
        show("triad_align result", r)
        record("triad_align", r)
    except Exception as e:
        print(f"  EXCEPTION: {e}")
        traceback.print_exc()
        results.append(("triad_align", FAIL, str(e)))

    # 18. triad_forge
    section("triad_forge")
    try:
        r = await forge(session_id=TRIAD_SID, plan="Forge a constitutional AI deployment plan.")
        show("triad_forge result", r)
        record("triad_forge", r)
    except Exception as e:
        print(f"  EXCEPTION: {e}")
        traceback.print_exc()
        results.append(("triad_forge", FAIL, str(e)))

    # 19. triad_audit
    section("triad_audit")
    try:
        r = await audit(session_id=TRIAD_SID, action="Audit the constitutional AI deployment.", token="")
        show("triad_audit result", r)
        record("triad_audit", r)
    except Exception as e:
        print(f"  EXCEPTION: {e}")
        traceback.print_exc()
        results.append(("triad_audit", FAIL, str(e)))

    # 20. triad_seal
    section("triad_seal")
    try:
        r = await seal(session_id=TRIAD_SID, task_summary="Triad test complete. All 9 functions exercised.")
        show("triad_seal result", r)
        record("triad_seal", r)
    except Exception as e:
        print(f"  EXCEPTION: {e}")
        traceback.print_exc()
        results.append(("triad_seal", FAIL, str(e)))

    # ════════════════════════════════════════════════════════════════════════
    # SUMMARY
    # ════════════════════════════════════════════════════════════════════════
    banner("FINAL SUMMARY — All Tools")
    print(f"\n{'Tool':<22} {'Status':<10} {'Verdict/Note'}")
    print(f"{'─'*22} {'─'*10} {'─'*36}")
    passes = 0
    fails = 0
    for tool, status, note in results:
        print(f"  {tool:<20} {status:<10} {note}")
        if PASS in status:
            passes += 1
        else:
            fails += 1

    print(f"\n{'─'*70}")
    print(f"  TOTAL: {len(results)} tools tested  |  ✅ {passes} passed  |  ❌ {fails} failed")
    print(f"{'═'*70}")
    if fails == 0:
        print("  VERDICT: SEAL — All tools operational")
    elif fails < len(results) // 2:
        print("  VERDICT: PARTIAL — Most tools operational")
    else:
        print("  VERDICT: VOID — Critical failures detected")
    print()


if __name__ == "__main__":
    asyncio.run(run_all())
