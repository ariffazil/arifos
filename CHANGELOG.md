# CHANGELOG — arifOS Constitutional AI Kernel

All changes follow [T000 versioning](T000_VERSIONING.md): `YYYY.MM.DD-PHASE-STATE`.  
**Creed:** DITEMPA BUKAN DIBERI — Forged, Not Given.

---

## [2026.2.18] — 2026-02-18 — FORGE-MCP-PROTOCOL-SEAL

**T000:** 2026.02.18-FORGE-MCP-PROTOCOL-SEAL  
**Theme:** Full MCP JSON-RPC protocol compliance for SSE transport

### Fixed
- **`/messages` endpoint** — Complete MCP JSON-RPC protocol implementation:
  - `initialize` — Returns protocolVersion, serverInfo, capabilities
  - `notifications/initialized` — Client acknowledgment (empty response)
  - `ping` — Keepalive method
  - `tools/list` — Returns full tool schemas with inputSchema
  - `tools/call` — Execute tools with proper JSON-RPC response format
- **Route ordering** — Moved catch-all `/{tool_name}` to END of route list to prevent
  intercepting `/sse` and `/messages` requests
- **POST /sse handling** — Now returns proper HTTP 405 (Method Not Allowed) instead of 404
- **FunctionTool calling** — Fixed `tools/call` to use `.fn` attribute for FastMCP FunctionTool
  objects (they are not directly callable)

### Technical Details
- Starlette routes now correctly ordered: specific routes first, catch-all last
- SSE endpoint accepts both GET (streaming) and POST (405 response)
- All MCP lifecycle methods return proper JSON-RPC 2.0 responses
- Tool schemas include full inputSchema with properties, required fields, and enums

---

## [2026.2.17] — 2026-02-17 — FORGE-VPS-SEAL

**T000:** 2026.02.17-FORGE-VPS-SEAL  
**Theme:** Infrastructure sovereignty + H1.1 Production Observability

### Added
- **H1.1 Production Observability** — `/health` now returns granular governance metrics:
  - `postgres.status` / `postgres.lag_ms` — VAULT999 ledger liveness
  - `redis.status` / `redis.version` — MindVault session cache liveness
  - `core_pipeline.verdict` — Live constitutional pipeline verdict on health check
  - `mcp_tools.tool_count` — Count of registered MCP tools
  - `memory.percent` / `memory.available` — Host memory pressure
- **Starlette lifespan context** in `aaa_mcp/rest.py` — health checks now register on
  application startup instead of requiring `main()` to be called
- `EnvironmentFile=/opt/arifos/.env` in systemd unit — secrets loaded securely from disk,
  not baked into service file

### Fixed
- `HealthMonitor.check_all` now merges dict return values from individual checks instead
  of discarding sub-fields (postgres lag, redis version, pipeline verdict were all silently lost)
- `HealthMonitor.status[name]` now correctly reflects `{"status": False}` dict results
  (previously `bool(dict)` was always `True`)
- `redis_client.get_redis_client` replaced brittle manual URL parser with `redis.from_url`
  — fixes crash on `redis://localhost:6379/0` (DB index `/0` broke `int(port_str)`)
- Postgres `permission denied for schema public` — granted `ALL ON SCHEMA public TO arifos`
- `monitoring.py` critical tool list updated to use MCP verb names (`anchor`, `reason`, …)
  instead of internal graph names (`init_gate`, `agi_sense`, …)
- `rest.py` missing stdlib imports (`datetime`, `asyncio`, `uvicorn`, `json`, `time`, `uuid`)
  that caused `NameError` on VPS startup after import refactor

### Changed
- **Deployment platform: Railway → Hostinger VPS** (primary)
  - `railway.toml` deleted
  - `docker-compose.railway-local.yml` → `docker-compose.yml`
  - `DEPLOYMENT.md` rewritten for VPS (systemd + nginx + certbot)
  - `arifosmcp.nginx.conf` rewritten: proxy to port 8080, SSE-safe (no buffering, `proxy_buffering off`)
  - `server.json` SSE URL updated: `arifos-production.up.railway.app` → `arifosmcp.arif-fazil.com`
- `pyproject.toml` URLs corrected: `aaamcp.arif-fazil.com` → `arifosmcp.arif-fazil.com`

