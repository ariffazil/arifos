# Deploy arifOS to Prefect Horizon

This guide explains how to deploy arifOS Sovereign Intelligence Kernel to Prefect Horizon (https://horizon.prefect.io).

## Prerequisites

1. **GitHub Account** - Your arifOS repository is at `ariffazil/arifOS`
2. **Prefect Horizon Account** - Sign in with GitHub at https://horizon.prefect.io

## Quick Deploy

### Step 1: Verify Repository Structure

Ensure these files exist in your repository root:

```
arifOS/
├── server.py          # Horizon entry point (exports mcp instance)
├── fastmcp.json       # Deployment configuration
├── pyproject.toml     # Python dependencies
└── arifosmcp/         # Main package
```

### Step 2: Push to GitHub

```bash
git add server.py fastmcp.json
git commit -m "Add Prefect Horizon deployment configuration"
git push origin main
```

### Step 3: Deploy on Horizon

1. Go to https://horizon.prefect.io
2. Sign in with your GitHub account
3. Click **"New Project"**
4. Select the `ariffazil/arifOS` repository
5. Enter the server entrypoint: `server.py:mcp`
6. Click **Deploy**

Your server will be available at:
```
https://arifos.fastmcp.app/mcp
```

## Configuration

### Environment Variables

Configure these in the Horizon dashboard:

| Variable | Description | Default |
|----------|-------------|---------|
| `ARIFOS_VERSION` | Deployment version | `2026.03.25` |
| `ARIFOS_ENABLE_CORS` | Enable CORS headers | `true` |
| `ARIFOS_RATE_LIMIT_ENABLED` | Enable rate limiting | `true` |
| `ARIFOS_RATE_LIMIT_CAPACITY` | Rate limit bucket size | `120` |
| `ARIFOS_RATE_LIMIT_REFILL_PER_SEC` | Rate limit refill rate | `2.0` |
| `ARIFOS_HTTP_MAX_BODY_BYTES` | Max request body size | `1048576` |

### Required Secrets (if using full features)

For production deployments with full arifOS capabilities:

```bash
# PostgreSQL for VAULT999 (optional)
DATABASE_URL=postgresql://user:pass@host/db

# Redis for session storage (optional)
REDIS_URL=redis://host:6379

# API keys for reality grounding
BRAVE_API_KEY=your_key
TAVILY_API_KEY=your_key
```

## Testing the Deployment

### Using FastMCP CLI

```bash
# List available tools
fastmcp list https://arifos.fastmcp.app/mcp

# Call a tool
fastmcp call https://arifos.fastmcp.app/mcp init_anchor actor_id=test
```

### Using Python Client

```python
from fastmcp import Client

async with Client("https://arifos.fastmcp.app/mcp") as client:
    # List tools
    tools = await client.list_tools()
    print(f"Available tools: {len(tools)}")
    
    # Call init_anchor
    result = await client.call_tool("init_anchor", {
        "actor_id": "test-user",
        "declared_name": "TestAgent"
    })
    print(result)
```

### Using curl

```bash
# Health check
curl https://arifos.fastmcp.app/health

# List tools (MCP protocol)
curl -X POST https://arifos.fastmcp.app/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

## arifOS Architecture on Horizon

```
┌─────────────────────────────────────────────────────────────┐
│                    Prefect Horizon                          │
│           https://arifos.fastmcp.app                        │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────┐   │
│  │           arifOS Sovereign Kernel                   │   │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌──────────┐  │   │
│  │  │000_INIT │ │333_MIND │ │666_HEART│ │888_JUDGE │  │   │
│  │  │  Anchor │ │  AGI    │ │  ASI    │ │  APEX    │  │   │
│  │  └─────────┘ └─────────┘ └─────────┘ └──────────┘  │   │
│  │                                                      │   │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌──────────┐  │   │
│  │  │555_MEM  │ │111_SENSE│ │444_ROUT │ │999_VAULT │  │   │
│  │  │Engineer │ │Reality  │ │Kernel   │ │Ledger    │  │   │
│  │  └─────────┘ └─────────┘ └─────────┘ └──────────┘  │   │
│  └─────────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────┤
│  Protocol Trinity: MCP (primary) | A2A | WebMCP            │
└─────────────────────────────────────────────────────────────┘
```

## Troubleshooting

### "File 'server.py' not found"

Ensure `server.py` exists in the repository root and exports the mcp instance:
```python
from arifosmcp.runtime.server import mcp
__all__ = ["mcp"]
```

### Import Errors

Check that `pyproject.toml` includes all dependencies:
```toml
dependencies = [
    "fastmcp==3.1.1",
    # ... other deps
]
```

### Port Configuration

The server uses port 8000 by default. This is configured in `fastmcp.json`:
```json
{
  "port": 8000,
  "transport": "http"
}
```

## Monitoring

Once deployed, monitor your server at:
- **Horizon Dashboard**: https://horizon.prefect.io
- **Health Endpoint**: https://arifos.fastmcp.app/health
- **Metrics**: https://arifos.fastmcp.app/metrics (Prometheus format)

## Support

- **Documentation**: https://github.com/ariffazil/arifOS
- **Issues**: https://github.com/ariffazil/arifOS/issues
- **Email**: arifbfazil@gmail.com

---

**arifOS** - *Ditempa Bukan Diberi* — Forged, Not Given [ΔΩΨ | ARIF]
