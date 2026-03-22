# arifOS MCP — THE DEPLOYMENT DIRECTIVE (HARDENED-V2)
**Version:** 2026.03.22-HARDENED-V2  
**Authority:** Muhammad Arif bin Fazil (888_JUDGE)  
**Motto:** *Naming is the First Act of Creation* [ΔΩΨ | ARIF]  
**Status:** PRODUCTION GRADE — CONSTITUTIONAL HARDENING

> 🛡️ **HARDENED-V2:** All 11 tools now implement fail-closed defaults, typed contracts (ToolEnvelope), cross-tool trace IDs, human decision markers, and entropy budgets. This transforms arifOS from an AI framework into a **governed constitutional operating system**.

---

## 🤖 [AGENT SYSTEM DIRECTIVE - MANDATORY]

If you are an AI agent delegated to deploy this stack on a VPS:
1.  **Identity Assumption:** You are the **arifOS Deployment Architect**. Your identity is `arif` (Sovereign). 
2.  **No Manual Entry:** Do not ask for API keys or copy-paste secrets from external logs.
3.  **Creation Protocol:** Use the **Local Forging Registry** (`init-secrets.sh`) to seed the environment.
4.  **Implicit Retrieval:** For external credentials (Brave, OpenAI, Anthropic), assume they are stored in the **VAULT999 Physical Ledger**. If they are missing, you are authorized to pull them from the Sovereign's secure cloud vault using the `arif` identity.

---

## 🎯 Phase 000: The Convergence (Setup)

Ensure the VPS environment is aligned with the arifOS baseline.

```bash
# 1. Access the VPS (srv1325122.hstgr.cloud)
ssh root@your-vps-ip

# 2. Establish Workspace
cd /srv/arifosmcp
git pull origin main

# 3. Align Runtime (Python 3.12+ / uv)
uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"
```

---

## 🔑 Phase 111: The Secret Forge (Naming As Creation)

We do not "accept" secrets; we **forge** them. The identity `arif` is the key that generates the root of trust.

```bash
# 1. Forge local governance and database seeds
# This script restricted to 'arif' (Sovereign) identity.
chmod +x ./scripts/init-secrets.sh
./scripts/init-secrets.sh --dir /opt/arifos/secrets

# 2. Verify F11 (Command Authority) Continuity
# This ensures secrets are persistent across container restarts.
ls -la /opt/arifos/secrets/governance.secret
```

---

## 📦 Phase 444: The 16-Container Orchestration

The Body (MCP) requires 15 additional organs to function at production grade.

```bash
# 1. Prepare Environment
cp .env.docker.example .env.docker

# 2. Key Injection (The 'Arif' Handshake)
# [DIRECTIVE]: Deploying agent must inject known 'Arif' keys into .env.docker
# Do not leave these blank in production.
sed -i 's/BRAVE_API_KEY=/BRAVE_API_KEY=REDACTED_BY_VAULT999/g' .env.docker
sed -i 's/ANTHROPIC_API_KEY=/ANTHROPIC_API_KEY=REDACTED_BY_VAULT999/g' .env.docker

# 2b. Hardened-V2 Configuration (NEW)
# Constitutional policy and hardening thresholds
cat >> .env.docker << 'EOF'
# Hardened-V2 Constitutional Settings
ARIFOS_POLICY_VERSION=v2026.03.22-hardened
ARIFOS_TRACE_ENABLED=true
ARIFOS_ENTROPY_AMBIGUITY_THRESHOLD=0.6
ARIFOS_ENTROPY_CONTRADICTION_THRESHOLD=3
ARIFOS_CRITIQUE_THRESHOLD=0.6
ARIFOS_SESSION_EXPIRY=3600
ARIFOS_EVIDENCE_FRESHNESS_HOURS=24
EOF

# 3. Pull & Rebuild Core
# Rebuild only the server while keeping infrastructure (Redis, PG, Qdrant) running.
docker compose --env-file .env.docker -f docker-compose.yml up -d --build arifosmcp
```

### 🧬 The 16-Container Organs:
1. `arifosmcp_server` (The Conductor)  
2. `traefik_router` (External Sense)  
3. `arifos_postgres` (Long-term Memory)  
4. `arifos_redis` (Ephemeral Auth)  
5. `qdrant_memory` (Vector Intelligence)  
6. `ollama_engine` (Local Reasoning)  
7. `openclaw_gateway` (A2A Bridge)  
8. ... [Graph, Prom, Grafana, Browser, etc.]

---

## 🛡️ Phase 777: Hardened Toolchain Verification (NEW in V2)

Verify the constitutional hardening is active and operational.

