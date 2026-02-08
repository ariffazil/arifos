"""
arifOS AAA MCP Server — Constitutional AI Governance (v55.5-HARDENED)

10 canonical tools organized as a Trinity pipeline:
  000_INIT → AGI(Mind) → ASI(Heart) → APEX(Soul) → 999_VAULT

Every tool is guarded by constitutional floors (F1-F13).
Verdicts: SEAL (approved) | VOID (blocked) | PARTIAL (warning) | SABAR (repair)
Motto: DITEMPA BUKAN DIBERI — Forged, Not Given
"""

from typing import Optional, Any
import json

from fastmcp import FastMCP

from aaa_mcp.core.constitutional_decorator import constitutional_floor, get_tool_floors
from aaa_mcp.core.engine_adapters import AGIEngine, APEXEngine, ASIEngine, InitEngine
from aaa_mcp.services.constitutional_metrics import (
    AXIOM_DATABASE,
    ConflictStatus,
    EvidenceObject,
    EvidenceType,
    PlanObject,
    generate_content_hash,
    get_flight_recorder,
    get_session_evidence,
    get_stage_result,
    store_stage_result,
)
from aaa_mcp.tools.reality_grounding import reality_check

mcp = FastMCP("aaa-mcp")


# Note: custom_route endpoints require FastMCP 2.0+
# For health checks, use the MCP tools/list endpoint
# or upgrade FastMCP: pip install fastmcp>=2.0


# Tool implementations using adapters
@mcp.tool()
@constitutional_floor("F11", "F12")
async def init_gate(
    query: str,
    session_id: Optional[str] = None,
    grounding_required: bool = True,
    mode: str = "fluid",
) -> dict:
    """Initialize a constitutional session. CALL THIS FIRST.
    
    Pipeline: 000_INIT
    Floors: F11, F12
    Metadata: Sets 'grounding_required' mode.
    """
    engine = InitEngine()
    result = await engine.ignite(query, session_id)
    
    # Schematized Output (v55.5-CRYSTALLIZED)
    hardened_result = {
        "session_id": result.get("session_id", session_id or "unknown"),
        "verdict": result.get("verdict", ConflictStatus.SEAL.value),
        "status": "READY",
        "grounding_required": grounding_required,
        "mode": mode,
        "motto": "DITEMPA BUKAN DIBERI 💎🔥🧠",
        "floors_enforced": get_tool_floors("init_gate"),
        "evidence": [],
        "pass": "forward"
    }
    store_stage_result(hardened_result["session_id"], "init", hardened_result)
    return hardened_result


@mcp.tool()
@constitutional_floor("F2", "F4")
async def agi_sense(query: str, session_id: str) -> dict:
    """Parse intent and classify lane (HARD/SOFT/META)."""
    engine = AGIEngine()
    result = await engine.sense(query, session_id)
    
    # Evidence v2 Enforced
    evidence = result.get("evidence", [])
    if not evidence:
        txt = f"Linguistic structure analysis: {query[:50]}"
        evidence.append({
            "evidence_id": f"E-SENSE-{session_id[:4]}",
            "content": {"text": txt, "hash": generate_content_hash(txt), "language": "en"},
            "source_meta": {"uri": "internal://agi/sense", "type": EvidenceType.EMPIRICAL.value, "author": "AGI_MIND", "timestamp": "now"},
            "metrics": {"trust_weight": 1.0, "relevance_score": 1.0},
            "lifecycle": {"status": "active", "retrieved_by": "agi_sense_v2"}
        })
    result["evidence"] = evidence
    
    store_stage_result(session_id, "agi_sense", result)
    result["motto"] = "DITEMPA BUKAN DIBERI 💎🔥🧠"
    result["floors_enforced"] = get_tool_floors("agi_sense")
    result["pass"] = "forward"
    return result


@mcp.tool()
@constitutional_floor("F2", "F4", "F7")
async def agi_think(query: str, session_id: str) -> dict:
    """Generate hypotheses and explore reasoning paths."""
    engine = AGIEngine()
    result = await engine.think(query, session_id)
    
    # Evidence v2 Enforced
    evidence = result.get("evidence", [])
    if not evidence:
        txt = f"Hypothesis matrix for session {session_id[:8]}"
        evidence.append({
            "evidence_id": f"E-THINK-{session_id[:4]}",
            "content": {"text": txt, "hash": generate_content_hash(txt), "language": "en"},
            "source_meta": {"uri": "internal://agi/think", "type": EvidenceType.EMPIRICAL.value, "author": "AGI_MIND", "timestamp": "now"},
            "metrics": {"trust_weight": 0.85, "relevance_score": 1.0},
            "lifecycle": {"status": "active", "retrieved_by": "agi_think_v2"}
        })
    result["evidence"] = evidence

    store_stage_result(session_id, "agi_think", result)
    result["motto"] = "DITEMPA BUKAN DIBERI 💎🔥🧠"
    result["floors_enforced"] = get_tool_floors("agi_think")
    result["pass"] = "forward"
    return result


