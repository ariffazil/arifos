---
description: How to set up and run the arifOS AAA MCP Server (FastMCP) locally
---

# arifOS Local MCP Startup Workflow

Run the arifOS Constitutional Kernel via the `aaa_mcp` package. Supports three transports: stdio (Claude Code), SSE (Railway), and streamable HTTP (ChatGPT/OpenAI).

## Prerequisites
- Python 3.10+
- `uv` or `pip` for package management

## Setup Steps

### 1. Initialize Workspace
```powershell
cd C:\Users\User\arifOS
```

### 2. Activate Virtual Environment
```powershell
# Activate existing venv (created by uv)
.\.venv\Scripts\Activate.ps1

# Prompt should change to: (arifos) PS C:\Users\User\arifOS>
```
If auto-activation is configured in your PowerShell profile, this happens automatically.

### 3. Install Dependencies
```powershell
# Editable install with dev dependencies (recommended)
pip install -e ".[dev]"
```

### 4. Run the MCP Server
```powershell
# stdio — Claude Code, Claude Desktop (default)
python -m aaa_mcp

# SSE — Railway, legacy remote clients
python -m aaa_mcp sse

# Streamable HTTP — ChatGPT, OpenAI Codex, modern remote
python -m aaa_mcp http
```

The console script `aaa-mcp` is also available after install:
```powershell
aaa-mcp          # stdio
aaa-mcp sse      # SSE
aaa-mcp http     # HTTP
```

## Verify Server Health
```powershell
# Run quick smoke test
pytest tests/test_mcp_quick.py -v

# Run full MCP tool integration tests
pytest tests/test_mcp_all_tools.py -v
```

## Troubleshooting

- **ModuleNotFoundError: aaa_mcp** — Venv is not activated, or editable install is missing. Run `pip install -e ".[dev]"`.
- **ModuleNotFoundError: mcp** — The MCP SDK (`mcp` package) is not installed. It is pulled in automatically by `pip install -e ".[dev]"`.
- **ImportError: cannot import from 'mcp'** — A local `mcp/` directory is shadowing the SDK. Ensure no directory named `mcp/` exists at the project root (it was renamed to `aaa_mcp/`).
- **Port conflict (SSE/HTTP)** — SSE and HTTP transports bind a network port. Ensure no other process is using it. Stdio has no port requirement.
