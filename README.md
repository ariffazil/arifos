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

Last verified on `2026-03-13` (Hardened).

| Item | Current state |
| --- | --- |
| GitHub `main` | `70b19e9a` |
| Public MCP version | `2026.03.13-FORGED` |
| Public transport | `streamable-http` |
| Public tools | `12` |
| Runtime health | `SEALED / HEALTHY` |
| Reality Lane | `Hardened (Brave 1.0 + Browserless Fallback)` |
| F11 Continuity | `Fingerprint-backed` |

---

## Unified Reality Lane (v1)

The current forged state introduces the **Reality Compass**, a hardened unification of search and fetch capabilities:

- **`reality_compass`**: The single entry point for all reality acquisition. Automatically routes between query search and deep URL scraping. Includes rich forensics (DNS timings, status codes, engine diagnostics).
- **`reality_atlas`**: Ingests `EvidenceBundles` into a semantic graph for ground-truth reasoning.
- **Brave 1.0 Integration**: Fixed 422 errors via optimized header/locale handling.
- **Fail-Safe Scrape**: Automatic `browserless` fallback for WAF-blocked (403/429) URLs.

## Public Tool Surface

The live registry exposes these `12` tools:

1.  `arifOS_kernel`: The main constitutional reasoning entrypoint.
2.  **`reality_compass`**: Unified search and fetch engine.
3.  **`reality_atlas`**: Semantic evidence graph manager.
4.  `init_anchor_state`: F11 session ignition.
5.  `check_vital`: Real-time system and constitutional health.
6.  `audit_rules`: Inspect 13 floors and runtime module hooks.
7.  `session_memory`: Contextual vector persistence.
8.  `bootstrap_identity`: Identity declaration and F11 anchoring.
9.  `verify_vault_ledger`: Forensic proof-of-work validation.
10. `open_apex_dashboard`: Integrated ops visualizer.
11. `search_reality`: (Alias) Hardened search.
12. `ingest_evidence`: (Alias) Hardened fetch.

---

## Repository Topography

| Path | Purpose |
| --- | --- |
| `arifosmcp/runtime/` | FastAPI/FastMCP runtime surface and public registry. |
| `arifosmcp/runtime/reality_handlers.py` | Hardened search/fetch logic and error mapping. |
| `core/` | Constitutional kernel, floors, and judgment logic. |
| `core/kernel/` | Stage orchestrators and engine adapters. |
| `tests/` | Runtime, contract, and adversarial validation. |

## Production Operations

Fast path on the VPS:

```bash
cd /srv/arifosmcp
git pull --ff-only
uv run python -m arifosmcp.runtime http
```

Verify deployment:
```bash
curl -fsS https://arifosmcp.arif-fazil.com/health
curl -fsS https://arifosmcp.arif-fazil.com/tools
```

*DITEMPA BUKAN DIBERI — Forged, Not Given.*
