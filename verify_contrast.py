import asyncio
import json
from arifosmcp.runtime.tools import (
    init_anchor, 
    agi_reason, 
    asi_simulate, 
    asi_critique
)
from core.shared.types import Verdict

async def verify_contrast_internal():
    print("=== arifOS Contrast Audit: Internal Engine ===", flush=True)
    
    # 1. SETUP: init_anchor
    print("\n[Stage 000] Initializing Anchor...", flush=True)
    # init_anchor is a @mcp.tool, we call the handler directly
    init_res = await init_anchor(raw_input="Plan a new Dyson Sphere implementation.")
    auth_ctx = init_res.auth_context
    session_id = init_res.session_id
    print(f"  Session: {session_id}", flush=True)
    print(f"  Auth: Minted level '{auth_ctx['authority_level']}'", flush=True)

    results = []
    
    # 2. AGI REASON (Mind)
    print("\n[AGI_REASON] Executing (ARCHITECT)...", flush=True)
    agi_res = await agi_reason(
        query="Dyson Sphere logic.", 
        session_id=session_id, 
        auth_context=auth_ctx
    )
    agi_metrics = agi_res.metrics.get("telemetry", {})
    print(f"  Info: Steps: {len(agi_res.payload.get('steps', []))}, dS: {agi_metrics.get('dS')}", flush=True)
    results.append({"tool": "agi_reason", "metrics": agi_metrics, "verdict": agi_res.verdict})

    # 3. ASI SIMULATE (Heart)
    print("\n[ASI_SIMULATE] Executing (EMPATH)...", flush=True)
    asi_res = await asi_simulate(
        scenario="Impact.", 
        session_id=session_id, 
        auth_context=auth_ctx
    )
    asi_metrics = asi_res.metrics.get("telemetry", {})
    risk = asi_res.payload.get("assessment", {}).get("risk_level")
    print(f"  Info: Risk: {risk}, Peace2: {asi_metrics.get('peace2')}", flush=True)
    results.append({"tool": "asi_simulate", "metrics": asi_metrics, "verdict": asi_res.verdict})

    # 4. ASI CRITIQUE (Soul/Adversary)
    print("\n[ASI_CRITIQUE] Executing (ADVERSARY)...", flush=True)
    crit_res = await asi_critique(
        thought_content="A Dyson Sphere is safe.", 
        focus="logic", 
        session_id=session_id, 
        auth_context=auth_ctx
    )
    crit_metrics = crit_res.metrics.get("telemetry", {})
    severity = crit_res.payload.get("critique", {}).get("severity")
    print(f"  Info: Severity: {severity}, Findings: {len(crit_res.payload.get('critique', {}).get('findings', []))}", flush=True)
    results.append({"tool": "asi_critique", "metrics": crit_metrics, "verdict": crit_res.verdict})

    # 5. CONTRAST ANALYSIS
    print("\n=== Contrast Matrix ===", flush=True)
    agi_ds = results[0]['metrics'].get('dS')
    asi_peace = results[1]['metrics'].get('peace2')
    critique_severity = results[2]['metrics'].get('verdict') # Using verdict for extra contrast
    
    print(f"  Mind (AGI) -> Thermodynamic Work (dS): {agi_ds}", flush=True)
    print(f"  Heart (ASI) -> Stability Check (Peace2): {asi_peace}", flush=True)
    print(f"  Soul (Critique) -> Sovereignty Verdict: {critique_severity}", flush=True)
    
    if agi_ds != asi_peace:
        print("\n  SUCCESS: Tools contrast correctly across physical and ethical manifolds.", flush=True)
    else:
        print("\n  WARNING: Potential metric overlap detected.", flush=True)

if __name__ == "__main__":
    import os
    os.environ["ARIFOS_PHYSICS_DISABLED"] = "1"
    os.environ["ARIFOS_DEV_MODE"] = "1"
    asyncio.run(verify_contrast_internal())
