# Codex Adapter for arifOS AGENTS CANON

**Target:** OpenAI Codex CLI  
**Format:** TOML  
**Location:** `~/.codex/config.toml` (global only)

---

## Configuration

Codex uses **TOML format**, not JSON. Manual conversion required.

---

## From Canon (JSON → TOML)

### Canon (JSON):
```json
{
  "mcpServers": {
    "aaa-mcp": {
      "command": "python.exe",
      "args": ["-m", "mcp"],
      "env": { "KEY": "value" }
    }
  }
}
```

### Codex (TOML):
```toml
[features]
shell_tool = false

[mcp_servers.aaa-mcp]
command = "python.exe"
args = ["-m", "mcp"]
env = { KEY = "value" }
```

---

## Conversion Rules

| JSON | TOML |
|------|------|
| `"mcpServers"` | `[mcp_servers.<name>]` |
| `"key": "value"` | `key = "value"` |
| `{ "a": "b" }` | `{ a = "b" }` |
| Arrays `[...]` | Arrays `[...]` (same) |

---

## Full Example

See: `333_APPS/L4_TOOLS/mcp-configs/codex/config.toml`

Or copy from:
```powershell
Copy-Item 333_APPS/L4_TOOLS/mcp-configs/codex/config.toml ~/.codex/config.toml
```

---

## Verification

```bash
codex --list-mcp-servers
```

---

**Note:** Codex config **cannot** be project-local. Must be in `~/.codex/`.

---

**Last Updated:** 2026-02-02
