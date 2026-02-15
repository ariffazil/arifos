# Gemini Adapter for arifOS AGENTS CANON

**Target:** Google Gemini / Gemini CLI  
**Format:** JSON (limited support)  
**Location:** `.gemini/mcp.json` (experimental)

---

## Transport Reality

arifOS server supports all three MCP transports:
- `stdio` (local)
- `sse` (remote)
- `http` / streamable HTTP (remote)

Gemini client behavior can vary by version, but the server itself is not SSE-only.

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
| MCP stdio | ✅ Supported (recommended) |
| MCP SSE | ✅ Supported via remote endpoint |
| MCP HTTP | ✅ Supported by server (client support may vary) |
| Tool calls | ⚠️ Depends on Gemini client build |
| arifOS integration | ⚠️ Validate with local smoke test |

---

## Recommendation

Use Gemini with local `stdio` first via `.gemini/mcp.json`.
If you need remote transport, use `/sse` or `/mcp` depending on Gemini's current MCP transport support.

---

**Last Updated:** 2026-02-06  
**Status:** Server supports stdio + SSE + HTTP; verify client build capabilities
