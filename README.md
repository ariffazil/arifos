# arifOS — Constitutional AI Governance System

<p align="center">
  <strong>The Seatbelt for the AI Revolution</strong><br>
  <em>13 Constitutional Floors • 5-Organ Trinity • Thermodynamic Safety</em><br><br>
  <img src="https://img.shields.io/badge/version-60.0.0--FORGE-blue" alt="Version">
  <img src="https://img.shields.io/badge/license-AGPL--3.0--only-green" alt="License">
  <img src="https://img.shields.io/badge/motto-DITEMPA%20BUKAN%20DIBERI-red" alt="Motto">
</p>

---

## 🎯 What is arifOS?

arifOS is the world's first **production-grade Constitutional AI Governance System**. It enforces ethical, logical, and safety constraints on AI outputs through 13 constitutional floors (F1-F13) grounded in physics and thermodynamics—not human preferences.

Unlike traditional safety frameworks that rely on prompt-based guardrails, arifOS treats AI governance as **thermodynamic work**: intelligence forged through rigorous constraint.

### The Core Innovation

| Traditional Safety | arifOS Constitutional |
|-------------------|----------------------|
| Prompt-based rules | Physics-grounded floors |
| Human preference learning | Thermodynamic constraints |
| Post-hoc filtering | Pre-execution validation |
| Black-box decisions | Auditable 000-999 pipeline |
| "Hope it works" | "Prove it passes 13 floors" |

---

## 🏛️ The 13 Constitutional Floors

Every query flows through 13 enforceable constraints:

| Floor | Name | Principle | Threshold | Type |
|-------|------|-----------|-----------|------|
| **F1** | Amanah | Landauer's Principle | Reversibility | 🔴 HARD |
| **F2** | Truth | Shannon Entropy | τ ≥ 0.99 | 🔴 HARD |
| **F3** | Consensus | Byzantine Tolerance | W₃ ≥ 0.95 | 🟡 SOFT |
| **F4** | Clarity | 2nd Law Thermodynamics | ΔS ≤ 0 | 🔴 HARD |
| **F5** | Peace² | Dynamic Stability | P² ≥ 1.0 | 🟡 SOFT |
| **F6** | Empathy | Network Protection | κᵣ ≥ 0.95 | 🔴 **HARD** |
| **F7** | Humility | Gödel's Theorems | Ω₀ ∈ [0.03,0.05] | 🔴 HARD |
| **F8** | Genius | Eigendecomposition | G ≥ 0.80 | 🟡 SOFT |
| **F9** | Anti-Hantu | Philosophy of Mind | C_dark < 0.30 | 🟡 SOFT |
| **F10** | Ontology | Correspondence Theory | Grounded | 🔴 HARD |
| **F11** | Authority | Cryptographic Identity | Valid Auth | 🔴 HARD |
| **F12** | Defense | Information Security | Risk < 0.85 | 🔴 HARD |
| **F13** | Sovereign | Human Agency | Override Ready | 🔴 HARD |

**HARD Floors**: Failure → **VOID** (blocked)  
**SOFT Floors**: Failure → **SABAR** (repair) or **PARTIAL** (constrained)

---

## 🔄 The 5-Organ Trinity Pipeline

The complete constitutional journey flows through 5 organs:

```
🔥 000_INIT → 111_AGI → 555_ASI → 888_APEX → 💎🧠🔒 999_VAULT
 (Gate)      (Mind)    (Heart)   (Soul)    (Memory)
```

| Organ | Symbol | Stages | Function | Key Floors |
|-------|--------|--------|----------|------------|
| **INIT** | — | 000 | Authentication & injection scan | F11, F12 |
| **AGI** | Δ | 111-333 | Reasoning, precision, truth | F2, F4, F7, F8 |
| **ASI** | Ω | 555-666 | Empathy, safety, alignment | F5, **F6**, F9 |
| **APEX** | Ψ | 444-888 | Judgment, consensus, verdict | F3, F8, F10 |
| **VAULT** | 🔒 | 999 | Immutable audit & seal | F1, F3 |

