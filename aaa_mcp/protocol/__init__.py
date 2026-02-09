"""
aaa_mcp/protocol — Formal Low-Entropy Protocol for AAA MCP

Machine-executable governance layer:
- JSON Schema definitions for all 13 tools
- Operators for 9 Principles
- Schema-to-motto mapping layer

Version: 1.0.0-LOW_ENTROPY
"""

from .operators import PrincipleOperator, OPERATOR_REGISTRY
from .mapping import SchemaMottoMapper, get_schema_for_stage
from .schemas import (
    TOOL_SCHEMAS,
    STAGE_OPERATORS,
    OUTPUT_CONTRACTS,
)

__all__ = [
    "PrincipleOperator",
    "OPERATOR_REGISTRY",
    "SchemaMottoMapper",
    "get_schema_for_stage",
    "TOOL_SCHEMAS",
    "STAGE_OPERATORS",
    "OUTPUT_CONTRACTS",
]
