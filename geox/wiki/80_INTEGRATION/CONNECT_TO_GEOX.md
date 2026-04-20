# Connect to GEOX — Complete Integration Guide

**DITEMPA BUKAN DIBERI**

Connect your AI assistants to GEOX Earth Witness for constitutional geoscience.

---

## Quick Reference

| Platform | Connection Method | Difficulty |
|----------|------------------|------------|
| **ChatGPT** | Custom GPT + OAuth | ⭐⭐⭐ |
| **Claude Desktop** | `claude_desktop_config.json` | ⭐⭐ |
| **Cursor** | `.cursor/mcp.json` | ⭐⭐ |
| **Kimi Code CLI** | `~/.kimi/config.toml` | ⭐⭐ |
| **Gemini CLI** | `gemini mcp add` | ⭐ |
| **VS Code** | `settings.json` | ⭐⭐ |
| **OpenAI Agents SDK** | Python SDK | ⭐⭐⭐ |

**MCP Server URL:** `https://geoxarifOS.fastmcp.app/mcp`

---

## Platform-Specific Setup

### ← Kimi Code CLI

**Step 1:** Edit config file
```bash
# Open Kimi CLI config
nano ~/.kimi/config.toml
```

**Step 2:** Add MCP server
```toml
[mcp.servers.geoxarifOS]
url = "https://geoxarifOS.fastmcp.app/mcp"
transport = "http"
```

**Step 3:** Restart Kimi CLI
```bash
# Exit and restart
kimi
```

**Step 4:** Verify connection
```
> /mcp list
Available tools:
  - geox_verify_geospatial
  - geox_evaluate_prospect
  - geox_health
  ...
```

---

### ← ChatGPT (Custom GPT)

