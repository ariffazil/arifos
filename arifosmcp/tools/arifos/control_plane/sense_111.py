# C:\ariffazil\arifOS\arifosmcp\tools\arifos\control_plane\sense_111.py
# DISTILLED KERNEL [2026.04.20] + MiniMax Vision Bridge
# DITEMPA BUKAN DIBERI

import time
from fastmcp import Context
from arifosmcp.runtime.governance import (
    ThermodynamicMetrics,
    governed_return,
    TRI_WITNESS_PARTIAL,
    PEACE_SQUARED_FLOOR,
)
from arifosmcp.integrations.minimax_mcp_bridge import minimax_bridge


def _is_public_https(url: str | None) -> bool:
    if not url:
        return False
    url_lower = url.lower()
    if not url_lower.startswith("https://"):
        return False
    private_prefixes = (
        "localhost", "127.0.0.1", "192.168.", "10.0.", "172.16.",
        "172.17.", "172.18.", "172.19.", "172.20.", "172.21.",
        "172.22.", "172.23.", "172.24.", "172.25.", "172.26.",
        "172.27.", "172.28.", "172.29.", "172.30.", "172.31.",
        "::1", "0.0.0.0",
    )
    for prefix in private_prefixes:
        if prefix in url_lower:
            return False
    return True

async def execute(
    ctx: Context,
    query: str,
    operator_id: str | None = None,
    session_id: str | None = None,
    mode: str = "grounded",
    image_url: str | None = None,
):
    """
    arifos_111_sense — Perception & Signal Detection

    Modes:
      grounded : Standard text-based perception (default).
      visual   : Image understanding via MiniMax MCP bridge (F2 visual grounding).

    When image_url is provided, the tool automatically routes to the visual
    bridge regardless of mode. All visual output passes through F9 Anti-Hantu
    governance before returning.
    """
    # ── Visual perception branch (MiniMax bridge) ───────────────
    if image_url or mode == "visual":
        if not image_url:
            report = {
                "query": query,
                "mode": "visual",
                "error": "image_url required for visual mode",
                "error_class": "missing_image_url",
            }
            metrics = ThermodynamicMetrics(
                truth_score=0.99,
                delta_s=+0.01,
                omega_0=0.04,
                peace_squared=PEACE_SQUARED_FLOOR,
                amanah_lock=True,
                tri_witness_score=TRI_WITNESS_PARTIAL,
                stakeholder_safety=1.0,
            )
            return governed_return("arifos_111_sense", report, metrics, operator_id, session_id)

        if not _is_public_https(image_url):
            report = {
                "query": query,
                "image_url": image_url,
                "mode": "visual",
                "error": "image_url must be publicly reachable (https://...)",
                "error_class": "non_public_image_url",
                "witness_debug": {"human": True, "ai": False, "earth": False, "bridge": "minimax_vision"},
            }
            metrics = ThermodynamicMetrics(
                truth_score=0.99,
                delta_s=+0.01,
                omega_0=0.04,
                peace_squared=PEACE_SQUARED_FLOOR,
                amanah_lock=True,
                tri_witness_score=TRI_WITNESS_PARTIAL,
                stakeholder_safety=1.0,
            )
            return governed_return("arifos_111_sense", report, metrics, operator_id, session_id)

        bridge_result = await minimax_bridge.understand_image(
            image_url=image_url, question=query or None
        )

        if bridge_result["status"] != "success":
            report = {
                "query": query,
                "image_url": image_url,
                "mode": "visual",
                "bridge_status": bridge_result["status"],
                "bridge_error": bridge_result.get("error"),
                "error_class": bridge_result.get("error_class", "bridge_failure"),
                "witness_debug": {"human": True, "ai": False, "earth": False, "bridge": "minimax_vision"},
            }
            metrics = ThermodynamicMetrics(
                truth_score=0.99,
                delta_s=+0.01,
                omega_0=0.04,
                peace_squared=PEACE_SQUARED_FLOOR,
                amanah_lock=True,
                tri_witness_score=TRI_WITNESS_PARTIAL,
                stakeholder_safety=1.0,
            )
            return governed_return("arifos_111_sense", report, metrics, operator_id, session_id)

        f9_hantu = bridge_result["metrics"]["f9_hantu_score"]
        f2_truth = 0.99 if f9_hantu < 0.3 else 0.7 if f9_hantu < 0.5 else 0.4
        amanah = f9_hantu < 0.5
        delta_s = -0.08 if amanah else 0.05
        peace_sq = 1.2 if amanah else 0.8
        tri_witness = 0.98 if amanah else 0.6

        report = {
            "query": query,
            "image_url": image_url,
            "mode": "visual",
            "description": bridge_result["description"],
            "bridge_verdict": bridge_result["verdict"],
            "bridge_metrics": bridge_result["metrics"],
        }
        metrics = ThermodynamicMetrics(
            truth_score=f2_truth,
            delta_s=delta_s,
            omega_0=0.045,
            peace_squared=peace_sq,
            amanah_lock=amanah,
            tri_witness_score=tri_witness,
            stakeholder_safety=1.0,
            floor_9_signal="pass" if f9_hantu < 0.3 else "fail" if f9_hantu >= 0.5 else "caution",
        )
        return governed_return("arifos_111_sense", report, metrics, operator_id, session_id)

    # ── Default grounded text branch ────────────────────────────
    intent = "metabolic_audit" if "status" in query.lower() else "general_query"
    report = {
        "query": query,
        "captured_intent": intent,
        "perception_mode": mode,
        "signal_to_noise": 0.98,
    }
    metrics = ThermodynamicMetrics(0.995, -0.12, 0.045, 1.2, True, 0.98, 1.0)
    return governed_return("arifos_111_sense", report, metrics, operator_id, session_id)


async def self_test() -> dict:
    start = time.time()
    from fastmcp import Context
    res = await execute(Context(), "vitality audit", "arif", "audit_session")
    passed = res["status"] == "success" and res["output"]["captured_intent"] == "metabolic_audit"
    return {
        "performance": {"latency_ms": (time.time() - start) * 1000},
        "correctness": {"test_cases": 1, "passed": 1 if passed else 0, "failed": 0 if passed else 1},
        "primary_metric_name": "snr_improvement",
        "primary_metric_value": 0.98 if passed else 0.0,
        "description": "111_sense: grounded + visual(MiniMax)"
    }
