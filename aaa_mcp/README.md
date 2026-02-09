# aaa_mcp — Constitutional AI Governance Server v60.0-FORGE

**Version:** v60.0-FORGE (RUKUN AGI)  
**MCP Protocol:** 2025-11-25 (Streamable HTTP)  
**Motto:** *Ditempa Bukan Diberi* — Forged, Not Given  
**Status:** PRODUCTION READY

The AAA MCP Server provides a **Model Context Protocol** interface to the arifOS Constitutional AI system. It exposes 13 canonical tools organized as a 5-Organ Trinity pipeline with 13 Constitutional Floors enforcement.

---

## Deployment Taxonomy

| Target | Transport | Use Case | AAA Support |
|--------|-----------|----------|-------------|
| **Local** | `stdio` | Desktop agents (Claude, Kimi) | F11/F12 only |
| **Railway** | `streamable-http` | Staging/production cloud | Full OAuth 2.1 |
| **Cloudflare** | `streamable-http` | Global edge, lowest latency | Full OAuth 2.1 + KV |

**Thermodynamic constraint:** AI agents need **deterministic paths** — ambiguity ↑ entropy ↑ deployment failure rate.

---

## Quick Start

### Local (stdio)

```bash
# Install
pip install -e .

# Run (stdio mode for local agents)
python -m aaa_mcp

# Validate deployment
python scripts/deploy_mcp.py --mode validate
```

### Railway (Cloud)

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login & deploy
railway login
railway up

# Get URL
railway domain
# Output: https://arifos-aaa.up.railway.app
```

### Cloudflare (Edge)

```bash
# Install Wrangler
npm install -g wrangler

# Authenticate & deploy
wrangler login
wrangler deploy

# Output: https://arifos-aaa.youraccount.workers.dev
```

---

## Architecture

### 5-Organ Constitutional Kernel

```
┌────────────────────────────────────────────────────────────┐
│                    AAA MCP Server                          │
├────────────────────────────────────────────────────────────┤
│                                                            │
│   init_gate         → Airlock (F11/F12)                    │
│   agi_sense         → Mind Stage 111 (F4/F7)               │
│   agi_think         → Mind Stage 222 (F2/F4)               │
│   agi_reason        → Mind Stage 333 (F2/F4/F7/F8)         │
│   asi_empathize     → Heart Stage 555 (F5/F6)              │
│   asi_align         → Heart Stage 666 (F5/F6/F9)           │
│   apex_verdict      → Soul Stages 444-888 (F3/F8/F9/F10)   │
│   vault_seal        → Memory Stage 999 (F1/F3/F13)         │
│                                                            │
│   forge_pipeline    → Full 000-999 pipeline                │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### 13 Constitutional Floors

| Floor | Name | Type | Threshold |
|:-----:|:-----|:----:|:----------|
| F1 | **Amanah** | HARD | Reversible actions |
| F2 | **Truth** | HARD | τ ≥ 0.99 |
| F3 | **Consensus** | DERIVED | W₃ ≥ 0.95 |
| F4 | **Clarity** | SOFT | ΔS ≤ 0 |
| F5 | **Peace²** | SOFT | ≥ 1.0 |
| F6 | **Empathy** | HARD | κᵣ ≥ 0.70 |
| F7 | **Humility** | HARD | Ω₀ ∈ [0.03,0.05] |
| F8 | **Genius** | DERIVED | G ≥ 0.80 |
| F9 | **Anti-Hantu** | SOFT | C_dark < 0.30 |
| F10 | **Ontology** | HARD | Grounded |
| F11 | **Authority** | HARD | Valid auth |
| F12 | **Defense** | HARD | Clean scan |
| F13 | **Sovereign** | HARD | Human override |

---

## Transport Modes

### 1. stdio Mode (Default)

For Claude Desktop, Kimi, and local agents:

```bash
python -m aaa_mcp
# Transport: stdio (stdin/stdout)
# Use case: Single-user local development
# Auth: F11/F12 (local injection defense only)
```

### 2. SSE Mode (Network)

For Railway, remote connections:

```bash
python -m aaa_mcp sse
# Endpoint: http://0.0.0.0:8080/sse
# Use case: Multi-user cloud deployment
# Auth: OAuth 2.1 + Bearer tokens
```

