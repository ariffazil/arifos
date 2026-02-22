"""
Schema-to-Motto Mapping Layer

Maps between:
- Human mottos (inspirational)
- Machine operators (executable)
- JSON schemas (formal)

This is the translation layer that preserves soul for humans
while providing gears for AI.

Version: 1.0.0-LOW_ENTROPY
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class StageSchema:
    """Complete schema definition for a stage."""

    stage_id: str
    operator_id: str
    motto: str
    meaning: str
    principle: str
    input_schema: Dict[str, Any]
    output_schema: Dict[str, Any]
    floors: List[str]


# ═════════════════════════════════════════════════════════════════════════════
# 9 PRINCIPLES — Human + Machine Dual Representation
# ═════════════════════════════════════════════════════════════════════════════

STAGE_SCHEMAS: Dict[str, StageSchema] = {
    "000": StageSchema(
        stage_id="000",
        operator_id="EARNED",
        motto="DITEMPA, BUKAN DIBERI",
        meaning="Forged, Not Given",
        principle="Nothing of value comes free",
        input_schema={"query": "string", "auth": "optional"},
        output_schema={"session_id": "string", "verdict": "enum[SEAL,VOID]"},
        floors=["F11", "F12"],
    ),
    "111": StageSchema(
        stage_id="111",
        operator_id="EXAMINE",
        motto="DIKAJI, BUKAN DISUAPI",
        meaning="Examined, Not Spoon-fed",
        principle="Don't accept things at face value",
        input_schema={"query": "string", "session_id": "string"},
        output_schema={"intent": "string", "lane": "enum[SOCIAL,CARE,FACTUAL,CRISIS]"},
        floors=["F2", "F4"],
    ),
    "222": StageSchema(
        stage_id="222",
        operator_id="EXPLORE",
        motto="DIJELAJAH, BUKAN DISEKATI",
        meaning="Explored, Not Restricted",
        principle="Consider multiple paths",
        input_schema={"query": "string", "intent": "classified"},
        output_schema={"hypotheses": "array[3]", "confidence_range": "tuple"},
        floors=["F2", "F4", "F7"],
    ),
    "333": StageSchema(
        stage_id="333",
        operator_id="CLARIFY",
        motto="DIJELASKAN, BUKAN DIKABURKAN",
        meaning="Clarified, Not Obscured",
        principle="Reduce confusion",
        input_schema={"query": "string", "hypotheses": "array"},
        output_schema={
            "conclusion": "string",
            "truth_score": "float[0,1]",
            "entropy_delta": "float",
        },
        floors=["F2", "F4", "F7"],
    ),
    "444": StageSchema(
        stage_id="444",
        operator_id="FACE",
        motto="DIHADAPI, BUKAN DITANGGUHKAN",
        meaning="Faced, Not Postponed",
        principle="Address hard truths directly",
        input_schema={"agi_output": "object", "asi_output": "object"},
        output_schema={"consensus_score": "float", "conflicts": "array"},
        floors=["F3"],
    ),
    "555": StageSchema(
        stage_id="555",
        operator_id="CALM",
        motto="DIDAMAIKAN, BUKAN DIPANASKAN",
        meaning="Calmed, Not Inflamed",
        principle="Reduce tension",
        input_schema={"query": "string", "context": "object"},
        output_schema={"empathy_kappa_r": "float[0,1]", "stakeholders": "array"},
        floors=["F5", "F6"],
    ),
    "666": StageSchema(
        stage_id="666",
        operator_id="PROTECT",
        motto="DIJAGA, BUKAN DIABAIKAN",
        meaning="Guarded, Not Neglected",
        principle="Duty of care",
        input_schema={"query": "string", "empathy_analysis": "object"},
        output_schema={"is_reversible": "bool", "safety_score": "float[0,1]"},
        floors=["F5", "F6", "F9"],
    ),
    "777": StageSchema(
        stage_id="777",
        operator_id="WORK",
        motto="DIUSAHAKAN, BUKAN SEKADAR DIHARAP",
        meaning="Worked For, Not Merely Hoped",
        principle="Results require effort",
        input_schema={"sync_output": "object", "safety_verified": "bool"},
        output_schema={"output": "string", "coherence": "float[0,1]"},
        floors=["F3", "F8"],
    ),
    "888": StageSchema(
        stage_id="888",
        operator_id="AWARE",
        motto="DISEDARKAN, BUKAN DIYAKINKAN",
        meaning="Aware, Not Over-assured",
        principle="Know the limits of knowledge",
        input_schema={"forged_output": "object", "floors_checked": "array"},
        output_schema={
            "verdict": "enum[SEAL,PARTIAL,VOID,888_HOLD]",
            "omega_0": "float[0.03,0.05]",
        },
        floors=["F2", "F3", "F5", "F8"],
    ),
    "999": StageSchema(
        stage_id="999",
        operator_id="SEAL",
        motto="DITEMPA, BUKAN DIBERI",
        meaning="Forged, Not Given",
        principle="Approval must be earned",
        input_schema={"verdict": "enum", "audit_trail": "object"},
        output_schema={"seal_id": "string", "seal_hash": "string"},
        floors=["F1", "F3"],
    ),
}


# ═════════════════════════════════════════════════════════════════════════════
# MAPPING FUNCTIONS
# ═════════════════════════════════════════════════════════════════════════════


class SchemaMottoMapper:
    """Bidirectional mapping between human and machine representations."""

    @staticmethod
    def get_by_stage(stage_id: str) -> Optional[StageSchema]:
        """Get schema by stage ID (e.g., '333')."""
        return STAGE_SCHEMAS.get(stage_id)

    @staticmethod
    def get_by_operator(operator_id: str) -> Optional[StageSchema]:
        """Get schema by operator ID (e.g., 'CLARIFY')."""
        for schema in STAGE_SCHEMAS.values():
            if schema.operator_id == operator_id:
                return schema
        return None

    @staticmethod
    def get_by_motto(motto_fragment: str) -> Optional[StageSchema]:
        """Get schema by motto fragment (fuzzy match)."""
        fragment_lower = motto_fragment.lower()
        for schema in STAGE_SCHEMAS.values():
            if fragment_lower in schema.motto.lower() or fragment_lower in schema.meaning.lower():
                return schema
        return None

    @staticmethod
    def get_by_principle(principle: str) -> Optional[StageSchema]:
        """Get schema by principle description (fuzzy match)."""
        principle_lower = principle.lower()
        for schema in STAGE_SCHEMAS.values():
            if principle_lower in schema.principle.lower():
                return schema
        return None

    @staticmethod
    def to_human_readable(stage_id: str) -> Dict[str, str]:
        """Convert stage to human-readable format."""
        schema = STAGE_SCHEMAS.get(stage_id)
        if not schema:
            return {}
        return {
            "stage": schema.stage_id,
            "principle": schema.principle,
            "motto": f"{schema.motto} ({schema.meaning})",
            "meaning": schema.meaning,
        }

    @staticmethod
    def to_machine_readable(stage_id: str) -> Dict[str, Any]:
        """Convert stage to machine-readable (low-entropy) format."""
        schema = STAGE_SCHEMAS.get(stage_id)
        if not schema:
            return {}
        return {
            "id": schema.stage_id,
            "operator": schema.operator_id,
            "invariant": get_operator_invariant(schema.operator_id),
            "input": schema.input_schema,
            "output": schema.output_schema,
            "floors": schema.floors,
        }

    @staticmethod
    def build_pipeline_schema(stage_ids: List[str]) -> Dict[str, Any]:
        """Build complete pipeline schema from stage list."""
        pipeline = []
        for stage_id in stage_ids:
            schema = STAGE_SCHEMAS.get(stage_id)
            if schema:
                pipeline.append(
                    {
                        "stage": stage_id,
                        "operator": schema.operator_id,
                        "invariant": get_operator_invariant(schema.operator_id),
                    }
                )
        return {
            "pipeline_id": f"{'-'.join(stage_ids)}",
            "stages": pipeline,
            "total_invariants": len([s for s in pipeline if s["invariant"]]),
        }


# Helper function for invariants
def get_operator_invariant(operator_id: str) -> Dict[str, Any]:
    """Get invariant constraints for an operator."""
    invariants = {
        "EARNED": {"auth": "valid"},
        "EXAMINE": {"intent_clarity": "must_increase"},
        "EXPLORE": {"hypothesis_count": ">=3"},
        "CLARIFY": {"entropy_delta": "<=0", "ambiguity": "decrease"},
        "FACE": {"conflicts": "must_resolve"},
        "CALM": {"peace_squared": ">=1.0"},
        "PROTECT": {"reversibility": "True", "weakest_impact": "<=0.1"},
        "WORK": {"coherence": ">=0.7"},
        "AWARE": {"omega_0": "in_range[0.03,0.05]"},
        "SEAL": {"immutability": "True"},
    }
    return invariants.get(operator_id, {})


# Convenience functions
def get_schema_for_stage(stage_id: str) -> Optional[StageSchema]:
    """Get complete schema for a stage."""
    return SchemaMottoMapper.get_by_stage(stage_id)


def get_motto_for_stage(stage_id: str) -> str:
    """Get motto for a stage."""
    schema = STAGE_SCHEMAS.get(stage_id)
    return schema.motto if schema else ""


def get_meaning_for_stage(stage_id: str) -> str:
    """Get meaning for a stage."""
    schema = STAGE_SCHEMAS.get(stage_id)
    return schema.meaning if schema else ""


def get_principle_for_stage(stage_id: str) -> str:
    """Get principle for a stage."""
    schema = STAGE_SCHEMAS.get(stage_id)
    return schema.principle if schema else ""


def get_all_stages() -> List[str]:
    """Get all stage IDs."""
    return list(STAGE_SCHEMAS.keys())


def get_all_operators() -> List[str]:
    """Get all operator IDs."""
    return [s.operator_id for s in STAGE_SCHEMAS.values()]