### Infrastructure (VPS)
- Systemd service `arifos-mcp.service` — auto-start, `Restart=always`, `RestartSec=5`
- Nginx reverse proxy with SSL (Let's Encrypt) — `arifosmcp.arif-fazil.com`
- PostgreSQL 17 (native) + Redis 8.0.2 (native) — both healthy and connected

---

## [2026.2.15] — 2026-02-15 — FORGE-TRINITY-SEAL

**T000:** 2026.02.15-FORGE-TRINITY-SEAL  
**Theme:** Codebase consolidation + MCP schema alignment + T000 versioning

### Added
- `core/shared/sbert_floors.py` — SBERT-based semantic floor classifier for F5/F6/F9
  replacing keyword heuristics (H1.2 foundation); lazy-loads `all-MiniLM-L6-v2`
- `aaa_mcp/config/capability_modules.yaml` — migrated from `arifos/config/`
- `MCP_NAME_TO_REGISTRY` dict and `get_tool_by_mcp_name()` in `aaa_mcp/protocol/tool_registry.py`
- `MCP_TO_GRAPH` dict in `aaa_mcp/protocol/tool_graph.py`
- `trinity_forge` added to `server.json` (was implemented but missing from schema)
- `AGENTS.md` rewritten as focused 150-line agent guide for coding agents

### Removed
- `arifos/` — entire pre-v52 legacy package (no `__init__.py`, not importable, 3 dead files)
- `codebase/` — 82 files / 21,047 lines of dead code (agi/, asi/, apex/, init/, shared/, vault/)
  Runtime (`aaa_mcp/server.py`) was already importing 100% from `core/`
- `core/asi/` — single-file subdirectory; `sbert_floors.py` moved to `core/shared/`
- `build/` — stale setuptools artifact directory
- `railway.toml`, `docker-compose.railway-local.yml` (renamed)
- 6 test files archived to `tests/archive/` (depended on deleted `codebase/` / `arifos/` APIs)

### Fixed
- `server.json` floor descriptions now match actual `@constitutional_floor()` decorators
  (e.g. `align` was claiming F5+F6+F9 but decorator is only F9)
- `core/shared/floors.py` F8 Genius check removed stale `from codebase.floors.genius import`
  try/except; collapsed to the fallback path that was always running
- `pyproject.toml` stale `arifos*` / `codebase*` package discovery entries removed
- mypy overrides updated from `arifos.*` to `core.*`

### Changed
- `core/organs/_2_asi.py` import: `from core.asi.sbert_floors` → `from core.shared.sbert_floors`
- `aaa_mcp/server.py` capability YAML path: `../arifos/config/…` → `config/…` (local)

---

## [2026.1.26] — 2026-01-26 — LIVE-DASHBOARD-SEAL

**Theme:** Live governance metrics, dashboard integration, constitutional floor pass 13/13

### Added
- `LiveMetricsService` — real-time constitutional metrics from VAULT999 ledger
- Live τ (truth), κᵣ (empathy), Ψ (vitality), ΔS (clarity) computation
- `/metrics/json` endpoint serving live data with `calibration_mode` transparency

### Fixed
- Removed all static placeholder metrics (0.99, 0.98, 0.85)
- τ now computed from actual eval harness; Ω₀ from uncertainty engine

---

## [2026.1.24] — 2026-01-24 — UNIFIED-CORE-SEAL

**Theme:** AAA_MCP unified, pure bridge architecture

### Changed
- `aaa_mcp/` becomes pure transport adapter — all decision logic moved to `core/`
- `core/` established as the single decision kernel with no transport imports

---

## [2026.1.18] — 2026-01-18 — CONSTITUTIONAL-FORGE

**Theme:** 13 Constitutional Floors, Trinity Engines, MCP foundation

### Added
- 13 constitutional floors F1–F13 with hard/soft enforcement
- Trinity architecture (ΔΩΨ): AGI Mind, ASI Heart, APEX Soul
- 9-tool MCP pipeline: anchor → reason → integrate → respond → validate → align → forge → audit → seal
- VAULT999 immutable ledger with Merkle chaining
- `@constitutional_floor()` decorator for automatic floor enforcement

---

*Format: [T000 Date] — Date — PHASE-STATE | Full spec: T000_VERSIONING.md*
