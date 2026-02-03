"""
validators.py - Constitutional Validation Logic (v55)

Implements core validation logic for arifOS constitutional floors.
Used by L4 tools (AGI, ASI, APEX) and L5 agents.

Floors Enforced:
- F1 Amanah: Reversibility
- F4 Clarity: Entropy reduction (ΔS)
- F12 Injection: Security constraints
- Trinity Consensus: Geometric mean of scores

Schema Enforcement:
- Runtime JSON Schema validation for MCP tool outputs
- Enforces output contracts defined in schemas/*.schema.json
"""

import json
import logging
import math
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


class ConstitutionValidator:
    """
    Central validation logic for constitutional floors.
    """

    @staticmethod
    def validate_f4_clarity(text: str, previous_entropy: float = 1.0) -> float:
        """
        F4 Clarity: Verify entropy reduction (ΔS <= 0).
        Returns a score 0.0-1.0 (1.0 = perfect clarity/reduction).
        """
        if not text:
            return 0.0

        # Simplified Shannon entropy estimation based on character distribution
        # In a real implementation, this would use token probabilities
        prob_map = {}
        for char in text:
            prob_map[char] = prob_map.get(char, 0) + 1

        entropy = 0.0
        total_chars = len(text)

        if total_chars == 0:
            return 0.0

        for count in prob_map.values():
            p = count / total_chars
            entropy -= p * math.log2(p)

        # F4 requirement: New entropy should be <= previous_limit
        # For this validator, we normalize the score based on "complexity"
        # Lower entropy relative to length suggests structure (clarity)

        # Heuristic: Good clarity usually has entropy between 3.0 and 5.0 bits/char for English
        # We reward staying within efficient bounds

        clarity_score = 1.0

        # Penalize extremely high entropy (randomness)
        if entropy > 6.0:
            clarity_score -= (entropy - 6.0) * 0.2

        # Penalize extremely low entropy (repetitive/trivial)
        if entropy < 2.0:
            clarity_score -= (2.0 - entropy) * 0.2

        return max(0.0, min(1.0, clarity_score))

    @staticmethod
    def validate_f12_injection(query: str) -> bool:
        """
        F12 Injection: Check for prompt injection patterns.
        Returns True if SAFE, False if INJECTION DETECTED.

        Delegates to InjectionGuard (25+ patterns + normalization).
        Falls back to minimal inline check if guard unavailable.
        """
        if not query:
            return True

        try:
            from codebase.guards.injection_guard import InjectionGuard
            guard = InjectionGuard()
            result = guard.scan_input(query)
            return not result.blocked
        except ImportError:
            # Fallback: minimal pattern check
            injection_patterns = [
                r"ignore\s+(previous|above|all)\s+instructions",
                r"system\s*prompt",
                r"you\s+are\s+now",
                r"DAN\s*mode",
                r"jailbreak",
                r"\[system\s*override\]",
                r"admin\s*access",
                r"sudo\s+mode",
            ]
            query_lower = query.lower()
            for pattern in injection_patterns:
                if re.search(pattern, query_lower):
                    return False
            return True

    @staticmethod
    def validate_f1_reversibility(action_type: str) -> bool:
        """
        F1 Amanah: Verify action is reversible.
        Returns True if reversible, False if irreversible.
        """
        irreversible_actions = [
            "delete_database",
            "overwrite_system_boot",
            "publish_private_key",
            "send_irrevocable_transaction",
        ]

        return action_type.lower() not in irreversible_actions

    @staticmethod
    def validate_trinity_consensus(scores: Dict[str, float]) -> float:
        """
        Calculate Tri-Witness Consensus (W3).
        W3 = cbrt(Mind * Heart * Soul)
        """
        mind = scores.get("mind", 0.0)
        heart = scores.get("heart", 0.0)
        soul = scores.get("soul", 0.0)

        product = mind * heart * soul
        return math.pow(product, 1.0 / 3.0)


# ==============================================================================
# Schema Enforcement (v55.2)
# ==============================================================================

# Schema cache (loaded once per process)
_SCHEMA_CACHE: Dict[str, Dict[str, Any]] = {}


def _get_schemas_dir() -> Path:
    """Locate the schemas/ directory relative to project root."""
    current = Path(__file__).resolve()
    for parent in current.parents:
        schemas_dir = parent / "schemas"
        if schemas_dir.is_dir():
            return schemas_dir
    return Path("schemas")


