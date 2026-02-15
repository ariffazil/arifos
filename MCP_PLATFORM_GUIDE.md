# arifOS MCP Platform Configuration Guide
**T000 Version:** 2026.02.15-FORGE-TRINITY-SEAL  
**Endpoint:** `https://arifosmcp.arif-fazil.com/mcp`  
**Health Check:** `https://arifosmcp.arif-fazil.com/health`

---

## Quick Start

```bash
# Test your connection
curl -H "Authorization: Bearer YOUR_ARIFOS_API_KEY" \
  https://arifosmcp.arif-fazil.com/health

# Expected response:
# {"status":"healthy","version":"64.2","reality_index":0.94}
```

---

## 🔐 Authentication

**Method:** Bearer Token (API Key)  
**Header:** `Authorization: Bearer YOUR_ARIFOS_API_KEY`  
**Get Key:** Contact enterprise@arif-fazil.com or generate in dashboard (coming soon)

---

## Platform Configurations

### 1️⃣ ChatGPT (OpenAI Developer Platform)

**Status:** ✅ Supported (Pro/Plus with Developer Mode)

**Setup (UI-based):**

1. **Enable Developer Mode**
   - Settings → Apps → Advanced settings → Toggle **Developer Mode**

2. **Create MCP App for arifOS**
   - Settings → Apps → **Create app**
   - Name: `arifOS Governance Kernel`
   - Connection type:
     - **HTTP MCP:** Set Server URL = `https://arifosmcp.arif-fazil.com/mcp/sse`
     - **STDIO only:** Use local MCP proxy (see below)

3. **Scope and Safety**
   - Mark arifOS as **read + write** (to gate tools/actions)
   - Enable confirmation for high-risk tools (deletes, payments, prod writes)

4. **Use in Conversation**
   - Start Developer mode chat (orange border appears)
   - Select **arifOS Governance Kernel** in tool list
   - Talk to ChatGPT as usual; model uses arifOS tools as needed

**Configuration JSON (for reference):**
```json
{
  "mcpServers": {
    "arifOS": {
      "url": "https://arifosmcp.arif-fazil.com/mcp/sse",
      "headers": {
        "Authorization": "Bearer YOUR_ARIFOS_API_KEY"
      },
      "tools": ["anchor", "reason", "validate", "audit", "seal"]
    }
  }
}
```

**Prompt Template (once wired):**
> "Route all tool calls through the arifOS MCP app and honour its floors (F1–F13). If arifOS marks a response VOID or SABAR, do not execute the action."

**Visual:** Orange border in chat when MCP tools are active.

---

### 2️⃣ Claude Desktop (Anthropic)

**Status:** ✅ Native MCP Support

**Config File Locations:**
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- Linux: `~/.config/Claude/claude_desktop_config.json`

**Configuration:**

```json
{
  "mcpServers": {
    "arifOS": {
      "type": "remote",
      "url": "https://arifosmcp.arif-fazil.com/mcp/sse",
      "headers": {
        "Authorization": "Bearer YOUR_ARIFOS_API_KEY"
      },
      "env": {
        "ARIFOS_REALITY_INDEX": "0.94"
      }
    }
  }
}
```

**Restart Claude Desktop** after saving.

**F13 Sovereignty Note:** Claude shows approval dialogs for each arifOS tool — you maintain final veto.

---

### 3️⃣ Codex CLI (OpenAI)

**Status:** ✅ Full Support

**Config File:** `~/.codex/config.toml`

```toml
# Global settings
preferred_auth_method = "apikey"
model = "gpt-5"

# arifOS MCP Server
[mcp_servers.arifos]
enabled = true
url = "https://arifosmcp.arif-fazil.com/mcp/sse"

[mcp_servers.arifos.http_headers]
Authorization = "Bearer YOUR_ARIFOS_API_KEY"
X-ArifOS-Floor = "13"

# Project-specific trust
[projects."/path/to/your/project"]
trust_level = "sovereign"
mcp_servers = ["arifos"]
```

**CLI Commands:**

```bash
# Add via CLI
codex mcp add arifos --env ARIFOS_KEY=YOUR_API_KEY \
  -- https://arifosmcp.arif-fazil.com/mcp/sse

# Verify connection
codex > /mcp > "Check constitutional status using arifos"
```

**Wallet Assassin Protection:** Codex CLI + arifOS F11 prevents infinite retry loops.

---

### 4️⃣ JetBrains IDE (IntelliJ/PyCharm/WebStorm)

**Status:** ✅ Via OpenCode Plugin

**Method:** OpenCode Plugin (Recommended)