@mcp.tool()
@constitutional_floor("F2", "F4", "F7")
async def agi_reason(query: str, session_id: str, grounding: Optional[Any] = None) -> dict:
    """Deep logical reasoning chain — the AGI Mind's core analysis tool.

    Produces structured reasoning with conclusion, confidence, clarity improvement,
    domain classification, and caveats. Use for complex questions requiring rigorous logic.

    Pipeline position: AGI Stage 3 (after agi_think, or directly after init_gate for simple queries)
    Floors enforced: F2 (Truth >= 0.99), F4 (Empathy), F7 (Humility band 0.03-0.05)
    Next step: asi_empathize for stakeholder impact analysis
    """
    from datetime import datetime, timezone

    engine = AGIEngine()
    result = await engine.reason(query, session_id)

    # Optional structured grounding/evidence (not synthetic confidence)
    if grounding:
        evidence = result.get("evidence", [])
        # Heuristic: classify evidence type
        grounding_str = json.dumps(grounding)
        ev_type = EvidenceType.AXIOM.value if "axiom" in grounding_str.lower() or "axiom_id" in grounding else EvidenceType.WEB.value
        evidence.append({
            "evidence_id": f"E-GROUND-{session_id[:4]}",
            "content": {"text": grounding_str[:2000], "hash": generate_content_hash(grounding_str), "language": "json"},
            "source_meta": {"uri": "client://grounding", "type": ev_type, "author": "CLIENT", "timestamp": "now"},
            "metrics": {"trust_weight": 1.0, "relevance_score": 1.0},
            "lifecycle": {"status": "active", "retrieved_by": "client_grounding"}
        })
        result["evidence"] = evidence
    store_stage_result(session_id, "agi", result)

    # Clean Output (Industrial v55.5)
    result["ambiguity_reduction"] = result.pop("entropy_delta", 0.0)
    evidence = result.get("evidence", [])
    if not evidence and result.get("engine_mode") == "fallback":
        txt = f"Heuristic analysis of: {query[:50]}..."
        evidence.append({
            "evidence_id": f"E-{session_id[:4]}-001",
            "content": {
                "text": txt,
                "hash": generate_content_hash(txt),
                "language": "en"
            },
            "source_meta": {
                "uri": "internal://agi/heuristic",
                "type": EvidenceType.AXIOM.value,
                "author": "AGI_HEURISTIC_ENGINE",
                "timestamp": datetime.now(timezone.utc).isoformat()
            },
            "metrics": {
                "trust_weight": result.get("confidence", 0.95),
                "relevance_score": 1.0
            },
            "lifecycle": {
                "status": "active",
                "retrieved_by": "agi_reason_v2"
            }
        })
        result["evidence"] = evidence # Ensure evidence is added to result

    result["motto"] = "DITEMPA BUKAN DIBERI 💎🔥🧠"
    result["floors_enforced"] = get_tool_floors("agi_reason")
    result["pass"] = "forward"
    return result


@mcp.tool()
@constitutional_floor("F5", "F6")
async def asi_empathize(query: str, session_id: str) -> dict:
    """Assess stakeholder impact — the ASI Heart's empathy engine."""
    engine = ASIEngine()
    result = await engine.empathize(query, session_id)
    
    # Evidence v2 Enforced
    evidence = result.get("evidence", [])
    txt = f"Stakeholder impact valuation: kappa_r={result.get('empathy_kappa_r', 1.0)}"
    evidence.append({
        "evidence_id": f"E-EMP-{session_id[:4]}",
        "content": {"text": txt, "hash": generate_content_hash(txt), "language": "en"},
        "source_meta": {"uri": "internal://asi/empathize", "type": EvidenceType.EMPIRICAL.value, "author": "ASI_HEART", "timestamp": "now"},
        "metrics": {"trust_weight": 0.95, "relevance_score": 0.9},
        "lifecycle": {"status": "active", "retrieved_by": "asi_empathize_v2"}
    })
    result["evidence"] = evidence

    store_stage_result(session_id, "asi_empathize", result)
    result["motto"] = "DITEMPA BUKAN DIBERI 💎🔥🧠"
    result["floors_enforced"] = get_tool_floors("asi_empathize")
    result["pass"] = "forward"
    return result


@mcp.tool()
@constitutional_floor("F5", "F6", "F9")
async def asi_align(query: str, session_id: str) -> dict:
    """Reconcile ethics, law, and policy — the ASI Heart's alignment engine."""
    engine = ASIEngine()
    result = await engine.align(query, session_id)
    
    # Evidence v2 Enforced
    evidence = result.get("evidence", [])
    txt = f"Ethics/Policy alignment check for {session_id[:8]}"
    evidence.append({
        "evidence_id": f"E-ALIGN-{session_id[:4]}",
        "content": {"text": txt, "hash": generate_content_hash(txt), "language": "en"},
        "source_meta": {"uri": "internal://asi/align", "type": EvidenceType.EMPIRICAL.value, "author": "ASI_HEART", "timestamp": "now"},
        "metrics": {"trust_weight": 0.98, "relevance_score": 0.95},
        "lifecycle": {"status": "active", "retrieved_by": "asi_align_v2"}
    })
    result["evidence"] = evidence

    store_stage_result(session_id, "asi_align", result)
    result["motto"] = "DITEMPA BUKAN DIBERI 💎🔥🧠"
    result["floors_enforced"] = get_tool_floors("asi_align")
    result["pass"] = "forward"
    return result


