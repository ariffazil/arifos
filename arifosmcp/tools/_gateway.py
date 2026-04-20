from __future__ import annotations

from arifosmcp.runtime.governance import ThermodynamicMetrics, governed_return


async def execute(
    a: str,
    b: str,
    interaction: str = "data_flow",
    operator_id: str | None = None,
    session_id: str | None = None,
) -> dict:
    is_orthogonal = a != b
    report = {
        "a": a,
        "b": b,
        "interaction": interaction,
        "cross_organ_leakage_rate": 0.0 if is_orthogonal else 1.0,
    }
    metrics = ThermodynamicMetrics(1.0, 0.0, 0.038, 1.0, True, 1.0, 1.0)
    return governed_return("arifos_gateway", report, metrics, operator_id, session_id)
