"""
arifOS MCP Stdio Transport
Standard input/output transport for local clients (Claude Desktop, Cursor).

v55.1: Spec-compliant tool listing with outputSchema, annotations, title.
       Structured JSON output alongside human-readable text.
       Hardened resource/prompt handlers with error handling.
"""

import json as _json
import logging
import sys
import time
from typing import Any

try:
    import mcp.types as mcp_types
except ImportError:
    # mcp >= 1.3.0 changed the package structure
    from mcp.server import types as mcp_types
from mcp.server import Server
from mcp.server.stdio import stdio_server

from ...enforcement.metrics import record_stage_metrics, record_verdict_metrics
from ...system.orchestrator.presenter import AAAMetabolizer
from ..config.modes import get_mcp_mode
from ..core.session_context import get_current_session_id, set_current_session_id
from ..core.tool_registry import ToolRegistry
from ..services.constitutional_metrics import record_verdict
from .base import BaseTransport

logger = logging.getLogger(__name__)


class StdioTransport(BaseTransport):
    """Stdio transport implementation using mcp-python SDK."""

    def __init__(self, tool_registry: ToolRegistry):
        super().__init__(tool_registry)
        self.server = Server("arifOS-Stdio")
        self.presenter = AAAMetabolizer()

    @property
    def name(self) -> str:
        return "stdio"

    async def start(self) -> None:
        """Start the MCP server over stdio."""
        mode = get_mcp_mode()
        print(
            f"[BOOT] arifOS MCP v55.1 StdioTransport starting in {mode.value} mode",
            file=sys.stderr,
        )

        # Register handlers
        self._register_handlers()

        # Run the server
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream, write_stream, self.server.create_initialization_options()
            )

    async def stop(self) -> None:
        pass  # Stdio server handles its own cleanup context

    async def send_response(self, request_id: str, response: Any) -> None:
        pass  # Handled internally by mcp server

    def _register_handlers(self):
        """Register tool, resource, and prompt handlers with the internal MCP server."""

        # --- TOOLS ---
        @self.server.list_tools()
        async def handle_list_tools() -> list[mcp_types.Tool]:
            tools = []
            for name, tool_def in self.tool_registry.list_tools().items():
                # Build ToolAnnotations from registry dict
                annotations = None
                if tool_def.annotations:
                    annotations = mcp_types.ToolAnnotations(
                        title=tool_def.annotations.get("title"),
                        readOnlyHint=tool_def.annotations.get("readOnlyHint"),
                        destructiveHint=tool_def.annotations.get("destructiveHint"),
                        idempotentHint=tool_def.annotations.get("idempotentHint"),
                        openWorldHint=tool_def.annotations.get("openWorldHint"),
                    )

                tools.append(
                    mcp_types.Tool(
                        name=tool_def.name,
                        title=tool_def.title,
                        description=tool_def.description,
                        inputSchema=tool_def.input_schema,
                        outputSchema=tool_def.output_schema,
                        annotations=annotations,
                    )
                )
            return tools

        @self.server.call_tool()
        async def handle_call_tool(
            name: str, arguments: dict | None
        ) -> list[mcp_types.TextContent | mcp_types.ImageContent | mcp_types.EmbeddedResource]:
            start_time = time.time()
            arguments = arguments or {}
            tool_def = self.tool_registry.get(name)

            if not tool_def:
                raise ValueError(f"Tool not found: {name}")

            # Implicit Session Binding: Extract or inject session_id
            session_id = arguments.get("session_id") or get_current_session_id()
            if session_id:
                set_current_session_id(session_id)
                if "session_id" not in arguments:
                    arguments["session_id"] = session_id

            try:
                result = await tool_def.handler(**arguments)

                # Metrics
                duration = time.time() - start_time
                duration_ms = duration * 1000
                verdict = result.get("verdict", "UNKNOWN")
                mode = get_mcp_mode()

                record_verdict(tool=name, verdict=verdict, duration=duration, mode=mode.value)
                record_stage_metrics(name, duration_ms)
                record_verdict_metrics(verdict)

                # Update implicit context if result contains a new session_id
                new_session_id = result.get("session_id")
                if new_session_id:
                    set_current_session_id(new_session_id)

                # Return human-readable presentation + machine-readable JSON
                formatted_text = self.presenter.process(result)
                return [
                    mcp_types.TextContent(type="text", text=formatted_text),
                    mcp_types.TextContent(type="text", text=_json.dumps(result, default=str)),
                ]

            except Exception as e:
                logger.error(f"Error executing tool {name}: {e}")
                return [mcp_types.TextContent(type="text", text=f"ERROR: {str(e)}")]

        # --- RESOURCES ---
        @self.server.list_resources()
        async def handle_list_resources() -> list[mcp_types.Resource]:
            resources = []
            for res_def in self.resource_registry.list_resources():
                resources.append(
                    mcp_types.Resource(
                        uri=res_def.uri,
                        name=res_def.name,
                        description=res_def.description,
                        mimeType=res_def.mime_type,
                    )
                )
            return resources

        @self.server.read_resource()
        async def handle_read_resource(uri) -> str:
            # SDK passes AnyUrl; convert to str for our registry
            uri_str = str(uri)
            try:
                return self.resource_registry.read_resource(uri_str)
            except ValueError as e:
                logger.warning(f"Unknown resource URI: {uri_str}")
                return _json.dumps({"error": str(e), "uri": uri_str})
            except Exception as e:
                logger.error(f"Error reading resource {uri_str}: {e}")
                return _json.dumps({"error": f"Internal error: {str(e)}", "uri": uri_str})

        # --- PROMPTS ---
        @self.server.list_prompts()
        async def handle_list_prompts() -> list[mcp_types.Prompt]:
            prompts = []
            for prompt_def in self.prompt_registry.list_prompts():
                args = None
                if prompt_def.arguments:
                    args = [
                        mcp_types.PromptArgument(
                            name=arg["name"],
                            description=arg.get("description", ""),
                            required=arg.get("required", "false") == "true",
                        )
                        for arg in prompt_def.arguments
                    ]
                prompts.append(
                    mcp_types.Prompt(
                        name=prompt_def.name,
                        description=prompt_def.description,
                        arguments=args,
                    )
                )
            return prompts

        @self.server.get_prompt()
        async def handle_get_prompt(
            name: str, arguments: dict | None = None
        ) -> mcp_types.GetPromptResult:
            try:
                text = self.prompt_registry.render_prompt(name, arguments)
                return mcp_types.GetPromptResult(
                    description=f"Constitutional prompt: {name}",
                    messages=[
                        mcp_types.PromptMessage(
                            role="user",
                            content=mcp_types.TextContent(type="text", text=text),
                        )
                    ],
                )
            except ValueError as e:
                logger.warning(f"Prompt not found: {name}")
                return mcp_types.GetPromptResult(
                    description=f"Error: {str(e)}",
                    messages=[
                        mcp_types.PromptMessage(
                            role="user",
                            content=mcp_types.TextContent(type="text", text=str(e)),
                        )
                    ],
                )
