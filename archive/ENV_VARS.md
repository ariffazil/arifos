# arifOS MCP — Environment Variables

**Epoch:** 2026-04-17
**Status:** SEALED — Day 3

---

## Axis Feature Flags

Control which tool axes are mounted in the live server. All default to enabled.
Set to `false` to gate an axis during staged rollout or incident response.

| Variable | Default | Axis | Risk |
|---|---|---|---|
| `ARIFOS_ENABLE_P_AXIS` | `true` | Perception (read-only sense) | low |
| `ARIFOS_ENABLE_T_AXIS` | `true` | Transformation (compute) | low |
| `ARIFOS_ENABLE_V_AXIS` | `true` | Valuation (economic compute) | low |
| `ARIFOS_ENABLE_G_AXIS` | `true` | Governance (judge/verdict) | high |
| `ARIFOS_ENABLE_E_AXIS` | `true` | Execution (forge/vault) | high |
| `ARIFOS_ENABLE_M_AXIS` | `true` | Meta (metacognition) | low |

Usage in `server.py`:

```python
import os
_axis_enabled = lambda axis: os.getenv(f"ARIFOS_ENABLE_{axis}_AXIS", "true").lower() != "false"
```

---

## Execution Gates

| Variable | Default | Effect |
|---|---|---|
| `ARIFOS_ENABLE_APPROVAL_PROVIDER` | `false` | Mount FastMCP F13 approval UI for 888_HOLD gates |
| `ENABLE_DANGEROUS_TOOLS` | `false` | Unlock destructive-risk tools (inherited from A-FORGE) |
| `ARIFOS_PUBLIC_BOOTSTRAP` | `true` | Strict public mode — legacy aliases and debug tools opt-in only |

---

## Constitutional Thresholds

| Variable | Default | Meaning |
|---|---|---|
| `ARIFOS_OMEGA_MIN` | `0.95` | Minimum Ω_ortho for gateway to pass |
| `ARIFOS_PEACE2_FLOOR` | `0.70` | Minimum Peace² for economic operations |
| `ARIFOS_W3_MIN` | `0.95` | Minimum W³ witness score for SEAL |
| `ARIFOS_KAPPA_H_LOW` | `0.03` | kappa-H band floor (epistemic calibration) |
| `ARIFOS_KAPPA_H_HIGH` | `0.15` | kappa-H band ceiling |

---

## Infrastructure

| Variable | Required | Purpose |
|---|---|---|
| `DATABASE_URL` | Yes (VPS) | PostgreSQL for VAULT999 Merkle ledger |
| `REDIS_URL` | No | Cache / pub-sub for session continuity |
| `QDRANT_URL` | No | Vector memory (arifos_memory tool) |
| `ANTHROPIC_API_KEY` | Yes | LLM backend for mind/heart tools |

---

*DITEMPA BUKAN DIBERI — Forged, Not Given*

---

## Ops Stack — API Keys & Secrets

**Principle (F1 Amanah + F11 Audit):** No live secrets in git. No secrets in environment variables that get exported to shell or logged. Agents read secrets from the vault path at container startup only.

### Canonical Secrets Path

```
/mnt/arifos/secrets/   ← bind-mounted into containers at runtime
```

| Secret | Source | Purpose |
|--------|--------|---------|
| `ARIFOS_API_KEY` | Vault (not git) | Master bearer token for Grafana, OpenClaw restart, webhook deploy |

### Reading Secrets at Runtime

```python
# In container startup (docker-compose env_file or entrypoint script)
# DO NOT: export ARIFOS_API_KEY=...
# DO:    read from vault and pass as file or secrets manager

import os

def load_secret(path: str) -> str:
    with open(path) as f:
        return f.read().strip()
```

### Agent Integration Contract

```
A-FORGE runtime injects:  ARIFOS_API_KEY (from vault → container env at startup)
arifOS agents read from:  os.environ["ARIFOS_API_KEY"]
Grafana auth:             Bearer token via Authorization header
OpenClaw restart hook:    POST /api/restart with Bearer token
```

### Docker Compose Reference (VPS infrastructure — NOT in git)

```yaml
# /root/compose/docker-compose.yml — VPS infrastructure
services:
  arifosmcp:
    env_file: /mnt/arifos/secrets/arifos.env
    volumes:
      - /mnt/arifos/secrets:/secrets:ro
```

*Vault-locked. F1 Amanah. F13 Sovereign — human holds the key.*