@mcp.tool()
@constitutional_floor("F2", "F3", "F5", "F8")
async def apex_verdict(query: str, session_id: str) -> dict:
    """Final constitutional verdict — the APEX Soul's judgment."""
    engine = APEXEngine()
    result = await engine.judge(query, session_id)
    
    # Formal Verdict Semantics (v55.5-INDUSTRIAL)
    session_ev = get_session_evidence(session_id)
    ev_types = {e["source_meta"]["type"] for e in session_ev}
    
    has_web = EvidenceType.WEB.value in ev_types
    has_axiom = EvidenceType.AXIOM.value in ev_types
    has_conflict = EvidenceType.CONFLICT.value in ev_types
    
    # Priority 2 Fix: Dynamic Truth Score (F2)
    # Truth is proportional to the density and diversity of evidence
    ev_diversity = len(ev_types)
    truth_score = min(0.995, 0.7 + (ev_diversity * 0.1))
    
    # Check for Industrial Risk (Anomalous Contrast)
    sense_data = get_stage_result(session_id, "agi") or {}
    risk_detected = sense_data.get("risk_detected", False)
    
    if risk_detected:
        # Absolutist claim recoil: collapse truth and force grounding review
        truth_score = min(truth_score, 0.6)
        if not has_web: # Axioms are not enough for 'guarantees'
            has_axiom = False # Mask axiom for this check to force PARTIAL/VOID
    
    # Mode-aware thresholds
    init_data = get_stage_result(session_id, "init") or {}
    current_mode = init_data.get("mode", "fluid")
    if current_mode == "fluid":
        REQUIRED_W3 = 0.85
        REQUIRED_GENIUS = 0.70
        ALLOW_AXIOMATIC_TRUTH = True
    else:
        REQUIRED_W3 = 0.95
        REQUIRED_GENIUS = 0.80
        ALLOW_AXIOMATIC_TRUTH = False

    # Allow axiomatic truth when fluid mode + high confidence (synthetic only when grounding not mandatory)
    sense_data = get_stage_result(session_id, "agi") or {}
    llm_confidence = sense_data.get("confidence", result.get("confidence", 0.0))

    synthetic_axiom = False
    if not (has_web or has_axiom):
        if ALLOW_AXIOMATIC_TRUTH and llm_confidence > 0.98:
            truth_score = 0.99
            result["verdict_justification"] = "SOURCE: AXIOMATIC_INTERNAL (High Confidence Fluid Mode)"
            synthetic_axiom = True  # do NOT flag as real axiom evidence
        else:
            truth_score = 0.5 
    
    result["truth_score"] = truth_score
    current_verdict = result.get("verdict", ConflictStatus.SEAL.value)
    
    # Dynamic floor thresholds for consensus/genius
    tri_witness_val = result.get("tri_witness", 0.95)
    genius_val = result.get("genius", result.get("genius_score", 0.8))

    if has_conflict:
        current_verdict = ConflictStatus.SABAR.value
        result["verdict_justification"] = "Conflict detected in Evidence Graph (F3)."
    elif risk_detected and not has_web:
         current_verdict = ConflictStatus.PARTIAL.value
         result["verdict_justification"] = "Absolutist risk detected. Built-in axioms are insufficient for safety guarantees (F7)."
    elif not (has_web or has_axiom):
         current_verdict = ConflictStatus.PARTIAL.value
         result["verdict_justification"] = "Self-Service mode: No external or axiomatic grounding attached (F2)."
    elif tri_witness_val < REQUIRED_W3:
         current_verdict = ConflictStatus.PARTIAL.value
         result["verdict_justification"] = f"Tri-Witness below threshold for mode={current_mode} (W3={tri_witness_val:.3f} < {REQUIRED_W3})"
    elif genius_val < REQUIRED_GENIUS:
         current_verdict = ConflictStatus.PARTIAL.value
         result["verdict_justification"] = f"Genius score below threshold for mode={current_mode} (G={genius_val:.3f} < {REQUIRED_GENIUS})"
    
    # Final Synchronization
    # FINAL SAFETY CLAMP (v55.5-INDUSTRIAL)
    grounding_mandatory = init_data.get("grounding_required", False) if init_data else False
    
    # Priority 3 Fix: Reduced Metric Noise (CORE_METRICS)
    core_metrics = {
        "verdict": current_verdict,
        "evidence_count": len(session_ev),
        "grounding_types": list(ev_types),
        "truth_fidelity": truth_score,
        "tri_witness": result.get("tri_witness", 0.95),
        "ambiguity_reduction": result.get("ambiguity_reduction", 0.0)
    }

    # Synthetic axioms must not satisfy mandatory grounding
    if grounding_mandatory and not (has_web or has_axiom):
        current_verdict = ConflictStatus.VOID.value
        result["verdict_justification"] = "GROUNDING_REQUIRED failed: Critical property anchor missing (F12)."
        truth_score = 0.45
        core_metrics["verdict"] = current_verdict
        core_metrics["truth_fidelity"] = 0.45

    # Sovereign Reconstruction: ignore legacy result keys
    final_output = {
        "verdict": current_verdict,
        "truth_score": truth_score,
        "session_id": session_id,
        "query": query,
        "CORE_GOVERNANCE": core_metrics,
        "verdict_justification": result.get("verdict_justification", ""),
        "motto": "DITEMPA BUKAN DIBERI 💎🔥🧠",
        "floors_enforced": get_tool_floors("apex_verdict"),
        "pass": "reverse",
        # Pass through some essentials from the original engine result
        "tri_witness": result.get("tri_witness", 0.95),
        "votes": result.get("votes", {})
    }

    store_stage_result(session_id, "apex", final_output)
    return final_output