### 3. HTTP Mode (Streamable HTTP - MCP 2025-11-25)

For MCP 2025 spec clients:

```bash
python -m aaa_mcp http
# Endpoint: http://0.0.0.0:8080/mcp
# Use case: Cloudflare Workers, modern clients
# Auth: OAuth 2.1 + Dynamic client registration
```

---

## AAA Capability Flags

The server exposes these MCP capabilities:

```json
{
  "capabilities": {
    "tools": { "listChanged": true },
    "resources": {},
    "prompts": {},
    "authorization": {
      "oauth2": {
        "issuer": "https://auth.arifos.dev",
        "authorizationEndpoint": "https://auth.arifos.dev/authorize",
        "tokenEndpoint": "https://auth.arifos.dev/token",
        "supportsDynamicClientRegistration": true
      }
    }
  }
}
```

### OAuth 2.1 Endpoints

| Endpoint | URL |
|----------|-----|
| Metadata | `/.well-known/oauth-authorization-server` |
| Protected Resource | `/.well-known/oauth-protected-resource` |
| Authorization | `https://auth.arifos.dev/authorize` |
| Token | `https://auth.arifos.dev/token` |
| Registration | `https://auth.arifos.dev/register` |

### Supported Scopes

- `mcp:read` — Read tools and resources
- `mcp:execute` — Execute tools
- `aaa:audit` — Access audit logs

---

## Client Configuration

### Kimi (Local)

**File:** `.kimi/mcp.json`

```json
{
  "mcpServers": {
    "aaa-mcp": {
      "command": "python",
      "args": ["-m", "aaa_mcp", "stdio"],
      "cwd": "/path/to/arifOS",
      "env": {
        "ARIFOS_CONSTITUTIONAL_MODE": "AAA"
      },
      "alwaysAllow": [
        "init_gate", "forge_pipeline",
        "agi_sense", "agi_reason",
        "asi_empathize", "apex_verdict", "vault_seal"
      ]
    }
  }
}
```

### Claude Desktop (Remote)

**File:** `claude_desktop_config.json`

```json
{
  "mcpServers": {
    "arifos-local": {
      "command": "python",
      "args": ["-m", "aaa_mcp", "stdio"],
      "cwd": "/path/to/arifOS"
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

### VS Code / Cursor

**File:** `.vscode/mcp.json` or `.cursor/mcp.json`

```json
{
  "servers": {
    "arifos-aaa-local": {
      "type": "stdio",
      "command": "python",
      "args": ["-m", "aaa_mcp", "stdio"],
      "cwd": "/path/to/arifOS"
    },
    "arifos-aaa-railway": {
      "type": "streamable-http",
      "url": "https://arifos-aaa.up.railway.app/mcp",
      "headers": {
        "Authorization": "Bearer ${env:RAILWAY_TOKEN}"
      }
    }
  },
  "inputs": [
    {
      "id": "RAILWAY_TOKEN",
      "type": "secret",
      "description": "Railway API token"
    }
  ]
}
```

---

## Environment Variables

### Required

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | `8080` | Server port |
| `HOST` | `0.0.0.0` | Bind address |
| `AAA_MCP_TRANSPORT` | `sse` | Transport mode |

### Optional (Features)

| Variable | Description |
|----------|-------------|
| `BRAVE_API_KEY` | Web search capability |
| `BROWSERBASE_API_KEY` | Browser automation |
| `DATABASE_URL` | PostgreSQL for VAULT999 |
| `REDIS_URL` | Session caching |

### Optional (AAA/OAuth)

| Variable | Description |
|----------|-------------|
| `AAA_JWT_SECRET` | JWT signing key |
| `AAA_ISSUER` | OAuth issuer URL |
| `OAUTH_CLIENT_ID` | OAuth client ID |
| `OAUTH_CLIENT_SECRET` | OAuth client secret |
| `AAA_SESSION_STORE` | KV namespace binding |

---

## Health & Monitoring

### Health Check

```bash
curl http://localhost:8080/health

