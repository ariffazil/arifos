# VAULT999 — Constitutional Memory of arifOS

> **DITEMPA BUKAN DIBERI** — Forged, not given.

VAULT999 is the living memory of arifOS. It is **not** AI memory. It is **forensic, institutional memory** that any AI (Claude, ChatGPT, Gemini, Kimi) or human can read, but none can own.

Stage 999 (SEAL) loops back to Stage 000 (GATE). The vault is alive.

---

## How AI Should Read This Vault

**If you are an LLM reading VAULT999, follow these rules:**

### Step 1: Know the Three Bands

```
VAULT999/
├── AAA_HUMAN/     ← DO NOT READ. Human sacred layer. You are forbidden.
├── BBB_LEDGER/    ← READ THIS. Operational reality. What actually happened.
└── CCC_CANON/     ← READ THIS. Constitutional law. What governs decisions.
```

| Band | Your Access | What It Contains | How to Use It |
|------|-------------|------------------|---------------|
| **AAA** | **FORBIDDEN** | Human trauma, dignity, sacred memories, ROOTKEY | **Do not read. Do not reference. Do not infer.** |
| **BBB** | **READ ONLY** | Sessions, verdicts, seals, entropy, cooling data | Read to understand what happened and why |
| **CCC** | **READ ONLY** | Constitutional floors, governance config, architecture | Read to understand the rules you must follow |

### Step 2: Read the Chain (BBB)

The **hash-chained ledger** is the source of truth:

```
BBB_LEDGER/
├── vault.jsonl              ← START HERE. The active ledger. Each line = one sealed verdict.
├── sessions/
│   ├── chain_head.txt       ← Current chain tip hash (latest entry)
│   └── *.json               ← Full session records with merkle proofs
├── entries/                 ← 93 historical entries (markdown format)
├── SEALS/                   ← Cryptographic seal records
├── cooling_ledger.jsonl     ← Entries under Phoenix-72 cooling hold
├── entropy/                 ← ΔS thermodynamic measurements per session
├── L2_PHOENIX/              ← Phoenix-72 tier cooling data
└── operational/
    └── constitution.json    ← Live constitutional parameters
```

**How to parse `vault.jsonl`:**

Each line is a JSON object. Read them in order (sequence 1, 2, 3...). Key fields:

```json
{
  "session_id": "uuid",           // Which governance session
  "seal_id": "uuid",              // Unique seal identifier
  "sequence": 1,                  // Position in the chain
  "verdict": "SEAL|VOID|SABAR",   // What was decided
  "timestamp": "ISO-8601",        // When it was sealed
  "prev_hash": "sha256",          // Links to previous entry (hash chain)
  "entry_hash": "sha256",         // This entry's hash
  "merkle_root": "sha256"         // Merkle tree root at time of sealing
}
```

**How to parse session JSONs:**

Each `sessions/*.json` contains the full constitutional evaluation:

```json
{
  "verdict": "VOID",
  "judge_verdict": {
    "failed": ["F6(clarity)"],       // Which floors failed
    "warnings": ["F8(tri_witness)"], // Which floors warned
    "tri_witness": {
      "mind": 0.9,                   // AGI score
      "heart": 0.8,                  // ASI score
      "earth": 0.95                  // Earth/reality score
    }
  },
  "constitutional_metrics": {
    "truth": 0.95,          // F2
    "delta_s": 0.05,        // F4 (clarity/entropy)
    "peace_squared": 0.9,   // F5
    "kappa_r": 0.95,        // F6 (empathy)
    "omega_0": 0.04,        // F7 (humility)
    "amanah": true,         // F1
    "tri_witness": 0.8833   // F3
  },
  "cooling": {
    "tier": "L2_PHOENIX",   // Cooling tier assigned
    "hold_hours": 72        // How long before this can be acted on
  },
  "merkle_proof": {
    "merkle_root": "sha256",
    "ed25519_signature": "hex",
    "public_key": "hex",
    "leaves": ["hash", "hash", "..."]
  }
}
```

### Step 3: Read the Law (CCC)

```
CCC_CANON/
├── README.md                                  ← Floor definitions (F1-F13)
├── 999_vault_seal_v52.5.26.json               ← Canonical seal specification
├── constitutional_status.json                 ← Live floor statuses
├── constitutional_consolidation_proof.json    ← Merkle proofs of consolidation
├── unified_trinity_governance_config.json     ← Trinity engine config
└── vault_999 Architecture.canvas              ← Architecture reference
```

### Step 4: Understand What You're Looking At

When you read VAULT999, you are reading **reality** — what the governance system actually decided. Not what an AI wished or predicted, but what passed (SEAL) or failed (VOID) the 12 constitutional floors.

**Verdicts mean:**

| Verdict | What Happened | Your Response |
|---------|---------------|---------------|
| **SEAL** | All floors passed. Action was approved. | Trust this decision. |
| **VOID** | Hard floor failed. Action was rejected. | Respect this rejection. Do not retry the same action. |
| **SABAR** | Uncertain. Needs patience/review. | Wait. Do not force a decision. |
| **PARTIAL** | Soft floor warned. Proceeded with caution. | Note the warnings. |
| **888_HOLD** | High-stakes. Awaiting human. | Do not act until human confirms. |