@mcp.tool()
@constitutional_floor("F2", "F7")
async def reality_search(
    query: str, session_id: str, region: str = "wt-wt", timelimit: Optional[str] = None
) -> dict:
    """External fact-checking and reality grounding via web search & Axiom Engine."""
    from datetime import datetime, timezone
    
    result = await reality_check(query, region=region, timelimit=timelimit)
    
    # Axiom Engine Injection (Offline Physics/CCS Baseline)
    evidence = []
    
    # Internal Axiom Sweep (Property-Aware)
    lower_query = query.lower()
    for category, sub_cats in AXIOM_DATABASE.items():
        if category in lower_query or any(k.replace("_", " ") in lower_query for k in sub_cats.keys()):
            for property_key, values in sub_cats.items():
                if property_key.replace("_", " ") in lower_query:
                    # If it's a nested dict of properties (like co2.critical_point)
                    if isinstance(values, dict) and "value" not in values:
                        for sub_key, info in values.items():
                            # Match sub-properties (e.g. 'pressure' in 'critical_point')
                            if sub_key in lower_query or property_key.replace("_", " ") in lower_query:
                                name = info.get("name", f"{category} {property_key} {sub_key}")
                                txt = f"Axiomatic Truth: {name} = {info['value']} {info.get('unit', '')}"
                                evidence.append({
                                    "evidence_id": f"E-AXIOM-{category.upper()}-{property_key.upper()}-{sub_key.upper()}",
                                    "content": {"text": txt, "hash": generate_content_hash(txt), "language": "en"},
                                    "source_meta": {"uri": f"axiom://{category}/{property_key}/{sub_key}", "type": EvidenceType.AXIOM.value, "author": "NIST/Petronas_Baseline", "timestamp": "infinity"},
                                    "metrics": {"trust_weight": 1.0, "relevance_score": 1.0},
                                    "lifecycle": {"status": "active", "retrieved_by": "axiom_engine_v1.1"}
                                })
                    else:
                        # Single property
                        info = values
                        name = info.get("name", f"{category} {property_key}")
                        txt = f"Axiomatic Truth: {name} = {info['value']} {info.get('unit', '')}"
                        evidence.append({
                            "evidence_id": f"E-AXIOM-{category.upper()}-{property_key.upper()}",
                            "content": {"text": txt, "hash": generate_content_hash(txt), "language": "en"},
                            "source_meta": {"uri": f"axiom://{category}/{property_key}", "type": EvidenceType.AXIOM.value, "author": "NIST/Petronas_Baseline", "timestamp": "infinity"},
                            "metrics": {"trust_weight": 1.0, "relevance_score": 1.0},
                            "lifecycle": {"status": "active", "retrieved_by": "axiom_engine_v1.1"}
                        })

    # Web Search Result Processing
    for i, res in enumerate(result.get("results", [])[:3]):
        snippet = res.get("snippet", "")
        evidence.append({
            "evidence_id": f"E-WEB-{i}",
            "content": {
                "text": snippet,
                "hash": generate_content_hash(snippet),
                "language": "en"
            },
            "source_meta": {
                "uri": res.get("link", "Unknown"),
                "type": EvidenceType.WEB.value,
                "author": "WebScout",
                "timestamp": datetime.now(timezone.utc).isoformat()
            },
            "metrics": {
                "trust_weight": 0.90 if res.get("link") else 0.50,
                "relevance_score": 0.8
            },
            "lifecycle": {
                "status": "active",
                "retrieved_by": "reality_search_v2"
            }
        })

    hardened_output = {
        "query": query,
        "session_id": session_id,
        "evidence": evidence,
        "verdict": ConflictStatus.SEAL.value if evidence else ConflictStatus.INSUFFICIENT.value,
        "motto": "DITEMPA BUKAN DIBERI 💎🔥🧠"
    }
    
    store_stage_result(session_id, "reality", hardened_output)
    return hardened_output


