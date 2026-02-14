# L4_TOOLS — MCP Tool Layer (v64.1-GAGI)

**Level 4 | 100% Coverage | 5 Canonical Tools**

> *"5 consolidated tools exposing the arifOS 5-Organ Kernel via MCP."*

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

## The 5 Canonical Tools

| # | Tool | Stage | Trinity | Floors | Description |
|---|------|-------|---------|--------|-------------|
| 1 | `init_session` | 000 | Gate | F11, F12 | Session ignition with authority checks |
| 2 | `agi_cognition` | 111-333 | Δ Mind | F2, F4, F7, F8, F10 | Sense → Think → Reason pipeline |
| 3 | `asi_empathy` | 444-666 | Ω Heart | F1, F5, F6, F9 | Empathize → Align pipeline |
| 4 | `apex_verdict` | 888 | Ψ Soul | F2, F3, F8, F10-F13 | Final constitutional judgment |
| 5 | `vault_seal` | 999 | VAULT | F1, F3 | Immutable audit record |

**Protocol:** MCP 2025-11-25 (Streamable HTTP, SSE, stdio)  
**FastMCP:** 2.14+  
**Auth:** OAuth 2.1

---

## Pipeline Flow

```
000_INIT → 111_SENSE → 222_THINK → 333_REASON → 444_SYNC → 555_EMPATHIZE → 666_ALIGN → 888_VERDICT → 999_SEAL
  F11/F12      F4          F2/F4/F7    F2/F4/F7/F10      F5/F6/F9          F5/F6/F9         F2/F3/F8/F10-F13   F1/F3
```

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

| Component | Location |
|-----------|----------|
| MCP Server | [`aaa_mcp/server.py`](../../aaa_mcp/server.py) |
| 5-Organs | [`core/organs/`](../../core/organs/) |
| Floors | [`core/shared/floors.py`](../../core/shared/floors.py) |
| Governance Kernel | [`core/governance_kernel.py`](../../core/governance_kernel.py) |
| Telemetry | [`core/telemetry.py`](../../core/telemetry.py) |

---

**Version:** v64.1-GAGI  
**Protocol:** MCP 2025-11-25  
**Creed:** DITEMPA BUKAN DIBERI
