# L4_TOOLS Manifest (v2026.3.6-CANON)

**Status:** LIVE | **Canonical source:** [`arifos_aaa_mcp/`](../../arifos_aaa_mcp/) | **Internal adapter:** [`aaa_mcp/`](../../aaa_mcp/)

---

## 13 Canonical Tools

| Layer | Count | Tools |
|---|:---:|---|
| Governance | 8 | `anchor_session`, `reason_mind`, `vector_memory`, `simulate_heart`, `critique_thought`, `eureka_forge`, `apex_judge`, `seal_vault` |
| Utility | 4 | `search_reality`, `ingest_evidence`, `audit_rules`, `check_vital` |
| Orchestration | 1 | `metabolic_loop` |

See [README.md](./README.md) for full dossier-level reference.

---

## Archived Tools (Removed from Public Surface)

| Tool | Replaced By |
|---|---|
| `recall_memory` | `vector_memory` |
| `fetch_content` | `ingest_evidence` (source_type="url") |
| `inspect_file` | `ingest_evidence` (source_type="file") |
| `query_openclaw` | Internal diagnostic — not in canon |

---

## Deployment

```bash
# Canonical entry point (PyPI package)
pip install arifos

# stdio — Claude Desktop / Cursor / Claude Code
python -m arifos_aaa_mcp stdio

# SSE — VPS / Coolify (default)
python -m arifos_aaa_mcp

# HTTP — Streamable HTTP (ChatGPT / OpenAI)
python -m arifos_aaa_mcp http

# Dev editable install
pip install -e ".[dev]"
```

---

## Client Configuration

See [`mcp-configs/`](./mcp-configs/) for platform-specific configs.

### Quick Config (Claude Desktop)

```json
{
  "mcpServers": {
    "arifOS": {
      "command": "python",
      "args": ["-m", "arifos_aaa_mcp", "stdio"],
      "env": {
        "ARIFOS_GOVERNANCE_SECRET": "your-local-dev-secret"
      }
    }
  }
}
```

---

**Version:** v2026.3.6-CANON
**Protocol:** MCP 2025-11-25
**Creed:** DITEMPA BUKAN DIBERI