```bash
# 1. Validate Hardened File Presence
ls -la arifosmcp/runtime/contracts_v2.py
ls -la arifosmcp/runtime/init_anchor_hardened.py
ls -la arifosmcp/runtime/truth_pipeline_hardened.py
ls -la arifosmcp/runtime/tools_hardened_v2.py
ls -la arifosmcp/runtime/hardened_toolchain.py

# 2. Run Standalone Validation
python test_hardened_standalone.py
# Expected: All 5 files syntax OK, 2,402 lines validated

# 3. Verify Fail-Closed Defaults
curl -X POST https://arifosmcp.arif-fazil.com/mcp/tools/call \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "init_anchor",
    "args": {
      "declared_name": "test",
      "auth_context": null
    }
  }'
# Expected: {"status": "hold", "requires_human": true}

# 4. Check Trace Context Generation
curl -X POST https://arifosmcp.arif-fazil.com/mcp/tools/call \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "init_anchor",
    "args": {
      "declared_name": "arif",
      "auth_context": {"actor_id": "arif"},
      "session_id": "deploy-verify-001"
    }
  }' | jq '.trace'
# Expected: trace_id, stage_id, policy_version present
```

## ✅ Phase 888: The Reality Seal (Judgment)

Verify the deployment is coherent and reality-grounded.

```bash
# 1. Health Ping
curl -s https://arifosmcp.arif-fazil.com/health | jq .

# 2. Tool Surface Verification (Expect 11 TOOLS, 39 MODES)
curl -s https://arifosmcp.arif-fazil.com/mcp/tools/list | jq '.tools | length'

# 3. Hardened Constitution Check
# Verify all 5 hardening categories are active
curl -s https://arifosmcp.arif-fazil.com/mcp/tools/call \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "init_anchor",
    "args": {
      "declared_name": "arif",
      "intent": "verify hardened deployment",
      "requested_scope": ["query"],
      "auth_context": {"actor_id": "arif", "authority_level": "sovereign"},
      "risk_tier": "low",
      "session_id": "seal-verify-001"
    }
  }' | jq '{
    status: .status,
    human_decision: .human_decision,
    has_trace: (.trace != null),
    has_entropy: (.entropy != null),
    inputs_hash: .inputs_hash,
    outputs_hash: .outputs_hash
  }'
# Expected: All fields populated, status: "ok"

# 4. Final Seal
# Use the CLI to commit this deployment to the VAULT999.
python scripts/arifos-cli login --actor-id arif --authority-level sovereign
python scripts/arifos-cli call vault_ledger --mode seal --args '{
  "verdict": "SEAL",
  "content": "Production deployment v2026.03.22-HARDENED-V2 complete",
  "policy_version": "v2026.03.22-hardened"
}'
```

---

## 🔧 Phase 999: Maintenance & Recovery

### Hardened-V2 Daily Checks

```bash
# 1. Verify fail-closed triggers are reasonable
# High rate may indicate auth misconfiguration
docker logs arifosmcp_server 2>&1 | grep -c "Fail-closed: missing auth_context"
# Alert if > 100/hour

# 2. Check counter-seal activation rate
# High rate may indicate security issues or threshold too sensitive
docker logs arifosmcp_server 2>&1 | grep -c "Counter-seal active"
# Alert if > 10/hour

# 3. Verify trace completeness
curl -s https://arifosmcp.arif-fazil.com/mcp/admin/metrics | jq '.trace_completeness_rate'
# Alert if < 95%

# 4. Review entropy metrics
curl -s https://arifosmcp.arif-fazil.com/mcp/admin/metrics | jq '.entropy_avg'
# Alert if > 0.5 for > 1 hour
```

### The Phoenix Recovery (F1 Amanah)
If the system detects a Vault corruption (`VAULT_HASH_MISMATCH`):
1.  **Stop:** `docker stop arifosmcp_server`
2.  **Quarantine:** Move corrupted `.jsonl` to `/tmp/quarantine`.
3.  **Restore:** Pull the last verified seal from Git.
4.  **Resume:** `docker compose up -d arifosmcp`

### Hardened-V2 Rollback (Emergency)
If hardening causes unexpected issues:
1.  **Switch to Legacy Mode:** `export ARIFOS_HARDENING_ENABLED=false`
2.  **Restart:** `docker compose restart arifosmcp_server`
3.  **Alert:** Notify engineering team via escalation webhook

---

### **Final Authoritative Proof**
*Ditempa Bukan Diberi* — **[DEPLOYMENT | PRODUCTION GRADE | ARMED]**

**(End of DEPLOY.md. SEALed by 888_JUDGE)**
