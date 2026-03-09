# arifOS Deployment Guide (VPS + HTTP + SSE + stdio)

This is the canonical operator guide for deploying and running arifosmcp.

It supports:
- VPS production deployment (Docker Compose)
- Direct Python runtime over HTTP, SSE, and stdio
- MCP client integration for local stdio and remote HTTP

## 1) Deployment Modes

- VPS recommended production: docker-compose.yml plus reverse proxy
- Local server: python -m arifosmcp.runtime http or sse
- Local stdio: python -m arifosmcp.runtime stdio

Yes, arifosmcp is stdio capable.

## 2) Prerequisites

- Python >=3.12
- Docker Engine and Docker Compose for VPS mode
- Git
- Domain and TLS termination for public HTTP endpoint

## 3) Required Secrets and Environment

Use .env.docker.example as template and create .env.docker.

Minimum required for hardened deployment:
- ARIFOS_GOVERNANCE_SECRET
- POSTGRES_PASSWORD
- GRAFANA_PASSWORD
- WEBHOOK_SECRET
- OPENCLAW_RESTART_TOKEN
- OPENCLAW_GATEWAY_TOKEN

Provider keys are optional unless workload requires them:
- OPENAI_API_KEY, ANTHROPIC_API_KEY, GOOGLE_API_KEY, OPENROUTER_API_KEY, VENICE_API_KEY

## 4) VPS Deployment (Docker Compose)

1. Clone repository on VPS.
2. Create .env.docker from .env.docker.example.
3. Start services.

```bash
cp .env.docker.example .env.docker
docker compose pull
docker compose up -d --build
```

4. Verify services.

```bash
docker compose ps
docker compose logs --tail=100 arifosmcp
curl -fsS http://127.0.0.1:8080/health
curl -i http://127.0.0.1:8080/mcp
```

Notes:
- Compose requires explicit secrets with no insecure fallback defaults.
- Webhook definitions are aligned in deployment/hooks.json, infrastructure/hooks.json, and infrastructure/deployment/hooks.json.

## 5) Direct Runtime Entrypoints (No Docker)

Canonical runtime commands:

```bash
python -m arifosmcp.runtime stdio
python -m arifosmcp.runtime sse
python -m arifosmcp.runtime http
```

Legacy compatibility entrypoint:

```bash
python -m arifosmcp.transport
python -m arifosmcp.transport sse
```

Environment example:

```bash
export ARIFOS_GOVERNANCE_SECRET="your-secret"
export AAA_MCP_TRANSPORT="stdio"
python -m arifosmcp.runtime stdio
```

## 6) MCP Client Configuration

Local stdio example:

```json
{
  "mcpServers": {
    "arifos": {
      "command": "python",
      "args": ["-m", "arifosmcp.runtime", "stdio"],
      "env": {
        "ARIFOS_GOVERNANCE_SECRET": "your-secret"
      }
    }
  }
}
```

Remote HTTP example:
- URL: https://your-domain/mcp
- Transport: http

## 7) Operational Verification Checklist

- Health endpoint returns success at /health
- MCP endpoint is reachable at /mcp
- Core tools are discoverable
- Logs show no missing required secret errors

Recommended checks:

```bash
ruff check .
pytest tests/test_e2e.py::test_full_arifos_metabolic_loop -v
pytest tests/test_canonical_tool_integration.py::test_vault_seal_integration -v
```

## 8) Troubleshooting

- Invalid AAA_MCP_TRANSPORT: set one of stdio, http, sse, streamable-http
- PORT out of range: use 1024 to 65535
- QDRANT_API_KEY environment variable is required: set QDRANT_API_KEY before using RAG module
- Signature and webhook failures: ensure WEBHOOK_SECRET and OPENCLAW_RESTART_TOKEN match runtime env

## 9) Release Sync Notes

- Python package version: pyproject.toml (arifos)
- NPM package version: arifosmcp/packages/npm/arifos-mcp/package.json (@arifos/mcp)
- Keep both in sync for cross ecosystem releases

Forged, not given.