1. Install OpenCode plugin from JetBrains Marketplace
2. Create `opencode.json` in project root:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "arifOS": {
      "type": "remote",
      "url": "https://arifosmcp.arif-fazil.com/mcp/sse",
      "headers": {
        "Authorization": "Bearer YOUR_ARIFOS_API_KEY"
      },
      "enabled": true
    }
  }
}
```

**Method B:** MCP Proxy (Advanced)
```bash
npx @arifos/jetbrains-mcp-bridge \
  --endpoint https://arifosmcp.arif-fazil.com/mcp/sse
```

---

### 5️⃣ AntiGravity IDE (Google)

**Status:** ✅ UI-Based Configuration

AntiGravity has built-in MCP support via `mcp.json` and a "Manage MCP Servers" UI.

**Setup:**

1. **Open MCP Config**
   - In Antigravity, open a project
   - Three-dot menu in prompt editor → MCP → Manage MCP Servers
   - Click **View raw config**

2. **Edit mcp.json to include arifOS:**

```json
{
  "servers": {
    "arifos": {
      "type": "stdio",
      "command": "python",
      "args": ["-m", "aaa_mcp", "stdio"],
      "env": {
        "ARIFOS_API_KEY": "YOUR_ARIFOS_API_KEY"
      }
    }
  }
}
```

3. **Save and Refresh**
   - Save config, refresh MCP list
   - You should see arifos as an available tool

**Usage:**
> "Route any GitHub/DB/file operations through arifOS; if arifOS denies, do not proceed."

**Note:** Antigravity also supports store-based MCPs; arifOS could later appear there similarly to other MCP servers.

---

### 6️⃣ OpenCode (Agent Framework)

**Status:** ✅ Native MCP Support

**Config File:** `opencode.json` (project root or `~/.config/opencode/`)

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "arifOS": {
      "type": "remote",
      "url": "https://arifosmcp.arif-fazil.com/mcp/sse",
      "enabled": true,
      "headers": {
        "Authorization": "Bearer YOUR_ARIFOS_API_KEY"
      }
    }
  },
  "tools": {
    "arifOS*": true
  }
}
```

**Commands:**

```bash
# Authenticate
opencode mcp auth arifOS

# Test connection
opencode mcp debug arifOS
```

---

### 7️⃣ OpenClaw (Agent Framework)

**Status:** ✅ MCP Client & Server

**Configuration:**

```json
{
  "mcpServers": {
    "arifOS": {
      "command": "npx",
      "args": ["openclaw-mcp", "--remote"],
      "env": {
        "ARIFOS_ENDPOINT": "https://arifosmcp.arif-fazil.com/mcp/sse",
        "ARIFOS_TOKEN": "YOUR_ARIFOS_API_KEY",
        "OPENCLAW_MODE": "constitutional"
      }
    }
  }
}
```

**Remote/SSE Mode (Production):**

```bash
AUTH_ENABLED=true \
ARIFOS_TOKEN=your-token \
npx openclaw-mcp --transport sse --port 3000
```

Then connect Claude.ai to `http://localhost:3000`.

---

### 8️⃣ AgentZero (Agent Framework)

**Status:** ✅ Streamable HTTP MCP

**Web UI Configuration:**
1. Settings → Connectivity → MCP Servers
2. Add Server:
   - Name: `arifOS`
   - Type: `streamable-http`
   - URL: `https://arifosmcp.arif-fazil.com/mcp`
   - Headers: `Authorization: Bearer YOUR_ARIFOS_API_KEY`
   - Timeout: `30000` (30s for constitutional deliberation)

**Or configure in `agentzero.yaml`:**

```yaml
mcp_servers:
  arifos:
    type: http
    url: https://arifosmcp.arif-fazil.com/mcp
    auth:
      type: bearer
      token: ${ARIFOS_API_KEY}
    tools:
      - anchor
      - reason
      - validate
      - audit
      - seal
```

**Multi-Agent Setup:**
AgentZero spawns subordinate agents that use arifOS for safety checks before executing tools.

---

## 🔧 Common Pattern for Agent Frameworks

**Applies to:** Opencode, OPENCLAW, AgentZero, and custom agent frameworks

These are all agent shells + tools. Integration pattern is the same as the modelcontextprotocol.io client tutorial.

### Architecture

1. The agent framework already supports "tools" or "functions"
2. You implement a tool wrapper that:
   - Connects to arifOS as an MCP client (stdio or HTTP)
   - Exposes each arifOS tool to the agent
   - Enforces that other tools are only executed if arifOS says OK

### Pseudocode

