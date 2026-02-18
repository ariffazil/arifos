"""
aaa_mcp/motto_schema.py — MCP Adapter for Constitutional Mottos

Transports core mottos to AI agents via MCP resources.
DITEMPA BUKAN DIBERI — Forged, Not Given
"""

from typing import Dict, Any
from core.shared.mottos import (
    ALL_MOTTOS,
    ERROR_MOTTOS,
    MOTTO_000_INIT_HEADER,
    MOTTO_999_SEAL_HEADER,
    get_motto_by_floor,
)

def get_mottos_resource() -> Dict[str, Any]:
    """Get the complete mottos resource for MCP."""
    mottos_data = {code.value: motto.to_dict() for code, motto in ALL_MOTTOS.items()}
    
    return {
        "uri": "constitutional://mottos",
        "mimeType": "application/json",
        "text": {
            "schema_version": "v64.2-CORE",
            "total_mottos": len(ALL_MOTTOS),
            "mottos": mottos_data,
            "bookends": {
                "init": {"header": MOTTO_000_INIT_HEADER},
                "seal": {"header": MOTTO_999_SEAL_HEADER}
            },
            "error_mottos": ERROR_MOTTOS,
            "cultural_context": "Nusantara constitutional governance error-handling language."
        },
    }

def format_failure_with_motto(floor: str, reason: str) -> str:
    """Format a failure message with cultural motto."""
    motto = get_motto_by_floor(floor)
    if not motto:
        return f"[!] {floor} Floor Breach: {reason}"
    
    return f"""[!] {floor} Floor Breach
    Reason: {reason}
    {motto.malay}
    ({motto.english})"""

def get_init_gate_message() -> str:
    return f"\n{MOTTO_000_INIT_HEADER}\n[000_INIT] Session Ignition\n"

def get_seal_gate_message() -> str:
    return f"\n{MOTTO_999_SEAL_HEADER}\n[999_SEAL] Immutable Commit\n"
