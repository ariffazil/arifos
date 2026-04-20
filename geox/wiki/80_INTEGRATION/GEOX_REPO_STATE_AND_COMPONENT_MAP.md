---
type: Integration
tags: [repo-state, component-map, refactor, merge, canonical]
epistemic_level: OBS
last_sync: 2026-04-11
---

# GEOX Repo State and Component Map

> **Type:** Repo-state map  
> **Epistemic Level:** OBS  
> **Last Updated:** 2026-04-11  
> **Scope:** `/root/GEOX` as currently checked into the repository  
> **Purpose:** give GEOX one merge/refactor map so we reduce redundancy without deleting signal

---

## Executive Summary

GEOX is **not one clean runtime yet**. The repository currently contains:

1. A large **canonical package candidate** under `arifos/geox/`
2. A second, smaller **Earth Intelligence Core branch** under `geox/`
3. Multiple **root-level FastMCP/server variants** with overlapping tool names
4. A **React cockpit** in `geox-gui/`
5. A wiki that still mixes these generations together as if they were already one surface

For merge/refactor work, the cleanest target is:

```text
arifos/geox/                       ← canonical domain package
  tools/core.py                    ← host-agnostic tool logic
  tools/adapters/fastmcp_adapter.py← canonical FastMCP transport
  contracts/ + services/ + physics/← structured domain/runtime support
geox-gui/                          ← canonical UI
wiki/                              ← canonical docs
```

Everything else should be treated as **transitional**, **legacy**, or **extract-only** until explicitly merged.

---

## Canonical vs Transitional vs Legacy

| Zone | Primary Paths | Current Role | Merge / Refactor Verdict |
|------|---------------|--------------|--------------------------|
| **Canonical backend target** | `arifos/geox/` | Main Python package with THEORY, ENGINE, governance, tools, schemas, memory, physics, renderers | **KEEP and converge into this** |
| **Canonical transport target** | `arifos/geox/tools/adapters/fastmcp_adapter.py` | Thin FastMCP layer over host-agnostic tool core | **KEEP as public server target** |
| **Canonical UI target** | `geox-gui/src/` | React/Vite cockpit with state, layouts, witnesses, Malay Basin dashboard | **KEEP** |
| **Docs target** | `wiki/` | Canonical documentation surface | **KEEP and sync to repo reality** |
| **Secondary backend branch** | `geox/` | Smaller Earth Intelligence Core package with its own tool registry and server | **DO NOT treat as primary runtime** |
| **Root-level server variants** | `geox_mcp_server.py`, `geox_sse_server.py`, `geox_unified*.py`, `geox_acp_integrated.py`, `geox_rest_bridge.py` | Mixed transport experiments, bridge surfaces, and older compositions | **COLLAPSE behind one wrapper or archive** |
| **Historical / parking lots** | `archive/`, `legacy/`, `_archive/`, `_deprecated/` | Old material and parked assets | **KEEP out of active architecture** |

---

## Component Map — Backend

### 1. Canonical package candidate: `arifos/geox/`

| Area | Key Paths | Responsibility |
|------|-----------|----------------|
| THEORY | `THEORY/` | ToAC taxonomy, governance policies, contrast canon |
| ENGINE | `ENGINE/` | contrast space, transform registry, anomaly / wrapper logic |
| Governance | `governance/` | floors, audits, verdict rendering |
| Core tools | `tools/core.py` | transport-agnostic domain functions |
| FastMCP adapter | `tools/adapters/fastmcp_adapter.py` | `@mcp.tool` bindings, health routes, CLI factory |
| Contracts | `contracts/` | typed results and schemas |
| Physics / petrophysics | `physics/`, `schemas/`, `tools/services/` | Sw, petrophysics, cutoff and hold logic |
| Memory | `geox_memory.py` | geological memory abstraction and fallback behavior |
| Examples / resources | `examples/`, `resources/`, `knowledge/` | demos, pilot data, supporting material |

### 2. Secondary package: `geox/`

| Path | What it is now | Refactor stance |
|------|----------------|-----------------|
| `geox/server.py` | Separate 7-tool Earth Intelligence Core server | Treat as an alternate branch, not the canonical runtime |
| `geox/core/` | Separate tool registry + AC risk logic | Mine useful pieces, then merge selectively into `arifos/geox` |
| `geox/apps/` | App-oriented surface for the smaller branch | Compare against `geox-gui`, then consolidate intentionally |

### 3. Root-level server files