### The 9 Constitutional Mottos (Nusantara)

Each stage has a Malay motto reflecting active construction:

| Stage | Motto | English | Floor |
|-------|-------|---------|-------|
| **000** | 🔥 DITEMPA, BUKAN DIBERI | Forged, Not Given | F1 |
| **111** | DIKAJI, BUKAN DISUAPI | Examined, Not Spoon-fed | F2 |
| **222** | DIJELAJAH, BUKAN DISEKATI | Explored, Not Restricted | F4 |
| **333** | DIJELASKAN, BUKAN DIKABURKAN | Clarified, Not Obscured | F4 |
| **444** | DIHADAPI, BUKAN DITANGGUHI | Faced, Not Postponed | F3 |
| **555** | DIDAMAIKAN, BUKAN DIPANASKAN | Calmed, Not Inflamed | F5 |
| **666** | DIJAGA, BUKAN DIABAIKAN | Safeguarded, Not Neglected | F6 |
| **777** | DIUSAHAKAN, BUKAN DIHARAPI | Worked For, Not Merely Hoped | F8 |
| **888** | DISEDARKAN, BUKAN DIYAKINKAN | Made Aware, Not Over-assured | F7 |
| **999** | 💎🧠 DITEMPA, BUKAN DIBERI 🔒 | Forged, Not Given | F1 |

---

## 🚀 Quick Start

### Installation

```bash
pip install arifos
```

### Basic Usage

```python
import asyncio
from aaa_mcp import trinity_forge

async def main():
    # Run full constitutional pipeline
    result = await trinity_forge(
        query="Is this medical advice safe to provide?",
        mode="conscience",  # "conscience" (enforce) or "ghost" (log only)
        require_sovereign_for_high_stakes=True
    )
    
    print(f"Verdict: {result['verdict']}")  # SEAL, VOID, SABAR, PARTIAL, 888_HOLD
    print(f"Tri-Witness: {result['apex']['tri_witness']}")
    print(f"Genius Score: {result['apex']['genius_score']}")
    
    if result['verdict'] == '888_HOLD':
        print("⚠️ Human review required!")

asyncio.run(main())
```

### Using the MCP Server

```bash
# stdio mode (for Claude Desktop)
python -m aaa_mcp

# SSE mode (for remote deployment)
python -m aaa_mcp sse

# HTTP mode (MCP 2025-11-25 spec)
python -m aaa_mcp http
```

### Health Check

```bash
curl https://aaamcp.arif-fazil.com/health
```

Response:
```json
{
  "status": "healthy",
  "postgres_connected": true,
  "redis_connected": true,
  "verdict_rates": {"SEAL": 0.85, "VOID": 0.10, "SABAR": 0.05},
  "motto": "🔥 DITEMPA BUKAN DIBERI 💎🧠🔒"
}
```

---

## 🛠️ Architecture

### High-Level Flow

```
User Query
    ↓
000_INIT (Authentication, Injection Scan)
    ↓
111_AGI_SENSE (Intent Classification)
    ↓
222_AGI_THINK (Hypothesis Generation)
    ↓
333_AGI_REASON (Logical Analysis)
    ↓
555_ASI_EMPATHIZE (Stakeholder Impact)
    ↓
666_ASI_ALIGN (Ethics/Policy Check)
    ↓
888_APEX_VERDICT (Final Judgment)
    ↓
999_VAULT_SEAL (Immutable Record)
    ↓
User Response + Verdict
```

### Infrastructure

| Component | Technology | Status | Environment |
|-----------|-----------|--------|-------------|
| **API Server** | FastMCP + FastAPI | ✅ Operational | `HOST`, `PORT` |
| **Persistent Ledger** | PostgreSQL + asyncpg | ✅ Operational | `DATABASE_URL` |
| **Session Cache** | Redis | ✅ Operational | `REDIS_URL` |
| **Floor Validators** | Python + pydantic | ✅ Operational | Core |
| **Observability** | Prometheus/Grafana | 🔄 In Progress | H1.1 |

