from __future__ import annotations

from arifos.core.governance import ThermodynamicMetrics, governed_return


async def execute(
    receipt: dict,
    organ: str,
    call: dict,
    dry_run: bool = False,
    operator_id: str | None = None,
    session_id: str | None = None,
) -> dict:
    seal_ok = receipt.get("verdict") == "SEAL"
    report = {
        "execution": "PENDING" if dry_run else "EXECUTED",
        "organ": organ,
        "call": call,
        "safe_execution_rate": 1.0 if seal_ok else 0.0,
    }
    metrics = (
        ThermodynamicMetrics(1.0, -0.2, 0.045, 1.5, True, 0.98, 1.0)
        if seal_ok
        else ThermodynamicMetrics(0.99, 0.01, 0.04, 1.0, False, 0.9, 0.8)
    )
    return governed_return("arifos_forge", report, metrics, operator_id, session_id)
