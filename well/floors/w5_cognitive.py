from arifos.well.models.state import SensorSnapshot, FloorResult
from arifos.well.const import W5_CLARITY_HARD_THROTTLE

def evaluate(snapshot: SensorSnapshot) -> FloorResult:
    readings = {r.metric: r.raw_value for r in snapshot.readings}
    clarity = readings.get("clarity", 10.0)
    fatigue = readings.get("decision_fatigue", 0.0)

    if clarity < W5_CLARITY_HARD_THROTTLE or fatigue > 8:
        return FloorResult(
            floor_id="W5", status="WARNING", score_delta=20.0,
            rationale="Cognitive entropy high / low clarity.",
            recommended_action="REDUCE_BANDWIDTH"
        )
    
    return FloorResult(floor_id="W5", status="PASS", score_delta=0.0, rationale="Cognitive nominal.", recommended_action="NONE")
