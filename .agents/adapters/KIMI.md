# Kimi Adapter for arifOS AGENTS CANON

**Target:** Moonshot Kimi CLI  
**Format:** JSON  
**Location:** `.kimi/mcp.json` (project)

---

## Configuration

Kimi uses the **same JSON format** as the canon:

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
# Direct copy - no conversion needed
Copy-Item .agents/mcp.json .kimi/mcp.json
```

---

## Kimi-Specific Features

### CLI Override
Kimi supports temporary config:

```bash
# Use custom config
kimi --mcp-config-file /path/to/custom/mcp.json

# Inline JSON
kimi --mcp-config '{"mcpServers": {...}}'
```

### Default Location
If not specified, Kimi looks for:
1. `--mcp-config-file` argument
2. `--mcp-config` inline
3. `.kimi/mcp.json` (project)
4. `~/.kimi/mcp.json` (global)

---

## Verification

```bash
kimi mcp list
```

---

**Last Updated:** 2026-02-02