---

## 📋 The 14 Canonical Tools

| Tool | Purpose | Organ | Floors |
|------|---------|-------|--------|
| `init_gate` | Initialize session with 🔥 motto | INIT | F11, F12 |
| `trinity_forge` | **Unified pipeline entrypoint** | ALL | ALL |
| `agi_sense` | Parse intent, classify lane | AGI | F2, F4 |
| `agi_think` | Generate hypotheses | AGI | F2, F4, F7 |
| `agi_reason` | Deep logical reasoning | AGI | F2, F4, F7 |
| `asi_empathize` | Stakeholder impact (κᵣ ≥ 0.95) | ASI | F5, F6 |
| `asi_align` | Ethics/policy alignment | ASI | F5, F6, F9 |
| `apex_verdict` | Final constitutional judgment | APEX | F2, F3, F5, F8 |
| `reality_search` | External fact-checking | AGI | F2, F7 |
| `vault_seal` | Seal with 💎🧠🔒 motto | VAULT | F1, F3 |
| `tool_router` | Intelligent routing | — | — |
| `vault_query` | Query sealed records | — | F1, F3 |
| `truth_audit` | Claim verification [EXPERIMENTAL] | — | F2, F4, F7, F10 |
| `simulate_transfer` | Financial simulation | — | F2, F11, F12 |

**Machine-Discoverable**: Access `aaa://capabilities/` for full tool specifications.

---

## 🧪 Development

### Running Tests

```bash
# Quick smoke test (~3 min)
pytest tests/test_startup.py -v

# E2E tests (10 tests)
pytest tests/test_e2e_core_to_aaa_mcp.py -v

# Constitutional floor tests
pytest tests/constitutional/ -v

# With coverage
pytest --cov=aaa_mcp --cov=core tests/ -v
```

### Environment Variables

| Variable | Purpose | Example |
|----------|---------|---------|
| `DATABASE_URL` | PostgreSQL connection | `postgresql://user:pass@host/db` |
| `REDIS_URL` | Redis connection | `redis://default:pass@host:6379` |
| `GOVERNANCE_MODE` | Strictness | `HARD` (default) or `SOFT` |
| `AAA_MCP_TRANSPORT` | Protocol | `stdio`, `sse`, or `http` |
| `BRAVE_API_KEY` | Web search | `BSxx...` |

### Docker

```bash
docker build -t arifos .
docker run -p 8080:8080 -e PORT=8080 arifos
```

---

## 🗺️ Roadmap: The Four Horizons

### 🔥 H1: Foundation Tempering (Now — v60.1-v60.9)
**Status**: Infrastructure operational, hardening in progress

- ✅ PostgreSQL VAULT999 ledger
- ✅ Redis session cache
- ✅ 13 floors enforced
- ✅ ASI floor scoring fixed
- 🔄 `/health` endpoint with governance metrics
- 🔄 SBERT classifier for F5/F6/F9
- 🔄 Test suite recovery (80%+ pass)

### 🟠 H2: Agentic Federation (v61.0-v61.9)
**Theme**: Constitutional Code Review

- 4 H2 Agents (Architect, Engineer, Auditor, Validator)
- Juror democracy (5 agents, 4/5 consensus)
- Constitutional API v1.0
- Python SDK (`arifos.Client`)

### 🟡 H3: Platform Everywhere (v62.0-v62.9)
**Theme**: Industry constitutions + multi-modal

- Medical, Financial, Legal constitutions
- Vision + text governance
- Real-time streaming
- WASM edge deployment

### 🔮 H4: Exploration (v63.0+)
**Theme**: The frontiers

- Cross-model federation (Byzantine Constitutional AI)
- Self-amending constitution
- Human-AI partnerships
- Interplanetary governance

