# Gemini Adapter for arifOS AGENTS CANON

**Target:** Google Gemini / Gemini CLI  
**Format:** JSON (limited support)  
**Location:** `.gemini/mcp.json` (experimental)

---

## ⚠️ Limited MCP Support

As of 2026-02-02, Gemini has **limited MCP support**. The config exists but may not be fully functional.

---

## Configuration

Gemini config follows the same JSON structure:

```json
{
  "mcpServers": {
    "aaa-mcp": { /* Copy from .agents/mcp.json */ }
  }
}
```

---

## From Canon

```powershell
# Copy (experimental)
Copy-Item .agents/mcp.json .gemini/mcp.json
```

---

## Current Status

| Feature | Status |
|---------|--------|
| MCP stdio | ⚠️ Experimental |
| MCP HTTP | ❌ Not supported |
| Tool calls | ⚠️ Limited |
| arifOS integration | ⚠️ Untested |

---

## Recommendation

For now, use Gemini for:
- Clipboard/image sharing (`.gemini/clipboard/`)
- Reference only

Use **Claude, Kimi, or Codex** for full MCP integration.

---

**Last Updated:** 2026-02-02  
**Status:** Monitor for Gemini MCP updates
