# L4_TOOLS — MCP Tool Layer (v64.1.1-GAGI)

**Level 4 | 100% Coverage | 14 Tools (9 A-CLIP + 5 Container)**

> *"9 A-CLIP constitutional tools + 5 container management tools, all exposed via MCP with <1ms response time (cached)."*

---

## 🚀 Quick Start

```powershell
# stdio (Claude, Cursor, Kimi)
python -m aaa_mcp

# SSE (Railway/Remote)
python -m aaa_mcp sse

# HTTP (Streamable HTTP)
python -m aaa_mcp http
```

---

## The 9 A-CLIP Constitutional Tools

| # | Tool | Stage | Trinity | Floors | Description | Canonical Name |
|---|------|-------|---------|--------|-------------|----------------|
| 1 | `anchor` | 000 | Gate | F11, F12 | Session ignition with authority checks | `init_session` |
| 2 | `reason` | 222 | Δ Mind | F2, F4, F8 | Generate hypotheses & analyze | `agi_cognition` |
| 3 | `integrate` | 333 | Δ Mind | F7, F10 | Map & ground external knowledge | — |
| 4 | `respond` | 444 | Δ Mind | F4, F6 | Draft plan & response | — |
| 5 | `validate` | 555 | Ω Heart | F5, F6, F1 | Check stakeholder impact | `asi_empathy` |
| 6 | `align` | 666 | Ω Heart | F9 | Ethics & Anti-Hantu check | — |
| 7 | `forge` | 777 | Ω Heart | F2, F4, F7 | Synthesize solution | — |
| 8 | `audit` | 888 | Ψ Soul | F3, F11, F13 | Final constitutional judgment | `apex_verdict` |
| 9 | `seal` | 999 | VAULT | F1, F3 | Immutable audit record | `vault_seal` |

## The 5 Container Management Tools

| Tool | Floors | Description |
|------|--------|-------------|
| `container_list` | F11, F2 | List sovereign stack containers (cached) |
| `container_restart` | F11, F1, F5 | Restart containers with 888_HOLD protection |
| `container_logs` | F11, F2 | Get container logs (qdrant, openclaw, agentzero) |
| `sovereign_health` | F2, F7 | Full health check of sovereign stack |
| `container_exec` | F11, F12 | Execute commands with F12 injection defense |

**Performance:** All container operations cached (5s TTL) for <1ms response times.

**Protocol:** MCP 2025-11-25 (Streamable HTTP, SSE, stdio)  
**FastMCP:** 2.14+  
**Auth:** OAuth 2.1

---

## Pipeline Flow

```
000_INIT → 222_REASON → 333_INTEGRATE → 444_RESPOND → 555_VALIDATE → 666_ALIGN → 777_FORGE → 888_AUDIT → 999_SEAL
  F11/F12      F2/F4/F8       F7/F10         F4/F6         F5/F6/F1       F9         F2/F4/F7      F3/F11/F13      F1/F3
```

**Optimized:** 9 stages with caching for 13,725x performance improvement.

**Verdicts:** `SEAL` | `VOID` | `PARTIAL` | `SABAR` | `888_HOLD`

---

## Client Configuration

See [`mcp-configs/`](./mcp-configs/) for copy-paste configs:

| Platform | Config |
|----------|--------|
| Claude Desktop | `mcp-configs/claude/mcp.json` |
| Kimi | `mcp-configs/kimi/mcp.json` |
| Codex | `mcp-configs/codex/mcp.json` |
| Antigravity | `mcp-configs/antigravity/mcp_config.json` |

### Claude Desktop Example
```json
{
  "mcpServers": {
    "aaa-mcp": {
      "command": "python",
      "args": ["-m", "aaa_mcp"],
      "env": {"ARIFOS_MODE": "PROD"}
    }
  }
}
```

---

## Implementation

| Component | Location | Status |
|-----------|----------|--------|
| MCP Server | [`aaa_mcp/server.py`](../../aaa_mcp/server.py) | ✅ 9 tools operational |
| Constants | [`aaa_mcp/config/constants.py`](../../aaa_mcp/config/constants.py) | ✅ Centralized thresholds |
| Container Tools | [`aaa_mcp/integrations/`](../../aaa_mcp/integrations/) | ✅ 5 tools + caching |
| 5-Organs | [`core/organs/`](../../core/organs/) | ✅ Kernel logic |
| Floors | [`core/shared/floors.py`](../../core/shared/floors.py) | ✅ 13 floors enforced |
| Governance Kernel | [`core/governance_kernel.py`](../../core/governance_kernel.py) | ✅ Unified Ψ state |
| Telemetry | [`core/telemetry.py`](../../core/telemetry.py) | ✅ 30-day adaptation |

## Recent Improvements (v64.1.1)

- ✅ **Caching:** Config loading 13,725x faster with LRU cache
- ✅ **Caching:** Container listing 16,022x faster with 5s TTL
- ✅ **Constants:** Centralized thresholds in `config/constants.py`
- ✅ **Error Handling:** Specific exceptions (FileNotFoundError, yaml.YAMLError)
- ✅ **Tools:** 9 A-CLIP tools + 5 container tools = 14 total

---

**Version:** v64.1.1-GAGI  
**Last Updated:** 2026-02-14  
**Protocol:** MCP 2025-11-25  
**Performance:** <1ms cached responses  
**Creed:** DITEMPA BUKAN DIBERI
