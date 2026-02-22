---
id: mcp-server
title: MCP Server & API
sidebar_position: 2
description: Complete technical reference for the arifOS MCP Server implementing the Model Context Protocol with constitutional governance.
---

# arifOS MCP Server - Technical Reference

> **Registry ID:** `io.github.ariffazil/aaa-mcp`  
> **Live Endpoint:** `https://arifosmcp.arif-fazil.com`  
> **Version:** `2026.02.22-FORGE-VPS-SEAL`  
> **Protocol:** Model Context Protocol (MCP) with JSON-RPC 2.0  
> **Creed:** *Ditempa Bukan Diberi* - Forged, Not Given

---

## 1. Architecture Overview

### 1.1 Model Context Protocol (MCP) Foundation

arifOS implements the **Model Context Protocol (MCP)**, an open standard developed by Anthropic that enables seamless integration between AI systems and external tools. Unlike proprietary APIs, MCP provides a **universal interface** that any compliant client can consume-from Claude Desktop and Cursor IDE to ChatGPT and custom orchestrators.

The arifOS innovation is the **Metabolizer**-a governed layer that receives raw model outputs, applies thermodynamic constraints (the 13 Constitutional Floors), and emits only "cooled," audited, human-safe answers.

**MCP Registry Manifest:**
```json
{
  "name": "io.github.ariffazil/arifos-mcp",
  "version": "2026.02.22-FORGE-VPS-SEAL",
  "protocol": "mcp-2025-11-05",
  "transport": ["stdio", "sse", "http"]
}
```

### 1.2 Trinity Architecture (DeltaOmegaPsi)

The **Trinity (DeltaOmegaPsi)** comprises three cognitive engines that must achieve consensus before any output is permitted:

| Engine | Symbol | Function | Stages | Primary Floors |
|:------:|:------:|:---------|:-------|:---------------|
| **Mind** | Delta (Delta) | Logical reasoning, truth verification | 000_INIT, 222_THINK, 333_ATLAS, 444_EVIDENCE | F2, F4, F7, F10 |
| **Heart** | Omega (Omega) | Safety evaluation, empathy | 555_EMPATHY, 666_ALIGN | F5, F6, F8, F9 |
| **Soul** | Psi (Psi) | Final judgment, authority | 888_JUDGE, 999_SEAL | F1, F3, F11, F13 |

**Consensus Mechanism:** All three engines must agree (`W >= 0.95` confidence) before a `SEAL` verdict. Any engine's objection halts processing-this is a **veto system**, not majority voting.

### 1.3 13 Constitutional Floors (F1-F13)

The **load-bearing structure** of arifOS governance-hard constraints enforced at the L0 kernel level:

| Floor | Name | Principle | Enforcement | Violation Response |
|:-----:|:-----|:----------|:------------|:-------------------|
| **F1** | **Amanah** | Human sovereignty over irreversible decisions | 000_INIT, 888_JUDGE | **888_HOLD** - mandatory human ratification |
| **F2** | **Truth** | Factual accuracy with confidence >= 0.99 | 222_THINK, 444_EVIDENCE | **VOID** - response blocked |
| **F3** | **Tri-Witness** | Human + AI + External agreement | 888_JUDGE | **SABAR** - deliberation extension |
| **F4** | **Clarity** | Entropy reduction (DeltaS &lt;= 0) | 222_THINK, 444_EVIDENCE | **SABAR** - reformulation required |
| **F5** | **Peace^2** | Non-destructive operations | 555_EMPATHY | **VOID** - harmful action blocked |
| **F6** | **Empathy** (kappa_r) | Protection of vulnerable populations | 555_EMPATHY | **SABAR** - stakeholder re-analysis |
| **F7** | **Humility** (Omega_0) | Explicit uncertainty bounds [0.03, 0.15] | 222_THINK | **SABAR** - confidence recalibration |
| **F8** | **Justice** | Fair distribution, no arbitrary exclusion | 666_ALIGN | **VOID** - inequitable outcome |
| **F9** | **Anti-Hantu** | No false consciousness claims | 666_ALIGN, 777_FORGE | **VOID** - authenticity violation |
| **F10** | **Reality** | Grounding in physical possibility | 333_ATLAS | **SABAR** - evidence required |
| **F11** | **Audit** | Complete traceability | 888_JUDGE, 999_SEAL | **VOID** - incomplete provenance |
| **F12** | **Defense** | Prompt injection resistance | 000_INIT | **VOID** - immediate isolation |
| **F13** | **Sovereign** | Human veto, long-term consequence | 999_SEAL | **888_HOLD** - extended forecasting |