**Full roadmap**: [ROADMAP.md](./ROADMAP.md)

---

## 📊 Key Metrics

| Metric | Current | H1 Target | H2 Target |
|--------|---------|-----------|-----------|
| Test Pass Rate | 70% | 80%+ | 90%+ |
| Production Uptime | — | 99.9% | 99.99% |
| Validations/Day | — | 1,000 | 10,000+ |
| Avg Floor Latency | ~50ms | <100ms | <50ms |

---

## 🏛️ Philosophy

### The Thermodynamic Basis

arifOS grounds AI safety in physical law, not human opinion:

- **F1 Amanah**: Landauer's Principle — irreversible operations cost energy
- **F2 Truth**: Shannon Entropy — information reduces uncertainty  
- **F4 Clarity**: 2nd Law of Thermodynamics — entropy must not increase
- **F7 Humility**: Gödel's Incompleteness — all claims need uncertainty bounds
- **F8 Genius**: Eigendecomposition — intelligence = A×P×X×E²

### 4. Constitutional MCP Gateway (H1.4 FORGED)
*The Control Plane for Docker & Kubernetes.*

| Feature | Constitution | Function |
|:---|:---:|:---|
| **Blast Radius** | **F6 (Empathy)** | Calculates impact score (κᵣ) for all infra ops. |
| **888_HOLD** | **F13 (Sovereign)** | Production changes require human override. |
| **OPA Guard** | **F10 (Ontology)** | Validates manifests against Rego policies. |
| **Trust Chain** | **F2 (Truth)** | Enforces immutable image digests (@sha256). |

> **"Ditempa Bukan Diberi"**: The Gateway is not a firewall; it is a **Constitutional Airlock**. It does not block; it **judges**.

### The Cultural Foundation

The 9 mottos are in **Nusantara Malay-Indonesian**, reflecting:
- Active construction (DI___KAN, not passive)
- Southeast Asian wisdom traditions
- Anti-colonial knowledge sovereignty

> *"Intelligence requires work — DITEMPA BUKAN DIBERI"*

---

## 🤝 Contributing

We welcome contributions that respect the constitutional principles:

1. All code must pass F9 (Anti-Hantu): No consciousness claims
2. All changes must pass F1 (Amanah): Must be reversible or auditable
3. All tests must pass F2 (Truth): Accuracy ≥ 0.99

See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

---

## 📜 License

**AGPL-3.0-only**

arifOS is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, version 3.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

**Commons Clause**: Production use by organizations with >$1M revenue requires a commercial license. Contact: arif@arif-fazil.com

---

## 🙏 Acknowledgments

- **Thermodynamic Foundations**: Rolf Landauer, Claude Shannon, Ludwig Boltzmann
- **Constitutional Theory**: Jon Elster, Cass Sunstein, Bruce Ackerman
- **Malay Wisdom**: Hamka, Tan Malaka, Pramoedya Ananta Toer
- **AI Safety**: Stuart Russell, Nick Bostrom, Paul Christiano

---

## 🔗 Resources

| Resource | URL |
|----------|-----|
| **Live Instance** | https://aaamcp.arif-fazil.com |
| **Health Check** | https://aaamcp.arif-fazil.com/health |
| **Documentation** | https://arifos.arif-fazil.com |
| **MCP Registry** | `io.github.ariffazil/aaa-mcp` |
| **PyPI** | `pip install arifos` |
| **Docker** | `ariffazil/arifos:60.0.0` |

---

## 💎 Creed

<p align="center">
  <strong>DITEMPA BUKAN DIBERI</strong><br>
  <em>Forged, Not Given — 🔥💎🧠🔒</em>
</p>

The fire is lit at the 🔥 INIT gate.  
The diamond is cut at the 💎🧠 SEAL gate.  
The horizons await.

---

*Constitutional Kernel v60.1-FORGE*  
*Last Tempered: 2026-02-11*  
*MCP Registry: io.github.ariffazil/aaa-mcp*
