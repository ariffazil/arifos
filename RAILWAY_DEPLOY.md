# Deploy arifOS to Railway

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.com/deploy/9cskSj?referralCode=_F5zGa)

> **Template ID:** `9cskSj` | **Referral Code:** `_F5zGa`

## One-Click Deploy

Click the button above to deploy your own instance of arifOS MCP Server on Railway.

## What Gets Deployed?

| Component | Description |
|-----------|-------------|
| **MCP Server** | Constitutional AI gateway with 9 canonical tools |
| **PostgreSQL** | VAULT999 ledger for immutable audit trail |
| **Redis** | Session state persistence (24h TTL) |
| **Health Endpoint** | `/health` for monitoring |

## ⚡ 3-Step Quick Deploy

### 1. Add Environment Variables
```bash
ARIFOS_ENV=production
VAULT_BACKEND=postgres
```

### 2. Deploy
- Click purple "Deploy" button above
- Wait for build (~2-3 minutes)
- Railway auto-creates URL

### 3. Test
```bash
curl https://your-app.railway.app/health
# Response: {"status": "ok"}
```

---

## Environment Variables Reference

| Variable | Default | Required | Description |
|----------|---------|----------|-------------|
| `PORT` | 8080 | ✅ Auto | Server port |
| `HOST` | 0.0.0.0 | ✅ Auto | Bind address |
| `DATABASE_URL` | `${{Postgres.DATABASE_URL}}` | ✅ Auto | PostgreSQL connection (Railway plugin) |
| `REDIS_URL` | `${{Redis.REDIS_URL}}` | ✅ Auto | Redis connection (Railway plugin) |
| `ARIFOS_ENV` | production | ✅ Manual | Runtime environment |
| `VAULT_BACKEND` | postgres | ✅ Manual | VAULT999 backend type |
| `AAA_MCP_TRANSPORT` | sse | ⚠️ Optional | MCP transport: sse, http, or stdio |
| `GOVERNANCE_MODE` | HARD | ⚠️ Optional | Constitutional mode: HARD or SOFT |
| `BRAVE_API_KEY` | (your key) | ⚠️ Optional | Brave Search for `reality_search` tool |
| `BROWSERBASE_API_KEY` | (your key) | ⚠️ Optional | Web browsing capabilities |

## Post-Deployment

1. **Health Check**: Visit `https://your-app.railway.app/health`
2. **MCP Endpoint**: `https://your-app.railway.app/sse` (for SSE transport)
3. **Connect Claude Desktop**: Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "arifos": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sse", "https://your-app.railway.app/sse"]
    }
  }
}
```

## Manual Deploy (without button)

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Deploy
railway up

# Add PostgreSQL plugin
railway add --plugin postgres

# Add Redis plugin
railway add --plugin redis
```

## Verification

```bash
# Check health
curl https://your-app.railway.app/health

# Expected response:
# {"status": "ok"}
```

---

**DITEMPA BUKAN DIBERI** — Forged, Not Given
