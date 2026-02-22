"""
aaa_mcp/protocol — Formal Low-Entropy Protocol for AAA MCP

Machine-executable governance layer:
- JSON Schema definitions for all 13 tools
- Operators for 9 Principles
- Schema-to-motto mapping layer
- Unified response envelope

Version: 1.1.0-LOW_ENTROPY
"""

from .mapping import SchemaMottoMapper, get_schema_for_stage
from .operators import OPERATOR_REGISTRY, PrincipleOperator
from .response import (
    NEXT_STEP_TEMPLATES,
    UnifiedResponse,
    build_align_response,
    build_empathize_response,
    build_error_response,
    build_init_response,
    build_reason_response,
    build_seal_response,
    build_sense_response,
    build_think_response,
    build_verdict_response,
    get_next_step_template,
    render_user_answer,
    validate_input,
)
from .schemas import (
    CANONICAL_TOOL_INPUT_SCHEMAS,
    CANONICAL_TOOL_OUTPUT_SCHEMAS,
    OUTPUT_CONTRACTS,
    STAGE_OPERATORS,
    TOOL_SCHEMAS,
    get_input_schema,
    get_output_schema,
)
from .tool_naming import CANONICAL_PUBLIC_TO_LEGACY, MCP_VERB_TO_LEGACY, resolve_protocol_tool_name
from .tool_registry import (
    CANONICAL_TOOLS,
    ToolSpec,
    export_tool_schema_for_agents,
    get_agent_selection_hints,
    get_next_tool,
    get_pipeline_sequence,
    get_tool_by_stage,
    get_tool_spec,
    validate_tool_path,
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
    "CANONICAL_TOOL_INPUT_SCHEMAS",
    "CANONICAL_TOOL_OUTPUT_SCHEMAS",
    "STAGE_OPERATORS",
    "OUTPUT_CONTRACTS",
    "get_input_schema",
    "get_output_schema",
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
    # Naming resolution
    "CANONICAL_PUBLIC_TO_LEGACY",
    "MCP_VERB_TO_LEGACY",
    "resolve_protocol_tool_name",
]
