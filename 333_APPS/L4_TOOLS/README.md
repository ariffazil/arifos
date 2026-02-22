# L4_TOOLS — MCP Tool Layer (v2026.02.22-FORGE)

**Level 4 | 100% Coverage | 14 Tools (5 Organs + 4 Utilities + 5 Container)**

> *"5-Organ Trinity public contract + utility and container tools, exposed via MCP with constitutional floor enforcement."*

---

## 🚀 Quick Start

```powershell
# stdio (Claude, Cursor, Kimi)
python -m aaa_mcp

# SSE (VPS/Remote)
python -m aaa_mcp sse

# HTTP (Streamable HTTP)
python -m aaa_mcp http
```

---

## The 9 Canonical MCP Tools

| # | Tool | Stage | Trinity | Floors | Description |
|---|------|-------|---------|--------|-------------|
| 1 | `init_session` | 000+555 | Ψ Init | F11, F12, F5, F6 | Session ignition + impact validation |
| 2 | `agi_cognition` | 222+333+444 | Δ Mind | F2, F4, F7, F8, F10 | Reason + integrate + draft |
| 3 | `asi_empathy` | 555+666 | Ω Heart | F5, F6, F9 | Stakeholder and ethics alignment |
| 4 | `apex_verdict` | 777+888 | Ψ Soul | F2, F3, F4, F11, F13 | Constitutional judgment |
| 5 | `vault_seal` | 999 | VAULT | F1, F3 | Immutable audit record |
| 6 | `search` | utility | External | F2, F7 | Web search (read-only) |
| 7 | `fetch` | utility | External | F2, F7 | Web fetch (read-only) |
| 8 | `analyze` | utility | Internal | F4 | Data/structure analysis |
| 9 | `system_audit` | utility | Internal | F2, F3 | Constitutional system verification |

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

## Internal Pipeline Flow

```
000_INIT → 222_REASON → 333_INTEGRATE → 444_RESPOND → 555_VALIDATE → 666_ALIGN → 777_FORGE → 888_AUDIT → 999_SEAL
  F11/F12      F2/F4/F8       F7/F10         F4/F6         F5/F6/F1       F9         F2/F4/F7      F3/F11/F13      F1/F3
```

The 9-stage sequence above is internalized behind the 5-organ public API to prevent abstraction leaks.

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
| MCP Server | [`aaa_mcp/server.py`](../../aaa_mcp/server.py) | ✅ 9 canonical tools operational |
| Constants | [`aaa_mcp/config/constants.py`](../../aaa_mcp/config/constants.py) | ✅ Centralized thresholds |
| Container Tools | [`aaa_mcp/integrations/`](../../aaa_mcp/integrations/) | ✅ 5 tools + caching |
| 5-Organs | [`core/organs/`](../../core/organs/) | ✅ Kernel logic |
| Floors | [`core/shared/floors.py`](../../core/shared/floors.py) | ✅ 13 floors enforced |
| Governance Kernel | [`core/governance_kernel.py`](../../core/governance_kernel.py) | ✅ Unified Ψ state |
| Telemetry | [`core/telemetry.py`](../../core/telemetry.py) | ✅ 30-day adaptation |

## Recent Improvements (v2026.02.22)

- ✅ **Caching:** Config loading 13,725x faster with LRU cache
- ✅ **Caching:** Container listing 16,022x faster with 5s TTL
- ✅ **Constants:** Centralized thresholds in `config/constants.py`
- ✅ **Error Handling:** Specific exceptions (FileNotFoundError, yaml.YAMLError)
- ✅ **Surface:** 5-organ trinity + 4 utility tools = 9 canonical public tools
- ✅ **Compatibility:** Legacy 9-subroutine flow internalized behind organ boundaries

---

**Version:** v2026.02.22-FORGE  
**Last Updated:** 2026-02-22  
**Protocol:** MCP 2025-11-25  
**Performance:** <1ms cached responses  
**Creed:** DITEMPA BUKAN DIBERI
