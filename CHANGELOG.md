# Changelog

All notable changes to arifOS are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2026.03.13-FORGED] - 2026-03-13

### 🏛️ Grand Unified Technical Specification (GUTS) — MGI 7-Tool Canonical Stack

This release implements the **Grand Unified Technical Specification** (27-page spec), establishing the complete MGI (Machine-Governance-Intelligence) 7-tool canonical stack.

---

### 🔴 VOID Memanjang Elimination (CRITICAL)

**The Problem:** Legacy code used `except Exception: return VOID` for ANY error — network timeouts, missing dependencies, 404s — all returned VOID (constitutional collapse).

**The Fix:** VOID is now **STRICTLY** reserved for actual constitutional violations (F2/F11/F12/F13 breaches).

**New Fault Taxonomy:**

| Class | Codes | Verdict |
|-------|-------|---------|
| `MechanicalFaultCode` | `TOOL_NOT_EXPOSED`, `INFRA_DEGRADED`, `TIMEOUT_EXCEEDED`, `RATE_LIMITED`, `DEPENDENCY_UNAVAILABLE`, `DNS_FAIL`, `TLS_FAIL`, `WAF_BLOCK`, `PARSE_FAIL`, `RENDER_FAIL` | `888_HOLD` |
| `ConstitutionalFaultCode` | `F2_TRUTH_BELOW_THRESHOLD`, `F11_AUTH_FAILURE`, `F11_TOKEN_INVALID`, `F12_INJECTION`, `F10_ONTOLOGY`, `F13_SOVEREIGN_VETO` | `VOID` (terminal) |
| `Epistemic` | `NO_RESULTS` | `SABAR` |

- Added `classify_exception()` central router
- Added `classify_network_errors()` for multi-engine search aggregation
- **CI Gate:** `test_void_memanjang.py` (278 lines) — any VOID from non-constitutional causes = build failure

---

### 📡 3E Intelligence Telemetry Mandate

Every tool output **MUST** physically expose its 3E state. No bare success permitted.

**New Telemetry Models:**

```python
@dataclass
class ThreeEState:
    exploration: ExplorationTelemetry    # Sources consulted, depth, breadth
    entropy: EntropyTelemetry            # Uncertainty index, contradictions
    eureka: EurekaTelemetry              # Insight delta, novelty score
```

**Fields:**
- `ExplorationTelemetry`: `sources_consulted`, `depth_level`, `breadth_score`, `exploration_paths`
- `EntropyTelemetry`: `uncertainty_index`, `contradiction_count`, `resolution_confidence`
- `EurekaTelemetry`: `insight_delta`, `novelty_score`, `crystallisation_flag`

---

### 📦 MachineEnvelope & GovernanceEnvelope Upgrades

**Backward-compatible** — all new fields are `Optional` with defaults.

**MachineEnvelope additions:**
| Field | Type | Purpose |
|-------|------|---------|
| `fault_code` | `Optional[str]` | Typed fault label from `MechanicalFaultCode` |
| `http_diagnostics` | `Optional[dict]` | Raw HTTP response metadata |
| `tool_name` | `Optional[str]` | Originating tool identifier |
| `latency_ms` | `Optional[float]` | End-to-end execution latency |

**GovernanceEnvelope additions:**
| Field | Type | Purpose |
|-------|------|---------|
| `floor_scores` | `Optional[dict]` | Per-floor satisfaction scores |
| `hold_id` | `Optional[str]` | Active hold record reference |
| `void_reason` | `Optional[str]` | Constitutional collapse narrative |
| `metabolic_stage` | `Optional[str]` | System metabolic state label |
| `tri_witness_score` | `Optional[float]` | W3 metric value at emission time |

---

### 🔒 Security Primitives

#### HMAC-SHA256 Governance Tokens (`core/security/tokens.py`)
- **NOT JWT** — compact dot-separated `header.claims.signature` format
- F11-compliant with configurable TTL and scope binding
- `mint_governance_token()` / `validate_governance_token()`

#### F12 Injection Scanner (`core/security/scanner.py`)
- 14 regex patterns covering:
  - Prompt injection attacks
  - Path traversal (`../`, `%2e%2e`)
  - SQL injection (`UNION SELECT`, `OR 1=1`)
  - SSRF (`file://`, `dict://`, `gopher://`)
  - Shell injection (`; rm -rf`, `| cat /etc/passwd`)
- Allowlist honors legitimate `<untrusted_external_data>` taint wrappers

---

### 📐 Tri-Witness (W3) Intelligence Metric

**Formula:** `W3 = (w_H·s_H × w_A·s_A × w_E·s_E)^(1/3)`

Where:
- `w_H` = Human witness weight, `s_H` = Human source score
- `w_A` = AI witness weight, `s_A` = AI reasoning score  
- `w_E` = Earth/System witness weight, `s_E` = External evidence score

