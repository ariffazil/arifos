"""
LSP Tools for arifOS MCP
Exposes Language Server Protocol via MCP tools.

@module: tools/lsp_tools
@version: 2026.03.13-FORGED
@status: 888_SAFE
"""

from __future__ import annotations

from typing import Any

import logging

from arifosmcp.intelligence.lsp_bridge import get_lsp_bridge

try:
    from fastmcp import FastMCP
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False

logger = logging.getLogger(__name__)


async def lsp_query(
    file_path: str,
    query_type: str,
    line: int = 0,
    character: int = 0,
) -> dict[str, Any]:
    """Query Language Server for code intelligence."""
    logger.info("LSP_TOOL_CALLED", tool="lsp_query", file=file_path, query_type=query_type)

    bridge = get_lsp_bridge()

    if not bridge._initialized:
        init_result = await bridge.start("python")
        if not init_result.success:
            return _make_error_response(f"Failed to start LSP: {init_result.error}")

    if query_type == "hover":
        result = await bridge.hover(file_path, line, character)
    elif query_type == "definition":
        result = await bridge.definition(file_path, line, character)
    elif query_type == "references":
        result = await bridge.references(file_path, line, character)
    elif query_type == "symbols":
        result = await bridge.document_symbols(file_path)
    elif query_type == "diagnostics":
        result = await bridge.diagnostics(file_path)
    else:
        return _make_error_response(f"Unknown query_type: {query_type}")

    return _make_success_response(result)


async def lsp_get_symbols(file_path: str) -> dict[str, Any]:
    """Get all symbols in a file."""
    logger.info("LSP_TOOL_CALLED", tool="lsp_get_symbols", file=file_path)

    bridge = get_lsp_bridge()

    if not bridge._initialized:
        init_result = await bridge.start("python")
        if not init_result.success:
            return _make_error_response(f"Failed to start LSP: {init_result.error}")

    result = await bridge.document_symbols(file_path)
    return _make_success_response(result)


async def lsp_get_diagnostics(file_path: str) -> dict[str, Any]:
    """Get errors and warnings for a file."""
    logger.info("LSP_TOOL_CALLED", tool="lsp_get_diagnostics", file=file_path)

    bridge = get_lsp_bridge()

    if not bridge._initialized:
        init_result = await bridge.start("python")
        if not init_result.success:
            return _make_error_response(f"Failed to start LSP: {init_result.error}")

    result = await bridge.diagnostics(file_path)
    return _make_success_response(result)


async def lsp_go_to_definition(file_path: str, line: int, character: int) -> dict[str, Any]:
    """Find where a symbol is defined."""
    logger.info("LSP_TOOL_CALLED", tool="lsp_go_to_definition", file=file_path)

    bridge = get_lsp_bridge()

    if not bridge._initialized:
        init_result = await bridge.start("python")
        if not init_result.success:
            return _make_error_response(f"Failed to start LSP: {init_result.error}")

    result = await bridge.definition(file_path, line, character)
    return _make_success_response(result)


async def lsp_find_references(file_path: str, line: int, character: int) -> dict[str, Any]:
    """Find all references to a symbol."""
    logger.info("LSP_TOOL_CALLED", tool="lsp_find_references", file=file_path)

    bridge = get_lsp_bridge()

    if not bridge._initialized:
        init_result = await bridge.start("python")
        if not init_result.success:
            return _make_error_response(f"Failed to start LSP: {init_result.error}")

    result = await bridge.references(file_path, line, character)
    return _make_success_response(result)


def _make_success_response(lsp_result: Any) -> dict[str, Any]:
    """Create standard RuntimeEnvelope for successful response."""
    return {
        "metrics": {
            "query_time_ms": getattr(lsp_result, "query_time_ms", 0),
            "success": True,
        },
        "trace": {
            "constitutional_floors": ["F4", "F12"],
            "tool_category": "lsp_intelligence",
        },
        "authority": {
            "verdict": "SEAL",
            "required_approval": "none",
            "888_HOLD": False,
        },
        "payload": lsp_result.data if hasattr(lsp_result, "data") else lsp_result,
        "errors": None,
        "meta": {
            "protocol": "LSP",
            "version": "3.17",
            "governance": "read_only_safe",
        },
    }


def _make_error_response(error_message: str) -> dict[str, Any]:
    """Create standard RuntimeEnvelope for error response."""
    return {
        "metrics": {"success": False},
        "trace": {"constitutional_floors": ["F4", "F12"]},
        "authority": {
            "verdict": "VOID",
            "required_approval": "none",
        },
        "payload": None,
        "errors": [{"message": error_message, "code": "LSP_ERROR"}],
        "meta": {"protocol": "LSP"},
    }


def register_lsp_tools(mcp: FastMCP) -> None:
    """Register all LSP tools with FastMCP server."""
    if not MCP_AVAILABLE:
        logger.warning("FastMCP not available - LSP tools not registered")
        return

    @mcp.tool()
    async def lsp_query_tool(file_path: str, query_type: str, line: int = 0, character: int = 0) -> dict[str, Any]:
        return await lsp_query(file_path, query_type, line, character)

    @mcp.tool()
    async def lsp_get_symbols_tool(file_path: str) -> dict[str, Any]:
        return await lsp_get_symbols(file_path)

    @mcp.tool()
    async def lsp_get_diagnostics_tool(file_path: str) -> dict[str, Any]:
        return await lsp_get_diagnostics(file_path)

    @mcp.tool()
    async def lsp_go_to_definition_tool(file_path: str, line: int, character: int) -> dict[str, Any]:
        return await lsp_go_to_definition(file_path, line, character)

    @mcp.tool()
    async def lsp_find_references_tool(file_path: str, line: int, character: int) -> dict[str, Any]:
        return await lsp_find_references(file_path, line, character)

    logger.info("LSP_TOOLS_REGISTERED", count=5)
