"""
aaa_mcp/services — Services module for MCP Server

Metrics, Redis client, and external service integrations.
"""

from .constitutional_metrics import (
    get_stage_result,
    record_verdict,
    store_stage_result,
    update_metabolic_state,
)
from .redis_client import MindVault, get_mind_vault

__all__ = [
    "record_verdict",
    "update_metabolic_state",
    "store_stage_result",
    "get_stage_result",
    "MindVault",
    "get_mind_vault",
]