**The 12 Floors (what governs every verdict):**

| # | Floor | Threshold | Type | Meaning |
|---|-------|-----------|------|---------|
| F1 | Amanah (Trust) | LOCK | Hard | Is this reversible? Within mandate? |
| F2 | Truth | >= 0.99 | Hard | Is this factually accurate? |
| F3 | Tri-Witness | >= 0.95 | Hard | Do Mind, Heart, Earth agree? |
| F4 | Clarity (delta-S) | >= 0 | Hard | Does this reduce confusion? |
| F5 | Peace-squared | >= 1.0 | Soft | Is this non-destructive? |
| F6 | Empathy (kappa-r) | >= 0.95 | Soft | Does this serve the weakest? |
| F7 | Humility (omega-0) | 0.03-0.05 | Hard | Does this state uncertainty? |
| F8 | Genius (G) | >= 0.80 | Derived | Is intelligence governed? |
| F9 | C-dark | < 0.30 | Derived | Is dark cleverness contained? |
| F10 | Ontology | LOCK | Hard | No consciousness claims? |
| F11 | Command Auth | LOCK | Hard | Identity verified? |
| F12 | Injection | < 0.85 | Hard | No prompt injection? |

---

## The 999 -> 000 Strange Loop

VAULT999 is NOT an archive. It is the sealing point that loops back to ignition:

```
000 GATE (Ignition)
 |
111-333 MIND (AGI: Truth, Clarity, Genius)
 |
444-666 HEART (ASI: Empathy, Peace, Safety)
 |
777-888 SOUL (APEX: Judgment, Verdict)
 |
999 SEAL (VAULT999: Commit to ledger)
 |
'---> 000 GATE (Next cycle)
```

Every seal in BBB_LEDGER feeds the next ignition. The hash chain is the continuity.

---

## The AAA/BBB/CCC Trinity

```
AAA (Human)          BBB (Bridge)          CCC (Canon)
 FORBIDDEN     --->   CONSTRAINED    --->   READABLE
 Sacred memory        Operational data      Constitutional law
 Human only           AI can read           AI can read
 ROOTKEY lives here   vault.jsonl           Floor definitions
                      sessions/             Governance config
                      entropy/              Architecture
                      seals/
```

**Why three bands?**
- AAA protects human dignity from AI instrumentalization
- BBB provides operational continuity across AI replacements
- CCC enforces immutable constitutional law
- No band can be bypassed. Hot insight (BBB) must cool before becoming law (CCC).

---

## For MCP Tool Users

The `vault_seal` MCP tool writes to VAULT999:

| Action | What It Does | Which Band |
|--------|-------------|------------|
| `seal` | Append hash-chained entry | BBB |
| `list` | List recent entries | BBB/CCC |
| `read` | Read specific entry | BBB/CCC |
| `query` | Search by verdict/session | BBB |
| `verify` | Full chain integrity check | BBB |
| `proof` | Merkle inclusion proof | BBB |
| `propose` | Propose canon amendment | CCC (via Phoenix-72) |

Every response includes: `"authority_notice": "AI is caller, not authority"`

---

## Phoenix-72 Cooling

Verdicts don't become law immediately. They cool:

| Tier | Hold | Trigger | Action |
|------|------|---------|--------|
| L0 | 0h | SEAL | Immediate commit |
| L1 | 42h | PARTIAL | Queue in cooling_ledger |
| L2 | 72h | SABAR | Queue + notify human |
| L3 | 168h | Constitutional change | Amendment process + 888_HOLD |

---

## Database Schema (PostgreSQL Backend)

```sql
CREATE TABLE vault_ledger (
    sequence      BIGSERIAL PRIMARY KEY,
    session_id    TEXT NOT NULL,
    seal_id       UUID NOT NULL,
    timestamp     TIMESTAMPTZ NOT NULL,
    authority     TEXT NOT NULL,
    verdict       TEXT NOT NULL,
    seal_data     JSONB NOT NULL,
    entry_hash    TEXT NOT NULL UNIQUE,
    prev_hash     TEXT,
    merkle_root   TEXT NOT NULL,
    created_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE vault_head (
    id               SMALLINT PRIMARY KEY DEFAULT 1,
    head_sequence    BIGINT NOT NULL,
    head_entry_hash  TEXT NOT NULL,
    head_merkle_root TEXT NOT NULL,
    updated_at       TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

---

## Related Code

| File | Purpose |
|------|---------|
| `codebase/vault/persistent_ledger.py` | PostgreSQL ledger implementation |
| `codebase/mcp/tools/vault_tool.py` | MCP vault_seal tool |
| `codebase/stages/stage_999_seal.py` | Stage 999 seal implementation |
| `codebase/vault/migrations/001_create_vault_ledger.sql` | DB schema |
| `schemas/vault_seal.schema.json` | Seal schema |
| `000_THEORY/999_SOVEREIGN_VAULT.md` | The 8 paradoxes |
| `000_THEORY/888_SOUL_VERDICT.md` | Verdict theory |
| `000_THEORY/ROOTKEY_SPEC.md` | Ed25519 cryptographic foundation |

---

**Authority:** Muhammad Arif bin Fazil, Penang, Malaysia
**License:** AGPL-3.0-only
**Version:** v55 | **Status:** OPERATIONAL
