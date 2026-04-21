from pydantic import BaseModel, Field
from datetime import datetime
from typing import Literal, Optional, List, Dict, Any

class SensorReading(BaseModel):
    sensor_type: str
    metric: str
    raw_value: float
    normalized: float = Field(ge=0, le=10)
    confidence: float = Field(ge=0, le=1)
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class SensorSnapshot(BaseModel):
    readings: List[SensorReading]
    data_quality: float = Field(ge=0, le=1)
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class FloorResult(BaseModel):
    floor_id: str
    status: Literal["PASS", "INFO", "CAUTION", "WARNING", "CRITICAL"]
    score_delta: float
    rationale: str
    recommended_action: Literal["NONE", "MONITOR", "REDUCE_BANDWIDTH", "PAUSE", "HARD_VETO"]
    metadata: Dict[str, Any] = {}

class WellState(BaseModel):
    operator_id: str = "arif"
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    well_score: float = Field(ge=0, le=100)
    ofs_class: Literal["NOMINAL", "ELEVATED", "DEGRADED", "CRITICAL"]
    floors_violated: List[FloorResult]
    metrics: Dict[str, Any]
    bandwidth: float = Field(ge=0, le=1)
    scope: Literal["FULL", "REDUCED", "LIMITED", "PAUSED"]
    w0_assertion: str = "OPERATOR_VETO_INTACT / HIERARCHY_INVARIANT"

class WellEvent(BaseModel):
    vault_type: str = "well_event"
    epoch: datetime = Field(default_factory=datetime.utcnow)
    well_score: float
    status: Literal["STABLE", "LOW", "DEGRADED"]
    violations: List[str]
    w0_assertion: str = "OPERATOR_VETO_INTACT / HIERARCHY_INVARIANT"
    trigger: Literal["VIOLATION", "CAPACITY", "DELTA", "MANUAL"]
    hash: str
