# 🚀 arifOS Hub — VPS Deployment Protocol (v2026.03.08-SEAL)

This document defines the canonical flow for deploying the arifOS MCP Hub to a production VPS.

---

## 🏗️ 1. Infrastructure Checklist

The following artifacts have been forged for the **Immutable Docker Overlay** flow:

- ✅ **`Dockerfile`**: Root-level multi-stage build (Hardened, Non-root arifos user).
- ✅ **`.env.docker`**: Production environment template (Amanah signing and F2 grounding).

### Prerequisites on VPS

1. **Docker Engine**: Installed and healthy (`systemctl status docker`).
2. **SSH Public Key**: Local machine authorized for `root` or a deployment user.
3. **App Dir**: Repository cloned at `/root/arifOS` (Standard remote location).

---

## 🔐 2. Configuration (The Amanah Handshake)

Before deployment, ensure your `.env.docker` has been hardened with production secrets.

```bash
# 1. Update your local environment
# 2. Transfer to your VPS securely
scp .env.docker root@YOUR_VPS_IP:/root/arifOS/.env.docker
```

**Required Production Keys:**

- `ARIFOS_GOVERNANCE_SECRET`: Cryptographic salt for F11 continuity.
- `BRAVE_API_KEY`: Real-world factual grounding (F2 Truth).
- `GOOGLE_API_KEY` / `ANTHROPIC_API_KEY`: Core reasoning organs.

---

## 🚀 3. Deployment (Zero-Downtime Overlay)

Run the deployment engine from your local machine. This protocol performs a remote build, verifies the 10-tool core constitutional stack, and performs an atomic swap while allowing legacy Phase 2 capability tools to remain enabled.

```bash
# A. Verify local integrity
python scripts/deploy_production.py --platform validate

# B. Execute remote VPS overlay
python scripts/deploy_production.py --platform vps-overlay --host root@YOUR_VPS_IP
```

---

## 🏥 4. Verification & Health

The server will be reachable on port **8088** (Production Bind). Verify the HTTP deployment surface at `/mcp/` and confirm the core stack is present:

```bash
# Health Check (Constitutional Seal)
curl -fsS http://YOUR_VPS_IP:8088/health

# MCP endpoint
curl -i http://YOUR_VPS_IP:8088/mcp/

# Tool Registry (core stack must be present; legacy Phase 2 tools may also appear)
curl -fsS http://YOUR_VPS_IP:8088/tools
```

## 🧭 5. Runtime Split

- Core constitutional stack (10 tools): `init_anchor_state`, `integrate_analyze_reflect`, `reason_mind_synthesis`, `metabolic_loop_router`, `vector_memory_store`, `assess_heart_impact`, `critique_thought_audit`, `quantum_eureka_forge`, `apex_judge_verdict`, `seal_vault_commit`
- External capability tools (Phase 2 integration): `aclip_*`, `search_reality`, `ingest_evidence`, `audit_rules`, `check_vital`, legacy `metabolic_loop`
- The new APEX-G metabolic loop only calls the 10 core tools. Phase 2 power tools stay enabled for compatibility but are not wired into Stage 444 yet.

## 🧪 6. FastMCP CLI Validation

FastMCP 3.x treats `fastmcp.json` as the local run/install truth source. The recommended production serving path is the exported ASGI app:

```bash
# Inspect manifest and server metadata
fastmcp inspect fastmcp.json

# Run locally over HTTP from the declarative config
fastmcp run fastmcp.json --transport http --host 0.0.0.0 --port 8080

# Recommended production path
uvicorn arifosmcp.runtime.server:app --host 0.0.0.0 --port 8080
```

**Ditempa Bukan Diberi — Forged, Not Given.**
*Status: [SEAL CANDIDATE]*
