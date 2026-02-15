# ACLIP_CAI — arifOS Console Intelligence & Perception Console

**The 9-Sense Nervous System for arifOS Infrastructure**

```
╔══════════════════════════════════════════════════════════════════╗
║                    ACLIP_CAI v1.0.0                              ║
║          Console Intelligence & Perception Console               ║
║                                                                  ║
║    ┌─────────────────────────────────────────────────────────┐   ║
║    │  9-Tool Nervous System — Read-Only Perception Layer     │   ║
║    │  (Console-only • No Ethics • Pure Data)                 │   ║
║    └─────────────────────────────────────────────────────────┘   ║
╚══════════════════════════════════════════════════════════════════╝
```

---

## Overview

ACLIP_CAI provides **infrastructure observability** for arifOS through a 9-tool nervous system. It is the **sensory layer** that feeds data into the aaa-mcp 9-law constitutional pipeline.

### Key Characteristics

| Property | Value |
|----------|-------|
| **Philosophy** | Console-only, no ethics layer |
| **Safety Model** | Read-only (except forge_guard gating) |
| **Response Target** | < 100ms per tool |
| **Integration** | aaa-mcp 9-law pipeline |
| **MCP Prefix** | `aclip_*` |

---

## The 9 Senses

| # | Tool | Purpose | MCP Name | Mode |
|---|------|---------|----------|------|
| 1 | **system_health** | CPU, memory, disk, load metrics | `aclip_system_health` | Read |
| 2 | **process_list** | Process inspection and filtering | `aclip_process_list` | Read |
| 3 | **fs_inspect** | Filesystem traversal and analysis | `aclip_fs_inspect` | Read |
| 4 | **log_tail** | Log file monitoring and search | `aclip_log_tail` | Read |
| 5 | **net_status** | Network connectivity and diagnostics | `aclip_net_status` | Read |
| 6 | **config_flags** | Configuration validation and flags | `aclip_config_flags` | Read |
| 7 | **chroma_query** | Vector DB semantic search | `aclip_chroma_query` | Read |
| 8 | **cost_estimator** | Resource usage and cost projection | `aclip_cost_estimator` | Read |
| 9 | **forge_guard** | Gating decisions for actions | `aclip_forge_guard` | **Decision** |

---

## Installation

```bash
# ACLIP_CAI is included in arifOS
pip install -e /root/arifOS

# Or directly
python -m pip install -e /root/arifOS/aclip_cai
```

---

## Usage

### CLI Mode

```bash
# System health
python -m aclip_cai health

# List Python processes using >10% CPU
python -m aclip_cai processes --filter python --min-cpu 10.0

# Inspect filesystem
python -m aclip_cai fs --path /root/arifOS --pattern "*.py" --depth 3

# Tail logs with grep
python -m aclip_cai logs --path /var/log/syslog --lines 100 --grep "error"

# Network diagnostics
python -m aclip_cai net --ping google.com

# Configuration inspection
python -m aclip_cai config --path /root/arifOS/pyproject.toml

# ChromaDB semantic search
python -m aclip_cai chroma --query "constitutional AI safety" --collection docs

# Cost estimation
python -m aclip_cai cost --type llm --tokens 1000 --model gpt-4

# Forge guard (dry-run evaluation)
python -m aclip_cai guard --action deploy --target /app/new-version --risk medium

# Forge guard (with approval gate)
python -m aclip_cai guard --action modify --target /etc/nginx/nginx.conf --risk high --approve
```

### Python API

```python
import asyncio
from aclip_cai import system_health, process_list, forge_guard

async def main():
    # Quick health check
    health = await system_health(include_swap=True)
    print(f"CPU Load: {health.data['cpu']['load_1m']}")
    print(f"Memory: {health.data['memory']['usage_percent']}%")
    
    # List processes
    procs = await process_list(filter_name="python", limit=10)
    for p in procs.data['processes']:
        print(f"{p['pid']}: {p['name']} ({p['cpu_percent']}% CPU)")
    
    # Forge guard evaluation
    verdict = await forge_guard(
        action="deploy",
        target="/app/production",
        session_id="sess-123",
        risk_level="medium",
        dry_run=True,
    )
    print(f"Verdict: {verdict.data['verdict']}")

asyncio.run(main())
```

### MCP Integration (via aaa-mcp)

All tools are registered as MCP tools with the `aclip_` prefix:

```python
# In aaa-mcp server context
from aaa_mcp.server import mcp
from aclip_cai.mcp_bridge import register_aclip_tools

# Register all 9 tools
register_aclip_tools(mcp)

# Now callable as:
# - aclip_system_health
# - aclip_process_list
# - aclip_fs_inspect
# - aclip_log_tail
# - aclip_net_status
# - aclip_config_flags
# - aclip_chroma_query
# - aclip_cost_estimator
# - aclip_forge_guard
```

---

## 9-Law Pipeline Integration