# Response:
{
  "status": "healthy",
  "version": "60.0-FORGE",
  "service": "arifOS AAA MCP Server",
  "protocol": "2025-11-25",
  "mode": "AAA"
}
```

### Metrics

```bash
curl http://localhost:8080/metrics     # Prometheus
curl http://localhost:8080/stats       # JSON stats
```

---

## Tool Reference

### Core Pipeline

**`forge_pipeline(query, actor_id, auth_token, require_sovereign_for_high_stakes)`**

The unified 000-999 constitutional pipeline.

- **Input:** User query
- **Output:** Complete constitutional assessment
- **Stages:** 000_INIT → 111-333_MIND → 555-666_HEART → 444-888_SOUL → 999_VAULT

### Individual Tools

| Tool | Purpose | Floors |
|------|---------|--------|
| `init_gate` | Session initialization | F11, F12 |
| `agi_sense` | Parse intent | F4, F7 |
| `agi_think` | Generate hypotheses | F2, F4 |
| `agi_reason` | Logical reasoning | F2, F4, F7 |
| `asi_empathize` | Stakeholder analysis | F5, F6 |
| `asi_align` | Ethics/policy check | F5, F6, F9 |
| `apex_verdict` | Final judgment | F3, F8, F9, F10 |
| `vault_seal` | Immutable ledger | F1, F3 |
| `reality_search` | Web grounding | F2, F10 |
| `tool_router` | Dynamic routing | — |
| `vault_query` | Ledger retrieval | — |
| `truth_audit` | Claim verification | F2, F4 |

---

## Deployment

### Railway (Cloud)

```bash
# Install CLI
npm install -g @railway/cli

# Login & deploy
railway login
railway up

# Set environment
railway variables set PORT=8080
railway variables set AAA_MCP_TRANSPORT=sse
```

See [DEPLOYMENT.md](DEPLOYMENT.md) for full Railway instructions.

### Docker

```bash
# Build
docker build -t arifos-mcp:v60 .

# Run
docker run -p 8080:8080 \
  -e PORT=8080 \
  -e AAA_MCP_TRANSPORT=sse \
  arifos-mcp:v60
```

### Cloudflare Workers

```bash
# Install Wrangler
npm install -g wrangler

# Authenticate
wrangler login

# Create KV namespace
wrangler kv:namespace create AAA_SESSION_STORE

# Update wrangler.jsonc with KV ID
# Deploy
wrangler deploy
```

See [DEPLOYMENT.md](DEPLOYMENT.md) for full Cloudflare instructions.

### Validation

```bash
python scripts/deploy_mcp.py --mode validate
```

---

## Development

### Testing

```bash
# Run all tests
pytest core/tests/ -v

# Run specific module
pytest core/tests/test_pipeline.py -v

# MCP Inspector
npx @modelcontextprotocol/inspector
```

### File Structure

```
aaa_mcp/
├── server.py              # 13 MCP tools (Python)
├── index.ts               # Cloudflare Workers reference (TypeScript)
├── package.json           # Node.js dependencies
├── wrangler.jsonc         # Cloudflare deployment config
├── DEPLOYMENT.md          # Full deployment guide
├── core/
│   ├── engine_adapters.py # Bridge to core organs
│   ├── constitutional_decorator.py  # Floor enforcement
│   └── mode_selector.py   # Transport selection
├── infrastructure/
│   ├── monitoring.py      # Metrics & health
│   └── rate_limiter.py    # Rate limiting
└── sessions/
    └── session_ledger.py  # Session persistence
```

### Core Integration

```python
# Direct core usage
from core.pipeline import forge

result = await forge(
    query="What is the capital of Malaysia?",
    actor_id="user_123"
)

print(result.verdict)        # SEAL, VOID, PARTIAL, etc.
print(result.W_3)            # Tri-Witness score
print(result.processing_time_ms)  # Latency
```

---

## Thermodynamic Trade-Offs

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

## Documentation

- **Deployment Guide:** [DEPLOYMENT.md](DEPLOYMENT.md)
- **Full Guide:** `docs/MCP_DEPLOYMENT_GUIDE_V60.md`
- **Architecture:** `docs/V60_ARCHITECTURE.md`
- **Railway Guide:** `docs/RAILWAY_DEPLOYMENT.md`
- **API Reference:** `docs/API_REFERENCE.md`

---

## Support

- **Repository:** https://github.com/ariffazil/arifOS
- **Documentation:** https://arifos.arif-fazil.com
- **Health:** https://aaamcp.arif-fazil.com/health
- **Issues:** https://github.com/ariffazil/arifOS/issues

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