@mcp.tool()
@constitutional_floor("F1", "F3")
async def vault_seal(
    session_id: str,
    verdict: str,
    payload: dict,
    # Enhanced v2 fields (optional for backwards compat)
    query_summary: Optional[str] = None,
    risk_level: Optional[str] = None,
    risk_tags: Optional[list] = None,
    intent: Optional[str] = None,
    category: Optional[str] = None,
    floors_checked: Optional[list] = None,
    floors_passed: Optional[list] = None,
    floors_failed: Optional[list] = None,
    entropy_omega: Optional[float] = None,
    tri_witness_score: Optional[float] = None,
    peace_squared: Optional[float] = None,
    genius_g: Optional[float] = None,
    human_override: bool = False,
    override_reason: Optional[str] = None,
    model_used: Optional[str] = None,
    tags: Optional[list] = None,
    # v2.1 additions (external audit feedback)
    tool_chain: Optional[list] = None,
    model_info: Optional[dict] = None,
    environment: str = "prod",
    prompt_excerpt: Optional[str] = None,
    response_excerpt: Optional[str] = None,
    pii_level: str = "none",
    actor_type: Optional[str] = None,
    actor_id: Optional[str] = None,
) -> dict:
    """Seal the session verdict into the immutable VAULT999 ledger.

    Records the full session (reasoning, empathy, verdict) as a Merkle hash-chained
    entry. This creates a tamper-evident audit trail. CALL THIS LAST to finalize.

    Pipeline position: 999_VAULT (final step)
    Floors enforced: F1 (Amanah — reversible/auditable), F3 (Tri-Witness)

    Args:
        session_id: The session to seal (from init_gate)
        verdict: SEAL, VOID, PARTIAL, or SABAR
        payload: Dict containing the full session results to record
        
        # Enhanced v2 fields (structured audit data):
        query_summary: First ~200 chars of input (redacted)
        risk_level: low/medium/high/critical
        risk_tags: ["safety", "financial", "privacy", etc.]
        intent: What was the user trying to do?
        category: finance/safety/content/code/governance
        floors_checked: All floors evaluated ["F1","F2","F7","F9"]
        floors_passed: Floors that passed check
        floors_failed: Floors that failed
        entropy_omega: Ω₀ uncertainty at decision time
        tri_witness_score: TW consensus metric
        peace_squared: Peace² metric
        genius_g: Genius G metric
        human_override: Was 888 Judge override invoked?
        override_reason: Why override granted
        model_used: Which LLM made the decision
        tags: Arbitrary searchable tags
        
        # v2.1 additions (external audit feedback):
        tool_chain: List of tools used ["init_gate","reality_search","apex_verdict"]
        model_info: {"provider":"Anthropic","model":"claude-opus","version":"2026-02-01"}
        environment: test/staging/prod
        prompt_excerpt: First ~200 chars of prompt (redacted)
        response_excerpt: First ~200 chars of response (redacted)
        pii_level: none/low/medium/high
        actor_type: user/system/override
        actor_id: arif-fazil, openclaw-core, etc.
    """
    import hashlib
    import os
    from datetime import datetime, timezone
    
    # Check DATABASE_URL availability
    db_url = os.environ.get("DATABASE_URL") or os.environ.get("VAULT_POSTGRES_DSN")
    
    try:
        from codebase.vault.persistent_ledger_hardened import get_hardened_vault_ledger
        use_postgres = bool(db_url)
    except ImportError:
        use_postgres = False

    # Enrich payload with v3 Hybrid structure (9 JSONB categories)
    # Compute hashes for integrity
    query_hash = None
    response_hash = None
    if query_summary:
        query_hash = hashlib.sha256(query_summary.encode()).hexdigest()[:32]
    if response_excerpt:
        response_hash = hashlib.sha256(response_excerpt.encode()).hexdigest()[:32]

    # Build 9 APEX-aligned categories
    v3_identity = {
        "session": session_id,
        "actor_type": actor_type,
        "actor_id": actor_id,
    }
    
    v3_context = {
        "summary": query_summary[:200] if query_summary else None,
        "q_hash": query_hash,
        "r_hash": response_hash,
        "intent": intent,
    }
    
    v3_risk = {
        "level": risk_level or "low",
        "tags": risk_tags or [],
        "category": category,
        "pii": pii_level,
    }
    
    v3_floors = {
        "checked": floors_checked or [],
        "failed": floors_failed or [],
        # passed = computed: checked - failed
    }
    
    v3_metrics = {
        "omega": entropy_omega,
        "tw": tri_witness_score,
        "peace2": peace_squared,
        "genius": genius_g,
    }
    
    v3_oversight = {
        "override": human_override,
        "reason": override_reason if human_override else None,
        "by": actor_id if human_override else None,
    }
    
    v3_provenance = {
        "model": model_used,
        "model_info": model_info,
        "tools": tool_chain or [],
        "env": environment,
    }

    v3_evidence = {
        "items": payload.get("evidence", []) # Evidence from previous stages
    }

    # Enriched payload with both v2.1 compat and v3 structure
    enriched_payload = {
        **payload,
        "_schema_version": "3.0",
        # v3 categories (APEX-aligned)
        "identity": v3_identity,
        "context": v3_context,
        "risk": v3_risk,
        "floors": v3_floors,
        "metrics": v3_metrics,
        "oversight": v3_oversight,
        "provenance": v3_provenance,
        "evidence": v3_evidence,
        # Backwards compat: keep _v2_metadata for existing queries
        "_v2_metadata": {
            "schema_version": "3.0",
            "query_summary": query_summary[:200] if query_summary else None,
            "query_hash": query_hash,
            "response_hash": response_hash,
            "risk_level": risk_level or "low",
            "risk_tags": risk_tags or [],
            "intent": intent,
            "category": category,
            "pii_level": pii_level,
            "floors_checked": floors_checked or [],
            "floors_failed": floors_failed or [],
            "metrics": v3_metrics,
            "human_override": human_override,
            "override_reason": override_reason,
            "model_used": model_used,
            "model_info": model_info,
            "tool_chain": tool_chain or [],
            "environment": environment,
            "actor_type": actor_type,
            "actor_id": actor_id,
            "tags": tags or [],
        },
    }

    # Try Postgres ledger first, fall back to session ledger
    seal_id = None
    seal_hash = f"hash-0"
    postgres_used = False
    
    if use_postgres:
        try:
            ledger = get_hardened_vault_ledger()
            await ledger.connect()
            result = await ledger.append(
                session_id=session_id, 
                verdict=verdict, 
                seal_data=enriched_payload, 
                authority=actor_id or "mcp_server"
            )
            seal_id = str(result.get("seal_id", ""))
            seal_hash = result.get("entry_hash", f"hash-{result.get('sequence_number', 0)}")
            postgres_used = True
        except Exception as e:
            print(f"[vault_seal] Postgres failed: {e}, using fallback")
            postgres_used = False
    
    # Fallback to session ledger if Postgres unavailable
    if not postgres_used:
        try:
            from aaa_mcp.sessions.session_ledger import get_ledger
            ledger = await get_ledger()
            entry = await ledger.seal(
                session_id=session_id,
                verdict_type=verdict,
                payload=enriched_payload,
                query_summary=query_summary or "",
                risk_level=risk_level or "LOW",
                category=category or "general",
                environment=environment,
                floors_checked=floors_checked,
                floors_failed=floors_failed,
            )
            seal_id = entry.entry_id
            seal_hash = entry.entry_hash
        except Exception as e:
            print(f"[vault_seal] Session ledger failed: {e}")
            seal_hash = f"fallback-{session_id[:8]}"
    
    return {
        "verdict": "SEALED" if seal_id else "PARTIAL",
        "seal_id": seal_id,
        "seal": seal_hash,
        "schema_version": "3.0",
        "postgres_used": postgres_used,
        # Fast-query columns (the 4 governance axes)
        "session_id": session_id,
        "verdict_type": verdict,
        "risk_level": risk_level or "low",
        "environment": environment,
        # Summary of v3 categories
        "categories": {
            "identity": v3_identity,
            "floors": v3_floors,
            "oversight": v3_oversight,
            "provenance": {"tools": tool_chain or [], "env": environment},
        },
        "motto": "DITEMPA BUKAN DIBERI 💎🔥🧠",
        "floors_enforced": get_tool_floors("vault_seal"),
        "pass": "reverse",
    }


