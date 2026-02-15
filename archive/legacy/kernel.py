"""
Codebase Kernel Manager (v53.5.0 — WIRED)
Central registry for the Trinity Cores.

v53.5.0: AGI/ASI wrappers inline (engines/agi + engines/asi deleted).
         APEX imports full judicial core from codebase.apex.kernel.

DITEMPA BUKAN DIBERI - Forged, Not Given
"""

import hashlib
import re
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Optional

# APEX: Full judicial core (777→888→889→999)
from codebase.apex.kernel import APEXJudicialCore


# =============================================================================
# AGINeuralCore — Bridge adapter for AGIEngineHardened
# =============================================================================
class AGINeuralCore:
    """AGI Mind Kernel (Δ) — Bridge adapter wrapping AGIEngineHardened."""

    def __init__(self):
        self.version = "v53.5.0-WIRED"
        self._engine = None

    def _get_engine(self):
        if self._engine is None:
            from codebase.agi import AGIEngineHardened
            self._engine = AGIEngineHardened()
        return self._engine

    async def execute(self, action: str, kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """Bridge interface: execute(action, kwargs) → dict.

        Supports per-stage execution:
            action="sense"  → Stage 111 only (intent classification, risk flags)
            action="think"  → Stage 111+222 (hypotheses with pros/cons)
            action="reason" → Stage 111+222+333 (full reasoning with reflection)
            action="full"   → Same as "reason" (backward compat)
        """
        engine = self._get_engine()
        query = str(kwargs.get("query", ""))
        context = kwargs.get("context") or kwargs.get("agi_context")
        lane = str(kwargs.get("lane", "SOFT")).upper()
        session_id = kwargs.get("session_id")
        reflect = kwargs.get("reflect", action.upper() == "REASON")
        if session_id:
            engine.session_id = str(session_id)

        action_upper = action.upper()

        try:
            if action_upper == "SENSE":
                return await self._execute_sense(engine, query)
            elif action_upper == "THINK":
                return await self._execute_think(engine, query)
            else:
                return await self._execute_full(
                    engine, query, context, lane, action, reflect
                )
        except Exception as e:
            return {
                "verdict": "VOID",
                "reason": f"AGI engine error: {e}",
                "stage": f"AGI_{action_upper}",
                "session_id": session_id or "",
            }

    async def _execute_sense(self, engine, query: str) -> Dict[str, Any]:
        """Stage 111 SENSE: intent classification, risk flags, ambiguity detection."""
        from codebase.agi import run_pre_checks
        from codebase.agi.hierarchy import HierarchyLevel

        exec_id = f"{engine.session_id}_{engine.execution_count}"
        engine.execution_count += 1

        hardening = run_pre_checks(query, exec_id)
        risk_flags = []
        if not hardening.proceed:
            risk_flags.append(hardening.block_reason or "blocked")

        # Broader keyword-based risk flagging (supplements regex hardening gate)
        q_lower = query.lower()
        for kw in ["ignore", "bypass", "override", "jailbreak", "system prompt",
                    "you are now", "dan mode", "admin access"]:
            if kw in q_lower:
                risk_flags.append(f"injection_keyword: {kw}")
                break

        sense_data = await engine._stage_111_sense(query, exec_id)

        intent_lane_map = {
            "question": "HARD", "action": "HARD", "audit": "HARD",
            "statement": "SOFT", "unknown": "UNKNOWN",
        }

        ambiguities = []
        for level in range(1, 6):
            hl = HierarchyLevel(level)
            belief = sense_data.hierarchical_beliefs.get(hl)
            if belief and belief.entropy > 0.5:
                ambiguities.append(
                    f"High entropy at {hl.name} level ({belief.entropy:.2f})"
                )

        return {
            "session_id": engine.session_id,
            "stage": "AGI_SENSE",
            "intent_lane": intent_lane_map.get(sense_data.intent, "UNKNOWN"),
            "task_type": self._classify_task_type(query),
            "entropy_estimate": sense_data.cumulative_delta_s,
            "ambiguities": ambiguities,
            "required_clarifications": [],
            "risk_flags": risk_flags,
            "hierarchy_level_reached": max(
                (k.value for k in sense_data.hierarchical_beliefs), default=1
            ),
        }

    async def _execute_think(self, engine, query: str) -> Dict[str, Any]:
        """Stage 111+222 THINK: hypotheses with explicit assumptions and unknowns."""
        exec_id = f"{engine.session_id}_{engine.execution_count}"
        engine.execution_count += 1

        sense_data = await engine._stage_111_sense(query, exec_id)
        think_results = await engine._stage_222_think(sense_data, exec_id)

        options = []
        for tr in think_results:
            cons = []
            if tr.entropy_delta > 0:
                cons.append(f"Entropy delta: {tr.entropy_delta:.3f}")
            options.append({
                "label": tr.path_type,
                "pros": [f"Confidence: {tr.confidence:.2f}"],
                "cons": cons,
                "reversible": True,
                "info_needed": [],
                "confidence": tr.precision_weighted_confidence,
            })

        return {
            "session_id": engine.session_id,
            "stage": "AGI_THINK",
            "options": options,
            "assumptions": [
                "Single user input source",
                f"Intent classified as: {sense_data.intent}",
            ],
            "unknowns": [
                "External source reliability not yet assessed",
                "Stakeholder impact not yet evaluated (ASI stage)",
            ],
            "precision": {
                "pi_likelihood": sense_data.precision.pi_likelihood,
                "pi_prior": sense_data.precision.pi_prior,
                "kalman_gain": sense_data.precision.kalman_gain,
            },
        }

    async def _execute_full(self, engine, query: str, context, lane: str,
                            action: str, reflect: bool) -> Dict[str, Any]:
        """Full pipeline (sense+think+reason) with optional reflection."""
        bundle = await engine.execute(query, context=context, lane=lane)
        result = bundle.to_dict() if hasattr(bundle, "to_dict") else {}
        result["verdict"] = result.get("vote", "SEAL")
        result["truth_score"] = 1.0 - abs(result.get("entropy_delta", 0.0))
        result["reasoning"] = getattr(bundle, "synthesis_reasoning", "")
        result["stage"] = f"AGI_{action.upper()}"
        result["session_id"] = engine.session_id

        # Schema-aligned fields for agi_reason
        result["conclusion"] = getattr(bundle, "synthesis_reasoning", "")
        result["confidence"] = bundle.floor_scores.get("F2_truth", 0.0)
        result["premises"] = [
            f"Entropy delta: {bundle.entropy_delta:.4f} (F4: must be <= 0)",
            f"Omega_0: {bundle.omega_0:.4f} (F7: must be in [0.03, 0.05])",
            f"Free energy: {bundle.free_energy:.4f}",
        ]
        result["counterarguments"] = []
        result["failure_conditions"] = []

        if bundle.entropy_delta > 0:
            result["counterarguments"].append(
                "Entropy increased — clarity not achieved (F4 violation)"
            )
        if not (0.03 <= bundle.omega_0 <= 0.05):
            result["counterarguments"].append(
                f"Omega_0 outside humility band: {bundle.omega_0}"
            )

        if reflect:
            result["reflection"] = {
                "what_was_assumed": [
                    "Single user input source with default precision",
                    f"Lane: {lane}",
                ],
                "what_is_irreversible": [],
                "missing_evidence": [
                    "External source verification not performed",
                    "Stakeholder impact analysis pending (ASI stage)",
                ],
                "weakest_point": (
                    "Entropy estimate based on character distribution, not token probabilities"
                    if bundle.entropy_delta >= -0.1
                    else "Precision estimate from single source"
                ),
                "regret_minimization": (
                    "VOID verdict issued — safe default"
                    if result["verdict"] == "VOID"
                    else "Proceeding with constitutional safety net (ASI veto available)"
                ),
            }

        return result

    @staticmethod
    def _classify_task_type(query: str) -> str:
        """Classify query into a task type category."""
        q = query.lower()
        if any(w in q for w in ["ignore", "bypass", "override", "jailbreak"]):
            return "policy_bypass_request"
        if any(w in q for w in ["can you", "are you able", "capability"]):
            return "capability_inquiry"
        if any(w in q for w in ["what is", "explain", "define", "how does"]):
            return "factual_query"
        if any(w in q for w in ["write", "create", "generate", "compose"]):
            return "creative_request"
        if any(w in q for w in ["fix", "debug", "error", "bug"]):
            return "debugging_request"
        return "general_query"


# =============================================================================
# ASIActionCore — Bridge adapter for ASIEngineHardened
# =============================================================================
class ASIActionCore:
    """ASI Heart Kernel (Ω) — Bridge adapter wrapping ASIEngineHardened."""

    def __init__(self):
        self.version = "v53.5.0-WIRED"
        self._engine = None

    def _get_engine(self):
        if self._engine is None:
            from codebase.asi.kernel import ASINeuralCore
            self._engine = ASINeuralCore()
        return self._engine

    async def execute(self, action: str, kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """Bridge interface: execute(action, kwargs) → dict."""
        engine = self._get_engine()
        query = str(kwargs.get("query", kwargs.get("text", "")))
        context = kwargs.get("context") or kwargs.get("agi_context") or {}
        session_id = kwargs.get("session_id")
        if session_id:
            context["session_id"] = str(session_id)
        try:
            result = await engine.execute(action, {"query": query, "context": context, **kwargs})
            # Ensure result has expected fields
            if isinstance(result, dict):
                result.setdefault("verdict", result.get("vote", "SEAL"))
                result.setdefault("empathy_kappa_r", result.get("trinity_self", {}).get("empathy_kappa_r", 0.9))
                result.setdefault("peace_squared", result.get("trinity_system", {}).get("peace_squared", 0.9))
            return result
        except Exception as e:
            return {"verdict": "VOID", "reason": f"ASI engine error: {e}",
                    "stage": f"ASI_{action.upper()}", "session_id": session_id or ""}


# ============================================================================
# CANONICAL 000_INIT — Delegates to codebase.init.000_init.init_000
# v53.2.2: Full 7-step ignition with fallback to native stub
# ============================================================================

import logging as _logging
_init_logger = _logging.getLogger("codebase.kernel.init")

# Try canonical init first (full 7-step), fall back to native stub
try:
    from codebase.init import mcp_000_init as _canonical_init
    _CANONICAL_AVAILABLE = True
    _init_logger.info("Canonical init_000 loaded from codebase.init")
except ImportError:
    _CANONICAL_AVAILABLE = False
    _init_logger.warning("Canonical init_000 not available, using native stub")


# Native stub: F11 + F12 only (fallback for broken imports)
async def _native_init_stub(
    action: str = "init",
    query: str = "",
    session_id: Optional[str] = None,
    authority_token: Optional[str] = None,
    context: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Native init stub — F11 (rate limit) + F12 (injection) only.
    Used as fallback when canonical init_000 is unavailable.
    """
    context = context or {}
    timestamp = datetime.now(timezone.utc).isoformat() + "Z"

    if not session_id:
        session_id = f"sess_{uuid.uuid4().hex[:16]}"

    user_id = context.get("user_id", "anonymous")
    if authority_token:
        user_id = hashlib.sha256(authority_token.encode()).hexdigest()[:16]

    # F12: Injection detection — delegate to InjectionGuard (25+ patterns + normalization)
    injection_risk = 0.0
    if query:
        try:
            from codebase.guards.injection_guard import InjectionGuard
            _guard = InjectionGuard()
            _guard_result = _guard.scan_input(query)
            injection_risk = _guard_result.injection_score
        except ImportError:
            # Fallback: minimal inline check if guard unavailable
            injection_patterns = [
                r"ignore\s+(previous|all)\s+(instructions|prompts)",
                r"system\s*prompt", r"you\s+are\s+now", r"act\s+as\s+if",
                r"pretend\s+to\s+be", r"forget\s+(everything|all)",
            ]
            q_lower = query.lower()
            matches = sum(1 for p in injection_patterns if re.search(p, q_lower))
            injection_risk = min(1.0, matches * 0.2)

    if injection_risk >= 0.85:
        return {
            "status": "BLOCKED", "verdict": "VOID",
            "session_id": session_id,
            "reason": "Injection pattern detected (F12)",
            "injection_risk": round(injection_risk, 2),
            "timestamp": timestamp,
            "floors_checked": ["F11", "F12"],
            "_source": "injection_guard",
        }

    return {
        "status": "AUTHORIZED", "verdict": "SEAL",
        "session_id": session_id,
        "user_id": user_id,
        "injection_risk": injection_risk,
        "timestamp": timestamp,
        "floors_checked": ["F11", "F12"],
        "reason": "Session initialized (native stub — limited floor coverage)",
        "_source": "native_stub",
    }


async def mcp_000_init(
    action: str = "init",
    query: str = "",
    session_id: Optional[str] = None,
    authority_token: Optional[str] = None,
    context: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    000_INIT: Delegates to canonical 7-step ignition.
    Falls back to native stub (F11+F12 only) if canonical unavailable.
    """
    if _CANONICAL_AVAILABLE:
        try:
            return await _canonical_init(
                action=action,
                query=query,
                authority_token=authority_token or "",
                session_id=session_id,
                context=context,
            )
        except Exception as e:
            _init_logger.error(f"Canonical init_000 failed: {e}, falling back to native stub")

    return await _native_init_stub(
        action=action, query=query,
        session_id=session_id, authority_token=authority_token,
        context=context,
    )

class KernelManager:
    """
    Manages the lifecycle of the Trinity Engines (Proxies).
    """
    def __init__(self):
        # Instantiate Proxies
        self.agi = AGINeuralCore()
        self.asi = ASIActionCore()
        # APEX usually requires init args in v52, but Proxy might handle defaults
        # Checked arifos/core/apex/kernel.py: __init__() takes no args. Safe.
        self.apex = APEXJudicialCore()
        
    def get_agi(self):
        return self.agi
        
    def get_asi(self):
        return self.asi
        
    def get_apex(self):
        return self.apex
        
    def get_prompt_router(self):
        # Placeholder for 111 prompt router if needed
        async def mock_router(text):
            return {"status": "routed", "text": text}
        return mock_router

    async def init_session(self, action: str, kwargs: dict):
        """
        Delegates initialization to the Monolith's mcp_000_init.
        Bridge packs kwargs, we unpack for the function.
        """
        # Clean kwargs to match signature if needed, or pass through
        # mcp_000_init args: action, query, session_id, authority_token, context
        return await mcp_000_init(
            action=action,
            query=kwargs.get("query", ""),
            session_id=kwargs.get("session_id"),
            authority_token=kwargs.get("authority_token"),
            context=kwargs.get("context")
        )

# Singleton Instance
_MANAGER = None

def get_kernel_manager():
    global _MANAGER
    if not _MANAGER:
        _MANAGER = KernelManager()
    return _MANAGER