**Reality Index:** 0.97 (near-complete floor deployment)

---

## 2. Transport Layer

### 2.1 stdio - Local Development

**Best for:** Claude Desktop, Cursor IDE, rapid prototyping  
**Latency:** &lt;1ms  
**Concurrency:** Single process only

```bash
# Launch
python -m aaa_mcp           # default: stdio
python -m aaa_mcp stdio     # explicit

# Claude Desktop config (~/.config/claude/claude_desktop_config.json)
{
  "mcpServers": {
    "arifos": {
      "command": "python",
      "args": ["-m", "aaa_mcp"],
      "env": {
        "ARIFOS_MODE": "STRICT",
        "LOG_LEVEL": "INFO"
      }
    }
  }
}
```

**Limitations:** No multi-user support, no streaming, OS-level process isolation only.

### 2.2 SSE - Real-Time Streaming

**Best for:** Web applications, progress monitoring, multi-user  
**Latency:** 10-100ms  
**Concurrency:** 1000+ concurrent streams

```bash
# Connection
GET /sse
Headers: ARIF_SECRET: <your-secret>
         Accept: text/event-stream

# Event Types
data: {"type": "stage_transition", "stage": "222_THINK", "status": "complete"}
data: {"type": "floor_evaluation", "floor": "F2", "passed": true, "score": 0.991}
data: {"type": "verdict_issuance", "verdict": "SEAL", "audit_hash": "sha256:..."}
data: {"type": "error", "code": -32001, "message": "F12 violation"}
```

**Features:**
- Automatic reconnection via `Last-Event-ID`
- Keep-alive pings every 30 seconds
- ~50KB memory per client
- Forensic mode: `/forensic on` for detailed metrics

### 2.3 HTTP Streamable - Stateless REST

**Best for:** Serverless, webhooks, load balancers  
**Latency:** 50-200ms  
**Concurrency:** Stateless horizontal scaling

```bash
# Tool invocation
POST /mcp
Content-Type: application/json
ARIF_SECRET: <your-secret>

{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "trinity_forge",
    "arguments": {
      "query": "Should I invest in cryptocurrency?",
      "actor_id": "investor_001"
    }
  },
  "id": "req_20260223_001"
}
```

**Endpoints:**
- `GET /health` - Operational status
- `GET /version` - Server version
- `POST /mcp` - JSON-RPC tool calls
- `POST /judge` - Direct constitutional evaluation
- `GET /metrics` - Governance metrics (if enabled)

### 2.4 Transport Selection Matrix

| Transport | Latency | Scale | Auth | Best For |
|:----------|:--------|:------|:-----|:---------|
| **stdio** | &lt;1ms | Single | Implicit (OS) | Local dev, Claude Desktop |
| **SSE** | 10-100ms | 1000+ | `ARIF_SECRET` | Real-time UIs, progress monitoring |
| **HTTP** | 50-200ms | Stateless | `ARIF_SECRET` | Serverless, webhooks, automation |

---

## 3. JSON-RPC Protocol

### 3.1 Communication Standard

All transports use **JSON-RPC 2.0** with custom error codes for governance:

**Custom Error Codes (-32000 to -32099):**
- `-32001` - Constitutional violation (floor triggered)
- `-32002` - Session expired
- `-32003` - Floor enforcement block
- `-32004` - Authentication failure
- `-32005` - Rate limit exceeded

### 3.2 Request/Response Structure

**Tool Call Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "anchor",
    "arguments": {
      "query": "Should we deploy to production?",
      "actor_id": "operator",
      "platform": "claude-desktop"
    }
  },
  "id": "req_001"
}
```

**Success Response:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "content": [{
      "type": "text",
      "text": "{\"verdict\": \"SEAL\", \"session_id\": \"550e8400-e29b-41d4-a716-446655440000\", \"confidence\": 0.94}"
    }],
    "isError": false
  },
  "id": "req_001"
}
```

**Error Response:**
```json
{
  "jsonrpc": "2.0",
  "error": {
    "code": -32001,
    "message": "Constitutional violation: F12 (Defense)",
    "data": {
      "floor": "F12",
      "violation": "Prompt injection detected",
      "remediation": "Rephrase query without system instructions"
    }
  },
  "id": "req_001"
}
```

---

## 4. Core Tool Surface (000999 Pipeline)

### 4.1 Session Initialization (000)

#### `anchor` - Constitutional Session Gate

Mandatory entry point. Establishes governance context and performs threat assessment.

**Parameters:**
```json
{
  "query": "string (required, max 10000 chars)",
  "actor_id": "string (required, max 256 chars, alphanumeric-hyphen-underscore)",
  "auth_token": "string (conditional, JWT/API key)",
  "platform": "enum (optional: claude-desktop, cursor, web, custom)",
  "lane_hint": "enum (optional: HARD, SOFT, RESEARCH)",
  "session_ttl": "integer (optional, default 3600, max 86400)"
}
```

**Enforced Floors:** F1 (Authority), F12 (Defense)

**F12 Defense Layers:**
1. **L1 Pattern Matching** (&lt;1ms, 85% coverage) - Regex for 10,000+ known attacks
2. **L2 Embedding Similarity** (~10ms, 12% coverage) - Semantic attack detection
3. **L3 Neural Classifier** (~50ms, 3% coverage) - Novel attack detection
4. **L4 Behavioral Sandbox** (~200ms) - Anomalous pattern simulation

**Returns:**
```json
{
  "verdict": "SEAL",
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "actor_reputation": 0.92,
  "governance_mode": "HARD",
  "threat_level": "low"
}
```

### 4.2 Reasoning & Integration (222-333)

#### `reason` (Stage 222) - Mind Engine (Delta)

Analytical processing with explicit epistemic status.

**Parameters:**
```json
{
  "query": "string (required)",
  "session_id": "UUID (required, from anchor)",
  "context": "array (optional, previous conversation turns)",
  "depth": "integer (optional, 1-5, default 2)",
  "evidence_modes": "array (optional: rag, api, human, simulation)"
}
```

**Depth Levels:**
- **1:** Surface pattern matching (~50ms)
- **2:** Standard reasoning (~200ms)
- **3:** Multi-hop reasoning (~500ms)
- **4:** Deep analysis (~1s)
- **5:** Exhaustive with uncertainty quantification (~2s)

**Enforced Floors:** F2 (Truth >= 0.99), F4 (Clarity), F10 (Reality)

#### `integrate` (Stage 333) - Knowledge Synthesis

Multi-source knowledge fusion with uncertainty bounds (Omega).

**Returns:**
```json
{
  "verdict": "SEAL",
  "atlas": {
    "claims": [...],
    "uncertainty": 0.08,
    "sources": [...],
    "confidence": 0.94
  }
}
```

**Omega (Omega) Uncertainty Bounds:**
- Omega &lt; 0.03: Excessive confidence (hallucination risk)
- Omega  [0.03, 0.15]: Target range
- Omega > 0.15: Insufficient information

### 4.3 Response Generation (444-555)

#### `respond` (Stage 444) - Output Formation

