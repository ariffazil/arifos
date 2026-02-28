# AAA MCP Deployment Guide v60.0-FORGE

**Version:** v60.0-FORGE (RUKUN AGI)  
**MCP Protocol:** 2025-11-25 (Streamable HTTP)  
**Purpose:** Zero-touch deployment orchestration for AI agents  
**Scope:** Local (stdio) → Railway (cloud) → Cloudflare (edge)

---

## Deployment Taxonomy

| Target | Transport | Use Case | AAA Support |
|--------|-----------|----------|-------------|
| **Local** | stdio | Desktop agents (Claude, Kimi) | F11/F12 only |
| **Railway** | Streamable HTTP | Staging/production cloud | Full OAuth 2.1 |
| **Cloudflare** | Streamable HTTP | Global edge, lowest latency | Full OAuth 2.1 + KV |
| **Hostinger VPS Overlay** | Streamable HTTP | Current production image refresh | Immutable overlay image |

## Current Production Path

Current production is a standalone Docker container behind Nginx:

- Host: `root@72.62.71.199`
- Repo path: `/root/arifOS`
- Container: `arifosmcp_server`
- Private bind: `127.0.0.1:8088:8080`
- Public base URL: `https://arifosmcp.arif-fazil.com`

## One-Command VPS Overlay Deploy

This is the canonical production deploy command for the current VPS.
It builds a thin immutable overlay image from `arifos/arifosmcp:latest`,
copies the current repo checkout into the image, validates a private candidate,
then swaps the live container with no bind mount.

```bash
python scripts/deploy_production.py --platform vps-overlay
```

What it does:

- SSH to the production VPS
- `git pull --ff-only` in `/root/arifOS`
- Build overlay image tag `arifos/arifosmcp:<version>-<sha>`
- Start a candidate container on `127.0.0.1:18089`
- Verify `/health` and `/tools` before cutover
- Replace `arifosmcp_server`
- Verify public `/health` and `/tools`
- Assert the live container has no bind mounts

Useful overrides:

```bash
python scripts/deploy_production.py --platform vps-overlay --dry-run
python scripts/deploy_production.py --platform vps-overlay --host root@your-vps
python scripts/deploy_production.py --platform vps-overlay --public-base-url https://your-domain
```

---

## A. Railway Deployment

### Prerequisites

```bash
# Install Railway CLI
npm install -g @railway/cli

# Verify installation
railway --version
```

### Step-by-Step Deployment

```bash
# 1. Navigate to project
cd arifOS

# 2. Login to Railway
railway login

# 3. Initialize project (or link existing)
railway init --name arifos-aaa-mcp
# OR: railway link

# 4. Set environment variables
railway variables set PORT=8080
railway variables set HOST=0.0.0.0
railway variables set AAA_MCP_TRANSPORT=sse
railway variables set ARIFOS_CONSTITUTIONAL_MODE=AAA
railway variables set PYTHONUNBUFFERED=1

# 5. Optional: Set external APIs
railway variables set BRAVE_API_KEY=<your_key>
railway variables set BROWSERBASE_API_KEY=<your_key>

# 6. Optional: Database for persistent VAULT999
railway variables set DATABASE_URL=<postgresql_url>

# 7. Deploy
railway up

# 8. Get deployment URL
railway domain
# Output: https://arifos-aaa-mcp.up.railway.app

# 9. Verify health
curl https://arifos-aaa-mcp.up.railway.app/health
```

### Client Configuration

**Claude Desktop (Remote):**
```json
{
  "mcpServers": {
    "arifos-aaa-railway": {
      "transport": "streamable-http",
      "url": "https://arifos-aaa-mcp.up.railway.app/mcp",
      "headers": {
        "Authorization": "Bearer ${RAILWAY_TOKEN}"
      }
    }
  }
}
```

**Environment Setup:**
```bash
# Add to ~/.bashrc or ~/.zshrc
export RAILWAY_TOKEN="your_railway_api_token"
```

---

## B. Cloudflare Workers Deployment

### Prerequisites

```bash
# Install Wrangler
npm install -g wrangler

# Authenticate
wrangler login
```

### 1. KV Namespace Setup

```bash
# Create KV namespace for session store
wrangler kv:namespace create AAA_SESSION_STORE

# Output:
# 🌀 Creating namespace with title "arifos-aaa-mcp-AAA_SESSION_STORE"
# ✨ Success!
# Add the following to your configuration file:
# [[kv_namespaces]]
# binding = "AAA_SESSION_STORE"
# id = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# Copy the ID to wrangler.jsonc
```

### 2. Configuration (wrangler.jsonc)

