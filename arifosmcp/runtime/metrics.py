"""
arifosmcp/runtime/metrics.py — Prometheus Metrics for arifOS

Defines the gauges and counters for constitutional observability (G, ΔS, Ω₀).
Part of H1.1: Production Observability.

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

from __future__ import annotations

from prometheus_client import Counter, Gauge, Histogram

# ---------------------------------------------------------------------------
# CONSTITUTIONAL METRICS (ΔΩΨ)
# ---------------------------------------------------------------------------

# G (Genius Score) - Fundamental governed intelligence (3E) metric [0, 1]
GENIUS_SCORE = Gauge(
    "arifos_genius_score",
    "Governed Intelligence (3E) Score (G) — Target ≥ 0.80",
    ["session_id", "tool", "provenance"],
)

# ΔS (Entropy Delta) - Information clarity metric (lower is better, ideally ≤ 0)
ENTROPY_DELTA = Gauge(
    "arifos_entropy_delta",
    "Information Entropy Delta (ΔS) — Lower reduces noise",
    ["session_id", "tool", "provenance"],
)

# Ω₀ (Humility / Uncertainty) - Stability band metric [0.03, 0.05]
HUMILITY_BAND = Gauge(
    "arifos_humility_band",
    "Humility / Uncertainty (Ω₀) — Target band [0.03, 0.05]",
    ["session_id", "tool", "provenance"],
)

# P² (Peace Squared) - Stakeholder safety metric [0, 1]
PEACE_SQUARED = Gauge(
    "arifos_peace_squared",
    "Stakeholder Stability (P²) — Target ≥ 1.0",
    ["session_id", "tool", "provenance"],
)

# κᵣ (Empathy Quotient) - Stakeholder care metric
EMPATHY_QUOTIENT = Gauge(
    "arifos_empathy_quotient",
    "Empathy Quotient (κᵣ) — Stakeholder care level",
    ["session_id", "tool", "provenance"],
)

# ---------------------------------------------------------------------------
# OPERATIONAL METRICS
# ---------------------------------------------------------------------------

# Metabolic Loop Latency
METABOLIC_LOOP_DURATION = Histogram(
    "arifos_metabolic_loop_seconds",
    "Latency of the 000-999 metabolic loop",
    buckets=(0.1, 0.5, 1.0, 2.5, 5.0, 10.0, 30.0, 60.0),
)

# Verdict Counters
VERDICT_TOTAL = Counter(
    "arifos_verdicts_total",
    "Total constitutional verdicts issued",
    ["verdict"],  # SEAL, VOID, HOLD_888, PARTIAL
)

# Request Counter
REQUESTS_TOTAL = Counter(
    "arifos_requests_total",
    "Total incoming requests processed by the runtime",
    ["method", "status"],
)

# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------


def record_constitutional_metrics(
    session_id: str,
    tool: str,
    metrics: dict[str, float],
    provenance_map: dict[str, str] | None = None,
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


# ---------------------------------------------------------------------------
# FORGED-2026.03: MGI CANONICAL TOOL METRICS
# Grand Unified Technical Specification additions
# ---------------------------------------------------------------------------

# W3 Tri-Witness score histogram (F3 Mirror Floor)
W3_SCORE = Histogram(
    "arifos_w3_score",
    "Tri-Witness W3 score distribution — SEAL threshold ≥ 0.95",
    ["tool"],
    buckets=[0.0, 0.25, 0.50, 0.70, 0.75, 0.85, 0.90, 0.95, 1.0],
)

# 888_HOLD queue depth (F13 Sovereign Gate backlog)
HOLD_QUEUE_DEPTH = Gauge(
    "arifos_hold_queue_depth",
    "Number of 888_HOLD events pending sovereign ratification",
)

# Vault record count (VAULT999 growth)
VAULT_RECORDS_TOTAL = Gauge(
    "arifos_vault_records_total",
    "Total records in VAULT999 Merkle chain",
)

# Floor violations by floor code (constitutional health)
FLOOR_VIOLATIONS = Counter(
    "arifos_floor_violations_total",
    "Constitutional floor violations — breach by floor and tool",
    ["floor", "tool"],
)

# Machine fault codes (VOID Memanjang elimination — mechanical faults only)
MACHINE_FAULTS = Counter(
    "arifos_machine_faults_total",
    "Machine-layer faults (NEVER maps to VOID) — by fault_code and tool",
    ["fault_code", "tool"],
)

# VOID events (constitutional only — should be rare)
VOID_EVENTS = Counter(
    "arifos_void_events_total",
    "VOID verdicts issued — constitutional violations only (F2/F11/F12/F13)",
    ["void_reason", "tool"],
)

# Merkle chain integrity check results
MERKLE_INTEGRITY = Counter(
    "arifos_merkle_integrity_checks_total",
    "VAULT999 Merkle chain integrity check outcomes",
    ["status"],  # VALID | TAMPERED
)


def record_w3(tool: str, w3_score: float) -> None:
    """Record a W3 Tri-Witness score observation."""
    W3_SCORE.labels(tool=tool).observe(w3_score)


def record_machine_fault(tool: str, fault_code: str) -> None:
    """
    Record a machine-layer fault.
    IMPORTANT: This must NEVER be called for constitutional violations.
    Constitutional violations use record_void_event().
    """
    MACHINE_FAULTS.labels(fault_code=fault_code, tool=tool).inc()


def record_void_event(tool: str, void_reason: str) -> None:
    """
    Record a VOID verdict (constitutional violation only).
    IMPORTANT: This must NEVER be called for infrastructure/mechanical faults.
    Mechanical faults use record_machine_fault().
    """
    VOID_EVENTS.labels(void_reason=void_reason, tool=tool).inc()


def record_floor_violation(tool: str, floor: str) -> None:
    """Record a constitutional floor violation."""
    FLOOR_VIOLATIONS.labels(floor=floor, tool=tool).inc()