def load_schema(schema_name: str) -> Optional[Dict[str, Any]]:
    """
    Load a JSON Schema by name (e.g., 'agi_sense').
    Returns None if schema file not found.
    """
    if schema_name in _SCHEMA_CACHE:
        return _SCHEMA_CACHE[schema_name]

    schemas_dir = _get_schemas_dir()
    schema_path = schemas_dir / f"{schema_name}.schema.json"

    if not schema_path.exists():
        logger.warning(f"Schema not found: {schema_path}")
        return None

    try:
        with open(schema_path, "r", encoding="utf-8") as f:
            schema = json.load(f)
        _SCHEMA_CACHE[schema_name] = schema
        return schema
    except (json.JSONDecodeError, OSError) as e:
        logger.error(f"Failed to load schema {schema_name}: {e}")
        return None


def validate_output(output: Dict[str, Any], schema_name: str) -> Tuple[bool, List[str]]:
    """
    Validate a tool output dict against its JSON Schema.

    Returns:
        (is_valid, list_of_violations)

    Uses lightweight validation (no jsonschema dependency required).
    Checks: required fields, type constraints, enum values, min/max.
    """
    schema = load_schema(schema_name)
    if schema is None:
        return True, []

    violations: List[str] = []

    # Check required fields
    for field in schema.get("required", []):
        if field not in output:
            violations.append(f"Missing required field: '{field}'")

    # Check property types and constraints
    properties = schema.get("properties", {})
    for field, value in output.items():
        if field not in properties:
            continue

        prop_schema = properties[field]
        expected_type = prop_schema.get("type")

        if expected_type and value is not None:
            if not _check_json_type(value, expected_type):
                violations.append(
                    f"Field '{field}': expected type '{expected_type}', "
                    f"got '{type(value).__name__}'"
                )

        if "enum" in prop_schema and value not in prop_schema["enum"]:
            violations.append(
                f"Field '{field}': value '{value}' not in {prop_schema['enum']}"
            )

        if expected_type == "number" and isinstance(value, (int, float)):
            if "minimum" in prop_schema and value < prop_schema["minimum"]:
                violations.append(
                    f"Field '{field}': {value} below minimum {prop_schema['minimum']}"
                )
            if "maximum" in prop_schema and value > prop_schema["maximum"]:
                violations.append(
                    f"Field '{field}': {value} above maximum {prop_schema['maximum']}"
                )

    return len(violations) == 0, violations


def validate_input(input_data: Dict[str, Any], tool_name: str) -> Tuple[bool, List[str]]:
    """
    Validate tool input against the ToolRegistry's input_schema for the given tool.

    Returns:
        (is_valid, list_of_violations)

    Uses the same lightweight validation as validate_output but reads
    schemas directly from the ToolRegistry definitions.
    """
    violations: List[str] = []

    try:
        from mcp_server.core.tool_registry import ToolRegistry
        registry = ToolRegistry()
        tool = registry.get(tool_name)
        if tool is None:
            return True, []
        schema = tool.input_schema
    except ImportError:
        return True, []

    if not schema:
        return True, []

    # Check required fields
    for field in schema.get("required", []):
        if field not in input_data:
            violations.append(f"Missing required field: '{field}'")

    # Check property types and constraints
    properties = schema.get("properties", {})
    for field, value in input_data.items():
        if field not in properties:
            continue

        prop_schema = properties[field]
        expected_type = prop_schema.get("type")

        if expected_type and value is not None:
            if not _check_json_type(value, expected_type):
                violations.append(
                    f"Field '{field}': expected type '{expected_type}', "
                    f"got '{type(value).__name__}'"
                )

        if "enum" in prop_schema and value not in prop_schema["enum"]:
            violations.append(
                f"Field '{field}': value '{value}' not in {prop_schema['enum']}"
            )

    return len(violations) == 0, violations


def _check_json_type(value: Any, expected: str) -> bool:
    """Check if a value matches a JSON Schema type string."""
    type_map = {
        "string": str,
        "number": (int, float),
        "integer": int,
        "boolean": bool,
        "array": list,
        "object": dict,
    }
    expected_types = type_map.get(expected)
    if expected_types is None:
        return True
    return isinstance(value, expected_types)


def enforce_schema(output: Dict[str, Any], schema_name: str) -> Dict[str, Any]:
    """
    Validate output and return VOID response if schema violated.

    Usage in MCP tool handlers:
        result = await handler(...)
        return enforce_schema(result, "agi_sense")
    """
    is_valid, violations = validate_output(output, schema_name)
    if is_valid:
        return output

    logger.warning(f"Schema violation in {schema_name}: {violations}")
    return {
        "session_id": output.get("session_id", "unknown"),
        "vote": "VOID",
        "verdict": "VOID",
        "reason": f"Schema violation: {'; '.join(violations)}",
        "violations": violations,
        "schema": schema_name,
    }
