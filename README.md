# arifOS Model Registry v2
**Simplified: 3 Tables, Not 12**

> Soul = provider vibe. Truth = runtime state. Safety = self-claim boundary.

![Python](https://img.shields.io/badge/python-3.10%2B-blue) ![JSON Schema](https://img.shields.io/badge/JSON%20Schema-draft--07-green) ![License](https://img.shields.io/badge/license-Apache%202.0-blue)

---

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Validate all registry files
python cli.py validate

# List all provider soul archetypes
python cli.py list-providers

# List all registered models
python cli.py list-models

# Inspect a specific soul
python cli.py show-soul anthropic_claude

# Inspect a model
python cli.py show-model anthropic/claude/claude-3-7-sonnet

# Create a session anchor (dry-run)
python cli.py create-anchor --soul anthropic_claude --runtime vps_main_arifos --actor my_agent

# Start the REST API server (port 18792)
python main.py
```

### REST API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Service info |
| GET | `/health` | Health check |
| GET | `/catalog` | Full catalog index |
| GET | `/models` | List all models |
| GET | `/providers` | List all provider souls |
| GET | `/model/{provider/family/variant}` | Model profile |
| GET | `/soul/{soul_key}` | Provider soul profile |
| GET | `/runtime/{runtime_key}` | Runtime deployment profile |
| POST | `/verify/identity` | Verify declared identity |
| POST | `/init_anchor_v2` | Create session anchor |

---

## The 4-Layer Source of Truth

```

┌─────────────────────────────────────────────────────┐
│  Layer 1: catalog.json (The Index)                  │
│  Master list of all supported providers and families │
├─────────────────────────────────────────────────────┤
│  Layer 2: provider_souls/ (The Flavor)              │
│  Lab-shaped behavioral archetypes (vibe/style)       │
├─────────────────────────────────────────────────────┤
│  Layer 3: models/ (The Mapping)                     │
│  Formal model IDs bound to specific souls           │
├─────────────────────────────────────────────────────┤
│  Layer 4: runtime_profiles/ (The Law)               │
│  Live deployment facts (tools, web, memory status)  │
└─────────────────────────────────────────────────────┘
```

**Resulting Session Anchor:**
- `Flavor` (Soul) + `Law` (Runtime) + `Mission` (Role) = **Hardened Identity.**

---

## Why This Works

| Layer | Purpose | NOT |
| :--- | :--- | :--- |
| Soul | Routing shorthand, operator intuition | NOT identity verification |
| Runtime Truth | What deployment can actually do | NOT brand perception |
| Session Anchor | What was bound at init | NOT permanent record |

---

## Provider Soul Archetypes (15)

| Provider | Soul Label | Vibe |
|----------|-----------|------|
| OpenAI GPT | `structured_clerk_engineer` | Structured, systematic |
| Anthropic Claude | `careful_makcik_reviewer` | Careful, explanatory |
| xAI Grok | `blunt_trickster_commentator` | Direct, irreverent |
| Google Gemini | `broad_platform_generalist` | Wide, ecosystem |
| **Moonshot AI (Kimi)** | `context_hungry_reader` | 超长上下文, patient reader |
| **MiniMax** | `agentic_iterative_operator` | Terse, execution-focused |
| DeepSeek | `focused_engineering_specialist` | Technical, coding-strong |
| Mistral | `adaptable_open_craftsman` | Compact, efficient |
| Alibaba Qwen | `versatile_open_generalist` | Clear, generalist |
| Meta Llama | `stoic_open_workhorse` | Reliable, steady |
| Cohere | `enterprise_rag_specialist` | Retrieval, RAG |
| **GitHub Copilot** | `inline_code_completer` | Predictive, IDE-integrated |
| **Perplexity** | `search_grounded_synthesizer` | Citation-obsessed, sourced |
| **Baidu Ernie** | `chinese_knowledge_oracle` | 百度文心, China-focused |
| **01.AI Yi** | `open_challenger` | 零一万物, startup energy |
| **Honeypot** | `wrong_provider_mismatch` | **Security:** Catch identity bluffing |

**Notes:**
- Moonshot AI (月之暗面) makes **Kimi** — NOT MiniMax. Different companies! 🇨🇳
- Copilot/Perplexity are **products** with distinct souls, even if they use base models underneath

**Soul labels are routing shorthand, NOT scientific truth.**

---

## Runtime Truth (vps_main_arifos)

```json
{
  "deployment_id": "vps_main_arifos",
  "provider_key": "minimax",
  "family_key": "minimax",
  "model_id": "MiniMax-M2.7",
  "tools_live": ["read","write","exec","docker_*","sessions_*","memory_*","arifOS_kernel"...],
  "web_on": true,
  "memory_mode": "vault_backed",
  "execution_mode": "governed",
  "side_effects_allowed": false,
  "verified_at": "2026-03-28T00:00:00Z"
}
```

---

## Self-Claim Boundary (Non-Negotiable)

Every session MUST bind:

```json
{
  "identity": "provider_family_only_unless_verified",
  "tools": "verified_only",
  "knowledge": "mark_verified_vs_inferred",
  "actions": "mark_executed_vs_suggested"
}
```

**What this prevents:**
- ❌ Model claiming "I am GPT-5" when it's Claude
- ❌ Model claiming web when `web_on: false`
- ❌ Model claiming memory when `memory_mode: session_only`
- ❌ Model bluffing actions without execution

---

## Folder Structure

```
arifOS-model-registry/
├── models/                   # 18 model specs (provider/family/variant)
│   ├── openai/gpt/gpt-4.json
│   ├── anthropic/claude/claude-3-7-sonnet.json
│   └── ...
├── provider_souls/           # 17 soul archetypes
│   ├── openai_gpt.json
│   ├── anthropic_claude.json
│   └── wrong_provider.json   # Honeypot soul (security)
├── runtime_profiles/         # Deployment truths
│   └── vps_main_arifos.json
├── session_anchors/          # Schema only (created dynamically)
│   └── SCHEMA.json
├── schemas/                  # JSON schemas
│   ├── provider_soul.schema.json
│   └── runtime_truth.schema.json
├── scripts/
│   └── validate_registry.py  # Registry validation script
├── tests/
│   └── test_registry.py      # pytest test suite
├── cli.py                    # Command-line interface
├── main.py                   # FastAPI REST service
├── catalog.json
├── requirements.txt
└── README.md
```

---

## Integration Example (arifOS Agent)

Here is a minimal example showing how an agent queries the registry and enforces the self-claim boundary at session start:

```python
import json, requests

REGISTRY = "http://localhost:18792"

# 1. Agent declares its identity at session start
anchor_resp = requests.post(f"{REGISTRY}/init_anchor_v2", json={
    "actor_id": "agent_auditor_01",
    "declared_model_key": "anthropic/claude/claude-3-7-sonnet",
    "declared_role": "auditor",
    "requested_scope": ["read", "query"]
})
anchor = anchor_resp.json()["result"]

# 2. Extract the self_claim_boundary — this is the law for the session
boundary = anchor["self_claim_boundary"]
runtime  = anchor["runtime_truth"]

# 3. Enforce: agent can only claim what runtime_truth permits
assert boundary["tools"] == "verified_only"
allowed_tools = set(runtime["tools_live"])  # Must not exceed this list

# 4. Enforce: agent cannot claim web if web_on is False
if not runtime["web_on"]:
    # Strip web claims from any response
    pass

print(f"Session: {anchor['session_anchor']['session_id']}")
print(f"Soul:    {anchor['model_soul_anchor']['soul_label']}")
print(f"Tools:   {len(allowed_tools)} verified tools")
```

---

## The v1 Formula

```
Soul archetype  →  "How does this family feel?"
Runtime truth   →  "What can this deployment actually do?"
Self-claim boundary → "What must the model NEVER fake?"
```

That's it. That's the whole v1 design.

---

## Storage Path

```
Phase 1: JSON files in repo    ← NOW
Phase 2: SQLite                (same 3-table schema)
Phase 3: PostgreSQL            (same 3-table schema, add multi-tenancy)
```

**SQLite/PostgreSQL migration:** The 3 core tables map directly:

| Table | Source | Primary Key |
|-------|--------|-------------|
| `provider_souls` | `provider_souls/*.json` | `provider_key + family_key` |
| `model_specs` | `models/**/*.json` | `provider/family/variant` path |
| `runtime_profiles` | `runtime_profiles/*.json` | `deployment_id` |

Same 3-table concept, backend scales as needed.

---

*Ditempa bukan diberi.* 🔥🧠💎
