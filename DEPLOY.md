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

Run the deployment engine from your local machine. This protocol performs a remote build, verifies the 13-tool surface, and performs an atomic swap.

```bash
# A. Verify local integrity
python scripts/deploy_production.py --platform validate

# B. Execute remote VPS overlay
python scripts/deploy_production.py --platform vps-overlay --host root@YOUR_VPS_IP
```

---

## 🏥 4. Verification & Health

The server will be reachable on port **8088** (Production Bind). Verify the 22-tool unified surface:

```bash
# Health Check (Constitutional Seal)
curl -fsS http://YOUR_VPS_IP:8088/health

# Tool Registry (Canonical 13 + Sensory 9)
curl -fsS http://YOUR_VPS_IP:8088/tools
```

**Ditempa Bukan Diberi — Forged, Not Given.**
*Status: [SEAL CANDIDATE]*
