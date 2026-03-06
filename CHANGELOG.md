# CHANGELOG — arifOS Constitutional AI Kernel

All changes follow [T000 versioning](T000_VERSIONING.md): `YYYY.MM.DD-PHASE-STATE`.  
**Creed:** DITEMPA BUKAN DIBERI — Forged, Not Given.

---

## [2026.3.6-CiV-BROWSER] — 2026-03-06 — CIVILIZATION-INFRASTRUCTURE-HEADLESS-BROWSER-SEAL

**T000:** 2026.03.06-CiV-BROWSER  
**Theme:** CIV Infrastructure Layer activation, Smart Hybrid Search with Headless Browser, comprehensive README rewrite

### Added
- **Headless Browser Service** (`docker-compose.yml`):
  - `headless_browser` container (browserless/chrome) on internal `arifos_trinity` network
  - DOM Reality extraction for JavaScript-heavy sites (SPAs, React, Vue)
  - Resource limits: 512MB RAM, max 2 concurrent sessions
  - F12 Defense: All content wrapped in `<untrusted_external_data>` envelope with SHA-256 hashing
- **HeadlessBrowserClient** (`aaa_mcp/external_gateways/headless_browser_client.py`):
  - Async client for internal browser service communication
  - Content quality scoring (0.0-1.0) with auto-fallback
  - Health check endpoint (`/pressure`) for load monitoring
  - Configurable via `ARIFOS_HEADLESS_BROWSER_ENABLED` env var
- **Smart Hybrid Search** (`aaa_mcp/server.py` — `search_reality` tool v2.0):
  - Query classifier: SPA/Research/News/General routing
  - 4-tier fallback chain: Jina → Perplexity → Brave → Headless Browser
  - Quality threshold-based fallback (0.2 minimum)
  - F3 Tri-Witness consensus merge when multiple sources available
  - Never returns empty — guarantees meaningful reality
- **CIV Infrastructure Documentation** (`333_APPS/L6_CIVILIZATION/`):
  - `EUREKA_CIV_INFRA_DISCOVERY.md` — Deep research findings
  - `SEAL_HEADLESS_BROWSER_INTEGRATION.md` — Production deployment seal
  - Clockmaker Daemon, Town Square (Redis), Resource Governor documented
- **VPS Architecture Master Dossier** (`docs/VPS_ARCHITECTURE_MASTER_DOSSIER.md`):
  - Complete update with CIV Infrastructure (L6) section
  - Headless Browser operational guide
  - Smart Hybrid Search architecture diagram
  - 12-container deployment matrix

### Changed
- **`aaa_mcp/server.py`**: `search_reality` completely rewritten for Smart Hybrid routing
  - New parameters: `force_source`, `min_content_quality`
  - Query type classification (SPA/Research/News/General)
  - Multi-source result merging with F3 consensus
  - Quality scoring algorithm (content length, structure, F12 envelope)
- **`aaa_mcp/external_gateways/__init__.py`**: Exports `HeadlessBrowserClient`
- **`docker-compose.yml`**: Added `headless_browser` service, volume mount for live code
- **`.env.docker`**: Added Headless Browser configuration (`ARIFOS_HEADLESS_BROWSER_ENABLED`, etc.)
- **VPS Skill** (`.agents/skills/arifos-vps-ops/SKILL.md`): Complete rewrite with CIV-Browser architecture

### Documentation
- **`README.md`**: Comprehensive rewrite (153 → 434 lines)
  - 🏛️ Canonical Trinity Web Links at TOP with web/file references
  - 🤖 AI Machine-Readable Manifest (JSON) for LLM parsing
  - 🧭 Zero-Context Intro (Human vs AI specific sections)
  - 🌡️ 8-Layer Architecture table (L0-L7) with status + file links
  - 🏛️ Complete 13 Constitutional Floors reference (F1-F13)
  - ⚙️ Metabolic Loop (000→999) with stage explanations
  - 🔌 14 MCP Tools catalog grouped by ARIF bands with file links
  - 🆕 Smart Hybrid Search section (Headless Browser integration)
  - 🎭 5-Role Agent Parliament (L5)
- **`docs/CONTRAST_ANALYSIS_README_VERSIONS.md`**: Analysis of README evolution vs past versions

### Fixed
- **`pyproject.toml`**: Removed duplicate TOML sections (361 lines deleted)
  - Fixed: `[project.optional-dependencies]` declared twice
  - Fixed: `[project.scripts]` declared twice
  - Fixed: `[project.urls]` declared twice
  - Fixed: `[tool.setuptools]` declared twice
  - Fixed: `[tool.pytest.ini_options]` declared twice