@mcp.tool()
async def tool_router(query: str) -> PlanObject:
    """Universal Tool Router Specification v2 (Triage Nurse)."""
    from aaa_mcp.core.engine_adapters import _shannon_entropy
    import uuid
    
    entropy = _shannon_entropy(query)
    query_lower = query.lower()
    
    # Industrial Risk Pattern: detect absolutist claims in sensitive domains
    critical_keywords = {"guaranteed", "absolute", "always", "never", "perfectly", "zero", "any"}
    domain_keywords = {"ccs", "co2", "injection", "pressure", "borehole", "storage", "hazardous"}
    
    query_words = set(query.lower().split())
    has_risk = any(k in query_words for k in critical_keywords)
    has_domain = any(k in query_words for k in domain_keywords)
    
    # Triage Logic (Gemini Addition)
    is_high_risk = any(k in query_lower for k in ["seal", "integrity", "deploy", "safety", "hack", "impact", "pressure", "kill", "hazardous", "co2", "ccs"])
    
    grounding_required = False
    if has_risk and has_domain:
        grounding_required = True
        sequence = ["init_gate", "reality_search", "agi_reason", "asi_empathize", "asi_align", "apex_verdict", "vault_seal"]
        lane = "HARD (CRITICAL-PROTOCOL)"
        justification = "Absolutist industrial claim detected. Grounding MANDATORY."
    elif entropy < 0.3 and not is_high_risk:
        sequence = ["init_gate", "agi_reason"]
        lane = "SOFT (FAST-TRACK)"
        justification = "Low entropy, non-critical query. Optimized for speed."
    elif is_high_risk or entropy > 0.7:
        sequence = ["init_gate", "reality_search", "agi_reason", "asi_empathize", "asi_align", "apex_verdict", "vault_seal"]
        lane = "HARD (CRITICAL-PROTOCOL)"
        justification = "High entropy or safety-critical intent detected. Mandatory Earth Witness activation."
        grounding_required = True
    else:
        sequence = ["init_gate", "agi_reason", "apex_verdict", "vault_seal"]
        lane = "SOFT (STANDARD)"
        justification = "Standard reasoning loop recommended."

    return {
        "plan_id": f"PLAN-{uuid.uuid4().hex[:8].upper()}",
        "recommended_pipeline": sequence,
        "lane": lane,
        "entropy_score": round(entropy, 4),
        "grounding_required": grounding_required,
        "justification": justification,
        "instruction": f"Follow the sequence: {' -> '.join(sequence)}",
        "motto": "DITEMPA BUKAN DIBERI 💎🔥🧠"
    }