```jsonc
{
  "name": "arifos-aaa-mcp",
  "main": "aaa_mcp/index.ts",
  "compatibility_date": "2026-02-09",
  "node_compat": true,
  
  // Custom domain (optional)
  "routes": [
    { "pattern": "mcp.arifos.dev/mcp", "zone_name": "arifos.dev" }
  ],
  
  // KV namespace for sessions
  "kv_namespaces": [
    {
      "binding": "AAA_SESSION_STORE",
      "id": "YOUR_KV_NAMESPACE_ID"
    }
  ],
  
  // Environment variables
  "vars": {
    "MCP_PROTOCOL_VERSION": "2025-11-25",
    "AAA_ISSUER": "https://auth.arifos.dev",
    "ARIFOS_CONSTITUTIONAL_MODE": "AAA",
    "FLOOR_ENFORCEMENT": "HARD"
  },
  
  // Secrets (set via wrangler secret)
  "secrets": [
    "AAA_JWT_SECRET",
    "OAUTH_CLIENT_SECRET",
    "BRAVE_API_KEY"
  ],
  
  // Dev configuration for MCP Inspector
  "dev": {
    "cors": {
      "origins": ["http://localhost:5173"],
      "methods": ["GET", "POST", "OPTIONS"],
      "headers": ["Content-Type", "Authorization"]
    }
  }
}
```

### 3. Deploy

```bash
# Set secrets
wrangler secret put AAA_JWT_SECRET
# Enter your JWT secret

wrangler secret put OAUTH_CLIENT_SECRET
# Enter your OAuth client secret

# Deploy
wrangler deploy

# Output:
# ✨ Successfully deployed to:
# https://arifos-aaa-mcp.youraccount.workers.dev
```

### 4. Test with MCP Inspector

```bash
# Open MCP Inspector
open http://localhost:5173

# Or manually navigate to:
# https://modelcontextprotocol.io/inspector

# Enter URL:
# https://arifos-aaa-mcp.youraccount.workers.dev/mcp
```

---

## C. OAuth 2.1 Setup (AAA Authorization)

### OAuth Authorization Server Metadata

Host this at `/.well-known/oauth-authorization-server`:

```json
{
  "issuer": "https://auth.arifos.dev",
  "authorization_endpoint": "https://auth.arifos.dev/authorize",
  "token_endpoint": "https://auth.arifos.dev/token",
  "registration_endpoint": "https://auth.arifos.dev/register",
  "scopes_supported": ["mcp:read", "mcp:execute", "aaa:audit"],
  "response_types_supported": ["code"],
  "grant_types_supported": ["authorization_code", "refresh_token"],
  "code_challenge_methods_supported": ["S256"],
  "token_endpoint_auth_methods_supported": ["client_secret_basic", "client_secret_post"]
}
```

### Protected Resource Metadata

Host this at `/.well-known/oauth-protected-resource`:

```json
{
  "resource": "https://mcp.arifos.dev",
  "authorization_servers": ["https://auth.arifos.dev"],
  "scopes_supported": ["mcp:read", "mcp:execute", "aaa:audit"],
  "bearer_methods_supported": ["header"]
}
```

### Dynamic Client Registration

```bash
# Register a new MCP client
curl -X POST https://auth.arifos.dev/register \
  -H "Content-Type: application/json" \
  -d '{
    "client_name": "Claude Desktop",
    "client_uri": "https://claude.ai",
    "redirect_uris": ["http://localhost:3000/callback"],
    "grant_types": ["authorization_code", "refresh_token"],
    "response_types": ["code"],
    "token_endpoint_auth_method": "client_secret_basic",
    "scope": "mcp:read mcp:execute"
  }'

# Response:
{
  "client_id": "mcp_client_abc123",
  "client_secret": "secret_xyz789",
  "client_id_issued_at": 1707494400,
  "client_secret_expires_at": 0
}
```

---

## D. Client Configuration Templates

### VS Code / Cursor (mcp.json)

```json
{
  "servers": {
    "arifos-aaa-local": {
      "type": "stdio",
      "command": "python",
      "args": ["-m", "aaa_mcp", "stdio"],
      "cwd": "/path/to/arifOS",
      "env": {
        "ARIFOS_CONSTITUTIONAL_MODE": "AAA"
      }
    },
    "arifos-aaa-railway": {
      "type": "streamable-http",
      "url": "https://arifos-aaa.up.railway.app/mcp",
      "headers": {
        "Authorization": "Bearer ${env:RAILWAY_TOKEN}"
      }
    },
    "arifos-aaa-cloudflare": {
      "type": "streamable-http",
      "url": "https://mcp.arifos.dev/mcp",
      "headers": {
        "Authorization": "Bearer ${env:CF_ACCESS_TOKEN}"
      }
    }
  },
  "inputs": [
    {
      "id": "RAILWAY_TOKEN",
      "type": "secret",
      "description": "Railway API token for arifOS AAA MCP"
    },
    {
      "id": "CF_ACCESS_TOKEN",
      "type": "secret",
      "description": "Cloudflare Access token"
    }
  ]
}
```

### Claude Desktop (Full)

