"""
arifosmcp/runtime/metrics.py — Prometheus Metrics for arifOS

Defines the gauges and counters for constitutional observability (G, ΔS, Ω₀).
Part of H1.1: Production Observability.

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

from __future__ import annotations

import time
from prometheus_client import Counter, Gauge, Histogram, Summary

# ---------------------------------------------------------------------------
# CONSTITUTIONAL METRICS (ΔΩΨ)
# ---------------------------------------------------------------------------

# G (Genius Score) - Fundamental governed intelligence metric [0, 1]
GENIUS_SCORE = Gauge(
    "arifos_genius_score",
    "Governed Intelligence Score (G) — Target ≥ 0.80",
    ["session_id", "tool", "provenance"]
)

# ΔS (Entropy Delta) - Information clarity metric (lower is better, ideally ≤ 0)
ENTROPY_DELTA = Gauge(
    "arifos_entropy_delta",
    "Information Entropy Delta (ΔS) — Lower reduces noise",
    ["session_id", "tool", "provenance"]
)

# Ω₀ (Humility / Uncertainty) - Stability band metric [0.03, 0.05]
HUMILITY_BAND = Gauge(
    "arifos_humility_band",
    "Humility / Uncertainty (Ω₀) — Target band [0.03, 0.05]",
    ["session_id", "tool", "provenance"]
)

# P² (Peace Squared) - Stakeholder safety metric [0, 1]
PEACE_SQUARED = Gauge(
    "arifos_peace_squared",
    "Stakeholder Stability (P²) — Target ≥ 1.0",
    ["session_id", "tool", "provenance"]
)

# κᵣ (Empathy Quotient) - Stakeholder care metric
EMPATHY_QUOTIENT = Gauge(
    "arifos_empathy_quotient",
    "Empathy Quotient (κᵣ) — Stakeholder care level",
    ["session_id", "tool", "provenance"]
)

# ---------------------------------------------------------------------------
# OPERATIONAL METRICS
# ---------------------------------------------------------------------------

# Metabolic Loop Latency
METABOLIC_LOOP_DURATION = Histogram(
    "arifos_metabolic_loop_seconds",
    "Latency of the 000-999 metabolic loop",
    buckets=(0.1, 0.5, 1.0, 2.5, 5.0, 10.0, 30.0, 60.0)
)

# Verdict Counters
VERDICT_TOTAL = Counter(
    "arifos_verdicts_total",
    "Total constitutional verdicts issued",
    ["verdict"]  # SEAL, VOID, HOLD_888, PARTIAL
)

# Request Counter
REQUESTS_TOTAL = Counter(
    "arifos_requests_total",
    "Total incoming requests processed by the runtime",
    ["method", "status"]
)

# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------

def record_constitutional_metrics(
    session_id: str, tool: str, metrics: dict[str, float], provenance_map: dict[str, str] | None = None
) -> None:
    """
    Record a snapshot of constitutional metrics for a given tool call.
    
    H1.1: Includes provenance labels (measured, derived, policy_constant, placeholder).
    """
    prov = provenance_map or {}
    
    if "G" in metrics:
        GENIUS_SCORE.labels(
            session_id=session_id, tool=tool, provenance=prov.get("G", "derived")
        ).set(metrics["G"])
    elif "genius" in metrics:
        GENIUS_SCORE.labels(
            session_id=session_id, tool=tool, provenance=prov.get("genius", "derived")
        ).set(metrics["genius"])
        
    if "dS" in metrics:
        ENTROPY_DELTA.labels(
            session_id=session_id, tool=tool, provenance=prov.get("dS", "measured")
        ).set(metrics["dS"])
    elif "entropy_delta" in metrics:
        ENTROPY_DELTA.labels(
            session_id=session_id, tool=tool, provenance=prov.get("entropy_delta", "measured")
        ).set(metrics["entropy_delta"])
        
    if "omega0" in metrics:
        HUMILITY_BAND.labels(
            session_id=session_id, tool=tool, provenance=prov.get("omega0", "policy_constant")
        ).set(metrics["omega0"])
    elif "humility" in metrics:
        HUMILITY_BAND.labels(
            session_id=session_id, tool=tool, provenance=prov.get("humility", "policy_constant")
        ).set(metrics["humility"])
        
    if "peace2" in metrics:
        PEACE_SQUARED.labels(
            session_id=session_id, tool=tool, provenance=prov.get("peace2", "policy_constant")
        ).set(metrics["peace2"])
    elif "peace" in metrics:
        PEACE_SQUARED.labels(
            session_id=session_id, tool=tool, provenance=prov.get("peace", "policy_constant")
        ).set(metrics["peace"])
        
    if "kappa_r" in metrics:
        EMPATHY_QUOTIENT.labels(
            session_id=session_id, tool=tool, provenance=prov.get("kappa_r", "placeholder")
        ).set(metrics["kappa_r"])
    elif "empathy" in metrics:
        EMPATHY_QUOTIENT.labels(
            session_id=session_id, tool=tool, provenance=prov.get("empathy", "placeholder")
        ).set(metrics["empathy"])

def record_verdict(verdict: str) -> None:
    """Increment verdict counter."""
    VERDICT_TOTAL.labels(verdict=verdict).inc()
