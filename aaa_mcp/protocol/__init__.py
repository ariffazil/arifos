"""
aaa_mcp/protocol — Formal Low-Entropy Protocol for AAA MCP

Machine-executable governance layer:
- JSON Schema definitions for all 13 tools
- Operators for 9 Principles
- Schema-to-motto mapping layer
- Unified response envelope

Version: 1.1.0-LOW_ENTROPY
"""

from .operators import PrincipleOperator, OPERATOR_REGISTRY
from .mapping import SchemaMottoMapper, get_schema_for_stage
from .schemas import (
    TOOL_SCHEMAS,
    STAGE_OPERATORS,
    OUTPUT_CONTRACTS,
)
from .response import (
    UnifiedResponse,
    build_init_response,
    build_sense_response,
    build_think_response,
    build_reason_response,
    build_empathize_response,
    build_align_response,
    build_verdict_response,
    build_seal_response,
    build_error_response,
    validate_input,
    render_user_answer,
    get_next_step_template,
    NEXT_STEP_TEMPLATES,
)
from .tool_registry import (
    ToolSpec,
    CANONICAL_TOOLS,
    get_tool_spec,
    get_tool_by_stage,
    get_next_tool,
    validate_tool_path,
    get_pipeline_sequence,
    export_tool_schema_for_agents,
    get_agent_selection_hints,
)

__all__ = [
    # Operators
    "PrincipleOperator",
    "OPERATOR_REGISTRY",
    # Mapping
    "SchemaMottoMapper",
    "get_schema_for_stage",
    # Schemas
    "TOOL_SCHEMAS",
    "STAGE_OPERATORS",
    "OUTPUT_CONTRACTS",
    # Response envelope
    "UnifiedResponse",
    "build_init_response",
    "build_sense_response",
    "build_think_response",
    "build_reason_response",
    "build_empathize_response",
    "build_align_response",
    "build_verdict_response",
    "build_seal_response",
    "build_error_response",
    "validate_input",
    "render_user_answer",
    "get_next_step_template",
    "NEXT_STEP_TEMPLATES",
    # Tool registry (v60)
    "ToolSpec",
    "CANONICAL_TOOLS",
    "get_tool_spec",
    "get_tool_by_stage",
    "get_next_tool",
    "validate_tool_path",
    "get_pipeline_sequence",
    "export_tool_schema_for_agents",
    "get_agent_selection_hints",
]