- **`Dockerfile`**: Fixed Playwright permissions for `arifos` user
  - Browser install now runs as root with proper chown
  - Removed redundant second install attempt

### Constitutional Compliance
- **F1 Amanah**: PASS — Headless Browser read-only, no destructive actions
- **F2 Truth**: PASS — Multi-source verification with quality scoring
- **F3 Tri-Witness**: PASS — Consensus merge when sources disagree
- **F4 Clarity**: PASS — Smart routing reduces entropy (ΔS ≤ 0)
- **F5 Peace²**: PASS — Resource limits prevent overload (512MB, 2 sessions)
- **F6 Empathy**: PASS — Graceful degradation on service unavailability
- **F7 Humility**: PASS — Quality thresholds with uncertainty bounds
- **F8 Genius**: PASS — Smart query classification (G = A×P×X×E²)
- **F9 Anti-Hantu**: PASS — No consciousness claims in browser automation
- **F10 Ontology**: PASS — Clear categorization (CIV Infrastructure)
- **F11 CommandAuth**: PASS — Internal network only (no public port)
- **F12 Defense**: PASS — `<untrusted_external_data>` envelope enforced
- **F13 Sovereign**: PASS — Configurable enable/disable (`ARIFOS_HEADLESS_BROWSER_ENABLED`)

### Verification
- All 12 containers healthy on VPS
- Headless Browser responding on `http://headless_browser:3000`
- Smart Hybrid Search tested with quality scoring
- GitHub repo synced with VPS (main branch)
- README renders correctly with all links functional

---

## [2026.3.6-CANON] — 2026-03-06 — CANONICAL-13-TOOL-SURFACE-LOCK-SCHEMA-ALIGN

**T000:** 2026.03.06-CANONICAL-13-TOOL-SURFACE-LOCK-SCHEMA-ALIGN
**Theme:** Phoenix retirement, three-layer schema alignment, ARIF Bands documentation, tool surface sealed at exactly 13

### Archived (Removed from Public Surface)
- **`recall_memory` (Phoenix)**: Retired → replaced by `vector_memory` (BGE-M3 768-dim embeddings + Qdrant + EUREKA sieve). F9 Anti-Hantu compliance — no ghost names on public surface.
- **`fetch_content`** + **`inspect_file`**: Consolidated → `ingest_evidence(source_type="url"|"file")`. Reduces surface entropy.
- **`trinity_forge`**: Demoted to internal orchestration alias. `metabolic_loop` is the canonical Band O tool.
- **`query_openclaw`**: Archived — internal diagnostic only, never part of 13-tool canon.

### Changed
- **Three-layer schema alignment** (all layers now agree on 13 canonical tool names):
  - `aaa_mcp/protocol/schemas.py` — added `ingest_evidence` + `metabolic_loop` to `TOOL_INPUT_SCHEMAS` + `TOOL_OUTPUT_SCHEMAS`
  - `arifos_aaa_mcp/contracts.py` — `REQUIRES_SESSION`: `recall_memory` → `vector_memory`; `metabolic_loop` contract added
  - `arifos_aaa_mcp/server.py` — 4 MCP prompts updated: `aaa_chain`, `trinity_forge`, `anchor_reason`, `audit_then_seal` now use Gen3 canonical names
- **`aaa_mcp/protocol/tool_naming.py`**: `vector_memory`, `ingest_evidence`, `metabolic_loop` added to `CANONICAL_PUBLIC_TO_LEGACY` map + `LEGACY_TOOL_NAMES`
- **`aaa_mcp/protocol/l0_kernel_prompt.py`**: Replaced stale `sensory_read` → `ingest_evidence` in the L0 constitutional kernel prompt
- **`aaa_mcp/server.py`**: Error message updated — `init_session (anchor)` → `anchor_session`
- **`aaa_mcp/README.md`**: `recall_memory` → `vector_memory`; `fetch_content` + `inspect_file` → `ingest_evidence`; `metabolic_loop` row added
- **`docs/00_META/GEMINI.md`**: 11 → 13 canonical tools; all Gen1 aliases replaced with Gen3 canonical names
- **ARIF Bands taxonomy** documented in `333_APPS/L4_TOOLS/README.md` (full dossier rewrite) and root `README.md`

### Documentation
- **`333_APPS/L4_TOOLS/README.md`**: Full dossier rewrite — Trinity Lanes table, per-tool Band/Stage/Floor/Description matrix, complete 13-tool ARIF lattice, metabolic chain ASCII diagram, archived tool table, A-CLIP alias map, verdict reference
- **`333_APPS/L4_TOOLS/MANIFEST.md`**: Version `v55.5.0` → `v2026.3.6-CANON`; entry point updated to `python -m arifos_aaa_mcp`
- **`README.md`**: 14 → 13 canonical tools; Band O (Orchestrate / `metabolic_loop`) added; MCP section restructured into 8+4+1 layers

