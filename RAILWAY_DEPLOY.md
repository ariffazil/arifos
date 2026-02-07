# Deploy arifOS to Railway

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/your-template-id)

## One-Click Deploy

Click the button above to deploy your own instance of arifOS MCP Server on Railway.

## What Gets Deployed?

| Component | Description |
|-----------|-------------|
| **MCP Server** | Constitutional AI gateway with 9 canonical tools |
| **PostgreSQL** | VAULT999 ledger for immutable audit trail |
| **Redis** | Session state persistence (24h TTL) |
| **Health Endpoint** | `/health` for monitoring |

## Environment Variables

The following variables are automatically configured:

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | 8080 | Server port |
| `HOST` | 0.0.0.0 | Bind address |
| `DATABASE_URL` | Auto | PostgreSQL connection (Railway plugin) |
| `REDIS_URL` | Auto | Redis connection (Railway plugin) |
| `AAA_MCP_TRANSPORT` | sse | MCP transport: sse, http, or stdio |
| `GOVERNANCE_MODE` | HARD | Constitutional mode: HARD or SOFT |

## Optional API Keys

Add these in Railway dashboard for enhanced functionality:

| Variable | Purpose |
|----------|---------|
| `BRAVE_API_KEY` | Brave Search for `reality_search` tool |
| `BROWSERBASE_API_KEY` | Web browsing capabilities |

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
