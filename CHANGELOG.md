# CHANGELOG — arifOS Constitutional AI Kernel

All changes follow [T000 versioning](T000_VERSIONING.md): `YYYY.MM.DD-PHASE-STATE`.  
**Creed:** DITEMPA BUKAN DIBERI — Forged, Not Given.

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
