# arifOS — The Sovereign Constitutional Kernel

> **DITEMPA BUKAN DIBERI — Forged, Not Given** [ΔΩΨ | ARIF]

[![Version](https://img.shields.io/badge/version-2026.03.28-blue)](./CHANGELOG.md)
[![MCP](https://img.shields.io/badge/MCP-Universal-purple)](https://arifosmcp.arif-fazil.com)
[![Tools](https://img.shields.io/badge/tools-11-brightgreen)](./TOOLS.md)
[![Status](https://img.shields.io/badge/status-SEALED-success)]()

arifOS is a **constitutional intelligence kernel** that transforms LLM capabilities into lawful, accountable, and human-anchored action. It runs a thermodynamic constitution (ΔΩΨ) on top of large language models.

---

## Quick Start

### Deploy to Prefect Horizon (Cloud)
```
Repository:  https://github.com/ariffazil/arifosmcp
Entrypoint:  server.py:mcp
Branch:      main
```
**URL:** https://arifos.fastmcp.app

### Deploy to VPS (Sovereign)
```bash
git clone https://github.com/ariffazil/arifOS.git
cd arifOS
docker compose up -d
```
**URL:** https://arifosmcp.arif-fazil.com

---

## Architecture

```
arifOS (Parent Repo)
├── arifosmcp/          ← Submodule: MCP Server
│   ├── server.py       ← Universal entry (auto-detects 2.x/3.x)
│   ├── server_horizon.py
│   └── runtime/        ← 11 mega-tools
├── horizon/            ← Legacy Horizon adapter
└── docker-compose.yml  ← VPS deployment
```

### Trinity Model

| Ring | Domain | Role |
|------|--------|------|
| **1** | Soul (Human) | Sovereign Intent |
| **2** | Mind (Kernel) | Constitutional Enforcement |
| **3** | Body (Action) | Tool Execution |

### Metabolic Pipeline (000–999)

```
000_INIT → 111_SENSE → 333_MIND → 444_ROUTER → 666_HEART → 777_OPS → 888_JUDGE → 999_SEAL
```

---

## Tool Inventory (11 Mega-Tools)

| Tool | Band | Purpose | Horizon | VPS |
|------|------|---------|---------|-----|
| `init_anchor` | 000_INIT | Session anchoring | ✅ | ✅ |
| `physics_reality` | 111_SENSE | Time/search | ✅ | ✅ |
| `agi_mind` | 333_MIND | Reasoning | ✅ | ✅ |
| `arifOS_kernel` | 444_ROUTER | Primary conductor | ✅ | ✅ |
| `asi_heart` | 666_HEART | Safety critique | ✅ | ✅ |
| `math_estimator` | 777_OPS | Cost estimation | ✅ | ✅ |
| `apex_soul` | 888_JUDGE | Constitutional verdict | ✅ | ✅ |
| `architect_registry` | 000_INIT | Tool discovery | ✅ | ✅ |
| `vault_ledger` | 999_SEAL | Secure storage | ❌ | ✅ |
| `engineering_memory` | — | Redis memory | ❌ | ✅ |
| `code_engine` | — | Code execution | ❌ | ✅ |

---

## Documentation

| Document | Purpose |
|----------|---------|
| [HORIZON_DEPLOYMENT.md](./HORIZON_DEPLOYMENT.md) | Cloud deployment guide |
| [DEPLOY.md](./DEPLOY.md) | VPS deployment guide |
| [AGENTS.md](./AGENTS.md) | Constitutional behavior |
| [horizon/README.md](./horizon/README.md) | Legacy adapter docs |

---

## Constitutional Governance

Implements **ΔΩΨ** framework:
- **Δ** Clarity: Reduce entropy (dS ≤ 0)
- **Ω** Humility: Stay within uncertainty
- **Ψ** Vitality: Every action witnessed

Full constitution: [000/000_CONSTITUTION.md](./000/000_CONSTITUTION.md)

---

**Version:** 2026.03.28-SEALED  
**Maintainer:** Muhammad Arif bin Fazil  
**License:** Theory (CC0) | Runtime (AGPL-3.0)