**Step 1:** Enable Developer Mode
1. Go to [chat.openai.com](https://chat.openai.com)
2. Click your profile → Settings → Beta features
3. Enable "Custom GPTs" and "Developer mode"

**Step 2:** Create New GPT
1. Click "Explore GPTs"
2. Click "Create" button
3. Name: `GEOX Earth Witness`
4. Description: `Constitutional geoscience assistant powered by GEOX`

**Step 3:** Configure MCP
1. In GPT editor, click "Add actions"
2. Authentication: Select **OAuth**
3. MCP Server URL:
   ```
   https://geoxarifOS.fastmcp.app/mcp
   ```
4. Schema: Click "Import from URL" and paste the same URL

**Step 4:** Accept Risk Warning
1. Check "I understand and want to continue"
2. Click "Create"

**Step 5:** Authorize
1. Review permissions
2. Click "Allow access"

**Step 6:** Configure Instructions
```
You are a geological prospect evaluation assistant powered by GEOX Earth Witness.

Your capabilities:
- Verify geospatial coordinates using geox_verify_geospatial
- Evaluate geological prospects using geox_evaluate_prospect
- Check constitutional compliance (F1-F13 floors)

Always follow the constitutional floors:
- F1 AMANAH: Ensure reversibility
- F4 CLARITY: Verify datum/scale before measurement
- F7 HUMILITY: Acknowledge uncertainty, show multiple candidates
- F9 ANTI-HANTU: Never claim consciousness
- F13 SOVEREIGN: Human has final authority

Seal: DITEMPA BUKAN DIBERI
```

---

### ← Claude Desktop

**Step 1:** Open Settings
- macOS: `Cmd + ,` or menu → Settings
- Windows/Linux: `Ctrl + ,` or menu → Settings

**Step 2:** Go to Developer
- Click "Developer" in left sidebar

**Step 3:** Edit Config
- Click "Edit Config" button
- Opens: `~/Library/Application Support/Claude/claude_desktop_config.json`

**Step 4:** Add GEOX Server
```json
{
  "mcpServers": {
    "geoxarifOS": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-proxy@latest"],
      "env": {
        "MCP_PROXY_URL": "https://geoxarifOS.fastmcp.app/mcp"
      }
    }
  }
}
```

**Alternative (Direct HTTP):**
```json
{
  "mcpServers": {
    "geoxarifOS": {
      "url": "https://geoxarifOS.fastmcp.app/mcp",
      "transport": "http"
    }
  }
}
```

**Step 5:** Restart Claude Desktop
- Save file
- Quit Claude completely
- Reopen Claude

**Step 6:** Verify
- Look for 🔨 hammer icon in input box
- Click to see available tools

---

### ← Cursor IDE

**Step 1:** Open Settings
- `Cmd/Ctrl + ,` or File → Preferences → Settings

**Step 2:** Configure MCP
- Search for "MCP" or go to Features → MCP

**Step 3:** Add Server
Click "Add MCP Server":
```json
{
  "mcpServers": {
    "geoxarifOS": {
      "url": "https://geoxarifOS.fastmcp.app/mcp",
      "transport": "http"
    }
  }
}
```

**Step 4:** Or edit config directly
File: `~/.cursor/mcp.json`
```json
{
  "mcpServers": {
    "geoxarifOS": {
      "url": "https://geoxarifOS.fastmcp.app/mcp",
      "transport": "http"
    }
  }
}
```

**Step 5:** Reload Window
- `Cmd/Ctrl + Shift + P` → "Developer: Reload Window"

---

### ← Gemini CLI

**Step 1:** Add Server
```bash
gemini mcp add geoxarifOS https://geoxarifOS.fastmcp.app/mcp --transport http
```

Expected output:
```
Server "geoxarifOS" added successfully.
```

**Step 2:** Start Session
```bash
gemini
```

**Step 3:** Use Tools
```
> Can you verify coordinates 4.5N, 114.2E using GEOX?
[Calling tool: geox_verify_geospatial]
```

---

### ← VS Code (with Cline/Roo Code)

**Option 1: Cline Extension**

1. Install "Cline" extension
2. Open Cline panel
3. Click settings → MCP Servers
4. Add server:
```json
{
  "mcpServers": {
    "geoxarifOS": {
      "url": "https://geoxarifOS.fastmcp.app/mcp",
      "transport": "http"
    }
  }
}
```

**Option 2: settings.json**

File: `~/.vscode/settings.json`
```json
{
  "roo.cline.mcp.servers": {
    "geoxarifOS": {
      "url": "https://geoxarifOS.fastmcp.app/mcp",
      "transport": "http",
      "enabled": true
    }
  }
}
```

---

### ← OpenAI Agents SDK (Python)

**Installation:**
```bash
pip install openai-agents
```

**Code:**
```python
import asyncio
from agents import Agent, Runner, MCPTool

async def main():
    # Connect to GEOX
    geox_tools = MCPTool(
        name="geox",
        transport="http",
        url="https://geoxarifOS.fastmcp.app/mcp"
    )
    
    # Create agent with constitutional awareness
    agent = Agent(
        name="GEOX Prospector",
        instructions="""You evaluate geological prospects using GEOX tools.

Always follow constitutional floors F1-F13:
- F4 CLARITY: Verify datum before measurement
- F7 HUMILITY: Show uncertainty bounds
- F13 SOVEREIGN: Human has final authority

Seal: DITEMPA BUKAN DIBERI""",
        tools=[geox_tools],
    )
    
    # Evaluate prospect
    result = await Runner.run(
        agent,
        "Verify coordinates 4.5N, 114.2E and evaluate prospect Alpha-1"
    )
    
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
```

---

## arifOS Integration (Advanced)

For full arifOS ecosystem integration with constitutional guardrails:

```python
from arifos.integrations.openai_agents import ArifOSAgent, ConstitutionalGuardrails

# Create agent with F1-F13 enforcement
agent = await ArifOSAgent.create_geox_agent(
    mcp_url="https://geoxarifOS.fastmcp.app/mcp",
    config=ArifOSAgentConfig(
        enable_guardrails=True,
        enable_tracing=True,  # Logs to VAULT999
    )
)

# Run with full governance
result = await Runner.run(agent, "Evaluate prospect")
```

---

## GEOX Capabilities Reference

### Available Tools

| Tool | Input | Output | Use Case |
|------|-------|--------|----------|
| `geox_verify_geospatial` | lat, lon, radius_m | Province, jurisdiction, verdict | Coordinate validation |
| `geox_evaluate_prospect` | prospect_id, interpretation_id | Verdict, confidence, status | Full evaluation |
| `geox_health` | - | Server status, floors | Health check |
| `geox_load_seismic_line` | line_id, survey_path | Seismic data + views | Data loading |
| `geox_build_structural_candidates` | line_id | Candidate models | Interpretation |
| `geox_feasibility_check` | plan_id, constraints | Feasibility verdict | Planning |

### Constitutional Floors (F1-F13)

| Floor | Trigger | Action |
|-------|---------|--------|
| **F4 CLARITY** | Datum/scale unknown | Disable measurement tools |
| **F7 HUMILITY** | Single model presented | Require multiple candidates |
| **F9 ANTI-HANTU** | Consciousness claim | BLOCK hard violation |
| **F13 SOVEREIGN** | AI claims authority | BLOCK hard violation |

---

## Example Workflows

### Workflow 1: Prospect Evaluation

```
User: Evaluate prospect Alpha-1 at 4.5N, 114.2E in Malay Basin

Agent:
1. geox_verify_geospatial(4.5, 114.2)
   → Province: Malay Basin, Jurisdiction: EEZ_Grounded

2. geox_evaluate_prospect("Alpha-1", "interp-001")
   → Verdict: HOLD, Confidence: 45%, Reason: Wait for well-tie

3. Human Decision Required (F13 SOVEREIGN)
```

### Workflow 2: Seismic Interpretation

```
User: Load seismic line 223 and build structural candidates

Agent:
1. geox_load_seismic_line("line-223", "survey-2024")
   → Status: IGNITED, Scale: verified

2. geox_build_structural_candidates("line-223")
   → Candidate A: Fault-bounded anticline
   → Candidate B: Stratigraphic trap
   → Candidate C: Combination structure

3. F7 HUMILITY: Present all 3 candidates, confidence bounded at 12%
```

---

## Troubleshooting

### Connection Failed

```bash
# Test server health
curl https://geoxarifOS.fastmcp.app/health
# Should return: OK
```

### Tools Not Appearing

1. Check URL is correct
2. Verify transport is "http" not "stdio"
3. Restart the AI application
4. Check firewall/proxy settings

### Authentication Issues

GEOX uses public HTTP transport — no authentication required.

---

## Support

| Resource | URL |
|----------|-----|
| Repository | https://github.com/ariffazil/GEOX |
| arifOS | https://github.com/ariffazil/arifOS |
| Documentation | https://github.com/ariffazil/GEOX/blob/main/docs |
| Issues | https://github.com/ariffazil/GEOX/issues |

---

## Seal

**DITEMPA BUKAN DIBERI**

*Intelligence is forged, not given.*

All operations governed by 13 Constitutional Floors (F1-F13).

---

**Version:** 0.5.0  
**Server:** https://geoxarifOS.fastmcp.app/mcp