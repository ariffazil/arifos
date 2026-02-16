"""
AGI stage data structures (compatibility layer).

Provides SenseOutput and build_delta_bundle used by AGIEngine.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from codebase.bundles import DeltaBundle, EngineVote, Hypothesis, ReasoningTree


@dataclass
class SenseOutput:
    """Output of 111 SENSE stage (minimal compatibility contract)."""

    session_id: str
    raw_query: str
    parsed_facts: List[str]
    detected_intent: str
    confidence: float
    f10_ontology_pass: bool = True
    f12_injection_risk: float = 0.0
    stage_pass: bool = True
    violations: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


def build_delta_bundle(
    *,
    sense_output: SenseOutput,
    hypotheses: Optional[List[Hypothesis]] = None,
    reasoning: Optional[ReasoningTree] = None,
    confidence_high: float = 0.95,
    confidence_low: float = 0.90,
    omega_0: float = 0.04,
    entropy_delta: float = 0.0,
    vote_reason: str = "",
) -> DeltaBundle:
    """Build a DeltaBundle from stage outputs (compatibility helper)."""

    bundle = DeltaBundle(
        session_id=sense_output.session_id,
        raw_query=sense_output.raw_query,
        parsed_facts=sense_output.parsed_facts,
        detected_intent=sense_output.detected_intent,
        hypotheses=hypotheses or [],
        reasoning=reasoning,
        confidence_high=confidence_high,
        confidence_low=confidence_low,
        omega_0=omega_0,
        entropy_delta=entropy_delta,
        vote=EngineVote.SEAL if confidence_high >= 0.8 else EngineVote.UNCERTAIN,
        vote_reason=vote_reason,
    )
    return bundle.seal()


__all__ = ["SenseOutput", "build_delta_bundle"]
