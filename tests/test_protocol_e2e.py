import pytest
import asyncio
import os
import sys
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

@pytest.mark.asyncio
async def test_arifosmcp_stdio_e2e_protocol():
    """
    E2E test for arifosmcp tools using the MCP stdio protocol.
    This test starts the server as a subprocess and interacts with it using a real MCP client.
    """
    # 1. Setup server parameters
    # Use sys.executable to ensure we use the same Python environment
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["-m", "arifosmcp.runtime", "stdio"],
        env={
            **os.environ,
            "ARIFOS_PHYSICS_DISABLED": "1",
            "AAA_MCP_OUTPUT_MODE": "debug",
            "ARIFOS_DEV_MODE": "1"
        }
    )

    # 2. Start the stdio client
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the session
            await session.initialize()

            # 3. List tools and verify core tools are present
            tools_response = await session.list_tools()
            tool_names = [t.name for t in tools_response.tools]
            
            print(f"Found tools: {tool_names}")
            
            assert "check_vital" in tool_names
            assert "audit_rules" in tool_names
            assert "arifOS_kernel" in tool_names
            
            # 4. Call check_vital - a safe read-only tool
            # Using call_tool from the session
            result = await session.call_tool("check_vital", {})
            
            # FastMCP usually returns a list of content items, first one being text
            assert len(result.content) > 0
            content_text = result.content[0].text
            envelope = json.loads(content_text)
            
            print(f"check_vital response: {json.dumps(envelope, indent=2)}")
            
            assert envelope["ok"] is True
            assert envelope["tool"] == "check_vital"
            assert envelope["verdict"] in ["SEAL", "PROVISIONAL", "SABAR"]
            
            # 5. Call audit_rules
            result_audit = await session.call_tool("audit_rules", {})
            envelope_audit = json.loads(result_audit.content[0].text)
            
            assert envelope_audit["ok"] is True
            assert "floors" in envelope_audit["payload"]
            assert len(envelope_audit["payload"]["floors"]) >= 13

if __name__ == "__main__":
    asyncio.run(test_arifosmcp_stdio_e2e_protocol())
