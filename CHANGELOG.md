# CHANGELOG — arifOS Constitutional AI Kernel

All changes follow [T000 versioning](T000_VERSIONING.md): `YYYY.MM.DD-PHASE-STATE`.  
**Creed:** DITEMPA BUKAN DIBERI — Forged, Not Given.

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