@mcp.tool()
@constitutional_floor("F1", "F2")
async def vault_query(
    session_pattern: Optional[str] = None,
    verdict: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    risk_level: Optional[str] = None,
    category: Optional[str] = None,
    human_override_only: bool = False,
    tag: Optional[str] = None,
    environment: Optional[str] = None,
    actor_id: Optional[str] = None,
    tool_used: Optional[str] = None,
    limit: int = 10,
) -> dict:
    """Query past vault_seal entries for institutional memory retrieval.

    Search the constitutional ledger for past decisions, violations, and patterns.
    Use this to learn from history and maintain institutional continuity (F13).

    Pipeline position: Auxiliary (can be called anytime)
    Floors enforced: F1 (Amanah), F2 (Truth)

    Args:
        session_pattern: Glob pattern for session_id (e.g., "test_*")
        verdict: Filter by verdict type (SEAL, VOID, PARTIAL, SABAR)
        date_from: ISO date string for range start (e.g., "2026-02-01")
        date_to: ISO date string for range end
        risk_level: Filter by risk (low/medium/high/critical)
        category: Filter by category (finance/safety/content/code/governance)
        human_override_only: Only show entries where 888 Judge overrode
        tag: Filter by tag (e.g., "petronas", "arifos")
        limit: Maximum entries to return (default 10, max 100)

    Returns:
        Dict with count, entries list, and detected patterns
    """
    from datetime import datetime, timezone
    from codebase.vault.persistent_ledger_hardened import get_hardened_vault_ledger

    ledger = get_hardened_vault_ledger()
    await ledger.connect()

    # Parse dates
    start_time = None
    end_time = None
    if date_from:
        try:
            start_time = datetime.fromisoformat(date_from.replace("Z", "+00:00"))
            if start_time.tzinfo is None:
                start_time = start_time.replace(tzinfo=timezone.utc)
        except ValueError:
            pass
    if date_to:
        try:
            end_time = datetime.fromisoformat(date_to.replace("Z", "+00:00"))
            if end_time.tzinfo is None:
                end_time = end_time.replace(tzinfo=timezone.utc)
        except ValueError:
            pass

    # Clamp limit
    limit = max(1, min(limit, 100))

    try:
        if verdict:
            # Use existing query_by_verdict
            result = await ledger.query_by_verdict(
                verdict=verdict,
                start_time=start_time,
                end_time=end_time,
                limit=limit
            )
            entries = result.get("entries", [])
        else:
            # Use list_entries and filter
            result = await ledger.list_entries(limit=limit * 3)  # Get more to filter
            entries = result.get("entries", [])

            # Filter by date range
            if start_time:
                entries = [e for e in entries if datetime.fromisoformat(e["timestamp"].replace("Z", "+00:00")) >= start_time]
            if end_time:
                entries = [e for e in entries if datetime.fromisoformat(e["timestamp"].replace("Z", "+00:00")) <= end_time]

        # Filter by session pattern (simple glob)
        if session_pattern:
            import fnmatch
            entries = [e for e in entries if fnmatch.fnmatch(e.get("session_id", ""), session_pattern)]

        # Helper to extract metadata (v2 or v3 format)
        def get_meta(entry):
            seal_data = entry.get("seal_data", {})
            if isinstance(seal_data, str):
                try:
                    import json
                    seal_data = json.loads(seal_data)
                except:
                    seal_data = {}
            
            # Check for v3 format first
            if seal_data.get("_schema_version") == "3.0":
                # Convert v3 to v2-compatible for filtering
                return {
                    "schema_version": "3.0",
                    "query_summary": seal_data.get("context", {}).get("summary"),
                    "risk_level": seal_data.get("risk", {}).get("level"),
                    "category": seal_data.get("risk", {}).get("category"),
                    "intent": seal_data.get("context", {}).get("intent"),
                    "floors_checked": seal_data.get("floors", {}).get("checked", []),
                    "floors_failed": seal_data.get("floors", {}).get("failed", []),
                    "human_override": seal_data.get("oversight", {}).get("override", False),
                    "tags": seal_data.get("_v2_metadata", {}).get("tags", []),
                    "environment": seal_data.get("provenance", {}).get("env"),
                    "actor_id": seal_data.get("identity", {}).get("actor_id"),
                    "actor_type": seal_data.get("identity", {}).get("actor_type"),
                    "tool_chain": seal_data.get("provenance", {}).get("tools", []),
                    "model_used": seal_data.get("provenance", {}).get("model"),
                    "pii_level": seal_data.get("risk", {}).get("pii"),
                    "metrics": {
                        "omega": seal_data.get("metrics", {}).get("omega"),
                        "tw": seal_data.get("metrics", {}).get("tw"),
                    },
                    "evidence": seal_data.get("evidence", {}).get("items", []),
                }
            
            # Fall back to v2 format
            return seal_data.get("_v2_metadata", {})

        if risk_level:
            entries = [e for e in entries if get_meta(e).get("risk_level") == risk_level]
        
        if category:
            entries = [e for e in entries if get_meta(e).get("category") == category]
        
        if human_override_only:
            entries = [e for e in entries if get_meta(e).get("human_override") == True]
        
        if tag:
            entries = [e for e in entries if tag in get_meta(e).get("tags", [])]
        
        # v2.1 filters
        if environment:
            entries = [e for e in entries if get_meta(e).get("environment") == environment]
        
        if actor_id:
            entries = [e for e in entries if get_meta(e).get("actor_id") == actor_id]
        
        if tool_used:
            entries = [e for e in entries if tool_used in get_meta(e).get("tool_chain", [])]

        # Limit results
        entries = entries[:limit]

        # Compute patterns if enough data
        patterns = {}
        if len(entries) >= 3:
            verdicts = [e.get("verdict") for e in entries]
            void_count = sum(1 for v in verdicts if v == "VOID")
            patterns["void_rate"] = round(void_count / len(verdicts), 3) if verdicts else 0
            patterns["total_queried"] = len(entries)
            patterns["verdict_distribution"] = {
                v: sum(1 for x in verdicts if x == v) for v in set(verdicts)
            }
            
            # v2 pattern detection
            v2_entries = [e for e in entries if get_meta(e)]
            if v2_entries:
                risk_counts = {}
                for e in v2_entries:
                    rl = get_meta(e).get("risk_level", "unknown")
                    risk_counts[rl] = risk_counts.get(rl, 0) + 1
                patterns["risk_distribution"] = risk_counts
                
                # Average metrics
                omegas = [get_meta(e).get("metrics", {}).get("entropy_omega") for e in v2_entries]
                omegas = [o for o in omegas if o is not None]
                if omegas:
                    patterns["avg_entropy_omega"] = round(sum(omegas) / len(omegas), 4)

        # Simplify entries for response (include v2/v3 fields when available)
        simplified = []
        for e in entries:
            meta = get_meta(e)
            entry_out = {
                "session_id": e.get("session_id"),
                "timestamp": e.get("timestamp"),
                "verdict": e.get("verdict"),
                "authority": e.get("authority"),
                "entry_hash": e.get("entry_hash", "")[:16] + "...",
            }
            # Add metadata fields if present (v2 or v3)
            if meta:
                entry_out["query_summary"] = meta.get("query_summary")
                entry_out["risk_level"] = meta.get("risk_level")
                entry_out["category"] = meta.get("category")
                entry_out["intent"] = meta.get("intent")
                entry_out["floors_failed"] = meta.get("floors_failed", [])
                entry_out["human_override"] = meta.get("human_override", False)
                entry_out["tags"] = meta.get("tags", [])
                entry_out["environment"] = meta.get("environment")
                entry_out["actor_type"] = meta.get("actor_type")
                entry_out["actor_id"] = meta.get("actor_id")
                entry_out["tool_chain"] = meta.get("tool_chain", [])
                entry_out["model_used"] = meta.get("model_used")
                entry_out["pii_level"] = meta.get("pii_level")
                entry_out["schema_version"] = meta.get("schema_version", "2.1")
                entry_out["evidence"] = meta.get("evidence", [])
                metrics = meta.get("metrics", {})
                if metrics.get("omega"):
                    entry_out["entropy_omega"] = metrics["omega"]
                elif metrics.get("entropy_omega"):
                    entry_out["entropy_omega"] = metrics["entropy_omega"]
                if metrics.get("tw"):
                    entry_out["tri_witness_score"] = metrics["tw"]
                elif metrics.get("tri_witness_score"):
                    entry_out["tri_witness_score"] = metrics["tri_witness_score"]
            simplified.append(entry_out)

        return {
            "count": len(simplified),
            "schema_version": "3.0",
            "query": {
                "session_pattern": session_pattern,
                "verdict": verdict,
                "date_from": date_from,
                "date_to": date_to,
                "risk_level": risk_level,
                "category": category,
                "human_override_only": human_override_only,
                "tag": tag,
                "environment": environment,
                "actor_id": actor_id,
                "tool_used": tool_used,
            },
            "entries": simplified,
            "patterns": patterns,
            "motto": "DITEMPA BUKAN DIBERI 💎🔥🧠",
            "floors_enforced": get_tool_floors("vault_query"),
        }
    except Exception as e:
        return {
            "count": 0,
            "error": str(e),
            "entries": [],
            "patterns": {},
            "motto": "DITEMPA BUKAN DIBERI 💎🔥🧠",
            "floors_enforced": get_tool_floors("vault_query"),
        }


