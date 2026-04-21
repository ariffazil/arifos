from arifos.well.models.state import SensorSnapshot, FloorResult
from arifos.well.const import W3_STRESS_LOAD_WARNING

def evaluate(snapshot: SensorSnapshot) -> FloorResult:
    readings = {r.metric: r.raw_value for r in snapshot.readings}
    load = readings.get("stress_load", 0.0)

    if load > 8:
        return FloorResult(
            floor_id="W3", status="CRITICAL", score_delta=25.0,
            rationale="Extreme stress load.",
            recommended_action="PAUSE"
        )
    if load > W3_STRESS_LOAD_WARNING:
        return FloorResult(
            floor_id="W3", status="WARNING", score_delta=15.0,
            rationale="High stress load detected.",
            recommended_action="REDUCE_BANDWIDTH"
        )
    
    return FloorResult(floor_id="W3", status="PASS", score_delta=0.0, rationale="Stress nominal.", recommended_action="NONE")
