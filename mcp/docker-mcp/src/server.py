#!/usr/bin/env python3
"""
arifOS Docker MCP Server
13 Floors Constitutional Architecture - F11 Command Floor
Provides Docker container management via Model Context Protocol
"""

import asyncio
import json
import subprocess
import os
from typing import Any, Optional
from mcp.server import Server
from mcp.server.sse import SseServerTransport
from mcp.types import Tool, TextContent
from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.responses import JSONResponse
import uvicorn

# Initialize MCP Server
app = Server("arifos-docker-mcp")
sse = SseServerTransport("/messages/")

# ========== Docker Tools ==========


@app.call_tool()
async def docker_list_containers() -> list[TextContent]:
    """List all Docker containers with their status"""
    try:
        result = subprocess.run(
            ["docker", "ps", "-a", "--format", "json"], capture_output=True, text=True, timeout=30
        )
        containers = []
        for line in result.stdout.strip().split("\n"):
            if line:
                containers.append(json.loads(line))

        # Format for readability
        output = []
        for c in containers:
            output.append(
                f"[{c.get('State', 'unknown').upper()}] {c.get('Names', 'unknown')} ({c.get('Image', 'unknown')}) - {c.get('Status', 'unknown')}"
            )

        return [
            TextContent(type="text", text="\n".join(output) if output else "No containers found")
        ]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


@app.call_tool()
async def docker_inspect_container(name: str) -> list[TextContent]:
    """Inspect a specific container"""
    try:
        result = subprocess.run(
            ["docker", "inspect", name], capture_output=True, text=True, timeout=30
        )
        if result.returncode != 0:
            return [TextContent(type="text", text=f"Error: {result.stderr}")]

        data = json.loads(result.stdout)[0]

        # Extract key info
        info = {
            "Name": data.get("Name", "").lstrip("/"),
            "State": data.get("State", {}),
            "Config": {
                "Image": data.get("Config", {}).get("Image"),
                "Env": data.get("Config", {}).get("Env", [])[:5],  # First 5 env vars
            },
            "NetworkSettings": {
                "Ports": data.get("NetworkSettings", {}).get("Ports", {}),
                "IPAddress": data.get("NetworkSettings", {}).get("IPAddress"),
            },
            "HostConfig": {
                "Privileged": data.get("HostConfig", {}).get("Privileged"),
                "Memory": data.get("HostConfig", {}).get("Memory"),
                "CpuShares": data.get("HostConfig", {}).get("CpuShares"),
            },
        }

        return [TextContent(type="text", text=json.dumps(info, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


@app.call_tool()
async def docker_container_logs(name: str, tail: int = 20) -> list[TextContent]:
    """Get logs from a container"""
    try:
        result = subprocess.run(
            ["docker", "logs", "--tail", str(tail), name],
            capture_output=True,
            text=True,
            timeout=30,
        )
        return [TextContent(type="text", text=result.stdout or result.stderr or "No logs")]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


@app.call_tool()
async def docker_start_container(name: str) -> list[TextContent]:
    """Start a stopped container"""
    try:
        result = subprocess.run(
            ["docker", "start", name], capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            return [TextContent(type="text", text=f"✅ Container {name} started successfully")]
        else:
            return [TextContent(type="text", text=f"❌ Failed: {result.stderr}")]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


@app.call_tool()
async def docker_stop_container(name: str, timeout: int = 30) -> list[TextContent]:
    """Stop a running container"""
    try:
        result = subprocess.run(
            ["docker", "stop", "-t", str(timeout), name],
            capture_output=True,
            text=True,
            timeout=timeout + 10,
        )
        if result.returncode == 0:
            return [TextContent(type="text", text=f"✅ Container {name} stopped successfully")]
        else:
            return [TextContent(type="text", text=f"❌ Failed: {result.stderr}")]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


@app.call_tool()
async def docker_restart_container(name: str) -> list[TextContent]:
    """Restart a container"""
    try:
        result = subprocess.run(
            ["docker", "restart", name], capture_output=True, text=True, timeout=60
        )
        if result.returncode == 0:
            return [TextContent(type="text", text=f"✅ Container {name} restarted successfully")]
        else:
            return [TextContent(type="text", text=f"❌ Failed: {result.stderr}")]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


@app.call_tool()
async def docker_exec_command(name: str, command: str) -> list[TextContent]:
    """Execute a command inside a container"""
    try:
        result = subprocess.run(
            ["docker", "exec", name, "sh", "-c", command],
            capture_output=True,
            text=True,
            timeout=30,
        )
        output = result.stdout if result.stdout else result.stderr
        return [TextContent(type="text", text=output or "Command executed (no output)")]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


@app.call_tool()
async def docker_health_check() -> list[TextContent]:
    """Check health of all containers in Sovereign Stack"""
    try:
        result = subprocess.run(
            [
                "docker",
                "ps",
                "-a",
                "--filter",
                "name=agentzero|openclaw|qdrant|arifos",
                "--format",
                "json",
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )

        containers = []
        for line in result.stdout.strip().split("\n"):
            if line:
                containers.append(json.loads(line))

        # Check health
        report = ["🏥 Sovereign Stack Health Report", "=" * 40]

        for c in containers:
            name = c.get("Names", "unknown")
            state = c.get("State", "unknown")
            status = c.get("Status", "")
            health = c.get("Health", "unknown")

            icon = "🟢" if state == "running" else "🔴" if state == "exited" else "🟡"
            report.append(f"{icon} {name}: {state} ({status})")

        return [TextContent(type="text", text="\n".join(report))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


# ========== MCP Server Setup ==========


@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(name="docker_list_containers", description="List all Docker containers"),
        Tool(name="docker_inspect_container", description="Inspect a specific container"),
        Tool(name="docker_container_logs", description="Get container logs"),
        Tool(name="docker_start_container", description="Start a stopped container"),
        Tool(name="docker_stop_container", description="Stop a running container"),
        Tool(name="docker_restart_container", description="Restart a container"),
        Tool(name="docker_exec_command", description="Execute command inside container"),
        Tool(name="docker_health_check", description="Check Sovereign Stack health"),
    ]


# HTTP Routes
async def handle_sse(request):
    async with sse.connect_sse(request.scope, request.receive, request._send) as streams:
        await app.run(streams[0], streams[1], app.create_initialization_options())


async def handle_messages(request):
    await sse.handle_post_message(request.scope, request.receive, request._send)


async def health(request):
    return JSONResponse({"status": "ok", "mode": "sovereign"})


# Create Starlette app
starlette_app = Starlette(
    debug=True,
    routes=[
        Route("/", health),
        Route("/health", health),
        Route("/sse", endpoint=handle_sse),
        Mount("/messages/", app=handle_messages),
    ],
)

if __name__ == "__main__":
    print("🚀 arifOS Docker MCP Server starting...")
    print("📡 Mode: Sovereign (F11 Command Floor)")
    print("🔗 Endpoint: http://0.0.0.0:8080/sse")
    uvicorn.run(starlette_app, host="0.0.0.0", port=8080)
