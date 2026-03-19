# Changelog

All notable changes to arifOS MCP are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed
- **Runtime Limits**: Increased memory ceilings for Traefik, AgentZero, and Browserless to prevent OOM under load.

### Fixed
- **Browserless Fetch**: Token is optional when unset; content requests now match Browserless payload validation.
- **REST Tool Output**: Normalized datetime serialization for `/tools/*` responses.

## [2026.03.19] - ANTI-CHAOS

### Added
- **One Truth for State**: Unified session and identity resolution via `resolve_runtime_context`.
- **Identity Precedence**: Hard enforcement of `actor_id` > `declared_name` > `anonymous`.
- **Session Truth Surface**: Tool envelopes now explicitly emit `transport_session_id` (debug) and `resolved_session_id` (canonical).
- **Recovery Packets**: Error envelopes now include `required_next_tool`, `required_fields`, and `example_payload` for autonomous healing.
- **Authority Levels**: Added `user` level to `AuthorityLevel` enum for standardized validation.
- **Hardened Preflight**: Enhanced `openclaw-preflight.sh` with Redis health checks and service-aware arifOS MCP routing.

### Changed
- **Truth Retirement**: Retired "Implicit Fallback Authority" — raw transport values can no longer masquerade as resolved truth.
- **`global` Demotion**: The `global` session ID is now explicitly labeled as a `fallback` transport value, not anchored truth.
- **`AuthorityLevel` Alignment**: Pydantic validation now strictly enforces the 9 canonical authority levels.

### Fixed
- **Identity Promotion Bug**: Prevented `declared_name` from overriding `actor_id` in `init_anchor` and `metabolic_loop`.
- **Preflight Reachability**: Fixed Docker-to-Host networking defaults in preflight scripts.

## [2026.03.17] - ANTICHAOS

### 🔐 Security & Identity (F11/F13)
- **Identity & Auth System**: Implemented complete F11/F13 constitutional identity layer
  - Actor registry with authority levels: `anonymous`, `declared`, `user`, `operator`, `agent`, `sovereign`
  - Signed auth_context with HMAC-SHA256 cryptographic verification
  - Scope-based access control for kernel execution
  - Time-bound tokens (15-minute TTL) with session binding
- **Authority Levels**:
  - `sovereign` (arif/ariffazil): Full access including vault seal and agentzero engineer
  - `agent` (openclaw/agentzero): Limited execution scope
  - `operator` (operator/cli): Execute access
  - `user` (user/test_user): Limited execution
  - `anonymous`: Blocked from kernel execution (diagnostics only)

### 🚀 Features
- **A2A Protocol**: Added `/a2a/execute` endpoint for Trinity Probe integration (Google A2A standard)
- **OpenClaw Integration**: Hardened configuration for production deployment
  - LAN binding with token auth
  - Telegram bot integration with pairing mode
  - Nervous system tools exposed to MCP
- **Static Sites**: Fixed routing and links for static file serving
- **Canonical Output Schema**: Unified envelope format across all 42 tools

### 🔧 Technical
- **Auth Context**: Properly minted auth_context with all required fields:
  - `session_id`, `actor_id`, `authority_level`
  - `token_fingerprint`, `nonce`, `iat`, `exp`
  - `approval_scope`, `parent_signature`, `signature`
- **Bridge Hardening**: F11 validation in `arifOS_kernel` calls
- **Tool Registry**: Fixed canonical naming (`arifOS_kernel` not `arifOS.kernel`)
- **VAULT999**: Synchronized ledger and integrity verification

### 🐛 Bug Fixes
- Fixed Verdict shadowing issues across modules
- Resolved Browserless 401 authentication errors
- Fixed MCP connection stability
- Restored provider breadth after probe concurrency issues
- Telegram bot config changed to pairing mode with user ID allowlist

### 📚 Documentation
- **AGENTS.md v2**: Complete rewrite with 42-tool runtime documentation
  - Identity & Auth section with actor registry
  - F1-F13 floor enforcement details
  - Canonical tool contract examples
- **SPEC.md**: Constitutional kernel specification
- **CLAUDE.md**: Agent instructions for Claude Code integration

### 🧪 Testing
- E2E benchmarks updated
- `get_caller_status` tests added
- VAULT999 ledger integrity tests

## [2026.03.14] - REALITY-SEALED

### Features
- **WebMCP Gateway**: W3C-standard MCP over HTTP endpoints
- **A2A Server**: Google Agent-to-Agent protocol implementation
- **Agent Card**: `/.well-known/agent.json` for agent discovery
- **Double Helix Architecture**: Inner ring (metabolic) + Outer ring (circulatory)

### Technical
- **42-Tool Runtime**: Constitutional kernel with F1-F13 enforcement
- **sBERT ML Floors**: Semantic validation for constitutional constraints
- **VAULT999**: Immutable ledger with SHA-256 Merkle chain
- **Qdrant Memory**: Vector memory for session continuity

### Integrations
- **Ollama Local**: `qwen2.5:3b`, `bge-m3`, `nomic-embed-text`
- **Venice AI**: Decentralized inference
- **OpenRouter**: Multi-provider routing
- **Browserless**: Headless browser automation

## [2026.03.08] - UNIFICATION

### Foundation
- **Constitutional Kernel**: 9-stage pipeline (000_INIT → 999_VAULT)
- **F1-F13 Floors**: Hard constraints on reversibility, truth, sovereignty
- **APEX Theory**: Governance framework for agent judgment
- **AgentZero**: Meta-agent orchestration layer

### Runtime
- **MCP 2025-11-25**: Streamable HTTP transport
- **Tool Unification**: Consolidated 26 → 42 canonical tools
- **Phase 1 Alignment**: SPEC.md canonical output schema

## [2026.03.01] - IGNITION

### Initial Release
- **arifOS MCP Server**: Constitutional kernel v1.0
- **APEX-G**: Metabolic governance engine
- **HELIX**: Session continuity and telemetry
- **VAULT999**: Immutable audit trail

---

## Version Naming Convention

- **YYYY.MM.DD** - Date-based versioning
- **Codename** - Philosophical state descriptor:
  - `IGNITION` - Initial spark
  - `UNIFICATION` - Consolidation phase
  - `REALITY-SEALED` - Production hardening
  - `ANTICHAOS` - Chaos reduction, alignment

## Categories

- 🔐 **Security**: Authentication, authorization, encryption
- 🚀 **Features**: New capabilities and integrations
- 🔧 **Technical**: Architecture, performance, refactoring
- 🐛 **Bug Fixes**: Error corrections
- 📚 **Documentation**: Guides, specs, examples
- 🧪 **Testing**: Test suites, benchmarks

---

*DITEMPA BUKAN DIBERI — Forged, Not Given*
