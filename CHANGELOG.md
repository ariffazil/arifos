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

## [2026.03.20] - SOVEREIGN11

### 🎯 MAJOR CONTRAST CHANGE: Complete Alignment & Truth Sealing
**This release represents the definitive alignment of all system surfaces—code, documentation, and configuration now reflect a single source of truth.**

#### Contrast: Before vs After
| Aspect | Before (CONSOLIDATION) | After (SOVEREIGN11) |
|--------|------------------------|---------------------|
| **Tool Count Claim** | 42 tools → 11 tools (37 modes) | **11 tools (39 modes)** — All modes verified |
| **apex_soul modes** | 6 modes (missing `probe`, `notify`) | **7 modes** — Full F12/F13 defense coverage |
| **engineering_memory modes** | 4 modes (missing `query`, `write`) | **5 modes** — Complete memory surface |
| **architect_registry modes** | 1 mode (`list` only) | **3 modes** — Full CRUD surface |
| **Documentation** | AGENTS.md claimed 26 legacy tools | **11 Mega-Tools** with exhaustive mode matrix |
| **Version Badge** | 2026.03.21-RELIABLE | **2026.03.20-SOVEREIGN11** — Matches server.py |
| **WebMCP** | Mounted 2x (duplicate root mounts) | **Single mount** — Clean routing |
| **mcp_tools.yaml** | 9 legacy tools (outdated) | **11 Mega-Tools** — Synced with implementation |

### 🔧 Alignment Fixes

#### Mode Enum Synchronization
- **`InitAnchorMode`**: Added `refresh` (was missing)
- **`ApexSoulMode`**: Added `notify`, `probe` (was missing)
- **`EngineeringMemoryMode`**: Added `recall`, `write` (was missing)
- **All 11 tools**: 39 modes now aligned across:
  - `tool_specs.py` (schema definitions)
  - `capability_map.py` (enum definitions)
  - `mcp_tools.yaml` (YAML config)
  - `README.md` (documentation)
  - `AGENTS.md` (agent guidance)

#### Documentation Truth Sealing
- **AGENTS.md**: Rewrote tool table — removed false 26-tool claim, documented actual 11 Mega-Tools
- **README.md**: 
  - Fixed version badge (2026.03.20-SOVEREIGN11)
  - Updated mode counts (37 → 39)
  - Added missing modes to tool descriptions
  - Fixed architect_registry (was incomplete)
  - Fixed engineering_memory (was incomplete)
- **mcp_tools.yaml**: Complete rewrite from 9 legacy tools to 11 Mega-Tools

#### Code Cleanup
- **server.py**: Removed duplicate WebMCP mounting (22 lines eliminated)
  - Was mounting WebMCP gateway twice at root `/`
  - Could cause routing conflicts and double initialization

### 🏛️ Architectural Verification
- **Contract Verification**: All 11 tools pass `verify_contract()`
- **Registry Drift Check**: 11/11 tools matched, 0 missing, 0 extra
- **Mode Alignment**: All 39 modes verified across all surfaces
- **No orphaned capabilities**: All legacy tools redirect to 11-tool modes

### 📚 Documentation
- **Trinity Matrix Rename**: `THE SURFACE` → `THE SOUL` (docs/AGENTS.md)
- **Comprehensive README Rewrite**: Full Trinity matrix, LLM formatting, 14-section structure
- **Geologist Identity**: README now emphasizes petroleum engineering background
- **Contrast Analysis**: Added explicit before/after tables

### 🐛 Bug Fixes
- **F10 Ontology Leak**: Fixed in `engineering_memory` modes
- **Enum Mismatches**: All 11 tool mode enums now consistent
- **Schema Alignment**: `tool_specs.py` ↔ `capability_map.py` ↔ `mcp_tools.yaml`

### 🔐 Governance Improvements
- **11-Tool Mega-Surface**: Definitive execution surface
  - Governance Layer: 4 tools (16 modes)
  - Intelligence Layer: 3 tools (10 modes)
  - Machine Layer: 4 tools (13 modes)
- **F1-F13 Mapping**: Explicit floor coverage per tool
- **Mode-Based Dispatch**: Legacy compatibility via `mode` parameter

### 📜 Key Commits in This Release
- `71d22521d` - docs: Fix F10 Ontology leak in engineering_memory modes
- `385c34637` - docs: Rename THE SURFACE to THE SOUL across Trinity Matrix
- `525225d4b` - docs: Rewrite comprehensive README with Trinity matrix
- `4214cf2e7` - README: HARDENED — geologist identity + contrast analysis
- `cd327a891` - forge: Wire Qdrant memory, Postgres audit
- `99d0029ff` - fix: VPS infrastructure wiring
- `2e3510add` - feat: Implement arifOS Metabolic Loop Orchestrator
- `0ff5c023b` - release: v2026.03.21-RELIABLE — Fixed Enum mismatch
- `2e98d95b6` - Forge: Smoke Test Remediation - Fix BUG-01/02/03
- `8b2f4fce6` - Forge: Sacred Chain Alignment - Final 000-999 hardening
- `2820f592c` - Forge: ABI Stability & Nervous System Unity
- `f305be498` - Forge: Final ABI Hardening - Structured intent alignment
- `4e1db8074` - fix: P0 CRITICAL FIXES — F11 Identity Hardening
- `8590e6ea5` - fix: COMPREHENSIVE CONTRACT DRIFT RESOLUTION
- `6162124fa` - release: v2026.03.20-CONSOLIDATION — 11-Tool surface

