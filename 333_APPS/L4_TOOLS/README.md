# L4_TOOLS — MCP Tool Layer (v2026.02.22-FORGE)

**Level 4 | 100% Coverage | 18 Tools (13 Canonical + 5 Container)**

> *"7-Organ Sovereign Stack public contract + utility and container tools, exposed via MCP with constitutional floor enforcement."*

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

## The 13 Canonical MCP Tools

| # | Tool | Stage | Trinity | Floors | Description |
|---|------|-------|---------|--------|-------------|
| 1 | `anchor_session` | 000 | Ψ Init | F11, F12, F13 | Session ignition + defense scan |
| 2 | `reason_mind` | 111-444 | Δ Mind | F2, F4, F7, F8, F10 | Reason + integrate + draft |
| 3 | `recall_memory` | 555 | PHOENIX | F4, F7, F8 | Memory continuity retrieval |
| 4 | `simulate_heart` | 555-666 | Ω Heart | F5, F6, F9 | Stakeholder and ethics alignment |
| 5 | `critique_thought` | 666 | Ω Heart | F4, F7, F8 | Constitutional critique |
| 6 | `eureka_forge` | 777 | Ψ Soul | F1, F11, F12 | Sandboxed forge execution |
| 7 | `apex_judge` | 888 | Ψ Soul | F1-F13 | Sovereign constitutional judgment |
| 8 | `seal_vault` | 999 | VAULT | F1, F3, F10 | Immutable audit record |
| 9 | `search_reality` | utility | External | F2, F7 | Web search grounding |
| 10 | `fetch_content` | utility | External | F2, F7 | Evidence content retrieval |
| 11 | `inspect_file` | utility | Internal | F1, F4, F11 | Filesystem inspection |
| 12 | `audit_rules` | utility | Internal | F2, F3, F10 | Constitutional system verification |
| 13 | `check_vital` | utility | Internal | F4, F5, F7 | Runtime health telemetry |

Alias compatibility:
- `forge_hand` -> `eureka_forge`
- `judge_soul` -> `apex_judge`

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

The 11-stage sequence above is internalized behind the 7-organ public API to prevent abstraction leaks.

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
| MCP Server | [`arifos_aaa_mcp/server.py`](../../arifos_aaa_mcp/server.py) | ✅ 13 canonical tools operational |
| Constants | [`aaa_mcp/config/constants.py`](../../aaa_mcp/config/constants.py) | ✅ Centralized thresholds |
| Container Tools | [`aaa_mcp/integrations/`](../../aaa_mcp/integrations/) | ✅ 5 tools + caching |
| 7-Organs | [`core/organs/`](../../core/organs/) | ✅ Kernel logic |
| Floors | [`core/shared/floors.py`](../../core/shared/floors.py) | ✅ 13 floors enforced |
| Governance Kernel | [`core/governance_kernel.py`](../../core/governance_kernel.py) | ✅ Unified Ψ state |
| Telemetry | [`core/telemetry.py`](../../core/telemetry.py) | ✅ 30-day adaptation |

## Recent Improvements (v2026.02.22)

- ✅ **Caching:** Config loading 13,725x faster with LRU cache
- ✅ **Caching:** Container listing 16,022x faster with 5s TTL
- ✅ **Constants:** Centralized thresholds in `config/constants.py`
- ✅ **Error Handling:** Specific exceptions (FileNotFoundError, yaml.YAMLError)
- ✅ **Surface:** canonical 13-tool public MCP surface + alias compatibility
- ✅ **Compatibility:** Legacy 9-subroutine flow internalized behind organ boundaries

---

**Version:** v2026.02.22-FORGE  
**Last Updated:** 2026-02-22  
**Protocol:** MCP 2025-11-25  
**Performance:** <1ms cached responses  
**Creed:** DITEMPA BUKAN DIBERI
