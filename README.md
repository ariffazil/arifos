<div align="center">

<img src="https://raw.githubusercontent.com/ariffazil/arifOS/main/sites/library/static/img/banner_sovereign.png" width="100%" alt="arifOS Ecosystem Banner">

# arifosmcp
### Hardened Constitutional MCP Runtime & Reality Engine

**[Theory](https://github.com/ariffazil/arifOS)** • **[Live MCP](https://arifosmcp.arif-fazil.com/mcp)** • **[Health](https://arifosmcp.arif-fazil.com/health)** • **[Status](https://arifosmcp.arif-fazil.com/status)** • **[Tools](https://arifosmcp.arif-fazil.com/tools)**

*Ditempa Bukan Diberi*

[![Status](https://img.shields.io/badge/Status-Hardened-00b894.svg?style=flat-square)](https://arifosmcp.arif-fazil.com/health)
[![Release](https://img.shields.io/badge/Release-2026.03.13--FORGED-blue.svg?style=flat-square)](https://github.com/ariffazil/arifosmcp/commits/main)
[![Public Tools](https://img.shields.io/badge/Public%20Tools-12-success.svg?style=flat-square)](https://arifosmcp.arif-fazil.com/tools)
[![License](https://img.shields.io/badge/License-AGPL%203.0-lightgrey.svg?style=flat-square)](./LICENSE)

</div>

`arifosmcp` is the **engine (BRAIN)** of the arifOS ecosystem. It is a production-grade Model Context Protocol (MCP) server that provides the live execution environment for the constitutional kernel, manages the unified reality acquisition lane, and serves real-time telemetry for sovereign AI agents.

## Layer Doctrine (Machine • Governance • Intelligence 3E)

- **Machine**: transport, auth, tool exposure, runtime health, continuity. Asks: Can the system run?
- **Governance**: constitutional checks, authority logic, verdict formation. Asks: Should the system proceed?
- **Intelligence (3E)**: Exploration → Entropy → Eureka. Asks: What is the best structure of understanding?

### MGI Schema Contracts (SEALTRIWITNESS Phase 2)

Every tool response now follows strict **Machine → Governance → Intelligence** separation:

```python
class GovernedResponse(BaseModel):
    machine: MachineEnvelope       # READY/BLOCKED/DEGRADED/FAILED
    governance: GovernanceEnvelope # APPROVED/PARTIAL/HOLD/REJECTED/VOID
    intelligence: IntelligenceEnvelope  # 3E: Exploration→Entropy→Eureka
```

This mechanizes **F7 Humility**: the AI cannot return READY without explicitly calculating `uncertainty_score` and listing `unstable_assumptions`.

## The Sovereign Quad Contrast

arifOS is distributed across four specialized domains. `arifosmcp` serves as the runtime backbone:

| Repository | Domain | Role | Analogy |
| --- | --- | --- | --- |
| **[arifOS](https://github.com/ariffazil/arifOS)** | **SOUL (Theory)** | Epistemic root, mathematical foundations, and Manifesto. | The Lawgiver |
| **[arifosmcp](https://github.com/ariffazil/arifosmcp)** | **BRAIN (Engine)** | Live execution, tool surface, and reality acquisition. | **The Engine Room** |
| **[arifos-apps](https://github.com/ariffazil/arifos-apps)** | **MIND (Safety)** | Human-facing interfaces, safety apps, and documentation. | The Curator |
| **[arif-fazil.com](https://arif-fazil.com)** | **BODY (Authority)** | Human epistemic root and final 888_JUDGE terminal. | The Sovereign |

---

## Live State

Last verified on `2026-03-13` (Hardened + SEALTRIWITNESS Phase 2).

| Item | Current state |
| --- | --- |
| GitHub `main` | `0cc47a6a` |
| Public MCP version | `2026.03.13-FORGED` |
| Public transport | `streamable-http` |
| Public tools | `12` |
| Runtime health | `SEALED / HEALTHY` |
| Reality Lane | `Hardened (Brave 1.0 + Browserless Fallback)` |
| F11 Continuity | `Bootstrap Whitelist Enabled` |
| Vector Memory | `Qdrant Auto-Ingest Active` |
| 3E Telemetry | `Universal Schema Wired` |

---

## Unified Reality Lane (v1)

The current forged state introduces the **Reality Compass**, a hardened unification of search and fetch capabilities:

- **`reality_compass`**: The single entry point for all reality acquisition. Automatically routes between query search and deep URL scraping. Includes rich forensics (DNS timings, status codes, engine diagnostics).
- **`reality_atlas`**: Ingests `EvidenceBundles` into a semantic graph for ground-truth reasoning.
- **`reality_dossier`**: **Tri-Witness Decoder** — synthesizes evidence into human-facing verdicts with full 3E telemetry (Exploration→Entropy→Eureka).
- **Brave 1.0 Integration**: Fixed 422 errors via optimized header/locale handling.
- **Fail-Safe Scrape**: Automatic `browserless` fallback for WAF-blocked (403/429) URLs.
- **Vector Auto-Ingest**: EvidenceBundles automatically sync to Qdrant with BGE-M3 embeddings.

## Public Tool Surface

The live registry exposes these `12` tools:

1.  `arifOS_kernel`: The main constitutional reasoning entrypoint.
2.  **`reality_compass`**: Unified search and fetch engine.
3.  **`reality_atlas`**: Semantic evidence graph manager.
4.  **`reality_dossier`**: Tri-Witness Decoder with 3E synthesis.
5.  `init_anchor_state`: F11 session ignition (bootstrap whitelisted).
6.  `revoke_anchor_state`: F11 session revocation.
7.  `check_vital`: Real-time system and constitutional health.
8.  `audit_rules`: Inspect 13 floors and runtime module hooks.
9.  `session_memory`: Contextual vector persistence.
10. `verify_vault_ledger`: Forensic proof-of-work validation.
11. `open_apex_dashboard`: Integrated ops visualizer.
12. `search_reality` / `ingest_evidence`: Hardened search/fetch aliases.

---

## SEALTRIWITNESS Phase 2 Features

### 🔒 F11 Bootstrap Whitelist
Phase 1 deadlock resolved: `init_anchor_state`, `revoke_anchor_state`, and `check_vital` can run without prior auth_context. The system can now bootstrap itself.

### 🧠 MGI Schema Contracts
Strict separation of concerns across three layers:
- **Machine**: Mechanical state (READY/BLOCKED/DEGRADED/FAILED)
- **Governance**: Constitutional verdict (APPROVED/PARTIAL/HOLD/REJECTED/VOID)
- **Intelligence**: 3E telemetry (Exploration→Entropy→Eureka)

### 🌊 Vector Auto-Ingest Bridge
Automatic synchronization of EvidenceBundles to Qdrant:
- BGE-M3 embeddings (1024 dims)
- Tri-Witness metadata preservation
- Fire-and-forget async (non-blocking)
- Configurable via `ARIFOS_AUTO_VECTOR_SYNC`

### 📊 Universal 3E Wiring
Every tool response includes:
```json
{
  "intelligence_state": {
    "exploration": "BROAD|SCOPED|EXHAUSTED",
    "entropy": "LOW|MANAGEABLE|HIGH|CRITICAL", 
    "eureka": "NONE|PARTIAL|FORGED",
    "uncertainty_score": 0.5,
    "unstable_assumptions": [],
    "conflicts": []
  }
}
```

---

## Repository Topography

| Path | Purpose |
| --- | --- |
| `arifosmcp/runtime/` | FastAPI/FastMCP runtime surface and public registry. |
| `arifosmcp/runtime/reality_handlers.py` | Hardened search/fetch logic and error mapping. |
| `arifosmcp/runtime/reality_dossier.py` | Tri-Witness Decoder with 3E synthesis. |
| `arifosmcp/intelligence/tools/vector_bridge.py` | Qdrant auto-sync with BGE-M3 embeddings. |
| `core/contracts/responses.py` | MGI Schema Contracts (Machine→Governance→Intelligence). |
| `core/` | Constitutional kernel, floors, and judgment logic. |
| `core/kernel/` | Stage orchestrators and engine adapters. |
| `core/governance/apex_notification.py` | 888_HOLD notification bridge (n8n, Telegram). |
| `scripts/arifos-cli` | Sovereign CLI with SALAM handshake. |
| `tests/` | Runtime, contract, and adversarial validation. |

## Production Operations

Fast path on the VPS:

```bash
cd /srv/arifosmcp
git pull --ff-only
docker restart arifosmcp_server
```

Verify deployment:
```bash
# Health check
curl -fsS https://arifosmcp.arif-fazil.com/health

# Tool registry
curl -fsS https://arifosmcp.arif-fazil.com/tools

# Bootstrap test (no auth required)
curl -X POST https://arifosmcp.arif-fazil.com/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"init_anchor_state","arguments":{"declared_name":"Sovereign"}}}'
```

---

## Architecture Principles

| Principle | Implementation |
|-----------|----------------|
| **F7 Humility** | `uncertainty_score` mandatory in all responses |
| **F11 Continuity** | Cryptographic session tokens with bootstrap whitelist |
| **F3 Tri-Witness** | Human × AI × Earth consensus in reality_dossier |
| **ΔS ≤ 0** | Entropy reduction tracked across all operations |
| **VOID Protection** | Machine failures ≠ Constitutional VOID |

*DITEMPA BUKAN DIBERI — Forged, Not Given.*
