---
type: Integration
tags: [platform, wiring, four-surface, mcp, a2a]
epistemic_level: OBS
last_sync: 2026-04-11
---

# GEOX Platform Wiring

> **Type:** platform wiring map  
> **Epistemic Level:** OBS  
> **Last Updated:** 2026-04-11  
> **Scope:** sibling platform repo at `/root/geox-platform`

---

## Summary

`geox-platform/` is a **real four-surface integration stack** around GEOX:

1. **Site** — static human-facing surface
2. **WebMCP** — browser-native capability surface
3. **MCP** — Python MCP server for tools/resources/prompts
4. **A2A** — agent-to-agent gateway

The important current-state fact is:

> **Surface 3 in `geox-platform` is wired to the root GEOX backend file `geox_unified.py`, not to the modular `arifos/geox/tools/adapters/fastmcp_adapter.py` target.**

That means the platform is **operational**, but it is operational on a **transitional backend surface**.

---

## Connection Map

| From | To | Method | Current Status |
|------|----|--------|----------------|
| Site | WebMCP | browser manifest | Active |
| WebMCP | browser handlers | JavaScript runtime | Active |
| MCP server | GEOX backend | Python import | Active |
| A2A gateway | MCP server | HTTP / MCP tool calls | Active |
| Site | static assets | nginx | Active |

---

## Key Files

| Path | Purpose |
|------|---------|
| `/root/geox-platform/docker-compose.yml` | Full four-surface orchestration |
| `/root/geox-platform/WIRING.md` | Detailed connection guide |
| `/root/geox-platform/PLATFORM.md` | High-level four-surface architecture |
| `/root/geox-platform/services/mcp-server/geox_mcp_server.py` | Wired MCP server |
| `/root/geox-platform/services/mcp-server/Dockerfile` | MCP container build |

---

## What Surface 3 Currently Imports

The platform MCP server imports directly from GEOX root-level unified code:

```python
from geox_unified import (
    geox_fetch_authoritative_state,
    geox_set_scene,
    geox_render_scene_context,
    geox_compute_stoiip,
    geox_validate_operation,
    geox_audit_hold_breach,
    geox_synthesize_causal_scene,
)
```

This gives the platform live access to:

- scene establishment
- authoritative scene fetch
- STOIIP computation
- operation validation
- hold-breach audit
- synthesis prompt building

---

## Deploy Topology

Current compose mapping in `geox-platform/docker-compose.yml`:

| Service | Port | Role |
|---------|------|------|
| `geox-site` | `8080` | Surface 1 — site |
| `geox-unified` | `8000` | GEOX backend |
| `geox-mcp` | `8001` external → `8000` container | Surface 3 — wired MCP |
| `geox-a2a` | `3002` | Surface 4 — agent gateway |
| `nginx` | `80` | reverse proxy |

The platform mounts the GEOX repo into the MCP container for imports:

```yaml
- ../GEOX:/app/geox-backend:ro
```

---

## No-Chaos Interpretation

This platform wiring changes the GEOX architectural picture in one specific way:

### True at the same time

1. **The preferred merge target inside `GEOX/` is still the modular adapter path**
   - `arifos/geox/tools/core.py`
   - `arifos/geox/tools/adapters/fastmcp_adapter.py`

2. **The live external platform currently depends on root `geox_unified.py`**
   - because `geox-platform/services/mcp-server/geox_mcp_server.py` imports it directly

So the correct documentation stance is:

- **Live integration truth:** platform MCP is wired and operational today
- **Refactor truth:** the current platform dependency is transitional and should eventually converge on one canonical backend surface

---

## Merge Guidance

### Short term

- Treat `geox-platform` as a valid deployed integration layer
- Do not document it as imaginary or future work
- Do not falsely describe its backend dependency as already modular

### Medium term

- Decide whether `geox_unified.py` becomes:
  1. the canonical backend wrapper, or
  2. a compatibility layer over `arifos/geox/tools/adapters/fastmcp_adapter.py`

- Update `geox-platform/services/mcp-server/geox_mcp_server.py` only after that decision

### Long term

- One GEOX backend surface
- One public MCP contract
- One platform wiring story

---

## Practical Rule

If you are tracing **what is live now**, start with:

1. `/root/geox-platform/services/mcp-server/geox_mcp_server.py`
2. `/root/GEOX/geox_unified.py`
3. `/root/geox-platform/docker-compose.yml`
4. `/root/geox-platform/WIRING.md`

If you are tracing **what GEOX should converge to**, start with:

1. `/root/GEOX/arifos/geox/tools/core.py`
2. `/root/GEOX/arifos/geox/tools/adapters/fastmcp_adapter.py`
3. `GEOX_REPO_STATE_AND_COMPONENT_MAP.md`

---

*Platform wiring map v2026-04-11*  
*DITEMPA BUKAN DIBERI — Forged, not given.*
