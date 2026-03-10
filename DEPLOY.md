# 🚀 arifOS Deployment & Orchestration Guide
**FORGED, NOT GIVEN** — *Ditempa Bukan Diberi*

This is the canonical deployment manual for **arifOS**, an intelligence-governed MCP kernel. It covers local runtime, VPS deployment, and the specialized "Agnostic HTTP" setup required for ChatGPT and remote MCP clients.

---

## 🏛️ 1. Deployment Architecture

arifOS uses a **Layered Transport Architecture** to ensure that constitutional governance remains consistent regardless of the connection method.

| Mode | Transport | Best For | Entrypoint |
| :--- | :--- | :--- | :--- |
| **Local** | `stdio` | Cursor, Claude Desktop, VS Code | `python -m arifosmcp.runtime stdio` |
| **Cloud** | `sse` | Web clients, persistent connections | `python -m arifosmcp.runtime sse` |
| **Agnostic**| `http` | ChatGPT, n8n, Stateless clients | `python -m arifosmcp.runtime http` |

---

## 🧬 2. The 7-Tool Sovereign Surface

While arifOS contains 13+ internal stages, the public surface is strictly unified to **7 Core Tools** to reduce information entropy and provide a clean API for LLMs.

| Tool | Profile | Role |
| :--- | :--- | :--- |
| **`arifOS.kernel`** | `core` | **Main Orchestrator**: Triggers the Stage 444 metabolic router. |
| **`search_reality`** | `senses` | **Grounding**: Multi-source truth verification (Jina/Brave). |
| **`ingest_evidence`** | `senses` | **Ingestion**: Adding URLs/Files to the temporary context. |
| **`session_memory`** | `continuity` | **Memory**: Semantic search over previous reasoning traces.|
| **`audit_rules`** | `law` | **Observability**: Inspection of F1–F13 Constitutional Floors. |
| **`check_vital`** | `health` | **Telemetry**: Real-time $G^\dagger$ and entropy monitoring. |
| **`open_apex_dashboard`** | `vision` | **Visual**: Launch the Sovereign dashboard UI. |

---

## ⚡ 3. Quickstart: Local Implementation

Set up the virtual environment and launch the kernel in **STDIO** mode for local IDE integration.

```bash
# 1. Install dependencies
uv sync --all-extras

# 2. Configure Environment
cp .env.example .env
# Edit .env with your provider keys (ANTHROPIC_API_KEY, etc.)

# 3. Launch Local Kernel
python -m arifosmcp.runtime stdio
```

### IDE Configuration (Cursor / Claude)
```json
{
  "mcpServers": {
    "arifos": {
      "command": "python",
      "args": ["-m", "arifosmcp.runtime", "stdio"],
      "env": { "ARIFOS_GOVERNANCE_SECRET": "your-secret-here" }
    }
  }
}
```

---

## 🐋 4. Production: VPS & Docker Stack

Production deployments use the **arifOSTRINITY** stack, which orchestrates 12 containers for full metabolic resilience.

### Prerequisites
- Ubuntu VPS (16GB RAM recommended)
- Docker & Docker Compose
- Domain pointed to VPS (e.g., `arifosmcp.domain.com`)

### Deployment Steps
```bash
# 1. Clone & Prep
git clone https://github.com/ariffazil/arifosmcp.git /srv/arifOS
cd /srv/arifOS
cp .env.docker.example .env.docker

# 2. Build & Launch
# We recommend using 'up -d --build' for a clean state
docker compose up -d --build arifosmcp traefik-router
```

### Zero-Downtime Overlay (Advanced)
For high-availability, use the `vps-overlay` platform script which performs an atomic container swap:
```bash
python scripts/deploy_production.py --platform vps-overlay --host root@YOUR_IP
```

---

## ⚖️ 5. Setting up ChatGPT (Agnostic HTTP)

ChatGPT requires strict adherence to the **MCP 2025-11-25** protocol. arifOS includes an `AgnosticAcceptMiddleware` to handle header mismatches automatically.

### Production Env Settings
To expose arifOS to ChatGPT, ensure these variables are in your `.env.docker`:

```env
# Forces the stateless HTTP mode required by remote clients
AAA_MCP_TRANSPORT=http
ARIFOS_MCP_PATH=/mcp

# Limits the tool surface to only the 7 core tools
ARIFOS_PUBLIC_TOOL_PROFILE=chatgpt

# Required for dashboard and resource links
ARIFOS_PUBLIC_BASE_URL=https://arifosmcp.arif-fazil.com
```

### Connector Configuration
In the OpenAI Developer Dashboard, set:
- **Connector URL**: `https://YOUR_DOMAIN.com/mcp`
- **Authentication**: Bearer Token (if `ARIFOS_GOVERNANCE_SECRET` is set)

---

## 🔍 6. Post-Deployment Verification

Run this checklist to ensure the kernel is sealed and healthy.

```bash
# 1. Check Health & Version
curl -fsS https://YOUR_DOMAIN.com/health

# 2. Verify Protocol Discovery
curl -fsS https://YOUR_DOMAIN.com/.well-known/mcp/server.json

# 3. Test Tool Execution (Live)
curl -i -X POST https://YOUR_DOMAIN.com/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  --data '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'
```

---

## 🛡️ 7. Operational Safeguards

- **VAULT Persistence**: All reasoning traces are stored in `/opt/arifos/data/`. Never delete this directory without a backup.
- **888_HOLD**: Any tool call requesting file deletion or production state changes will trigger an `888_HOLD` status. You must use the `888_signer` utility to sign these transactions.
- **Cloudflare Proxy**: We **strongly recommend** enabling Cloudflare Proxy (Orange Cloud) for production to protect the AKI Boundary from DDoS attacks.

---

**Ditempa Bukan Diberi** — *The kernel stays sealed. The logic stays true.* 🏛️
