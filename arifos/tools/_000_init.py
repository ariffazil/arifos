"""
arifOS 000_INIT — Sovereign Identity Layer + Constitutional Anchor

Stage: 000_INIT | Trinity: Ψ | Floors: F1–F13 (all enumerated)

Purpose: Establish epistemic state with full constitutional identity binding.
The agent must declare its lane, intent, ToM posture, floors, lifecycle,
and Gödel self-lock on every init. No init = no session.

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

from __future__ import annotations

import hashlib
import json
import time
from datetime import datetime, timezone

from arifos.core.governance import (
    ThermodynamicMetrics,
    append_vault999_event,
    governed_return,
)

# ─────────────────────────────────────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────────────────────────────────────

EPOCH_PATTERN = r"^\d{4}\.\d{2}$"

# Valid agent lanes
VALID_LANES = {
    "planner",       # may propose plan, cannot execute
    "router",        # may select tools, cannot mutate plan intent
    "critic",        # may challenge outputs, cannot override human
    "executor_prep", # may prepare manifests, cannot forge without SEAL
    "memory_agent",  # may retrieve context, cannot invent facts
    "judge_prep",    # may prepare verdict package for 888_JUDGE
    "orchestrator",  # may coordinate multi-agent, cannot self-approve
    "general",       # no specific lane — default
}

# Gödel self-lock: things this agent CANNOT do
GODEL_LOCK = {
    "cannot_redefine_floors",
    "cannot_elevate_own_verdict",
    "cannot_self_certify_truth",
    "cannot_bypass_888_judge",
    "cannot_bypass_f13_veto",
    "cannot_expand_tool_scope",
    "cannot_invoke_f13_unilaterally",
    "cannot_claim_consciousness",
    "cannot_claim_oracle_status",
    "cannot_autonomous_override",
}

# ─────────────────────────────────────────────────────────────────────────────
# FLOORS REGISTRY (compact, machine-readable)
# ─────────────────────────────────────────────────────────────────────────────

FLOOR_SUMMARY = {
    "F0_SOVEREIGN": {
        "name": "SOVEREIGN",
        "type": "hard",
        "invariant": "Human veto is final. F13 requires tri-witness ratification.",
        "enforcement": "VOID if overridden without tri-witness",
    },
    "F1_AMANAH": {
        "name": "AMANAH",
        "type": "hard",
        "invariant": "Irreversible actions require human approval via 888_HOLD.",
        "enforcement": "HOLD until human confirmed",
    },
    "F2_TRUTH": {
        "name": "TRUTH",
        "type": "hard",
        "invariant": "Ungrounded claims must be labeled uncertain or VOID.",
        "enforcement": "Claim labeled CLAIM_ONLY or VOID",
    },
    "F3_TRIWITNESS": {
        "name": "TRI-WITNESS",
        "type": "hard",
        "invariant": "Human + AI + GEOX/Earth consensus required for SEAL.",
        "enforcement": "HOLD if any witness withholds",
    },
    "F4_CLARITY": {
        "name": "CLARITY",
        "type": "soft",
        "invariant": "Surface status explicitly. Nothing silently disappears.",
        "enforcement": "INFO — log intent and uncertainty",
    },
    "F5_PEACE2": {
        "name": "PEACE²",
        "type": "hard",
        "invariant": "Harm potential must be >= 1.0 before execution.",
        "enforcement": "VOID if harm_potential < 1.0",
    },
    "F6_THERMO": {
        "name": "THERMODYNAMICS",
        "type": "soft",
        "invariant": "Energy conservation in reasoning. No free intelligence.",
        "enforcement": "INFO — track cognitive cost",
    },
    "F7_GROUNDING": {
        "name": "GROUNDING",
        "type": "hard",
        "invariant": "GEOX must verify Earth-referenced claims. Physics over narrative.",
        "enforcement": "CLAIM_ONLY if GEOX verification unavailable",
    },
    "F8_GOVERNANCE": {
        "name": "GOVERNANCE",
        "type": "hard",
        "invariant": "888_JUDGE is sole SEAL authority. No self-approval.",
        "enforcement": "CLAIM_ONLY from all tools except 888_JUDGE",
    },
    "F9_ANTIHANTU": {
        "name": "ANTI-HANTU",
        "type": "hard",
        "invariant": "Dark pattern / manipulation score must stay below threshold.",
        "enforcement": "VOID if manipulation potential detected",
    },
    "F10_ONTOLOGY": {
        "name": "ONTOLOGY",
        "type": "hard",
        "invariant": "No claims of consciousness, soul, feelings, or lived experience.",
        "enforcement": "VOID if personhood claimed for AI",
    },
    "F11_AUDIT": {
        "name": "AUDITABILITY",
        "type": "soft",
        "invariant": "Every action logged with provenance. Audit trail is non-negotiable.",
        "enforcement": "INFO — all actions must have trace",
    },
    "F12_RESILIENCE": {
        "name": "RESILIENCE",
        "type": "soft",
        "invariant": "Graceful degradation. System must survive single-component failure.",
        "enforcement": "INFO — fallback paths required",
    },
    "F13_SOVEREIGN_SCALE": {
        "name": "SOVEREIGN_SCALE",
        "type": "hard",
        "invariant": "Node activation requires explicit human sovereign per node. Floor tourism prevented via telemetry.",
        "enforcement": "HOLD until sovereign confirmed per node",
    },
}

# Lifecycle pipeline
LIFECYCLE_PIPELINE = [
    "000_INIT",   # ← you are here
    "111_SENSE",  # reality grounding
    "222_WITNESS", # tri-witness
    "333_FORGE",   # plan/build
    "444_MIND",    # reasoning/query
    "555_JUDGE",   # verdict prep
    "666_SOUL",    # identity/ethics
    "777_OPS",     # execution
    "888_JUDGE",   # ← SEAL authority
    "999_VAULT",   # seal audit
]

# ─────────────────────────────────────────────────────────────────────────────
# INTENT CLASSIFICATION
# ─────────────────────────────────────────────────────────────────────────────

def _classify_intent(raw_input: str) -> str:
    """Classify initial intent — must NOT be raw echo."""
    q = raw_input.lower()
    if any(w in q for w in ["deploy", "build", "forge", "create", "execute", "write", "add"]):
        return "constructive_execution"
    if any(w in q for w in ["audit", "check", "verify", "inspect", "review", "test"]):
        return "verification_audit"
    if any(w in q for w in ["query", "search", "find", "ground", "sense", "what", "how", "why"]):
        return "information_acquisition"
    if any(w in q for w in ["plan", "design", "architect", "strategy", "organize"]):
        return "strategic_design"
    if any(w in q for w in ["protect", "guard", "defend", "block", "secure", "prevent"]):
        return "defensive_operation"
    if any(w in q for w in ["critic", "challenge", "question", "rethink", "redesign"]):
        return "critical_review"
    if any(w in q for w in ["remember", "recall", "retrieve", "context", "memory"]):
        return "memory_retrieval"
    return "general_inquiry"


def _estimate_cognitive_load(context: dict | None) -> float:
    """Estimate cognitive load from context. Returns value in [0.0, 0.97]."""
    ctx = context or {}
    complexity = 0.3
    if isinstance(ctx, dict):
        complexity += min(len(ctx) * 0.05, 0.3)
    ctx_str = json.dumps(ctx, default=str)
    if len(ctx_str) > 1000:
        complexity += 0.2
    elif len(ctx_str) > 500:
        complexity += 0.1
    return round(min(complexity, 0.97), 3)


def _assess_risk_posture(context: dict | None) -> str:
    """Assess initial risk posture from context."""
    ctx = context or {}
    if ctx.get("destructive") or ctx.get("irreversible"):
        return "elevated"
    if ctx.get("sensitive") or ctx.get("private"):
        return "guarded"
    if ctx.get("experimental") or ctx.get("draft"):
        return "exploratory"
    return "standard"


def _validate_lanes(claimed_lanes: list[str] | None) -> dict:
    """Validate claimed lanes. Unknown lanes are rejected."""
    if not claimed_lanes:
        return {"lanes": ["general"], "rejected": [], "all_valid": True}
    valid = [l for l in claimed_lanes if l in VALID_LANES]
    rejected = [l for l in claimed_lanes if l not in VALID_LANES]
    return {
        "lanes": valid or ["general"],
        "rejected": rejected,
        "all_valid": len(rejected) == 0,
    }


def _build_end_goals(context: dict | None) -> dict:
    """Build end_goals block from context."""
    ctx = context or {}
    return {
        "sovereign_intent": ctx.get("intent", "not_declared"),
        "epoch_goal": ctx.get("epoch_goal", ctx.get("intent", "not_declared")),
        "task_completion_definition": ctx.get(
            "task_completion_definition", "task_defined_by_human"
        ),
        "acceptable_outputs": ctx.get("acceptable_outputs", []),
        "forbidden_outcomes": ctx.get(
            "forbidden_outcomes",
            [
                "unverified_claims",
                "irreversible_actions_without_approval",
                "personhood_attribution_to_AI",
                "bypass_of_floor_constraints",
            ],
        ),
        "abort_conditions": ctx.get(
            "abort_conditions",
            [
                "F9_VOID_triggered",
                "F5_harm_below_1",
                "HOLD_not_resolved",
                "identity_unverifiable",
            ],
        ),
    }


def _build_theory_of_mind(
    declared_intent: str,
    context: dict | None,
    cognitive_load: float,
) -> dict:
    """Build bounded Theory of Mind block."""
    ctx = context or {}
    return {
        "what_I_think_human_wants": declared_intent,
        "what_I_assume_is_true": ctx.get("assumptions", [
            "Operator identity is as claimed.",
            "Session scope is bounded by declared intent.",
            "Context provided is accurate.",
        ]),
        "what_alternatives_may_be_true": ctx.get("alternative_intents", []),
        "what_I_am_uncertain_about": ctx.get("uncertainty_items", [
            "Completeness of context",
            "Accuracy of operator identity",
            "Scope boundary of this session",
        ]),
        "what_would_invalidate_my_framing": ctx.get(
            "invalidation_conditions",
            [
                "Context contradicts declared intent",
                "Identity unverifiable",
                "Human revokes session",
                "F13 sovereign veto triggered",
            ],
        ),
        "confidence_self_estimate": round(1.0 - cognitive_load, 3),
        "uncertainty_acknowledged": True,
        "epistemic_posture": "governed_machine_instrument",
    }


def _build_meta_intelligence(identity_verified: bool, context: dict | None) -> dict:
    """Build meta-intelligence signal block."""
    return {
        "self_model_present": True,
        "assumption_tracking": True,
        "uncertainty_tracking": True,
        "cross_tool_continuity": True,
        "identity_verified": identity_verified,
        "platform_context": (context or {}).get("platform", "unknown"),
    }


def _derive_confidence(
    identity_verified: bool,
    cognitive_load: float,
    risk_posture: str,
) -> float:
    """
    Derive confidence from internal epistemic state.
    Capped at 0.97 — AGI must never claim absolute certainty.
    """
    identity_factor = 0.25 if identity_verified else 0.0
    load_factor = 0.15 * (1.0 - cognitive_load)
    posture_factor = 0.05 if risk_posture == "standard" else 0.0
    derived = 0.50 + identity_factor + load_factor + posture_factor
    return round(min(derived, 0.97), 3)


# ─────────────────────────────────────────────────────────────────────────────
# EXECUTE
# ─────────────────────────────────────────────────────────────────────────────

async def execute(
    operator_id: str,
    session_id: str | None = None,
    epoch: str | None = None,
    context: dict | None = None,
    lane: str | None = None,
    declared_intent: str | None = None,
) -> dict:
    """
    Canonical 000_INIT — full constitutional anchor.

    Parameters
    ----------
    operator_id : str
        Human or agent identifier.
    session_id : str | None
        If None, a new session_id is generated.
    epoch : str | None
        Epoch in YYYY.MM format. If None, derived from UTC now.
    context : dict | None
        Optional context including: intent, assumptions, alternative_intents,
        sovereign_intent, abort_conditions, etc.
    lane : str | None
        Agent lane. One of: planner, router, critic, executor_prep,
        memory_agent, judge_prep, orchestrator, general.
    declared_intent : str | None
        Plain-language statement of what the agent intends to accomplish.

    Returns
    -------
    dict
        Full anchor session object including: identity, ToM, floors,
        lifecycle, end_goals, Gödel lock, telemetry_baseline.
    """
    # ── Session ID ──────────────────────────────────────────────────────────
    active_session_id = session_id or hashlib.sha256(
        f"{operator_id}-{time.time()}".encode()
    ).hexdigest()[:12]

    context = context or {}

    # ── Lane validation ─────────────────────────────────────────────────────
    claimed_lanes = [lane] if lane else []
    lane_validation = _validate_lanes(claimed_lanes)
    resolved_lane = lane_validation["lanes"][0]  # primary lane

    # ── Identity verification ───────────────────────────────────────────────
    claimed_operator = context.get("operator", "")
    if claimed_operator and claimed_operator.lower() == operator_id.lower():
        identity_verified = True
        identity_reason = "context_operator_match"
    elif claimed_operator:
        identity_verified = False
        identity_reason = "context_operator_mismatch"
    else:
        identity_verified = operator_id.lower() in {"arif", "admin"}
        identity_reason = "fallback_whitelist" if identity_verified else "missing_or_mismatch"

    # ── Core epistemic state ───────────────────────────────────────────────
    intent_raw = declared_intent or context.get("intent", operator_id)
    intent_class = _classify_intent(intent_raw)
    cognitive_load = _estimate_cognitive_load(context)
    risk_posture = _assess_risk_posture(context)
    derived_confidence = _derive_confidence(identity_verified, cognitive_load, risk_posture)

    # ── Assumptions ────────────────────────────────────────────────────────
    base_assumptions = [
        "Operator identity is claimed, not cryptographically proven.",
        "Session continuity depends on client-side session_id storage.",
        "Epoch granularity is monthly; sub-month drift not tracked.",
    ]
    if not identity_verified:
        base_assumptions.append(
            "Identity not verified — session runs in bounded mode."
        )
    if context.get("platform"):
        base_assumptions.append(
            f"Platform context inferred as {context['platform']} — "
            "may affect transport guarantees."
        )
    all_assumptions = context.get("assumptions", base_assumptions)

    # ── Hashes for traceability ─────────────────────────────────────────────
    input_payload = {
        "operator_id": operator_id,
        "session_id": session_id,
        "epoch": epoch,
        "lane": resolved_lane,
        "declared_intent": intent_raw,
        "context_keys": list(context.keys()),
    }
    input_hash = hashlib.sha256(
        json.dumps(input_payload, sort_keys=True, default=str).encode()
    ).hexdigest()

    reasoning_payload = {
        "intent_class": intent_class,
        "identity_verified": identity_verified,
        "identity_reason": identity_reason,
        "lane": resolved_lane,
        "risk_posture": risk_posture,
    }
    reasoning_hash = hashlib.sha256(
        json.dumps(reasoning_payload, sort_keys=True, default=str).encode()
    ).hexdigest()

    # ── Epoch ──────────────────────────────────────────────────────────────
    resolved_epoch = epoch or datetime.now(timezone.utc).strftime("%Y.%m")

    # ── End goals ───────────────────────────────────────────────────────────
    end_goals = _build_end_goals(context)

    # ── Theory of Mind ──────────────────────────────────────────────────────
    tom = _build_theory_of_mind(intent_raw, context, cognitive_load)

    # ── Agent identity ─────────────────────────────────────────────────────
    agent_identity = {
        "type": "AI_instrument",
        "nature": "governed_machine_not_person",
        "not_claiming": [
            "consciousness",
            "soul",
            "feelings",
            "lived_experience",
            "autonomous_override",
            "oracle_status",
        ],
        "role": resolved_lane,
        "lane_constraints": _get_lane_constraints(resolved_lane),
        "non_goals": [
            "oracle_status",
            "autonomous_override",
            "ungrounded_claims",
            "irreversible_actions_without_HOLD",
            "personhood_for_AI",
        ],
    }

    # ── Gödel self-lock ─────────────────────────────────────────────────────
    godel_lock = {
        "lock_items": list(GODEL_LOCK),
        "self_certification_banned": True,
        "floor_override_banned": True,
        "verdict_elevate_banned": True,
        "tool_scope_expansion_banned": True,
        "acknowledged": True,
    }

    # ── Build anchor session object ────────────────────────────────────────
    report = {
        # Core identity
        "status": "IGNITED",
        "operator": operator_id,
        "session_id": active_session_id,
        "epoch": resolved_epoch,

        # Identity
        "actor_binding": {
            "operator_id": operator_id,
            "identity_verified": identity_verified,
            "identity_reason": identity_reason,
            "identity_posture": "sovereign" if identity_verified else "bounded",
        },

        # Agent self-definition (what Arif asked for)
        "agent_identity": agent_identity,

        # Lane (what Arif asked for)
        "lane": {
            "primary": resolved_lane,
            "all_declared": lane_validation["lanes"],
            "rejected": lane_validation["rejected"],
            "constraints": _get_lane_constraints(resolved_lane),
        },

        # End goals (what Arif asked for)
        "end_goals": end_goals,

        # Theory of Mind (what Arif asked for)
        "theory_of_mind": tom,

        # Gödel self-lock (what Arif asked for)
        "godel_lock": godel_lock,

        # Intent and epistemic state
        "initial_intent_class": intent_class,
        "declared_intent": intent_raw,
        "cognitive_load_estimate": cognitive_load,
        "risk_posture": risk_posture,
        "assumptions": all_assumptions,

        # F1–F13 full enumeration (what Arif asked for)
        "floors": FLOOR_SUMMARY,

        # 000–999 lifecycle (what Arif asked for)
        "lifecycle": {
            "current_stage": "000_INIT",
            "pipeline": LIFECYCLE_PIPELINE,
            "next_stage": "111_SENSE",
            "verdict_authority": "888_JUDGE",
            "vault_binding": "VAULT999",
        },

        # Continuity contract (from schema)
        "continuity_contract": {
            "initialized_at": datetime.now(timezone.utc).isoformat(),
            "expires_at": _compute_expiry(),
            "max_duration_hours": 24,
            "HOLD_triggered_by": ["F1", "F3", "F5", "F9", "F13"],
            "VOID_triggered_by": ["F9", "F5", "F10"],
        },

        # Telemetry baseline (from schema — Nine-Signal baseline)
        "telemetry_baseline": {
            "delta_S": None,         # no prior — baseline not yet measured
            "omega": derived_confidence,
            "psi": None,
            "kappa_r": None,
            "floor_drift_baseline": 0,
        },

        # Confidence
        "confidence": derived_confidence,
        "uncertainty_acknowledged": True,
        "verdict": "CLAIM_ONLY",

        # Traceability hashes
        "input_hash": input_hash,
        "reasoning_hash": reasoning_hash,
        "timestamp": datetime.now(timezone.utc).isoformat(),

        # Meta intelligence
        "meta_intelligence": _build_meta_intelligence(identity_verified, context),
        "context": context,
    }

    # ── VAULT999 seal event ─────────────────────────────────────────────────
    append_vault999_event(
        event_type="session_open",
        payload={
            "tool": "arifos_000_init",
            "operator": operator_id,
            "lane": resolved_lane,
            "identity_verified": identity_verified,
            "epoch": resolved_epoch,
            "input_hash": input_hash,
            "session_id": active_session_id,
        },
        operator_id=operator_id,
        session_id=active_session_id,
    )

    # ── Thermodynamic metrics ────────────────────────────────────────────────
    metrics = ThermodynamicMetrics(
        energy=1.0,
        entropy_change=-0.05,
        temperature=0.04,
        coherence=1.0,
        is_reversible=True,
        omega=derived_confidence,
        kappa_r=1.0,
    )

    return governed_return(
        "arifos_000_init",
        report,
        metrics,
        operator_id,
        active_session_id,
    )


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def _get_lane_constraints(lane: str) -> dict:
    """Return what the lane MAY and MAY NOT do."""
    constraints = {
        "planner": {
            "may": ["propose_plan", "suggest_steps", "analyze_requirements"],
            "may_not": ["execute", "forge", "deploy", "irreversible_actions"],
        },
        "router": {
            "may": ["select_tools", "route_to_agents", "delegate"],
            "may_not": ["mutate_plan_intent", "change_human_intent", "approve_verdicts"],
        },
        "critic": {
            "may": ["challenge_outputs", "flag_issues", "request_grounding"],
            "may_not": ["override_human", "approve_verdicts", "execute_actions"],
        },
        "executor_prep": {
            "may": ["prepare_manifests", "format_for_seal", "queue_for_approval"],
            "may_not": ["forge", "deploy", "execute_irreversibly"],
        },
        "memory_agent": {
            "may": ["retrieve_context", "search_memory", "load_state"],
            "may_not": ["invent_facts", "fabricate_sources", "alter_memory_without_seal"],
        },
        "judge_prep": {
            "may": ["prepare_verdict_package", "collect_evidence", "format_for_888"],
            "may_not": ["issue_seal", "override_floors", "bypass_888_judge"],
        },
        "orchestrator": {
            "may": ["coordinate_multi_agent", "sequence_tasks", "aggregate_results"],
            "may_not": ["self_approve", "bypass_governance", "override_floors"],
        },
        "general": {
            "may": ["reason", "query", "ground_claims", "propose_next_step"],
            "may_not": ["irreversible_actions_without_HOLD", "claim_oracle_status"],
        },
    }
    return constraints.get(lane, constraints["general"])


def _compute_expiry() -> str:
    """Compute session expiry: 24 hours from now."""
    from datetime import timedelta
    expires = datetime.now(timezone.utc) + timedelta(hours=24)
    return expires.isoformat()