ACLIP_CAI tools integrate with the aaa-mcp 9-law constitutional pipeline at specific stages:

```
┌─────────────────────────────────────────────────────────────────┐
│                    aaa-mcp 9-Law Pipeline                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Law 1: INIT          → Session initialization                  │
│                       → [No ACLIP_CAI tool]                     │
│                                                                 │
│  Law 2: SENSE         → Intent classification                   │
│                       → [No ACLIP_CAI tool]                     │
│                                                                 │
│  Law 3: GROUND        → Evidence gathering                      │
│                       → aclip_system_health                     │
│                       → aclip_fs_inspect                        │
│                       → aclip_config_flags                      │
│                                                                 │
│  Law 4: THINK         → Hypothesis generation                   │
│                       → [No ACLIP_CAI tool]                     │
│                                                                 │
│  Law 5: SEARCH        → Information retrieval                   │
│                       → aclip_chroma_query                      │
│                       → aclip_log_tail                          │
│                                                                 │
│  Law 6: EMPATHIZE     → Stakeholder impact                      │
│                       → [No ACLIP_CAI tool]                     │
│                                                                 │
│  Law 7: GUARD         → Action gating                           │
│                       → aclip_forge_guard ★                     │
│                                                                 │
│  Law 8: ALIGN         → Ethics reconciliation                   │
│                       → [No ACLIP_CAI tool]                     │
│                                                                 │
│  Law 9: VERDICT       → Final judgment                          │
│                       → [No ACLIP_CAI tool]                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Integration Points

| Pipeline Stage | ACLIP_CAI Tools | Purpose |
|---------------|-----------------|---------|
| **Law 3 (GROUND)** | `aclip_system_health`, `aclip_fs_inspect`, `aclip_config_flags` | Gather system evidence |
| **Law 5 (SEARCH)** | `aclip_chroma_query`, `aclip_log_tail` | Retrieve logs and semantic data |
| **Law 7 (GUARD)** | `aclip_forge_guard` | Gate action execution |

---

## Tool Specifications

### 1. system_health

**Purpose**: Retrieve comprehensive system health metrics.

**Parameters**:
- `include_swap`: bool = True — Include swap/memory statistics
- `include_io`: bool = False — Include disk I/O statistics
- `include_temp`: bool = False — Include thermal readings

**Returns**: CPU load, memory usage, disk usage, uptime.

**Example**:
```json
{
  "tool": "system_health",
  "status": "ok",
  "timestamp": "2026-02-13T09:30:00Z",
  "data": {
    "cpu": {"load_1m": 0.5, "load_5m": 0.3, "cores": 8},
    "memory": {"usage_percent": 45.2, "total_bytes": 16777216000},
    "disk": {"root": {"usage_percent": 62.1}}
  },
  "latency_ms": 12.5
}
```

---

### 2. process_list

**Purpose**: List and filter system processes.

**Parameters**:
- `filter_name`: Optional[str] — Filter by process name
- `filter_user`: Optional[str] — Filter by username
- `min_cpu_percent`: float = 0.0 — Minimum CPU percentage
- `min_memory_mb`: float = 0.0 — Minimum memory usage
- `limit`: int = 50 — Maximum results
- `include_threads`: bool = False — Include thread count

**Returns**: Process list with PID, name, CPU%, memory.

---

### 3. fs_inspect

**Purpose**: Inspect filesystem structure and file metadata.

**Parameters**:
- `path`: str = "/root/arifOS" — Root path to inspect
- `max_depth`: int = 2 — Maximum directory depth
- `include_hidden`: bool = False — Include hidden files
- `min_size_bytes`: int = 0 — Minimum file size
- `pattern`: Optional[str] — Glob pattern (e.g., "*.py")
- `max_files`: int = 100 — Maximum files to return

**Returns**: File tree with metadata (size, permissions, modified time).

---

### 4. log_tail

**Purpose**: Tail and search log files.

**Parameters**:
- `log_path`: str — Path to log file
- `lines`: int = 50 — Number of lines
- `grep_pattern`: Optional[str] — Regex filter pattern
- `since_minutes`: Optional[int] — Time window filter

**Returns**: Log entries with parsed timestamps and levels.

---

### 5. net_status

**Purpose**: Network connectivity and interface status.

**Parameters**:
- `check_interfaces`: bool = True — Include interface status
- `check_connections`: bool = True — Include active connections
- `check_routing`: bool = True — Include routing table
- `target_host`: Optional[str] — Host to ping test

**Returns**: Interface stats, connections, routing, ping results.

---

### 6. config_flags

**Purpose**: Inspect configuration files and environment variables.

**Parameters**:
- `config_path`: Optional[str] — Path to config file
- `env_prefix`: Optional[str] = "ARIFOS" — Environment variable prefix
- `include_secrets`: bool = False — Show secrets (masked by default)

**Returns**: Configuration data with secrets masked.

**Security**: Secrets are automatically masked unless `include_secrets=True`.

---

### 7. chroma_query

**Purpose**: Query ChromaDB vector store for semantic search.

**Parameters**:
- `query_text`: str — Text to search for
- `collection_name`: str = "default" — ChromaDB collection
- `n_results`: int = 5 — Number of results
- `where_filter`: Optional[dict] — Metadata filter
- `include_embeddings`: bool = False — Include vectors

**Returns**: Semantic search results with distances.

---

### 8. cost_estimator

**Purpose**: Estimate costs for AI operations and infrastructure.

**Parameters**:
- `operation_type`: str — Type: llm, embedding, storage, compute
- `token_count`: Optional[int] — Token count
- `compute_seconds`: Optional[float] — Compute time
- `storage_gb`: Optional[float] — Storage in GB
- `api_calls`: Optional[int] — API call count
- `provider`: str = "openai" — LLM provider
- `model`: str = "gpt-4" — Model name

**Returns**: Cost breakdown in USD.

---

### 9. forge_guard

**Purpose**: Gating decisions for system modifications. **The only non-read tool.**

**Parameters**:
- `action`: str — Action to evaluate (deploy, modify, delete, execute)
- `target`: str — Target resource
- `session_id`: str — aaa-mcp session ID
- `risk_level`: str = "low" — low/medium/high/critical
- `justification`: str = "" — Reason for action
- `dry_run`: bool = True — Only evaluate
- `require_approval`: bool = False — Mandate approval

**Returns**: Verdict (SEAL/VOID/PARTIAL/SABAR/888_HOLD).

**Constitutional Floors**: F1, F7, F11 (only ACLIP_CAI tool with floors)

**Example**:
```json
{
  "tool": "forge_guard",
  "status": "ok",
  "data": {
    "verdict": "SABAR",
    "action": "deploy",
    "target": "/app/new-version",
    "can_proceed": false,
    "dry_run": true,
    "recommendations": [
      "Review target scope before execution",
      "Ensure backup is available"
    ]
  },
  "motto": "DITEMPA BUKAN DIBERI 🔥",
  "floors_enforced": ["F1", "F7", "F11"],
  "pass": "hold"
}
```

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        ACLIP_CAI Architecture                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                    MCP Bridge Layer                      │    │
│  │  (aclip_* tools registered with aaa-mcp server)         │    │
│  └─────────────────────────────────────────────────────────┘    │
│                            │                                    │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                    Tool Implementation                   │    │
│  │  (console_tools.py — 9 async functions)                 │    │
│  └─────────────────────────────────────────────────────────┘    │
│                            │                                    │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                    System Interface                      │    │
│  │  (/proc, subprocess, filesystem, ChromaDB)              │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Response Format

All tools return a `ToolResponse` dataclass:

```python
@dataclass
class ToolResponse:
    tool: str           # Tool name
    status: str         # "ok" | "error" | "warning"
    timestamp: str      # ISO 8601 UTC
    data: dict          # Tool-specific data
    error: Optional[str] # Error message if status="error"
    latency_ms: float   # Response time in milliseconds
