from fastmcp import FastMCP
from typing import Optional, List, Dict, Any
from datetime import datetime
from arifos.well.models.state import WellState, SensorReading
from arifos.well.core.aggregator import Aggregator
from arifos.well.core.classifier import Classifier
from arifos.well.core.evaluator import Evaluator
from arifos.well.core.scorer import Scorer
from arifos.well.core.throttle import Throttle
from arifos.well.sensors.manual import ManualSensor
from arifos.well.persistence.vault_bridge import VaultBridge

mcp = FastMCP("WELL — Biological Substrate v2.0")

# Singleton components
_manual = ManualSensor()
_aggregator = Aggregator()
_classifier = Classifier()
_evaluator = Evaluator()
_scorer = Scorer()
_throttle = Throttle()
_vault = VaultBridge()

async def _get_live_state() -> WellState:
    # 1. Fetch readings from available sensors
    # For Phase 2, we rely on the Manual substrate
    metrics = ["sleep_hours", "sleep_debt_days", "sleep_quality", "stress_load", 
               "clarity", "decision_fatigue", "metabolic_stability", "hydration", 
               "pain_max", "movement_count", "intent_loop_count", "days_since_practice"]
    readings = []
    for m in metrics:
        r = _manual.read_metric(m)
        if r: readings.append(r)
    
    snapshot = _aggregator.aggregate(readings)
    violations = _evaluator.evaluate_all(snapshot)
    score = _scorer.compute_score(violations)
    ofs = _classifier.classify(score)
    bandwidth, scope, rationale = _throttle.emit(score, violations)
    
    return WellState(
        timestamp=datetime.utcnow(),
        well_score=score,
        ofs_class=ofs,
        floors_violated=violations,
        metrics={r.metric: r.raw_value for r in readings},
        bandwidth=bandwidth,
        scope=scope
    )

@mcp.tool()
async def well_readiness_check() -> Dict[str, Any]:
    """P-Axis: Return scalar well_score (0-100), bandwidth recommendation, and scope rationale."""
    state = await _get_live_state()
    return {
        "well_score": state.well_score,
        "bandwidth": state.bandwidth,
        "scope": state.scope,
        "rationale": "Biological substrate grounded in Phase 2 metrics."
    }

@mcp.tool()
async def well_log_update(
    sleep_hours: float = None, sleep_debt_days: float = None,
    stress_load: float = None, clarity: float = None,
    decision_fatigue: float = None, intent_loop_count: float = None,
    days_since_practice: float = None
) -> Dict[str, Any]:
    """E-Axis: Inject manual biological telemetry into the substrate."""
    update = {}
    if sleep_hours is not None: update["sleep_hours"] = sleep_hours
    if sleep_debt_days is not None: update["sleep_debt_days"] = sleep_debt_days
    if stress_load is not None: update["stress_load"] = stress_load
    if clarity is not None: update["clarity"] = clarity
    if decision_fatigue is not None: update["decision_fatigue"] = decision_fatigue
    if intent_loop_count is not None: update["intent_loop_count"] = intent_loop_count
    if days_since_practice is not None: update["days_since_practice"] = days_since_practice
    
    _manual.update(update)
    state = await _get_live_state()
    # Trigger vault anchor on significant update
    await _vault.anchor(state, trigger="MANUAL")
    
    return {"status": "SUCCESS", "current_score": state.well_score, "ofs": state.ofs_class}

if __name__ == "__main__":
    mcp.run()
