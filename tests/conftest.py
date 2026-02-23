"""Pytest fixtures for arifOS AAA MCP tests.

Aligned with FastMCP testing guidance:
- use in-memory transport by passing the server instance to Client
- avoid global shared state
"""

from __future__ import annotations

import pytest

from fastmcp import Client

from arifos_aaa_mcp.server import create_aaa_mcp_server


@pytest.fixture
async def aaa_client():
    """In-memory MCP client for the AAA server."""
    async with Client(create_aaa_mcp_server()) as client:
        yield client