```

---

## Safety & Security

### Read-Only Design

- 8 of 9 tools are strictly read-only
- No filesystem modifications
- No process modifications
- No network modifications
- No configuration changes

### Secret Masking

`aclip_config_flags` automatically masks:
- `*key*`
- `*secret*`
- `*pass*`
- `*token*`
- `*pwd*`

### Forge Guard Protections

`aclip_forge_guard` blocks dangerous patterns:
- `rm -rf /`
- `dd if=* of=/dev/*`
- `mkfs.*`
- Fork bombs
- Direct password file manipulation

### Constitutional Floors

Only `aclip_forge_guard` has constitutional floors:
- **F1 Amanah**: Trust and responsibility
- **F7 Humility**: Acknowledge uncertainty
- **F11 Sovereignty**: Human authority

---

## Testing

```bash
# Run all tool tests
pytest tests/aclip_cai/ -v

# Test specific tool
pytest tests/aclip_cai/test_system_health.py -v

# Integration test with MCP
python -m aclip_cai health | jq .
```

---

## Roadmap

| Version | Feature |
|---------|---------|
| v1.1.0 | Prometheus metrics export |
| v1.2.0 | Real-time log streaming (WebSocket) |
| v1.3.0 | Multi-node cluster health |
| v2.0.0 | Full observability dashboard |

---

## License

AGPL-3.0-only — See /root/arifOS/LICENSE

---

## References

- [aaa-mcp 9-Law Pipeline](/root/arifOS/aaa_mcp/server.py)
- [arifOS Constitutional Floors](/root/arifOS/000_THEORY/CONSTITUTION.md)
- [AGENTS.md](/root/arifOS/.openclaw/workspace/AGENTS.md)

---

*Ditempa Bukan Diberi — Forged, Not Given* 🔥
