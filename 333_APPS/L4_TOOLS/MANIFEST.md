# L4_TOOLS Manifest (v55.5.0)

**Status:** 🟢 LIVE | **Source:** [`aaa_mcp/`](../../aaa_mcp/)

---

## 13 Canonical Tools

See [README.md](./README.md) for detailed tool reference.

---

## Deployment

```powershell
# Production
pip install -e ".[dev]"
python -m aaa_mcp

# SSE (VPS)
python -m aaa_mcp sse

# HTTP (Streamable)
python -m aaa_mcp http
```

---

## Client Configuration

See [`mcp-configs/`](./mcp-configs/) for platform-specific configs.

### Quick Config (Claude Desktop)
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

**Version:** v55.5.0  
**Protocol:** MCP 2025-11-25  
**Creed:** DITEMPA BUKAN DIBERI
