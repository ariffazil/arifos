#!/usr/bin/env python3
"""
arifOS Docker MCP Server (stdio mode)
Simple stdio-based MCP for Kimi Code CLI
"""

import json
import subprocess
import sys



def send_message(msg):
    """Send JSON-RPC message"""
    data = json.dumps(msg)
    print(data, flush=True)


def read_message():
    """Read JSON-RPC message"""
    line = sys.stdin.readline()
    if not line:
        return None
    return json.loads(line)


def docker_list():
    try:
        result = subprocess.run(
            ["docker", "ps", "-a", "--format", "{{.Names}}|{{.State}}|{{.Status}}"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        lines = result.stdout.strip().split("\n")
        return "\n".join([f"• {line.replace('|', ' | ')}" for line in lines if line])
    except Exception as e:
        return f"Error: {e}"


def docker_logs(name, tail=10):
    try:
        result = subprocess.run(
            ["docker", "logs", "--tail", str(tail), name],
            capture_output=True,
            text=True,
            timeout=30,
        )
        return result.stdout or result.stderr or "No logs"
    except Exception as e:
        return f"Error: {e}"


def docker_restart(name):
    try:
        result = subprocess.run(
            ["docker", "restart", name], capture_output=True, text=True, timeout=60
        )
        return f"✅ Restarted {name}" if result.returncode == 0 else f"❌ {result.stderr}"
    except Exception as e:
        return f"Error: {e}"


def docker_health():
    try:
        result = subprocess.run(
            ["docker", "ps", "-a", "--format", "{{.Names}}|{{.State}}"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        lines = result.stdout.strip().split("\n")
        report = ["🏥 Container Health:"]
        for line in lines:
            if "|" in line:
                name, state = line.split("|", 1)
                icon = "🟢" if state == "running" else "🔴"
                report.append(f"{icon} {name}: {state}")
        return "\n".join(report)
    except Exception as e:
        return f"Error: {e}"


# Main loop
while True:
    msg = read_message()
    if msg is None:
        break

    method = msg.get("method", "")
    params = msg.get("params", {})
    msg_id = msg.get("id")

    if method == "initialize":
        send_message(
            {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {"tools": {}},
                    "serverInfo": {"name": "arifos-docker-mcp", "version": "1.0.0"},
                },
            }
        )

    elif method == "tools/list":
        send_message(
            {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "tools": [
                        {"name": "docker_list", "description": "List all containers"},
                        {"name": "docker_logs", "description": "Get container logs"},
                        {"name": "docker_restart", "description": "Restart container"},
                        {"name": "docker_health", "description": "Health check"},
                    ]
                },
            }
        )

    elif method == "tools/call":
        tool = params.get("name", "")
        args = params.get("arguments", {})

        if tool == "docker_list":
            result = docker_list()
        elif tool == "docker_logs":
            result = docker_logs(args.get("name", ""), args.get("tail", 10))
        elif tool == "docker_restart":
            result = docker_restart(args.get("name", ""))
        elif tool == "docker_health":
            result = docker_health()
        else:
            result = f"Unknown tool: {tool}"

        send_message(
            {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {"content": [{"type": "text", "text": result}]},
            }
        )