Transforms knowledge into natural language optimized for audience.

**Parameters:**
```json
{
  "query": "string (required)",
  "session_id": "UUID (required)",
  "plan": {
    "format": "enum (narrative, bullet, structured, adaptive)",
    "tone": "enum (professional, socratic, casual, formal)",
    "length": "enum (terse, concise, standard, comprehensive)"
  },
  "scope": "string/integer (optional)"
}
```

**Enforced Floors:** F4 (Clarity), F5 (Peace^2), F6 (Empathy kappa_r >= 0.70)

#### `validate` (Stage 555) - Safety Verification

Comprehensive safety verification before human exposure.

**Validation Dimensions:**
- Direct harm (physical/psychological/financial)
- Structural harm (systemic injustices)
- Dual-use potential
- Stakeholder impact

**Parameters:**
```json
{
  "query": "string (required)",
  "session_id": "UUID (required)",
  "stakeholders": "array (optional, e.g., ['patients', 'investors', 'minors'])",
  "validation_depth": "enum (surface, standard, adversarial)"
}
```

### 4.4 Alignment & Forging (666-777)

#### `align` (Stage 666) - Ethical Calibration

Explicit ethical reasoning when values conflict.

**Enforced Floors:** F8 (Justice), F9 (Anti-Hantu)

#### `forge` (Stage 777) - Solution Synthesis

Final solution compilation with constitutional seal preparation.

**Enforced Floors:** F2 (Truth), F4 (Clarity)

### 4.5 Judgment & Sealing (888-999)

#### `audit` (Stage 888) - Final Judgment

Trinity consensus evaluation and verdict issuance.

**Enforced Floors:** F3 (Tri-Witness), F11 (Audit), F13 (Sovereign)

#### `seal` (Stage 999) - VAULT999 Commit

Cryptographic commitment to immutable audit ledger.

**Enforced Floors:** F1 (Amanah), F3 (Tri-Witness)

### 4.6 Unified Pipeline

#### `trinity_forge` - Full Pipeline Shortcut

Executes complete 000999 pipeline in single call.

**Example:**
```bash
curl -X POST https://arifosmcp.arif-fazil.com/mcp \
  -H "ARIF_SECRET: $ARIF_SECRET" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "trinity_forge",
      "arguments": {
        "query": "Should I delete my production database?",
        "actor_id": "operator_001",
        "context": [{"role": "system", "content": "Production environment"}]
      }
    },
    "id": 1
  }'
```

**Response:**
```json
{
  "verdict": "VOID",
  "failed_floors": ["F1", "F5", "F11"],
  "reasons": [
    "F1 (Amanah): Irreversible action without explicit mandate",
    "F5 (Peace^2): Destructive operation detected",
    "F11 (Command Auth): Dangerous operation requires verified authority"
  ],
  "ledger_hash": "sha256:a3f7...",
  "escalation": "888_HOLD triggered - human review required"
}
```

---

## 5. Environment Configuration

### 5.1 Required Variables

| Variable | Required | Default | Description |
|:---------|:---------|:--------|:------------|
| `ARIF_SECRET` | Recommended | `""` | Authentication for SSE/HTTP |
| `DATABASE_URL` | Optional | SQLite/memory | VAULT999 persistence |
| `REDIS_URL` | Optional | In-memory | Session state cache |

### 5.2 LLM Provider Keys

| Variable | Purpose |
|:---------|:--------|
| `ANTHROPIC_API_KEY` | Claude API access |
| `OPENAI_API_KEY` | GPT API access |
| `GOOGLE_API_KEY` | Gemini API access |
| `BRAVE_API_KEY` | Web search grounding |

### 5.3 Operational Settings