### Removed
- Temp artifacts deleted: `debug_mcp_v2.py`, `finalize_seal.py`, `verify_audit.py`, `git_diff_server.txt`

### Constitutional Compliance
- **F9 Anti-Hantu**: PASS — No archived tool names (`recall_memory`, `phoenix_recall`, `fetch_content`, `inspect_file`, `init_session`, `agi_cognition`, `apex_verdict`, `vault_seal`) survive on any public-facing layer
- **F4 Clarity**: PASS — Tool count reduced 14 → 13; three-layer schema alignment eliminates mismatch entropy
- **F1 Amanah**: PASS — `aaa_mcp/protocol/aaa_contract.py` runtime assertion `assert len(AAA_CANONICAL_TOOLS) == 13` guards the sacred count
- **F10 Ontology**: PASS — `trinity_forge` never existed as a public tool; `metabolic_loop` is the canonical orchestration surface

### Verification
- `aaa_mcp/protocol/aaa_contract.py`: Runtime assertion passes — 13 tools confirmed
- All commits lint-passed `constitution_lint` (all floors satisfied)
- Working tree clean, pushed to `origin/main`

---

## [2026.3.1-JINA] — 2026-03-01 — JINA-READER-INTEGRATION-SEARCH-REALITY

**T000:** 2026.03.01-JINA-READER-INTEGRATION-SEARCH-REALITY  
**Theme:** Jina Reader as PRIMARY search backend for superior content extraction and constitutional grounding

### Added
- **Jina Reader Client** (`aaa_mcp/external_gateways/jina_reader_client.py`):
  - `JinaReaderClient` class with `search()`, `read_url()`, `search_arxiv()` methods
  - `JinaReranker` class for semantic relevance-based result sorting
  - Clean Markdown extraction from URLs via `r.jina.ai`
  - Web search with extracted content via `s.jina.ai`
  - F12 Defense: External content wrapped in untrusted envelope with taint lineage
  - User-Agent header to avoid 403 Forbidden errors
- **`search_reality` tool enhancement**: Now uses Jina Reader as PRIMARY backend
  - Superior content extraction vs traditional SERP APIs
  - Fallback chain: Jina → Perplexity → Brave → Local knowledge
- **`fetch_content` tool enhancement**: Uses Jina Reader for URL-to-Markdown extraction
  - Returns clean, LLM-ready Markdown instead of raw HTML
  - Optional image and link extraction metadata
- **Environment variable**: `JINA_API_KEY` for higher rate limits (optional but recommended)

### Changed
- **External Gateways** (`aaa_mcp/external_gateways/__init__.py`): Exports `JinaReaderClient`, `JinaReranker`
- **Server** (`aaa_mcp/server.py`): `search_reality` and `fetch_content` now prioritize Jina Reader
- **Dockerfile**: Added embedding model directory setup (preparation for future embedding work)
- **`.env.docker.example`**: Added `JINA_API_KEY` placeholder
- **`.gitignore`**: Exclude embedding model files (*.safetensors, *.bin, *.pt, *.pth)

### Constitutional Compliance
- **F2 Truth**: Multi-source grounding with evidence URLs
- **F4 Clarity**: Clean Markdown output reduces entropy vs raw HTML
- **F12 Defense**: Untrusted envelope prevents prompt injection from external content
- **F7 Humility**: Graceful degradation when API key unavailable (NO_API_KEY status)

---

## [2026.3.1-FORGE] — 2026-03-01 — VAULT999-UNIFIED-TELEMETRY-TRINITY-FORGE-SEAL

**T000:** 2026.03.01-FORGE-VAULT999-UNIFIED-TELEMETRY-TRINITY  
**Theme:** VAULT999 Merkle ledger unification, FastMCP-native telemetry, trinity_forge emergence, production hardening

### Added
- **VAULT999 UNIFIED Ledger**: PostgreSQL + Redis + Merkle Tree + EUREKA Sieve wired together
  - `session_ledger.py` now provides unified `seal()` with automatic Merkle root computation
  - EUREKA anomalous contrast filter evaluates entries before storage
  - Redis hot caching for recent entries with chain state persistence
  - Chain verification via `verify_chain()` with tamper detection