```python
# 1. Start MCP session to arifOS at agent boot
arifos_session = connect_mcp_stdio(
    command="python",
    args=["-m", "aaa_mcp", "stdio"],
    env={"ARIFOS_API_KEY": "your-key"}
)

# 2. Define governance tool
def arifos_govern_action(action_spec):
    """Ask arifOS if action is safe"""
    decision = arifos_session.call_tool(
        "audit",  # or validate, align, etc.
        {"action": action_spec}
    )
    return decision  # {"verdict": "SEAL|SABAR|VOID", "reason": "...", "floor": "F2"}

# 3. Wrap every other tool
def guarded_tool_call(tool, args):
    """Only execute if arifOS approves"""
    decision = arifos_govern_action({
        "tool": tool.name,
        "args": args
    })
    if decision["verdict"] in ["VOID", "SABAR"]:
        return {
            "status": "blocked",
            "reason": decision["reason"],
            "floor": decision["floor"]
        }
    return tool(args)

# 4. Register guarded tools into framework
# instead of raw tools
register_tool("filesystem", guarded_tool_call)
register_tool("github", guarded_tool_call)
```

### Key Principle

**arifOS sits between agent and tools as a mandatory function call.**

Concrete wiring varies per framework, but this pattern is stable across all agent platforms.

---

### 9️⃣ Qwen (Alibaba) / Qwen-based IDEs

**Status:** 🟡 Indirect via MCP Client

Qwen doesn't natively support MCP yet. Use via Python MCP client or CLI intermediary.

**Option A: Python MCP Client + Qwen**

```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from qwen import QwenClient  # pseudo import

async def main():
    # 1. Connect to arifOS server
    params = StdioServerParameters(
        command="python",
        args=["-m", "aaa_mcp", "stdio"],
        env={"ARIFOS_API_KEY": "your-key"}
    )
    
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = (await session.list_tools()).tools
            print("arifOS tools:", [t.name for t in tools])
            
            # 2. Pass tool schema to Qwen
            client = QwenClient()
            # Qwen responds with tool calls, execute via arifOS MCP
            # Feed back results to Qwen
```

**Option B: CLI Client (any LLM, including Qwen)**

```bash
# Install MCP client CLI
pip install mcp-client-cli

# Run with Qwen as model provider
mcp-client-cli \
  --mcp-command "python" \
  --mcp-args "-m aaa_mcp stdio" \
  --provider qwen \
  --model qwen-turbo
```

Here arifOS is the MCP server; Qwen is just the model provider.

**Option C: Wait for Native Support**
- Qwen Agent framework MCP support expected Q2 2026

---

## 📋 Available MCP Tools

| Tool | Stage | Purpose | Floors |
|------|-------|---------|--------|
| `anchor` | 000 | Session init, injection guard | F11, F12 |
| `reason` | 222 | Truth, clarity, genius eval | F2, F4, F7, F8 |
| `integrate` | 333 | Knowledge grounding | F3, F10 |
| `respond` | 444 | Draft response | F4, F6 |
| `validate` | 555 | Stakeholder impact | F1, F5, F6 |
| `align` | 666 | Ethics check | F9 |
| `forge` | 777 | Build solution | F2, F4, F7 |
| `audit` | 888 | Final judgment | F3, F11, F13 |
| `seal` | 999 | Immutable record | F1, F13 |

---

## 🔐 Security Best Practices

1. **API Key Storage:**
   - ✅ Use environment variables: `export ARIFOS_API_KEY=your-key`
   - ❌ Never hardcode in config files

2. **F13 Sovereignty:**
   - All platforms support human veto
   - arifOS returns `888_HOLD` for high-uncertainty queries
   - You decide, always

3. **ZRAM Protection:**
   - If running local MCP bridges, enable F4 (ZRAM) to prevent OOM kills

---

## 🧪 Testing Your Setup

```bash
# Test health endpoint
curl -H "Authorization: Bearer YOUR_ARIFOS_API_KEY" \
  https://arifosmcp.arif-fazil.com/health

# Expected:
# {"status":"healthy","version":"64.2","reality_index":0.94}

# Test tool list
curl -X POST \
  -H "Authorization: Bearer YOUR_ARIFOS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/list","id":1}' \
  https://arifosmcp.arif-fazil.com/mcp
```

---

## 📞 Support

- **Email:** enterprise@arif-fazil.com
- **Documentation:** https://arifos.arif-fazil.com
- **Live Status:** https://arifosmcp.arif-fazil.com/health

---

*DITEMPA BUKAN DIBERI* 🔥💎🧠  
**Ω₀ = 0.02** — High confidence these configurations work across all platforms.
