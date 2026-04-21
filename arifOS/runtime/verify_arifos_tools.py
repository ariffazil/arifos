"""
arifOS runtime vitality and metrics — merged adapter + runtime constants.
DITEMPA BUKAN DIBERI
"""
from pathlib import Path

# ── Primary metric per tool (for /tools endpoint) ─────────────────────────
PRIMARY_METRIC_NAME = {
    "arifos_000_init": "identity_consistency_rate",
    "arifos_111_sense": "snr_improvement",
    "arifos_222_witness": "witness_consistency",
    "arifos_333_mind": "logical_consistency_rate",
    "arifos_444_kernel": "orthogonality_score",
    "arifos_555_memory": "temporal_coherence",
    "arifos_666_heart": "harm_avoidance_rate",
    "arifos_777_ops": "cost_accuracy",
    "arifos_888_judge": "verdict_calibration",
    "arifos_999_vault": "ledger_integrity",
    "arifos_forge": "safe_execution_rate",
    "arifos_gateway": "gateway_uptime_ratio",
    "arifos_sabar": "sabar_reliability",
}

# ── Vitality log paths ─────────────────────────────────────────────────────
VITALITY_JSONL = Path("/usr/src/project/arifos/runtime/tool_vitality.jsonl")
VITALITY_TSV   = Path("/usr/src/project/arifos/runtime/tool_vitality.tsv")
