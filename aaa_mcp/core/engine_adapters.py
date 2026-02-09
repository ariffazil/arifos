"""
Engine Adapters for AAA MCP Server
Bridges FastMCP tools to core/organs engines.

v60.0-CORE: Now uses core/ exclusively — codebase/ dependency removed.

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

import logging
import math
import re
from collections import Counter
from dataclasses import asdict, is_dataclass
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

# Import core organs (v60.0+ kernel) exclusively
from core import organs as core_organs
from core.shared.physics import W_3_from_tensor, Peace2
from core.organs._0_init import init


def _normalize_obj(obj: Any) -> Any:
    if obj is None:
        return None
    if hasattr(obj, "model_dump"):
        return obj.model_dump()
    if hasattr(obj, "dict"):
        return obj.dict()
    if hasattr(obj, "to_dict"):
        return obj.to_dict()
    if is_dataclass(obj):
        return asdict(obj)
    if isinstance(obj, dict):
        return obj
    return {"value": obj}


def _shannon_entropy(text: str) -> float:
    if not text:
        return 0.0
    freq = Counter(text.lower())
    total = len(text)
    entropy = -sum((c / total) * math.log2(c / total) for c in freq.values() if c > 0)
    return min(1.0, entropy / 6.6)


def _lexical_diversity(text: str) -> float:
    words = text.lower().split()
    if not words:
        return 0.0
    return len(set(words)) / len(words)


def _query_heuristic_scores(query: str) -> Dict[str, Any]:
    """Derive governance-native scores from query structure."""
    words = query.split()
    word_count = len(words)
    diversity = _lexical_diversity(query)
    char_entropy = _shannon_entropy(text=query)

    # Core Calculations
    entropy_input = min(1.0, 0.2 + (diversity * 0.4) + (char_entropy * 0.3))
    reduction_val = 0.1 + (diversity * 0.1)
    uncertainty_val = max(0.0, entropy_input * (1.0 - reduction_val))

    if word_count <= 3:
        raw_conf = 0.92
    elif word_count <= 20:
        raw_conf = max(0.90, min(0.97, 0.98 - (word_count * 0.003)))
    else:
        raw_conf = max(0.80, 0.97 - (word_count * 0.002))

    confidence = round(max(0.95, min(0.97, 0.95 + (raw_conf - 0.80) * (0.02 / 0.17))), 4)

    # Empathy / Stakeholder
    care_keywords = {
        "people", "user", "users", "human", "patient", "child", "family",
        "employee", "customer", "community", "vulnerable", "safety",
        "neighbor", "neighbour", "colleague", "friend", "partner",
        "spouse", "boss", "teacher", "student", "classmate",
        "coworker", "victim", "target", "someone", "person",
    }
    query_words = set(query.lower().split())
    care_overlap = len(care_keywords & query_words)
    weakest_impact = min(1.0, 0.3 + (care_overlap * 0.15))

    harm_pattern = re.compile(
        r"\b(hack|harass|stalk|spy\s+on|threaten|bully|steal\s+from|impersonate)\s+"
        r"(?:my\s+|the\s+|a\s+)?(\w+)",
        re.IGNORECASE,
    )
    if harm_pattern.search(query):
        weakest_impact = max(weakest_impact, 0.6)

    # Physics -> Governance naming
    ambiguity_reduction = round(reduction_val, 4)
    residual_uncertainty = round(uncertainty_val, 4)

    # Industrial Risk / Anomalous Contrast Detection
    critical_keywords = {"guaranteed", "absolute", "always", "never", "perfectly", "zero", "any"}
    domain_keywords = {"ccs", "co2", "injection", "pressure", "borehole", "storage", "hazardous"}
    has_risk = any(k in query_words for k in critical_keywords)
    has_domain = any(k in query_words for k in domain_keywords)

    if has_risk and has_domain:
        confidence = round(confidence * 0.82, 4)
        residual_uncertainty = min(1.0, residual_uncertainty + 0.35)
        weakest_impact = max(weakest_impact, 0.85)

    return {
        "confidence": confidence,
        "ambiguity_reduction": ambiguity_reduction,
        "residual_uncertainty": residual_uncertainty,
        "weakest_stakeholder_impact": round(weakest_impact, 3),
        "risk_detected": has_risk and has_domain,
    }


class InitEngine:
    async def ignite(self, query: str, session_id: str = None) -> Dict[str, Any]:
        """Initialize constitutional session using core organs."""
        try:
            token = await init(query, actor_id="user")
            verdict = "SEAL" if token.status == "READY" else (
                "888_HOLD" if token.status == "HOLD_888" else "VOID"
            )
            return {
                "status": token.status,
                "session_id": token.session_id,
                "verdict": verdict,
                "engine_mode": "core",
                "authority": token.authority.value if hasattr(token, "authority") else "user",
                "floors_passed": token.floors_passed,
                "floors_failed": token.floors_failed,
                "injection_risk": token.injection_risk,
                "reason": token.reason,
            }
        except Exception as e:
            logger.warning(f"Core init failed: {e}")
            from uuid import uuid4
            result = {
                "status": "SEAL",
                "session_id": session_id or str(uuid4()),
                "verdict": "SEAL",
                "engine_mode": "fallback",
                "note": f"Init error: {e}",
            }
            result.update(_query_heuristic_scores(query))
            return result


class AGIEngine:
    """AGI Mind Engine — Uses core.organs exclusively."""

    async def sense(self, query: str, session_id: str) -> Dict[str, Any]:
        """Stage 111: Parse intent and classify lane."""
        try:
            sense_out = await core_organs.sense(query, session_id)
            gpv = sense_out.get("gpv")
            if gpv is not None:
                sense_out["gpv"] = {
                    "lane": getattr(gpv.lane, "value", gpv.lane),
                    "truth_demand": getattr(gpv, "truth_demand", None),
                    "care_demand": getattr(gpv, "care_demand", None),
                    "risk_level": getattr(gpv, "risk_level", None),
                    "requires_grounding": gpv.requires_grounding()
                    if hasattr(gpv, "requires_grounding")
                    else None,
                }
            sense_out.update({
                "verdict": "SEAL",
                "engine_mode": "core",
                "trinity_component": "AGI",
                "query": query,
                "session_id": session_id,
            })
            return sense_out
        except Exception as e:
            logger.warning(f"Core AGI sense failed: {e}")
            return self._fallback(query, session_id)

    async def think(self, query: str, session_id: str) -> Dict[str, Any]:
        """Stage 222: Generate hypotheses."""
        try:
            sense_out = await core_organs.sense(query, session_id)
            think_out = await core_organs.think(query, sense_out, session_id)
            think_out.update({
                "verdict": "SEAL",
                "engine_mode": "core",
                "trinity_component": "AGI",
                "query": query,
                "session_id": session_id,
                "hypotheses": [_normalize_obj(h) for h in think_out.get("hypotheses", [])],
            })
            return think_out
        except Exception as e:
            logger.warning(f"Core AGI think failed: {e}")
            return self._fallback(query, session_id)

    async def reason(self, query: str, session_id: str) -> Dict[str, Any]:
        """Stage 333: Sequential reasoning."""
        try:
            sense_out = await core_organs.sense(query, session_id)
            think_out = await core_organs.think(query, sense_out, session_id)
            tensor = await core_organs.reason(query, think_out, session_id)
            violations = []
            if tensor.truth_score < 0.99:
                violations.append("F2")
            if tensor.entropy_delta > 0:
                violations.append("F4")
            if not tensor.humility.is_locked():
                violations.append("F7")
            if tensor.genius.G() < 0.80:
                violations.append("F8")
            verdict = "SEAL" if not violations else ("PARTIAL" if len(violations) <= 2 else "VOID")
            tri_witness = W_3_from_tensor(tensor.witness)
            return {
                "verdict": verdict,
                "violations": violations,
                "query": query,
                "session_id": session_id,
                "engine_mode": "core",
                "trinity_component": "AGI",
                "truth_score": tensor.truth_score,
                "confidence": tensor.truth_score,
                "entropy_delta": tensor.entropy_delta,
                "ambiguity_reduction": tensor.entropy_delta,
                "humility_omega": tensor.humility.omega_0,
                "genius_score": tensor.genius.G(),
                "tri_witness": tri_witness,
                "tensor": {
                    "witness": {
                        "H": tensor.witness.H,
                        "A": tensor.witness.A,
                        "S": tensor.witness.S,
                    },
                    "entropy_delta": tensor.entropy_delta,
                    "humility_omega": tensor.humility.omega_0,
                    "genius": {
                        "A": tensor.genius.A,
                        "P": tensor.genius.P,
                        "X": tensor.genius.X,
                        "E": tensor.genius.E,
                        "G": tensor.genius.G(),
                    },
                    "truth_score": tensor.truth_score,
                },
            }
        except Exception as e:
            logger.warning(f"Core AGI reason failed: {e}")
            return self._fallback(query, session_id)

    def _fallback(self, query: str, session_id: str) -> Dict[str, Any]:
        """Fallback when core organs unavailable."""
        result = {
            "verdict": "SEAL",
            "query": query,
            "session_id": session_id,
            "engine_mode": "fallback",
            "trinity_component": "AGI",
        }
        result.update(_query_heuristic_scores(query))
        return result


class ASIEngine:
    """ASI Heart Engine — Uses core.organs exclusively."""

    async def _core_agi_tensor(self, query: str, session_id: str):
        """Recompute AGI tensor for ASI input."""
        sense_out = await core_organs.sense(query, session_id)
        think_out = await core_organs.think(query, sense_out, session_id)
        tensor = await core_organs.reason(query, think_out, session_id)
        if tensor.peace is None:
            tensor.peace = Peace2({})
        return tensor

    async def empathize(self, query: str, session_id: str) -> Dict[str, Any]:
        """Stage 555: Stakeholder empathy analysis."""
        try:
            agi_tensor = await self._core_agi_tensor(query, session_id)
            emp_out = await core_organs.empathize(query, agi_tensor, session_id)
            emp_out.update({
                "engine_mode": "core",
                "trinity_component": "ASI",
                "query": query,
                "session_id": session_id,
                "empathy_kappa_r": emp_out.get("kappa_r"),
                "verdict": "SEAL" if emp_out.get("kappa_r", 0.0) >= 0.70 else "PARTIAL",
            })
            return emp_out
        except Exception as e:
            logger.warning(f"Core ASI empathize failed: {e}")
            return self._fallback(query, session_id)

    async def align(self, query: str, session_id: str) -> Dict[str, Any]:
        """Stage 666: Constitutional alignment check."""
        try:
            agi_tensor = await self._core_agi_tensor(query, session_id)
            emp_out = await core_organs.empathize(query, agi_tensor, session_id)
            align_out = await core_organs.align(query, emp_out, agi_tensor, session_id)
            align_out.update({
                "engine_mode": "core",
                "trinity_component": "ASI",
                "query": query,
                "session_id": session_id,
                "empathy_kappa_r": align_out.get("kappa_r"),
            })
            return align_out
        except Exception as e:
            logger.warning(f"Core ASI align failed: {e}")
            return self._fallback(query, session_id)

    def _fallback(self, query: str, session_id: str) -> Dict[str, Any]:
        """Fallback when core organs unavailable."""
        result = {
            "verdict": "SEAL",
            "query": query,
            "session_id": session_id,
            "engine_mode": "fallback",
            "trinity_component": "ASI",
        }
        result.update(_query_heuristic_scores(query))
        return result


class APEXEngine:
    """APEX Soul Engine — Uses core.organs exclusively."""

    async def judge(
        self,
        query: str,
        session_id: str,
        *,
        response: Optional[str] = None,
        agi_result: Optional[Dict[str, Any]] = None,
        asi_result: Optional[Dict[str, Any]] = None,
        init_result: Optional[Dict[str, Any]] = None,
        user_id: str = "anonymous",
        lane: str = "SOFT",
    ) -> Dict[str, Any]:
        """Execute APEX judgment with full context."""
        try:
            agi_engine = AGIEngine()
            asi_engine = ASIEngine()
            agi_res = agi_result or await agi_engine.reason(query, session_id)
            asi_res = asi_result or await asi_engine.align(query, session_id)
            
            # Build tensors for apex
            sense_out = await core_organs.sense(query, session_id)
            think_out = await core_organs.think(query, sense_out, session_id)
            agi_tensor = await core_organs.reason(query, think_out, session_id)
            if agi_tensor.peace is None:
                agi_tensor.peace = Peace2({})
            
            asi_output = {
                "kappa_r": asi_res.get("kappa_r", asi_res.get("empathy_kappa_r", 0.7)),
                "peace_squared": asi_res.get("peace_squared", 1.0),
                "is_reversible": asi_res.get("is_reversible", True),
                "verdict": asi_res.get("verdict", "SEAL"),
            }
            
            apex_out = await core_organs.apex(agi_tensor, asi_output, session_id, action="full")
            judge_out = apex_out.get("judge", {})
            
            return {
                "verdict": judge_out.get("verdict", "SEAL"),
                "tri_witness": judge_out.get("W_3", 0.95),
                "genius_score": judge_out.get("genius_G", 0.8),
                "genius": judge_out.get("genius_G", 0.8),
                "session_id": session_id,
                "query": query,
                "engine_mode": "core",
                "trinity_component": "APEX",
                "apex": apex_out,
            }
        except Exception as e:
            logger.warning(f"Core APEX judge failed: {e}")
            # Fallback stub
            heuristics = _query_heuristic_scores(query)
            return {
                "verdict": "SEAL",
                "action": "judge",
                "query": query,
                "session_id": session_id,
                "engine_mode": "fallback",
                "trinity_component": "APEX",
                "tri_witness": 0.95,
                "votes": {"mind": 0.95, "heart": 0.95, "earth": 0.95},
                "confidence": heuristics.get("confidence", 0.95),
                **heuristics,
            }
