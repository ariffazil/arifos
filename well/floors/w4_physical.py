from arifos.well.models.state import SensorSnapshot, FloorResult
from arifos.well.const import W4_SEDENTARY_LIMIT_HOURS, W4_PAIN_CAUTION_THRESHOLD

def evaluate(snapshot: SensorSnapshot) -> FloorResult:
    readings = {r.metric: r.raw_value for r in snapshot.readings}
    pain = readings.get("pain_max", 0.0)
    movement = readings.get("movement_count", 10.0)

    if pain > W4_PAIN_CAUTION_THRESHOLD:
        return FloorResult(
            floor_id="W4", status="CAUTION", score_delta=10.0,
            rationale="Unmanaged pain affecting focus.",
            recommended_action="MONITOR"
        )
    
    return FloorResult(floor_id="W4", status="PASS", score_delta=0.0, rationale="Physical nominal.", recommended_action="NONE")