---

## [2026.03.20] - CONSOLIDATION

### 🔧 11-Tool Mega-Surface Consolidation
**BREAKING CHANGE**: The 42-tool surface has been consolidated into 11 constitutional mega-tools with mode-based dispatch.

- **Governance Layer (4 tools)**
  - `init_anchor` — Session establishment with modes: `init`, `revoke`, `refresh`
  - `arifOS_kernel` — Metabolic orchestration with modes: `kernel`, `status`
  - `apex_soul` — Constitutional judgment with modes: `judge`, `rules`, `validate`, `hold`, `armor`, `notify`, `probe`
  - `vault_ledger` — Immutable persistence with modes: `seal`, `verify`

- **Intelligence Layer (3 tools)**
  - `agi_mind` — First-principles reasoning with modes: `reason`, `reflect`, `forge`
  - `asi_heart` — Safety & empathy with modes: `critique`, `simulate`
  - `engineering_memory` — Technical execution with modes: `engineer`, `query`, `recall`, `write`, `generate`

- **Machine Layer (4 tools)**
  - `physics_reality` — World grounding with modes: `search`, `ingest`, `compass`, `atlas`
  - `math_estimator` — Quantitative analysis with modes: `cost`, `health`, `vitals`
  - `code_engine` — System introspection with modes: `fs`, `process`, `net`, `tail`, `replay`
  - `architect_registry` — Resource discovery with modes: `register`, `list`, `read`

**Impact**: 39 modes across 11 tools provide the same functional surface as 42 individual tools, with cleaner constitutional governance and reduced cognitive load for agent callers.

### 🐛 Bug Fixes
- **Circular Import Resolution**: Fixed infinite recursion in `arifosmcp/runtime/__init__.py` that blocked server startup
  - Changed `from . import tools_internal` to `importlib.import_module()` pattern
  - All 11 tools now load without ImportError

### 📚 Documentation
- **DEPLOY_CHECKLIST.md**: Comprehensive VPS deployment guide
- **FINAL_SEAL.md**: Pre-deployment verification checklist
- **AUDIT_REPORT_11_MEGA_TOOLS.md**: Architecture audit of tool consolidation

### 🏛️ Architectural Improvements
- **F1-F13 Coverage**: All 13 constitutional floors explicitly mapped to 11-tool surface
- **Mode Dispatch**: Legacy tool functions accessible via `mode` parameter (no orphaned capabilities)
- **Tool Registry**: Updated `public_registry.py` with 11-tool contracts and mode specifications

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
- **AGENTS.md v2**: Complete rewrite with 11-tool mega-surface documentation
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

## Appendix: Evolution Contrast Matrix

### Major Version Contrasts

| Release | Tool Surface | Architecture | Identity | Documentation |
|---------|--------------|--------------|----------|---------------|
| **2026.03.01 IGNITION** | 0 tools (concept) | Theory only | None | Manifesto |
| **2026.03.08 UNIFICATION** | 26 tools | 9-stage pipeline | Implicit | SPEC.md draft |
| **2026.03.14 REALITY-SEALED** | 42 tools | Double Helix | Implicit | Protocol Trinity |
| **2026.03.17 ANTICHAOS** | 42 tools | F11/F13 Auth | **Explicit registry** | Identity docs |
| **2026.03.19 ANTI-CHAOS** | 42 tools | One Truth State | Authority levels | Session truth |
| **2026.03.20 CONSOLIDATION** | **11 Mega-Tools** | Mode dispatch | Token lifecycle | 11-tool audit |
| **2026.03.20 SOVEREIGN11** | **11 Mega-Tools (39 modes)** | **Aligned surfaces** | **Verified auth** | **Truth-sealed** |

### Key Contrast: 42 Tools → 11 Mega-Tools

**Before (Fragmented):**
```
search_reality(mode="search")
ingest_evidence(url)
reality_compass(query)
reality_atlas(bundles)
↓
4 separate tools, 4 different signatures, 4 cognitive loads
```

**After (Consolidated):**
```
physics_reality(mode="search", input=...)
physics_reality(mode="ingest", input=url)
physics_reality(mode="compass", input=query)
physics_reality(mode="atlas", bundles=...)
↓
1 mega-tool, 4 modes, unified interface, single cognitive load
```

**Benefits:**
- Reduced API surface complexity by 74% (42 → 11)
- Unified error handling and recovery
- Simpler constitutional governance (map 11 tools, not 42)
- Mode-based dispatch preserves all functionality

### Mode Discovery Pattern

All 11 Mega-Tools follow the same interface:
```python
{
  "mode": "MODE_NAME",     # One of N modes per tool
  "payload": {...},        # Mode-specific parameters
  "auth_context": {...},   # F11 identity proof
  "risk_tier": "medium",   # Execution posture
  "dry_run": true          # Safety first
}
```

---

*DITEMPA BUKAN DIBERI — Forged, Not Given*