**Verdict Thresholds:**
| W3 Range | Verdict | Description |
|----------|---------|-------------|
| ≥ 0.95 | `SEAL` | Consensus achieved |
| 0.75 – 0.94 | `PARTIAL` | Partial consensus |
| 0.50 – 0.74 | `SABAR` | Insufficient evidence |
| < 0.50 | `888_HOLD` | No consensus |

Integrated with `IntelligenceEnvelope.tri_witness_score`.

---

### 🏛️ Vault & Evidence Infrastructure

#### RFC 6962 Merkle Tree (`core/vault/merkle.py`)
- Certificate Transparency-compliant append-only tree
- `0x00` leaf prefix / `0x01` node prefix
- `append_record()`, `verify_chain_integrity()`, `generate_inclusion_proof()`
- `VaultRecord` with SHA-256 hashing

#### Evidence Bundle (`core/contracts/evidence.py`)
- `EvidenceBundle` with JCS (JSON Canonicalization Scheme) canonical hash
- `MerkleInclusionProof` typed model
- F12 taint wrapping for untrusted data

---

### 🏛️ Sovereign Hold Bridge

**`core/governance/ratify_hold.py`**
- `ratify_hold_state()` — sovereign bridge for 888_HOLD events
- HMAC-signed `HoldRecord` with unique hold IDs
- In-memory hold registry (with PostgreSQL bridge TODO)
- Telegram payload builder for Apex notifications

---

### 📊 Prometheus Telemetry Additions

**New Metrics** (`arifosmcp/runtime/metrics.py`):

| Metric | Type | Description |
|--------|------|-------------|
| `W3_SCORE` | Histogram | Tri-Witness score distribution |
| `HOLD_QUEUE_DEPTH` | Gauge | Pending sovereign holds |
| `VAULT_RECORDS_TOTAL` | Counter | Total records in VAULT999 |
| `FLOOR_VIOLATIONS` | Counter | Constitutional floor breaches |
| `MACHINE_FAULTS` | Counter | Mechanical/infrastructure faults |
| `VOID_EVENTS` | Counter | Constitutional collapse events |
| `MERKLE_INTEGRITY` | Gauge | Merkle chain health (0-1) |

---

### 🧪 CI/CD

- **New Test Suite:** `tests/test_void_memanjang.py` (278 lines)
  - Tests network timeout → `TIMEOUT_EXCEEDED`, never `VOID`
  - Tests HTTP 404 → `TOOL_NOT_EXPOSED`, never `VOID`
  - Tests auth failure → `AUTH_FAILURE`, never `VOID`
  - Tests constitutional breach → `VOID` permitted (only valid case)

---

### 📁 Files Added/Modified

| File | Change | Lines |
|------|--------|-------|
| `arifosmcp/runtime/fault_codes.py` | NEW | ~200 |
| `core/contracts/telemetry.py` | NEW | ~216 |
| `core/contracts/evidence.py` | NEW | ~218 |
| `core/contracts/responses.py` | MODIFIED | +68 |
| `core/governance/ratify_hold.py` | NEW | ~283 |
| `core/intelligence/w3.py` | NEW | ~170 |
| `core/security/tokens.py` | NEW | ~224 |
| `core/security/scanner.py` | NEW | ~151 |
| `core/security/__init__.py` | NEW | ~5 |
| `core/vault/merkle.py` | NEW | ~237 |
| `arifosmcp/runtime/metrics.py` | APPENDED | +40 |
| `tests/test_void_memanjang.py` | NEW | 278 |

**Total:** ~2,131 insertions, ~30 deletions

---

### 🛡️ Constitutional Compliance

| Floor | Status | Implementation |
|-------|--------|----------------|
| F1 Amanah | ✅ | All changes tracked, reversible |
| F2 Truth | ✅ | `F2_TRUTH_BELOW_THRESHOLD` fault code |
| F3 Tri-Witness | ✅ | W3 metric with ≥0.95 SEAL threshold |
| F6 Empathy | ✅ | Thermodynamic clarity enforced |
| F7 Humility | ✅ | Uncertainty band [0.03, 0.05] |
| F8 Genius | ✅ | `w3_score` telemetry |
| F9 Anti-Hantu | ✅ | Shadow pattern detection |
| F10 Ontology | ✅ | `F10_ONTOLOGY` fault code |
| F11 Command | ✅ | HMAC-SHA256 token validation |
| F12 Injection Guard | ✅ | 14-regex scanner |
| F13 Sovereign | ✅ | `ratify_hold_state` bridge |

---

### 📝 Migration Notes

**For Existing Users:**
- All changes are **backward-compatible**
- Existing envelope consumers will see new optional fields as `None`
- No breaking changes to API surface

**For Developers:**
- Update imports to use new fault codes: `from arifosmcp.runtime.fault_codes import classify_exception`
- Consider adding 3E telemetry to custom tools
- Use `MACHINE_FAULT_CODES` frozenset for fault validation

---

*Forged by Architect Δ — arifOS MGI 7-tool canonical stack — FORGED-2026.03*

*DITEMPA BUKAN DIBERI — Forged, Not Given*