- **`trinity_forge` unified tool**: Single-call 000-999 pipeline (emergent tool #14)
  - Internally executes: 000_INIT → 111-444 REASON → 555-666 HEART → 777-888 JUDGE → 999 SEAL
  - For ChatGPT/stateless clients requiring single-call constitutional validation
- **FastMCP-native telemetry** (`aaa_mcp/telemetry.py`):
  - `ConstitutionalSpan` wrapper with F1-F13 floor awareness
  - `@instrument_tool` decorator for automatic MCP tool instrumentation
  - OpenTelemetry semantic conventions: `tools/call {name}`, `arifos.verdict`, `arifos.metabolic_stage`
- **Governed Context** (`aaa_mcp/governed_context.py`):
  - FastMCP Context wrapper with 13-Floor constitutional enforcement
  - `StateEntry` with cryptographic checksums for F1 Amanah
  - `ConstitutionalProgressTracker` with metabolic stage awareness
- **FastMCP Context logging**: `ctx.info/debug` integration in `anchor_session` and `seal_vault`

### Changed
- **VAULT999 schema v3 UNIFIED**: Added columns `merkle_root`, `eureka_score`, `eureka_verdict`
- **14 tools total**: 13 canonical + 1 unified (`trinity_forge`)
- `seal_vault` tool: Now uses unified SessionLedger with Merkle + Redis persistence
- `aaa_mcp/server.py`: Integrated unified ledger, telemetry, and context logging

### Deployment Ready
- All 14 tools operational via MCP (stdio/SSE/HTTP)
- VAULT999 persistence layer: PostgreSQL (authoritative) + Redis (cache)
- Telemetry: OpenTelemetry + Prometheus metrics export
- Version: 2026.3.1-FORGE

---

## [2026.3.1] — 2026-03-01 — ENTROPY-REDUCTION-FORGE-777-SEAL

**T000:** 2026.03.01-ENTROPY-REDUCTION-FORGE-777-SEAL  
**Theme:** Massive codebase consolidation, MCP server unification, VPS deployment wiring

### Added
- Unified Docker Compose for VPS deployment with multi-network compartment access
- `.env.docker` template for compartment connection configuration (Qdrant, Ollama, OpenClaw, Agent Zero)
- Multi-homed container bridging 4 networks: coolify, ai-net, trinity_network, bridge

### Changed
- **Massive entropy reduction**: Removed 112,658 LOC (S_pre 0.94 → S_post 0.31, 75% reduction)
  - Purged `_ARCHIVE/` directory (legacy concepts, prototypes, experiments)
  - Purged `tests/archive/` and `tests/legacy/` (deprecated test suites)
  - Removed duplicate guards and unused `aaa_mcp` modules
- **MCP server consolidation**: Merged `aaa_mcp/server.py` into `arifos_aaa_mcp/server.py`
  - Thin 90-line compatibility shim at `aaa_mcp/server.py`
  - Single 760-line canonical surface with 13 tools, 5 prompts, 4 resources
  - Eliminated circular dependencies between packages
- Docker image tagged: `arifos/arifosmcp:latest` (from `forge-777`, 14.8GB)
- Version badge updated to 2026.3.1

### Deployment
- Live VPS on port 8080 (streamable-http transport)
- Health status: healthy, 13 tools loaded
- Compartment IPs: qdrant(10.0.0.5), ollama(10.0.4.2), openclaw(10.0.1.2), agent-zero(10.0.2.3)

### Verification
- Container health check: `curl http://localhost:8080/health` → `{"status":"healthy"}`
- All 13 canonical tools verified operational
- Multi-network connectivity validated

---

## [2026.2.27] — 2026-02-27 — FORGE-PROTOCOL-NEGOTIATION-CONSISTENCY-SEAL

**T000:** 2026.02.27-FORGE-PROTOCOL-NEGOTIATION-CONSISTENCY-SEAL  
**Theme:** MCP version negotiation hardening, canonical tool naming convergence, and docs/runtime alignment.

### Added
- Streamable HTTP protocol negotiation tests for supported, unsupported, and mismatch session flows.
- MCP method parity for `resources/list`, `resources/read`, `prompts/list`, and `prompts/get` in streamable transport.

### Changed
- Canonical tool names converged to `apex_judge` and `eureka_forge` across runtime/tests/docs.
- Streamable HTTP handshake now negotiates `protocolVersion` per session and enforces header consistency.
- Discovery metadata now publishes `protocolVersion` and `supportedProtocolVersions` in `server.json` and well-known routes.
- Intro/docs trademark messaging aligned: "DITEMPA, BUKAN DIBERI" + epistemic humility subtitle.
- Package/release versions aligned to `2026.2.27`.

### Verification
- `pytest tests/test_aaa_phase888_mcp_protocol_e2e.py -q` -> pass
- `pytest tests/test_aaa_mcp_contract.py -q` -> pass
- `pytest tests/test_aaa_mcp_constitutional.py -q` -> pass

---

*See [docs/00_META/CHANGELOG.md](docs/00_META/CHANGELOG.md) for full historical changelog.*