```json
{
  "mcpServers": {
    "arifos-local": {
      "command": "python",
      "args": ["-m", "aaa_mcp", "stdio"],
      "cwd": "/path/to/arifOS",
      "env": {
        "ARIFOS_CONSTITUTIONAL_MODE": "AAA"
      }
    },
    "arifos-railway": {
      "transport": "streamable-http",
      "url": "https://arifos-aaa.up.railway.app/mcp",
      "headers": {
        "Authorization": "Bearer ${RAILWAY_TOKEN}"
      }
    },
    "arifos-cloudflare": {
      "transport": "streamable-http",
      "url": "https://mcp.arifos.dev/mcp",
      "oauth2": {
        "issuer": "https://auth.arifos.dev",
        "authorization_endpoint": "https://auth.arifos.dev/authorize",
        "token_endpoint": "https://auth.arifos.dev/token",
        "client_id": "${OAUTH_CLIENT_ID}",
        "scope": "mcp:read mcp:execute"
      }
    }
  }
}
```

### Kimi (Remote)

```json
{
  "mcpServers": {
    "aaa-mcp-remote": {
      "transport": "streamable-http",
      "url": "https://arifos-aaa.up.railway.app/mcp",
      "headers": {
        "Authorization": "Bearer ${RAILWAY_TOKEN}"
      },
      "alwaysAllow": [
        "init_gate",
        "trinity_forge",
        "agi_sense",
        "agi_reason",
        "asi_empathize",
        "apex_verdict",
        "vault_seal"
      ]
    }
  }
}
```

---

## E. Validation Checklist

Before declaring deployment complete:

```bash
# 1. Local validation
python scripts/deploy_mcp.py --mode validate

# 2. Health check (local)
curl http://localhost:8080/health

# 3. Health check (remote)
curl https://arifos-aaa.up.railway.app/health

# 4. MCP Inspector test
npx @modelcontextprotocol/inspector \
  https://arifos-aaa.up.railway.app/mcp

# 5. Tool listing test
curl https://arifos-aaa.up.railway.app/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

---

## F. Troubleshooting

### Issue: "Connection refused" (Railway)

**Fix:**
```bash
# Verify PORT is set to 8080
railway variables get PORT
# Should output: 8080

# If not, set it
railway variables set PORT=8080
railway up
```

### Issue: "CORS error" (Cloudflare)

**Fix:**
Add CORS configuration to `wrangler.jsonc`:
```jsonc
"dev": {
  "cors": {
    "origins": ["http://localhost:5173"],
    "methods": ["GET", "POST", "OPTIONS"],
    "headers": ["Content-Type", "Authorization"]
  }
}
```

### Issue: "OAuth token invalid"

**Fix:**
```bash
# Verify OAuth metadata is accessible
curl https://auth.arifos.dev/.well-known/oauth-authorization-server

# Check token endpoint
curl -X POST https://auth.arifos.dev/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials" \
  -d "client_id=YOUR_CLIENT_ID" \
  -d "client_secret=YOUR_CLIENT_SECRET"
```

---

## G. Environment Variable Reference

### Required

| Variable | Local | Railway | Cloudflare |
|----------|-------|---------|------------|
| `PORT` | 8080 | 8080 | — |
| `HOST` | 127.0.0.1 | 0.0.0.0 | — |
| `AAA_MCP_TRANSPORT` | stdio | sse | — |
| `MCP_PROTOCOL_VERSION` | — | — | 2025-11-25 |

### Optional (AAA)

| Variable | Purpose |
|----------|---------|
| `AAA_JWT_SECRET` | JWT signing key |
| `AAA_ISSUER` | OAuth issuer URL |
| `OAUTH_CLIENT_ID` | OAuth client ID |
| `OAUTH_CLIENT_SECRET` | OAuth client secret |
| `AAA_SESSION_STORE` | KV namespace binding |

### Optional (Features)

| Variable | Purpose |
|----------|---------|
| `BRAVE_API_KEY` | Web search capability |
| `BROWSERBASE_API_KEY` | Browser automation |
| `DATABASE_URL` | PostgreSQL for VAULT999 |
| `REDIS_URL` | Session caching |

---

## H. Thermodynamic Trade-Offs

| Deployment | Latency | Complexity | Scale | Best For |
|------------|---------|------------|-------|----------|
| stdio | 0ms | Low | Single user | Local development |
| Railway | 50-200ms | Medium | Multi-user | Staging, small teams |
| Cloudflare | <50ms | High | Global | Production, high scale |

**Recommendation:**
- **Development:** stdio (local)
- **Staging:** Railway (cloud)
- **Production:** Cloudflare Workers (edge)

---

## Attribution

**arifOS Constitutional AI Governance**  
GitHub: https://github.com/ariffazil/arifOS  
Documentation: https://arifos.arif-fazil.com

**Sources:**
- MCP Specification 2025-11-25
- Cloudflare Workers MCP Guide
- Railway Deployment Documentation
- OAuth 2.1 for MCP (RFC draft)

---

*DITEMPA BUKAN DIBERI* 💎🔥🧠