| File | Observed role | Risk |
|------|---------------|------|
| `geox_mcp_server.py` | Root FastMCP server exposing bridge/physics tools like `geox_compute_stoiip`, `geox_verify_physics` | Name suggests canonical entrypoint, but behavior diverges from modular adapter |
| `geox_sse_server.py` | SSE/HTTP-oriented server variant | Extra transport surface |
| `geox_unified.py` / `geox_unified_fixed.py` / `geox_unified_backup.py` | Unified experiments / backups | High drift risk |
| `geox_acp_integrated.py` | ACP-focused integrated variant | Specialized, not a clean public entrypoint |
| `geox_rest_bridge.py` | REST bridge wired to unified server | Depends on non-canonical variant |

**Rule:** only one root-level entrypoint should remain visible to operators. Everything else should either become:

1. an internal module,
2. a wrapper to the canonical adapter, or
3. an archived artifact.

---

## Component Map — Tool Surfaces

The repo currently exposes **multiple tool surfaces with overlapping names**.

| Surface | File | Observed tool shape |
|--------|------|---------------------|
| **Canonical modular FastMCP surface** | `arifos/geox/tools/adapters/fastmcp_adapter.py` | 12 tools: seismic, prospect, memory, saturation, petrophysics, hold check, health |
| Governed seismic/prospect surface | `arifos/geox/geox_mcp_server.py` | 5 tools centered on seismic/prospect workflows |
| Smaller EIC surface | `geox/server.py` | 7 tools centered on AC risk + EIC interpretation |
| Root bridge/physics surface | `geox_mcp_server.py` | 8 tools centered on scene synthesis, STOIIP, physics verification |
| Root unified surface | `geox_unified.py` | scene-setting and unified bridge functions used by sibling platform wiring |
| AAA / hardened variants | `arifos/geox/mcp_server_aaa.py`, `mcp_server_hardened.py`, `mcp_petrophysics_server.py` | Specialized or historical subsets/supersets |

### Canonical modular tool surface

The strongest merge target is still the modular adapter:

```text
arifos/geox/tools/core.py
        ↓
arifos/geox/tools/adapters/fastmcp_adapter.py
        ↓
one supported public entrypoint
```

Why:

- transport and business logic are already separated
- petrophysics and health are already wired here
- docs already point to this structure in several places
- it is easier to test, wrap, and expose consistently

---

## External Integration Map — `geox-platform/`

There is also a sibling integration repo at `/root/geox-platform` that packages GEOX as a **four-surface platform**:

1. Site
2. WebMCP
3. MCP
4. A2A

### Current live wiring

| Platform Surface | Path | Current GEOX dependency |
|------------------|------|-------------------------|
| Site | `geox-platform/apps/site/` | static assets + registry |
| WebMCP | `geox-platform/apps/site/webmcp.manifest.json` and browser handlers | browser-only capability layer |
| MCP | `geox-platform/services/mcp-server/geox_mcp_server.py` | **imports from root `geox_unified.py`** |
| A2A | `geox-platform/services/a2a-gateway/` | delegates to MCP over HTTP |

### Why this matters

The external platform is **real and wired now**, but it is wired to a **transitional GEOX backend surface**:

```text
geox-platform/services/mcp-server/geox_mcp_server.py
        ↓ imports
/root/GEOX/geox_unified.py
```

So two things are true at once:

- **Live integration truth:** `geox-platform` is operational and uses real GEOX code
- **Convergence truth:** GEOX should still reduce toward one canonical backend path inside `arifos/geox/`

See [[GEOX_PLATFORM_WIRING]] for the four-surface wiring map.

---

## Component Map — GUI

| Area | Key Paths | Notes |
|------|-----------|-------|
| Active app shell | `geox-gui/src/main.tsx` → `App.tsx` | **Current GUI boot path** |
| Active layout branch | `components/Layout/MainLayout.tsx` | Used by `App.tsx` |
| Alternate design branch | `AppForge.tsx`, `components/Layout/MainLayoutForge.tsx`, `forge/domain/*` | Valuable design work, but currently parallel to active app shell |
| Core state | `store/geoxStore.ts` | Governance floors, connection state, layers, selections |
| Domain panels | `components/EarthWitness/`, `LogDock/`, `MalayBasinPilot/`, `WellContextDesk/`, `WitnessBadges/` | Main feature modules |
| Domain experiments | `domains/Domain1D.tsx`, `Domain2D.tsx`, `Domain3D.tsx`, `DomainLEM.tsx`, `DomainVoid.tsx` | Parallel domain modeling surface |
| Host adapters | `adapters/openai_adapter.ts`, `useOpenAI.ts` | Host integration layer |

### GUI merge rule

Choose **one** of these as the public shell:

1. `App.tsx` + `MainLayout.tsx`
2. `AppForge.tsx` + `MainLayoutForge.tsx`

Do not keep both as equal first-class entrypoints long term. Keep one active, move the other to an explicit experimental path.

---

## Observed Drift and Redundancy

These are the biggest no-chaos issues visible in the repo right now:

| Drift | Evidence | Why it matters |
|------|----------|----------------|
| Root entrypoint name implies canonical status | `pyproject.toml` exposes `geox-server = "geox_mcp_server:mcp.run"` | Operators are steered to a root server that is not the modular adapter |
| Docs claim unified behavior across entrypoints | `wiki/80_INTEGRATION/FASTMCP_CLI_GUIDE.md` said legacy and modern paths are identical | They are not identical today |
| External platform depends on transitional surface | `geox-platform/services/mcp-server/geox_mcp_server.py` imports `geox_unified` directly | Integration is live, but the dependency path is not yet the modular target |
| Wiki mixes multiple tool counts and eras | `README.md`, `wiki/index.md`, `Tool_Index.md`, and server files describe different tool sets | Causes operator confusion and bad integration assumptions |
| Backend duplication | `arifos/geox/`, `geox/`, and root-level `geox_*` server files coexist | Same concepts are implemented multiple times |
| GUI branch duplication | `App.tsx` and `AppForge.tsx` both exist as app shells | Easy for refactors to diverge silently |
| Adapter self-report drift | `fastmcp_adapter.py` logs `Tools (11)` while the file defines 12 `@mcp.tool` functions | Even internal diagnostics are out of sync |

---

## Recommended Merge Target Architecture

```text
wiki/                                   ← source of truth docs
geox-gui/                               ← one active cockpit shell
arifos/geox/
  THEORY/ ENGINE/ governance/           ← domain foundations
  tools/core.py                         ← one host-agnostic tool layer
  tools/adapters/fastmcp_adapter.py     ← one FastMCP transport
  contracts/ schemas/ services/ physics/← supporting types and engines
root geox_mcp_server.py                 ← thin wrapper only, or remove
```

### Public surface rule

Only these should be public-facing after consolidation:

1. **One Python package:** `arifos/geox`
2. **One supported MCP entrypoint:** the FastMCP adapter or a thin wrapper to it
3. **One GUI shell:** the selected `geox-gui` app entry
4. **One tool registry source:** the canonical registry tied to the chosen adapter

---

## Merge / Refactor Lanes

### Lane 1 — Backend package convergence

- Keep `arifos/geox/` as the target package
- Compare `geox/core/*` against `arifos/geox/tools/services/*` and `contracts/*`
- Move useful logic by extraction, not copy-paste duplication
- Do not let both `geox/` and `arifos/geox/` keep evolving in parallel

### Lane 2 — Entrypoint convergence

- Make `geox_mcp_server.py` either:
  - a thin compatibility wrapper around `arifos.geox.tools.adapters.fastmcp_adapter`, or
  - an explicitly deprecated legacy file
- Retire or quarantine extra variants: `geox_unified*.py`, `geox_sse_server.py`, `geox_acp_integrated.py`, `geox_rest_bridge.py`

### Lane 3 — Registry and tool truth

- Choose one registry as authoritative
- Align docs, health endpoints, and CLI discovery to that registry
- Ensure tool counts in docs/logs are generated from code, not hand-maintained tables

### Lane 4 — GUI convergence

- Decide whether `App.tsx` or `AppForge.tsx` is the main shell
- Keep the other as an explicit design lab or archive it
- Keep governance badges and floor visibility as non-negotiable UI constraints

### Lane 5 — Test and deploy convergence

- Point tests at the chosen entrypoint
- Point `pyproject.toml` scripts at the chosen entrypoint
- Point wiki quickstarts and deployment docs at the chosen entrypoint
- Update `geox-platform` imports only after the canonical backend wrapper decision is explicit

---

## No-Chaos Rules

1. **One concept, one home.** If a capability has two live homes, choose one and demote the other.
2. **One public entrypoint.** Root-level convenience files must not diverge from the real runtime.
3. **One registry of tools.** Tables in docs should follow code, not opinion.
4. **One active UI shell.** Parallel shells are allowed only if one is clearly experimental.
5. **Archive aggressively, not ambiguously.** If a file is historical, move it where history is expected.
6. **Document transitional status explicitly.** Do not call a file "thin wrapper" unless it truly is one.

---

## Immediate Practical Reading Order

If you need to understand GEOX quickly, read in this order:

1. `arifos/geox/__init__.py`
2. `arifos/geox/tools/core.py`
3. `arifos/geox/tools/adapters/fastmcp_adapter.py`
4. `geox-gui/src/main.tsx`
5. `geox-gui/src/App.tsx`
6. `geox-gui/src/store/geoxStore.ts`
7. `wiki/50_TOOLS/Tool_Index.md`
8. `wiki/80_INTEGRATION/FASTMCP_CLI_GUIDE.md`

That path gives the cleanest picture of where GEOX should converge, even though the repo still contains older branches.

---

*Repo-state map v2026-04-11*  
*DITEMPA BUKAN DIBERI — Forged, not given.*
