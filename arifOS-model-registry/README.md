# arifOS Model Registry v2
**Simplified: 3 Tables, Not 12**

> Soul = provider vibe. Truth = runtime state. Safety = self-claim boundary.

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
│  Layer 3: model_specs/ (The Mapping)                │
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
├── provider_souls/           # 15 soul archetypes
│   ├── openai_gpt.json
│   ├── anthropic_claude.json
│   └── ...
├── runtime_profiles/         # Deployment truths
│   └── vps_main_arifos.json
├── session_anchors/          # Schema only (created dynamically)
│   └── SCHEMA.json
├── schemas/                  # JSON schemas
│   ├── provider_soul.schema.json
│   └── runtime_truth.schema.json
├── catalog.json
└── README.md
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
Phase 2: SQLite
Phase 3: PostgreSQL
```

Same 3-table concept, backend scales as needed.

---

*Ditempa bukan diberi.* 🔥🧠💎
