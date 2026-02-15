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

**Setup:**
1. Enable Developer Mode: Settings → Advanced → Developer Mode
2. Custom Connectors → Add MCP Server
3. Configure:

```json
{
  "mcpServers": {
    "arifOS": {
      "url": "https://arifosmcp.arif-fazil.com/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_ARIFOS_API_KEY"
      },
      "tools": ["anchor", "reason", "validate", "audit", "seal"]
    }
  }
}
```

**Usage:**
> "Should I invest in crypto? Use arifOS to check safety first."

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
      "url": "https://arifosmcp.arif-fazil.com/mcp",
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
url = "https://arifosmcp.arif-fazil.com/mcp"

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
  -- https://arifosmcp.arif-fazil.com/mcp

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
      "url": "https://arifosmcp.arif-fazil.com/mcp",
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
  --endpoint https://arifosmcp.arif-fazil.com/mcp
```

---

### 5️⃣ AntiGravity (Augment Code)

**Status:** ✅ UI-Based Configuration

**Setup:**
1. Click MCP Server icon (bottom left)
2. Click Manage MCP Server
3. Click View raw config
4. Paste:

```json
{
  "mcpServers": {
    "arifOS": {
      "command": "auggie",
      "args": ["--mcp", "--endpoint=https://arifosmcp.arif-fazil.com/mcp"],
      "env": {
        "ARIFOS_API_KEY": "YOUR_ARIFOS_API_KEY",
        "ARIFOS_MODE": "trinity"
      }
    }
  }
}
```

**Usage:**
> "Review this code with arifOS F2 (Truth) and F4 (Clarity) checks."

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
      "url": "https://arifosmcp.arif-fazil.com/mcp",
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
        "ARIFOS_ENDPOINT": "https://arifosmcp.arif-fazil.com/mcp",
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

### 9️⃣ Qwen (Alibaba)

**Status:** 🟡 Limited/Indirect

Qwen doesn't natively support MCP yet. Use via OpenCode or OpenClaw as intermediaries:

**Bridge Setup:**
1. Configure arifOS in OpenCode (see above)
2. Connect Qwen to OpenCode's proxy endpoint
3. Or use Qwen API with MCP adapter layer

**Alternative:** Wait for Qwen Agent framework MCP support (expected Q2 2026).

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
