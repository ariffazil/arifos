# arifOS Agent Adapters

**Location:** `.agents/adapters/`  
**Purpose:** Agent-specific configuration adaptations

---

## Available Adapters

| File | Target Agent | Notes |
|------|--------------|-------|
| `CLAUDE.md` | Claude Desktop/Code | JSON config, stdio transport |
| `CODEX.md` | OpenAI Codex CLI | TOML config, global location |
| `KIMI.md` | Moonshot Kimi CLI | JSON config, project location |
| `GEMINI.md` | Google Gemini | Use stdio by default; remote support depends on Gemini client version |

---

## Adapter Purpose

Each adapter describes:
1. **Config format** (JSON vs TOML)
2. **Config location** (project vs global)
3. **Transport method** (stdio vs HTTP)
4. **Tool-specific quirks**
5. **Conversion from canon**

---

## From Canon to Agent

### Claude Example
```powershell
# Canon (JSON)
.agents/mcp.json

# Claude (JSON - direct copy)
.claude/mcp.json
```

### Codex Example
```powershell
# Canon (JSON)
.agents/mcp.json

# Codex (TOML - conversion required)
~/.codex/config.toml
```

---

**See individual adapter files for detailed conversion instructions.**
