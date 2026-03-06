# arifOS — Deployment & Operations Guide

This guide provides the canonical instructions for deploying and operating the arifOS AAA MCP server.

## 🚀 Quickstart (Local Development)

### CLI Mode (stdio)
Use this mode for local testing or integration with Claude Desktop.

```bash
# Install dependencies
uv pip install -e .

# Run the server in stdio mode
python -m arifos_aaa_mcp stdio
```

### FastMCP Mode
Use the FastMCP CLI for hot-reloading and automatic UI discovery.

```bash
# Run with FastMCP
fastmcp run arifos_aaa_mcp/server.py:mcp
```

---

## 🏗️ Production Deployment (VPS)

The recommended production stack uses **Docker Compose** with **Traefik** as a reverse proxy.

### Prerequisites
- Docker & Docker Compose (v2.20+)
- Domain pointed to your VPS IP
- Port 80 and 443 open

### Deployment Steps
1. Clone the repository to `/srv/arifOS`.
2. Configure your `.env.docker` (see [Environment Variables](#environment-variables)).
3. Start the stack:
   ```bash
   docker compose up -d --build
   ```

### service: arifosmcp
- Internal Port: `8080`
- Transport: `streamable-http` (SSE/HTTP)
- Custom Routes:
  - `/health`: Live health status
  - `/tools`: Tool discovery
  - `/dashboard`: Constitutional Visualizer

---

## 🔑 Environment Variables

| Variable | Description | Default |
|:---|:---|:---|
| `ARIFOS_GOVERNANCE_SECRET` | Used for HMAC signing of verdicts. | *Required* |
| `ANTHROPIC_API_KEY` | For Claude/Reasoning tasks. | - |
| `OPENCLAW_URL` | OpenClaw gateway endpoint. | `http://openclaw:18789` |
| `OLLAMA_URL` | Local LLM engine. | `http://ollama:11434` |
| `DATABASE_URL` | Vault999 persistence (PostgreSQL). | - |

---

## 🛠️ Troubleshooting

- **Check logs**: `docker compose logs -f arifosmcp`
- **Restart service**: `docker compose restart arifosmcp`
- **Verify health**: `curl http://localhost:8080/health`

## ⚖️ Governance
All material actions must pass the **13 Constitutional Floors**. View the live status at your domain's `/dashboard` endpoint.

---
*DITEMPA BUKAN DIBERI — Forged, Not Given*