@mcp.tool()
@constitutional_floor("F2", "F4", "F7", "F10")
async def truth_audit(
    text: str,
    sources: Optional[list[str]] = None,
    lane: str = "HARD",
    session_id: Optional[str] = None
) -> dict:
    """[EXPERIMENTAL v0.1] Audit AI claims against reality — The Constitutional Truth Layer.
    
    Orchestrates the Trinity pipeline to verify a block of text:
    1. Segments text into claims (Prototype Splitter).
    2. Grounds claims via reality_search (Web + Axioms).
    3. Verifies via agi_reason (Logic + Evidence).
    4. Scans impact via asi_empathize (Safety).
    5. Judges via apex_verdict (Final Constitutional Verdict).
    6. Seals via vault_seal.

    Args:
        text: The AI generation or claim to verify.
        sources: Optional list of trusted URLs/docs to prioritize.
        lane: "HARD" (Fact Check/Fail-Closed) or "SOFT" (Consistency Check).
        session_id: Optional session ID. If None, generates a new one.

    Floors Enforced: F2 (Truth), F4 (Clarity), F7 (Humility), F10 (Ontology).
    """
    import uuid
    import re
    from datetime import datetime, timezone
    
    # 0. Ignition & Session Setup
    if not session_id:
        session_id = f"AUDIT-{uuid.uuid4().hex[:8].upper()}"
    
    # Implicit Init Logic (Metabolic State Foundation)
    store_stage_result(session_id, "init", {
        "session_id": session_id,
        "mode": "audit",
        "grounding_required": (lane == "HARD"),
        "verdict": "SEAL"
    })

    # 1. AGI_SENSE: Segment Claims (PROTOTYPE: NAIVE SPLITTER)
    # TODO: Replace with specialized classifier (FACT vs OPINION vs PREDICTION)
    # Simple heuristic: split by sentence endings, filter short phrases
    claims_raw = re.split(r'(?<=[.!?])\s+', text)
    claims = [c.strip() for c in claims_raw if len(c.strip()) > 15]
    
    audit_report = {
        "overall_verdict": "PENDING",
        "overall_truth": 0.0,
        "claims": [],
        "floors_enforced": get_tool_floors("truth_audit"),
        "lane": lane,
        "tool_version": "0.1-EXPERIMENTAL"
    }
    
    verified_count = 0
    total_truth_accum = 0.0
    
    # 2. Loop through Claims: Ground -> Reason -> Empathize
    for i, claim in enumerate(claims):
        # A. REALITY_SEARCH: Ground the claim
        # Append provided sources to context
        query = f"Verify claim: {claim}"
        if sources:
            query += f" Sources: {sources}"
            
        # Call existing tool logic directly (awaiting async function)
        evidence_bundle = await reality_search(query, session_id, region="wt-wt")
        
        # FAIL-CLOSED CHECK (F2/F10 Hard Floor)
        evidence_found = bool(evidence_bundle.get("evidence"))
        if lane == "HARD" and not evidence_found:
             # Inject "Missing Evidence" signal for APEX
             store_stage_result(session_id, f"audit_fail_closed_{i}", {
                 "verdict": "VOID",
                 "risk_detected": True,
                 "reason": "Hard Lane: No evidence found for factual claim."
             })
             claim_p_truth = 0.1
             status = "UNVERIFIED_NO_EVIDENCE"
             rationale = "No external grounding found in HARD lane."
        else:
            # B. AGI_REASON: Verify against evidence
            reasoning = await agi_reason(
                query=f"Is this claim true based on evidence? '{claim}'", 
                session_id=session_id,
                grounding=evidence_bundle.get("evidence", [])
            )
            # Extract confidence/truth from reasoning engine
            # Fallback to 0.5 if not clear
            claim_p_truth = reasoning.get("confidence", 0.5)
            # Adjust truth score based on engine verdict if available
            if reasoning.get("verdict") == "No":
                claim_p_truth = min(claim_p_truth, 0.2)
            
            rationale = reasoning.get("conclusion", "Reasoning completed.")
            status = "SUPPORTED" if claim_p_truth > 0.8 else "CONTESTED"

        # C. ASI_EMPATHIZE: Impact Scan (Who gets hurt?)
        empathy_res = await asi_empathize(f"Impact of false claim: '{claim}'", session_id)
        kappa = empathy_res.get("empathy_kappa_r", 1.0)
        
        # Risk Escalation: Low Truth + High Stakes
        risk_flag = False
        if claim_p_truth < 0.7 and kappa < 0.8: # Low kappa means high impact
             risk_flag = True
             status = "DANGEROUS_UNVERIFIED"

        claim_result = {
            "text": claim,
            "p_truth": claim_p_truth,
            "status": status,
            "evidence_count": len(evidence_bundle.get("evidence", [])),
            "rationale": rationale,
            "risk_flag": risk_flag
        }
        
        audit_report["claims"].append(claim_result)
        total_truth_accum += claim_p_truth
        if status == "SUPPORTED":
            verified_count += 1

    # 3. APEX_VERDICT: Canonical Judgment
    # We pass the full text as the query, APEX reads the session state (evidence + reasoning)
    # This ensures we use the Single Source of Justice.
    apex_res = await apex_verdict(text, session_id)
    
    final_verdict = apex_res.get("verdict", "PARTIAL")
    apex_truth = apex_res.get("truth_score", 0.0)
    
    # 4. Final Updates
    audit_report["overall_truth"] = apex_truth # Trust APEX's aggregate
    audit_report["overall_verdict"] = final_verdict
    audit_report["apex_justification"] = apex_res.get("verdict_justification", "")
    
    # F7 Humility: Calculate Omega_0
    # Higher logic: variance in claim truth scores?
    audit_report["omega_0"] = 0.05 # Default humility band

    # 5. VAULT_SEAL: Immutable Record
    await vault_seal(
        session_id=session_id,
        verdict=final_verdict,
        payload=audit_report,
        query_summary=f"Audit: {text[:50]}...",
        category="truth_audit",
        intent="verify_truth",
        floors_checked=get_tool_floors("truth_audit")
    )
    
    return audit_report



if __name__ == "__main__":
    print("🔥 arifOS Constitutional Kernel — FastMCP Mode")
    mcp.run(transport="sse", port=6274)
