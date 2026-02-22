# Claude Adapter for arifOS AGENTS CANON

**Target:** Claude Desktop / Claude Code  
**Format:** JSON  
**Location:** `.claude/mcp.json` (project) or `~/.claude/mcp.json` (global)

---

## Configuration

Claude uses the **same JSON format** as the canon:

```json
{
  "mcpServers": {
    "aaa-mcp": { /* Copy from .agents/mcp.json */ },
    "filesystem": { /* Copy from .agents/mcp.json */ }
    // ... etc
  }
}
```

---

## From Canon

```powershell
# Direct copy - no conversion needed
Copy-Item .agents/mcp.json .claude/mcp.json
```

---

## Claude-Specific Features

### alwaysAllow
Claude supports `alwaysAllow` array for tool auto-approval:

```json
{
  "mcpServers": {
    "aaa-mcp": {
      "command": "...",
      "alwaysAllow": [
        "init_gate",
        "agi_sense",
        "vault_seal"
      ]
    }
  }
}
```

### Placement
`alwaysAllow` goes **inside** the server config, not top-level.

---

## Verification

In Claude Code, run:
```
/mcp
```

Should list all 11 MCP servers from TIER 0-2.

---

**Last Updated:** 2026-02-02
