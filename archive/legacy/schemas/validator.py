"""
Lightweight Schema Validator for arifOS MCP Tools (v55.5)

Validates tool outputs against JSON schemas without heavy dependencies.
Uses basic type checking and structure validation.

Usage:
    from codebase.schemas.validator import validate_output, ValidationError
    
    try:
        validate_output(result, schema="asi_output", strict=True)
    except ValidationError as e:
        logger.warning(f"Schema validation failed: {e}")
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

logger = logging.getLogger(__name__)

# Schema cache
_schema_cache: Dict[str, Dict] = {}


class ValidationError(Exception):
    """Raised when output fails schema validation."""
    pass


def _load_schema(schema_name: str) -> Optional[Dict]:
    """Load schema from file, with caching."""
    if schema_name in _schema_cache:
        return _schema_cache[schema_name]
    
    # Try multiple paths
    search_paths = [
        Path(f"schemas/{schema_name}.schema.json"),
        Path(f"schemas/{schema_name}.json"),
        Path(__file__).parent / f"{schema_name}.schema.json",
        Path(__file__).parent.parent.parent / "schemas" / f"{schema_name}.schema.json",
    ]
    
    for path in search_paths:
        if path.exists():
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    schema = json.load(f)
                _schema_cache[schema_name] = schema
                return schema
            except Exception as e:
                logger.debug(f"Failed to load schema from {path}: {e}")
                continue
    
    return None


def _validate_type(value: Any, expected_type: Union[str, List], path: str = "") -> List[str]:
    """Validate a value against an expected type."""
    errors = []
    
    if isinstance(expected_type, list):
        # Union type - check if any matches
        type_errors = []
        for t in expected_type:
            sub_errors = _validate_type(value, t, path)
            if not sub_errors:
                return []  # At least one type matched
            type_errors.extend(sub_errors)
        return [f"{path}: value '{value}' doesn't match any of {expected_type}"]
    
    if expected_type == "string":
        if not isinstance(value, str):
            errors.append(f"{path}: expected string, got {type(value).__name__}")
    elif expected_type == "number":
        if not isinstance(value, (int, float)):
            errors.append(f"{path}: expected number, got {type(value).__name__}")
    elif expected_type == "integer":
        if not isinstance(value, int) or isinstance(value, bool):
            errors.append(f"{path}: expected integer, got {type(value).__name__}")
    elif expected_type == "boolean":
        if not isinstance(value, bool):
            errors.append(f"{path}: expected boolean, got {type(value).__name__}")
    elif expected_type == "array":
        if not isinstance(value, list):
            errors.append(f"{path}: expected array, got {type(value).__name__}")
    elif expected_type == "object":
        if not isinstance(value, dict):
            errors.append(f"{path}: expected object, got {type(value).__name__}")
    elif expected_type == "null":
        if value is not None:
            errors.append(f"{path}: expected null, got {type(value).__name__}")
    
    return errors


def _validate_value(value: Any, schema: Dict, path: str = "") -> List[str]:
    """Recursively validate a value against a schema."""
    errors = []
    
    # Check type
    if "type" in schema:
        errors.extend(_validate_type(value, schema["type"], path))
    
    # Check enum
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: value '{value}' not in enum {schema['enum']}")
    
    # Check object properties
    if schema.get("type") == "object" and isinstance(value, dict):
        if "properties" in schema:
            for prop, prop_schema in schema["properties"].items():
                if prop in value:
                    errors.extend(_validate_value(value[prop], prop_schema, f"{path}.{prop}"))
        
        # Check required properties
        if "required" in schema:
            for req in schema["required"]:
                if req not in value:
                    errors.append(f"{path}: missing required property '{req}'")
        
        # Check additionalProperties
        if schema.get("additionalProperties") is False:
            allowed = set(schema.get("properties", {}).keys())
            for key in value.keys():
                if key not in allowed:
                    errors.append(f"{path}: unexpected property '{key}'")
    
    # Check array items
    if schema.get("type") == "array" and isinstance(value, list):
        if "items" in schema:
            for i, item in enumerate(value):
                errors.extend(_validate_value(item, schema["items"], f"{path}[{i}]"))
    
    # Check numeric constraints
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            errors.append(f"{path}: value {value} below minimum {schema['minimum']}")
        if "maximum" in schema and value > schema["maximum"]:
            errors.append(f"{path}: value {value} above maximum {schema['maximum']}")
    
    return errors


def validate_output(
    output: Dict[str, Any],
    schema: Union[str, Dict],
    strict: bool = False
) -> bool:
    """
    Validate tool output against a schema.
    
    Args:
        output: The output dictionary to validate
        schema: Schema name (e.g., "asi_output") or schema dict
        strict: If True, raise ValidationError on failure. If False, log warning.
    
    Returns:
        True if valid, False if invalid (when strict=False)
    
    Raises:
        ValidationError: If validation fails and strict=True
    """
    # Load schema if string
    if isinstance(schema, str):
        schema_dict = _load_schema(schema)
        if schema_dict is None:
            msg = f"Schema '{schema}' not found"
            if strict:
                raise ValidationError(msg)
            logger.warning(f"[Schema] {msg}")
            return False
    else:
        schema_dict = schema
    
    # Validate
    errors = _validate_value(output, schema_dict, "$")
    
    if errors:
        error_msg = f"Schema validation failed: {'; '.join(errors)}"
        if strict:
            raise ValidationError(error_msg)
        logger.warning(f"[Schema] {error_msg}")
        return False
    
    return True


def validate_output_async(
    output: Dict[str, Any],
    schema: Union[str, Dict],
    strict: bool = False
) -> bool:
    """Async wrapper for validate_output (for consistency with async tools)."""
    return validate_output(output, schema, strict)


# Convenience functions for common schemas
def validate_asi_output(output: Dict, strict: bool = False) -> bool:
    return validate_output(output, "asi_output", strict)


def validate_apex_output(output: Dict, strict: bool = False) -> bool:
    return validate_output(output, "apex_output", strict)


def validate_reality_output(output: Dict, strict: bool = False) -> bool:
    return validate_output(output, "reality_output", strict)


def validate_vault_output(output: Dict, strict: bool = False) -> bool:
    return validate_output(output, "vault_output", strict)


def validate_agi_output(output: Dict, strict: bool = False) -> bool:
    return validate_output(output, "agi_sense", strict)


__all__ = [
    "validate_output",
    "validate_output_async",
    "validate_asi_output",
    "validate_apex_output",
    "validate_reality_output",
    "validate_vault_output",
    "validate_agi_output",
    "ValidationError",
]