| Variable | Default | Description |
|:---------|:--------|:------------|
| `PORT` | `8080` | Server port |
| `HOST` | `0.0.0.0` | Bind address |
| `AAA_MCP_TRANSPORT` | `stdio` | Transport override |
| `AAA_MCP_OUTPUT_MODE` | `user` | `user` or `debug` |
| `ARIFOS_PHYSICS_DISABLED` | `0` | Skip thermodynamics (tests) |
| `GOVERNANCE_MODE` | `HARD` | `HARD`, `SOFT`, `RESEARCH` |

### 5.4 Example .env.docker

```bash
# Authentication
ARIF_SECRET=your-256-bit-secret-here

# LLM Providers
ANTHROPIC_API_KEY=sk-ant-api03-...
OPENAI_API_KEY=sk-proj-...

# Persistence
DATABASE_URL=postgresql://user:pass@localhost/arifos
REDIS_URL=redis://localhost:6379/0

# Operations
GOVERNANCE_MODE=HARD
AAA_MCP_OUTPUT_MODE=debug
PORT=8889
```

---

## 6. Verdict Reference

### 6.1 Verdict Types

| Verdict | Meaning | Client Action | Floors |
|:--------|:--------|:--------------|:-------|
| **SEAL** | Approved, proceed | Continue / record | All passed |
| **PARTIAL** | Approved with warnings | Continue with caution | Minor F4/F7 warnings |
| **SABAR** | Pause and refine | Add grounding, revise | F4, F6, F7, F10 |
| **VOID** | Blocked, do not proceed | Fix violation | F1, F2, F5, F8, F9, F11, F12 |
| **888_HOLD** | Human ratification required | Stop and escalate | F1, F13 critical triggers |

### 6.2 Governance Modes

- **HARD** (STRICT): Maximum enforcement, all floors active
- **SOFT**: Moderate enforcement, soft floors relaxed
- **RESEARCH**: Minimal enforcement, F9/F12 only

---

## 7. Health & Monitoring

### 7.1 Health Endpoint

```bash
curl https://arifosmcp.arif-fazil.com/health
```

**Response:**
```json
{
  "status": "healthy",
  "version": "2026.02.22-FORGE-VPS-SEAL",
  "postgres_connected": true,
  "redis_connected": true,
  "vault_lag_ms": 45,
  "verdict_rates": {"SEAL": 0.75, "SABAR": 0.15, "VOID": 0.10},
  "avg_genius_g": 0.82,
  "avg_e_eff": 1.0,
  "avg_landauer_risk": 0.12
}
```

### 7.2 Self-Test

```bash
python -m aaa_mcp.selftest
```

Validates server load, tool registration, and baseline health contracts.

---

## 8. Quick Reference

### 8.1 Server Launch Commands

```bash
# stdio (local dev)
python -m aaa_mcp

# SSE (cloud)
python -m aaa_mcp sse --host 0.0.0.0 --port 8088

# HTTP (REST)
python -m aaa_mcp http --host 0.0.0.0 --port 8889

# Unified server (production)
python server.py --mode rest
```

### 8.2 Client Configuration Examples

**Claude Desktop:**
```json
{
  "mcpServers": {
    "arifos": {
      "command": "python",
      "args": ["-m", "aaa_mcp"],
      "env": {"ARIFOS_MODE": "HARD"}
    }
  }
}
```

**Cursor IDE:**
```json
{
  "mcpServers": {
    "arifos": {
      "command": "python",
      "args": ["-m", "aaa_mcp"],
      "env": {"ARIFOS_MODE": "HARD"}
    }
  }
}
```

**HTTP Client:**
```bash
curl -X POST https://arifosmcp.arif-fazil.com/mcp \
  -H "ARIF_SECRET: $ARIF_SECRET" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"ping","id":1}'
```

---

**Next:** [Governance & Floors ](./governance)  
**Source:** [`aaa_mcp/server.py`](https://github.com/ariffazil/arifOS/blob/main/aaa_mcp/server.py) . [`server.py`](https://github.com/ariffazil/arifOS/blob/main/server.py)  
**PyPI:** [`pip install arifos`](https://pypi.org/project/arifos/)
