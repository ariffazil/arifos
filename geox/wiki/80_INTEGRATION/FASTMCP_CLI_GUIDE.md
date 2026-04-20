# FastMCP CLI Guide for GEOX

> **Version:** 0.5.0 · **Status:** 🔐 SEALED  
> **Motto:** *DITEMPA BUKAN DIBERI*

This guide covers running and deploying GEOX using the FastMCP CLI.

---

## Table of Contents

1. [Quick Start](#1-quick-start)
2. [Run Modes](#2-run-modes)
3. [Development Tools](#3-development-tools)
4. [Server Inspection](#4-server-inspection)
5. [Client Integration](#5-client-integration)
6. [VPS Deployment](#6-vps-deployment)
7. [Configuration](#7-configuration)

---

## 1. Quick Start

### Prerequisites

```bash
# Install FastMCP with apps support
pip install "fastmcp[apps]>=2.0.0"

# Verify installation
fastmcp --version
```

### Basic Usage

```bash
# Clone and setup
git clone https://github.com/ariffazil/arifos-geox.git
cd arifos-geox
pip install -e ".[dev]"

# Run in stdio mode (Claude Desktop)
fastmcp run geox_mcp_server.py

# Or use the config file
fastmcp run fastmcp.json
```

---

## 2. Run Modes

### 2.1 Stdio Mode (Local Development)

For Claude Desktop, Cursor, and local testing:

```bash
# Default stdio mode
fastmcp run geox_mcp_server.py

# Explicit stdio
fastmcp run geox_mcp_server.py:mcp --transport stdio

# With logging
fastmcp run geox_mcp_server.py --log-level debug
```

### 2.2 HTTP Mode (Server Deployment)

For VPS, cloud, or remote access:

```bash
# HTTP mode
fastmcp run geox_mcp_server.py --transport http --host 0.0.0.0 --port 8000

# Using factory function (advanced)
fastmcp run geox_mcp_server.py:create_server --transport http --port 9000

# Production with config file
fastmcp run fastmcp.json
```

### 2.3 Factory Function Pattern

For programmatic configuration:

```bash
# Factory function with custom args
fastmcp run arifos.geox.tools.adapters.fastmcp_adapter:create_server \
  --transport http \
  --host 127.0.0.1 \
  --port 8080
```

**Python API:**

```python
from arifos.geox.tools.adapters.fastmcp_adapter import create_server

# Create configured server
mcp = create_server(
    transport="http",
    host="0.0.0.0",
    port=8000
)

# Run (or let CLI handle it)
mcp.run(transport="http", host="0.0.0.0", port=8000)
```

---

## 3. Development Tools

### 3.1 Prefab UI Preview

Preview GEOX Apps in a browser with hot reload:

```bash
# Basic preview
fastmcp dev apps geox_mcp_server.py

# With custom ports
fastmcp dev apps geox_mcp_server.py \
  --mcp-port 8000 \
  --dev-port 8080

# With specific app
fastmcp dev apps geox_mcp_server.py \
  --app geox.seismic.viewer
```

### 3.2 MCP Inspector

Interactive testing and debugging:

```bash
# Launch inspector
fastmcp dev inspector geox_mcp_server.py

# Inspector with HTTP
fastmcp dev inspector geox_mcp_server.py --transport http --port 8000
```

The Inspector provides:
- Tool discovery and testing
- Real-time request/response inspection
- Schema validation
- Performance metrics

---

## 4. Server Inspection

### 4.1 List Tools

```bash
# List all available tools
fastmcp list geox_mcp_server.py

# List with details
fastmcp list geox_mcp_server.py --verbose

# List from remote server
fastmcp list https://geox.arif-fazil.com/mcp
```

**Example Output:**
```
GEOX Earth Witness v0.5.0 — DITEMPA BUKAN DIBERI

Tools (11):
  geox_load_seismic_line        Load seismic data and ignite visual mode
  geox_build_structural_candidates  Build structural model candidates
  geox_feasibility_check        Check if plan is physically possible
  geox_verify_geospatial        Verify geospatial grounding
  geox_evaluate_prospect        Provide governed prospect verdict
  geox_query_memory             Query geological memory store
  geox_health                   Server health check
  geox_select_sw_model          Evaluate Sw model admissibility
  geox_compute_petrophysics     Full petrophysics pipeline
  geox_validate_cutoffs         Apply cutoff policy
  geox_petrophysical_hold_check Constitutional floor check
```

### 4.2 Inspect Server

```bash
# Inspect capabilities
fastmcp inspect geox_mcp_server.py

# Inspect with config
fastmcp inspect fastmcp.json
```

### 4.3 Call Tools

```bash
# Health check
fastmcp call geox_mcp_server.py geox_health

# Evaluate prospect
fastmcp call geox_mcp_server.py geox_evaluate_prospect \
  prospect_id="PROSPECT-001" \
  interpretation_id="INT-001"

# Select Sw model
fastmcp call geox_mcp_server.py geox_select_sw_model \
  well_id="WELL-001" \
  depth_top_m=1500 \
  depth_base_m=1600 \
  has_shale=true \
  vsh_max=0.25

# With JSON args
fastmcp call geox_mcp_server.py geox_compute_petrophysics '{
  "well_id": "WELL-001",
  "sw_model": "archie",
  "rw_ohm_m": 0.1,
  "rt_ohm_m": 10.0,
  "phi_fraction": 0.25
}'
```

### 4.4 Discover Servers

```bash
# Discover configured servers
fastmcp discover

# Discover with details
fastmcp discover --verbose
```

---

## 5. Client Integration

### 5.1 Claude Desktop

```bash
# Install to Claude Desktop
fastmcp install geox_mcp_server.py --client claude-desktop

# Install with environment
fastmcp install geox_mcp_server.py \
  --client claude-desktop \
  --env-file .env

# Uninstall
fastmcp uninstall geox_mcp_server.py --client claude-desktop
```

**Manual Configuration:**

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "geox": {
      "command": "fastmcp",
      "args": ["run", "/path/to/geox_mcp_server.py"],
      "env": {
        "GEOX_VERSION": "0.5.0",
        "GEOX_SEAL": "DITEMPA BUKAN DIBERI"
      }
    }
  }
}
```

### 5.2 Cursor

```bash
# Install to Cursor
fastmcp install geox_mcp_server.py --client cursor

# Or manual: Add to ~/.cursor/mcp.json
```

### 5.3 Claude Code

```bash
# Install to Claude Code
fastmcp install geox_mcp_server.py --client claude-code
```

### 5.4 Custom Client

```json
{
  "mcpServers": {
    "geox": {
      "command": "python",
      "args": ["-m", "arifos.geox.tools.adapters.fastmcp_adapter"],
      "transport": "stdio"
    }
  }
}
```

---

## 6. VPS Deployment

### 6.1 Direct FastMCP CLI

```bash
# SSH to VPS
ssh srv1325122.hstgr.cloud

cd /opt/arifos/geox
git pull origin main

# Run with FastMCP CLI
fastmcp run geox_mcp_server.py \
  --transport http \
  --host 0.0.0.0 \
  --port 8000

# Or with factory function
fastmcp run arifos.geox.tools.adapters.fastmcp_adapter:create_server \
  --transport http \
  --host 0.0.0.0 \
  --port 8000
```

### 6.2 Systemd Service

Create `/etc/systemd/system/geox.service`:

```ini
[Unit]
Description=GEOX Earth Witness MCP Server
After=network.target

[Service]
Type=simple
User=geox
WorkingDirectory=/opt/arifos/geox
Environment=GEOX_VERSION=0.5.0
Environment=GEOX_SEAL=DITEMPA BUKAN DIBERI
Environment=PYTHONPATH=/opt/arifos/geox
ExecStart=/usr/local/bin/fastmcp run geox_mcp_server.py --transport http --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start
sudo systemctl enable geox
sudo systemctl start geox
sudo systemctl status geox
```

### 6.3 Docker Compose

Using `fastmcp.json` config:

```yaml
# docker-compose.yml
services:
  geox:
    image: python:3.11-slim
    container_name: geox_server
    working_dir: /app
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    environment:
      - GEOX_VERSION=0.5.0
      - GEOX_SEAL=DITEMPA BUKAN DIBERI
    command: >
      sh -c "pip install -e '.[dev]' && fastmcp run fastmcp.json"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

```bash
docker compose up -d geox
docker compose logs -f geox
```

### 6.4 Health Checks

```bash
# Health endpoint
curl https://geox.arif-fazil.com/health
# Output: OK

# Detailed health
curl https://geox.arif-fazil.com/health/details
# Output: {"ok": true, "version": "0.5.0", ...}

# Tool list
curl -X POST https://geox.arif-fazil.com/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'

# Using FastMCP CLI
fastmcp list https://geox.arif-fazil.com/mcp
```

---

## 7. Configuration

### 7.1 Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `GEOX_TRANSPORT` | `stdio` | Transport: `stdio` or `http` |
| `GEOX_HOST` | `0.0.0.0` | HTTP bind host |
| `GEOX_PORT` | `8000` | HTTP bind port |
| `GEOX_VERSION` | `0.5.0` | Server version |
| `GEOX_SEAL` | `DITEMPA BUKAN DIBERI` | Constitutional seal |
| `GEOX_LOG_LEVEL` | `INFO` | Logging level |

### 7.2 fastmcp.json Config

```json
{
  "$schema": "https://gofastmcp.com/schemas/fastmcp.json",
  "name": "geox-earth-witness",
  "version": "0.5.0",
  "entrypoint": "geox_mcp_server.py:mcp",
  "transport": {
    "stdio": { "enabled": true },
    "http": {
      "enabled": true,
      "host": "0.0.0.0",
      "port": 8000,
      "path": "/mcp"
    }
  },
  "dependencies": [
    "fastmcp[apps]>=2.0.0"
  ],
  "tools": {
    "visibility": {
      "model": ["geox_*"],
      "app": ["geox_*"]
    }
  }
}
```

### 7.3 Architecture Selection

**Legacy / transitional root path:**
```bash
fastmcp run geox_mcp_server.py
```

**Preferred modular path:**
```bash
fastmcp run arifos.geox.tools.adapters.fastmcp_adapter:create_server
```

They do **not** represent the exact same tool surface today.

- The **preferred modular path** is the refactor target and should be treated as canonical for new integration work.
- The **root path** is still present for compatibility and historical reasons, but it has drifted into a separate server surface.

If you are wiring GEOX into another system, prefer the modular adapter path unless you explicitly need the root transitional server.

---

## Command Reference

| Command | Purpose |
|---------|---------|
| `fastmcp run` | Production server |
| `fastmcp run ...:create_server` | Factory pattern |
| `fastmcp dev apps` | Prefab UI preview |
| `fastmcp dev inspector` | Interactive testing |
| `fastmcp list` | Tool inventory |
| `fastmcp call` | Tool testing |
| `fastmcp inspect` | Capabilities |
| `fastmcp discover` | Server discovery |
| `fastmcp install` | Client integration |
| `fastmcp uninstall` | Remove from client |

---

*DITEMPA BUKAN DIBERI — Forged, not given.*
