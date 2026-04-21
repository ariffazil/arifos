import pytest
from datetime import datetime
from arifos.well.models.state import SensorReading, SensorSnapshot
from arifos.well.core.aggregator import Aggregator
from arifos.well.core.scorer import Scorer
from arifos.well.core.throttle import Throttle
from arifos.well.floors import w1_sleep, w5_cognitive

def test_w1_sleep_boundary():
    # Test Normal
    snap = SensorSnapshot(readings=[
        SensorReading(sensor_type="manual", metric="sleep_hours", raw_value=8.0, normalized=8.0, confidence=1.0, timestamp=datetime.utcnow())
    ], data_quality=1.0, timestamp=datetime.utcnow())
    res = w1_sleep.evaluate(snap)
    assert res.status == "PASS"

    # Test Critical (Hours < 3)
    snap_crit = SensorSnapshot(readings=[
        SensorReading(sensor_type="manual", metric="sleep_hours", raw_value=2.0, normalized=2.0, confidence=1.0, timestamp=datetime.utcnow())
    ], data_quality=1.0, timestamp=datetime.utcnow())
    res_crit = w1_sleep.evaluate(snap_crit)
    assert res_crit.status == "CRITICAL"
    assert res_crit.recommended_action == "PAUSE"

def test_throttle_logic():
    throttle = Throttle()
    # Mock a critical violation
    from arifos.well.models.state import FloorResult
    v = FloorResult(floor_id="W3", status="CRITICAL", score_delta=25, rationale="Test", recommended_action="PAUSE")
    
    bw, scope, rat = throttle.emit(75.0, [v])
    assert bw == 0.0
    assert scope == "PAUSED"

def test_w5_hard_throttle():
    throttle = Throttle()
    from arifos.well.models.state import FloorResult
    v = FloorResult(floor_id="W5", status="WARNING", score_delta=20, rationale="Low clarity", recommended_action="REDUCE_BANDWIDTH")
    
    bw, scope, rat = throttle.emit(80.0, [v])
    assert bw == 0.3
    assert scope == "LIMITED"
