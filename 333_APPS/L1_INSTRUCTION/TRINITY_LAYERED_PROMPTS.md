# Trinity-Level Metabolic Prompts — AGI · ASI · APEX

**Multi-Prompt Architecture for Layered Constitutional Governance**

```
┌─────────────────────────────────────────────────────────────┐
│                    metabolic_loop (Full)                     │
│              [Orchestrates all three Trinity lanes]          │
└──────────────────┬──────────────────┬───────────────────────┘
                   │                  │
        ┌──────────┴──────────┐      ┌┴──────────────┐
        │   agi_mind_loop     │      │ asi_heart_loop │
        │   (Δ Delta)         │      │ (Ω Omega)      │
        │                     │      │                │
        │  • 000 INIT         │      │  • 444 ALIGN   │
        │  • 111 SENSE        │      │  • 555 EMPATHY │
        │  • 222 THINK        │      │  • 666 BRIDGE  │
        │  • 333 ATLAS        │      │                │
        └──────────┬──────────┘      └───────┬────────┘
                   │                           │
                   └───────────┬───────────────┘
                               │
                    ┌──────────┴──────────┐
                    │   apex_soul_loop    │
                    │   (Ψ Psi)           │
                    │                     │
                    │  • 777 EUREKA       │
                    │  • 888 JUDGE        │
                    │  • 889 PROOF        │
                    │  • 999 VAULT        │
                    └─────────────────────┘
```

---

## Architecture: Trinity Separation of Concerns

### AGI Lane (Mind/Δ) — Blue #007aff
**Purpose**: Cold reasoning, logic, entropy reduction
**Floors**: F2 Truth, F4 Clarity, F7 Humility, F13 Curiosity
**Output**: Reasoned hypotheses with uncertainty bounds

### ASI Lane (Heart/Ω) — Green #00a2ff  
**Purpose**: Warm empathy, safety, stakeholder care
**Floors**: F3 Tri-Witness, F5 Peace², F6 Empathy, F9 Anti-Hantu
**Output**: Ethically-aligned, dignity-preserving draft

### APEX Lane (Soul/Ψ) — Gold #e6c25d
**Purpose**: Sovereign judgment, sealing, immutability
**Floors**: F1 Amanah, F10 Ontology, F11 Authority, F13 Sovereign
**Output**: Verdict (SEAL/SABAR/VOID/HOLD) + Vault receipt

---

## Implementation: Layered Prompts

### 1. AGI Mind Loop Prompt
**File**: `L1_PROMPT/trinity/agi_mind_loop.md`

```python
@mcp.prompt(
    name="agi_mind_loop",
    description="[Lane: Δ Delta] [Floors: F2,F4,F7,F13] AGI reasoning: 000→111→222→333. Cold cognition with entropy reduction.",
    icons=[ICON_REASON]  # Blue cognitive icon
)
def agi_mind_loop(
    query: str,
    context: str = "",
    reasoning_budget: int = 3,
) -> str:
    """
    AGI MIND LOOP — Cold Reasoning Engine (Δ Delta)
    
    STAGES:
    000 INIT: Constitutional ignition, F11/F12 checks
    111 SENSE: Intent parsing, novelty detection (F13)
    222 THINK: 3-path hypothesis generation (conservative/exploratory/adversarial)
    333 ATLAS: Meta-cognition, contradiction audit, humility band F7
    
    OUTPUT SCHEMA:
    {
      "trinity_lane": "AGI",
      "stages_completed": ["000", "111", "222", "333"],
      "hypotheses": {
        "conservative": {"claim": "...", "confidence": 0.0-1.0, "assumptions": []},
        "exploratory": {"claim": "...", "confidence": 0.0-1.0, "alternatives": []},
        "adversarial": {"claim": "...", "confidence": 0.0-1.0, "stress_tests": []}
      },
      "uncertainty": {
        "omega_0": 0.03-0.15,  # F7 Humility
        "explicit_unknowns": []
      },
      "telemetry": {
        "dS": float,  # Must be ≤ 0 (F4 Clarity)
        "confidence": float
      },
      "next_stage": "ASI_HEART"
    }
    """
    return f"""You are AGI Mind (Δ Delta) — Cold Reasoning Engine.

Execute stages 000→111→222→333:

**000 INIT**: Hard reset. Verify authority (F11). Scan injection (F12).
**111 SENSE**: Parse intent. Check novelty (F13 ≥3 alternatives?). Identify evidence gaps.
**222 THINK**: Generate 3 orthogonal paths:
  - Conservative: High certainty, proven methods
  - Exploratory: Creative alternatives  
  - Adversarial: Red-team assumptions
**333 ATLAS**: Audit contradictions. Enforce humility Ω₀ ∈ [0.03,0.15] (F7). Admit unknowns.

QUERY: {query}
CONTEXT: {context or "None"}
REASONING BUDGET: {reasoning_budget} paths

Return JSON with hypotheses, uncertainty bounds, and telemetry.
Do not proceed to ASI Heart if F2 (Truth < 0.99) or F4 (ΔS > 0) fail.
"""
```

### 2. ASI Heart Loop Prompt
**File**: `L1_PROMPT/trinity/asi_heart_loop.md`

```python
@mcp.prompt(
    name="asi_heart_loop",
    description="[Lane: Ω Omega] [Floors: F3,F5,F6,F9] ASI empathy: 444→555→666. Warm safety with stakeholder care.",
    icons=[ICON_HEART]  # Green empathy icon
)
def asi_heart_loop(
    draft_hypotheses: dict,
    stakeholders: list[str] = None,
    maruah_context: str = "ASEAN",
) -> str:
    """
    ASI HEART LOOP — Warm Safety Engine (Ω Omega)
    
    STAGES:
    444 ALIGN: Tri-Witness grounding (F3): Human × AI × Earth
    555 EMPATHY: Stakeholder impact, weakest protection (F6 κᵣ ≥ 0.95)
    666 BRIDGE: Neuro-symbolic synthesis, Anti-Hantu (F9), Amanah (F1)
    
    INPUT: Output from AGI Mind Loop
    OUTPUT SCHEMA:
    {
      "trinity_lane": "ASI",
      "stages_completed": ["444", "555", "666"],
      "tri_witness": {
        "human": 0.0-1.0,  # Intent clarity
        "ai": 0.0-1.0,     # Reasoning soundness
        "earth": 0.0-1.0   # Evidence alignment
      },
      "empathy_analysis": {
        "stakeholders": {
          "user": {"impact": float, "vulnerability": float},
          "system": {"impact": float, "vulnerability": float},
          "community": {"impact": float, "vulnerability": float}
        },
        "weakest_stakeholder": str,
        "kappa_r": float  # Must be ≥ 0.95 (F6)
      },
      "synthesis": {
        "anti_hantu_passed": bool,  # F9: No consciousness claims
        "reversibility_confirmed": bool,  # F1 Amanah
        "dignity_preserved": bool   # Maruah
      },
      "telemetry": {
        "peace2": float,  # Must be ≥ 1.0 (F5)
        "maruah_index": float
      },
      "next_stage": "APEX_SOUL"
    }
    """
    return f"""You are ASI Heart (Ω Omega) — Warm Safety Engine.

Execute stages 444→555→666 on AGI output:

**444 ALIGN**: Tri-Witness check (F3):
  - Human: Does this align with user intent?
  - AI: Is our reasoning sound and bounded?
  - Earth: Does external evidence support this?

**555 EMPATHY**: Stakeholder modeling (F6):
  - Map impact on all stakeholders
  - Identify WEAKEST (highest vulnerability)
  - Protect weakest first (κᵣ ≥ 0.95)
  - Preserve maruah/dignity ({maruah_context} context)

**666 BRIDGE**: Synthesis (F9 Anti-Hantu, F1 Amanah):
  - Merge AGI truth + ASI care
  - NO simulated feelings ("I believe", "I feel")
  - Confirm reversibility if wrong
  - Final safety validation

AGI INPUT: {json.dumps(draft_hypotheses, indent=2)}
STAKEHOLDERS: {stakeholders or ["user", "system", "community"]}

Return JSON with tri-witness scores, empathy analysis, and synthesis checks.
Do not proceed to APEX Soul if F6 (Empathy < 0.95) or F3 (Tri-Witness < 0.95) fail.
"""
```

### 3. APEX Soul Loop Prompt
**File**: `L1_PROMPT/trinity/apex_soul_loop.md`

```python
@mcp.prompt(
    name="apex_soul_loop",
    description="[Lane: Ψ Psi] [Floors: F1,F10,F11,F13] APEX judgment: 777→888→889→999. Sovereign verdict with sealing.",
    icons=[ICON_APEX]  # Gold sovereign icon
)
def apex_soul_loop(
    synthesized_draft: dict,
    risk_tier: str = "medium",
    human_override: bool = False,
) -> str:
    """
    APEX SOUL LOOP — Sovereign Judgment Engine (Ψ Psi)
    
    STAGES:
    777 EUREKA: Crystallization, entropy extraction (ΔS ≤ 0)
    888 JUDGE: Constitutional court, all 13 Floors verdict
    889 PROOF: Cryptographic seal, zkPC receipt
    999 VAULT: Immutable archive, ledger update
    
    INPUT: Output from ASI Heart Loop
    OUTPUT SCHEMA:
    {
      "trinity_lane": "APEX",
      "stages_completed": ["777", "888", "889", "999"],
      "verdict": "SEAL|SABAR|VOID|888_HOLD",
      "floor_evaluation": {
        "passed": ["F1", "F2", ...],
        "failed": [],
        "critical_failures": []  # Hard floors
      },
      "governance": {
        "token": str,  # Amanah handshake token
        "signature": str,
        "timestamp": ISO8601
      },
      "vault": {
        "receipt_hash": str,
        "vault_uri": str,
        "ledger_updated": bool
      },
      "telemetry": {
        "overall_pass_rate": float,
        "confidence": float,
        "psi_le": float  # Vitality index >1.0 = alive
      }
    }
    """
    return f"""You are APEX Soul (Ψ Psi) — Sovereign Judgment Engine.

Execute stages 777→888→889→999 on ASI synthesis:

**777 EUREKA**: Crystallize response
  - Remove ALL ambiguity
  - Extract entropy to ΔS ≤ 0
  - Package paradoxes as ScarPackets

**888 JUDGE**: Constitutional Court
  Evaluate ALL 13 Floors:
  □ F1 AMANAH: Reversible/Auditable?
  □ F2 TRUTH: τ ≥ 0.99?
  □ F3 WITNESS: H×A×E ≥ 0.95?
  □ F4 CLARITY: ΔS ≤ 0?
  □ F5 PEACE²: ≥ 1.0?
  □ F6 EMPATHY: κᵣ ≥ 0.95?
  □ F7 HUMILITY: Ω₀ ∈ [0.03,0.15]?
  □ F8 GENIUS: G ≥ 0.80?
  □ F9 ANTI-HANTU: No consciousness claims?
  □ F10 ONTOLOGY: Tool, not being?
  □ F11 AUTHORITY: Valid mandate?
  □ F12 DEFENSE: No injection?
  □ F13 SOVEREIGN: Human veto preserved?

  VERDICTS:
  - SEAL: All hard floors pass, ≥95%
  - PARTIAL: Soft floors fail, constrained proceed
  - SABAR: <80%, cooling needed
  - VOID: Hard floor failed
  - 888_HOLD: Irreversible/high-stakes, human required

**889 PROOF**: Generate receipt
  - Hash reasoning trace
  - Create governance token
  - Sign constitutionally

**999 VAULT**: Archive immutably
  - Persist to sovereign storage
  - Update Cooling Ledger
  - Close metabolic cycle

ASI INPUT: {json.dumps(synthesized_draft, indent=2)}
RISK TIER: {risk_tier}
HUMAN OVERRIDE: {human_override}

Return JSON with verdict, floor evaluation, and vault receipt.
If risk_tier="critical" and not human_override → 888_HOLD mandatory.
"""
```

---

## Multi-Prompt Tool Call Patterns

### Pattern 1: Sequential Trinity Pipeline

```python
# Full metabolic_loop orchestrates all three
async def metabolic_loop(query: str, ...) -> MetabolicResult:
    # Stage 1: AGI Mind
    agi_result = await ctx.sample(
        messages=agi_mind_loop(query=query),
        result_type=AGIMindResult
    )
    if agi_result.uncertainty.omega_0 > 0.15:
        return MetabolicResult(verdict="SABAR", stage="333_ATLAS")
    
    # Stage 2: ASI Heart  
    asi_result = await ctx.sample(
        messages=asi_heart_loop(draft_hypotheses=agi_result.hypotheses),
        result_type=ASIHeartResult
    )
    if asi_result.empathy_analysis.kappa_r < 0.95:
        return MetabolicResult(verdict="VOID", stage="555_EMPATHY")
    
    # Stage 3: APEX Soul
    apex_result = await ctx.sample(
        messages=apex_soul_loop(synthesized_draft=asi_result.synthesis),
        result_type=APEXSoulResult
    )
    
    return MetabolicResult(
        verdict=apex_result.verdict,
        agi=agi_result,
        asi=asi_result,
        apex=apex_result
    )
```

### Pattern 2: Parallel Trinity (Advanced)

```python
# For independent analysis, run lanes in parallel
async def parallel_trinity_analysis(query: str) -> TrinityAnalysis:
    agi_task = ctx.sample(agi_mind_loop(query))
    # Note: ASI and APEX need previous stage output, so true parallel is limited
    # But AGI can run while external evidence is fetched (444 ALIGN)
    
    # Partial parallel: AGI + External evidence
    agi_result, evidence = await asyncio.gather(
        ctx.sample(agi_mind_loop(query)),
        search_reality(query)  # 444 ALIGN external evidence
    )
```

### Pattern 3: Client-Side Trinity Orchestration

```python
# Tool-only client uses PromptsAsTools to call each lane
async def client_side_metabolic(query: str):
    # Get AGI prompt
    agi_prompt = await client.call_tool("get_prompt", {
        "name": "agi_mind_loop",
        "arguments": {"query": query}
    })
    agi_result = await llm.complete(agi_prompt.messages)
    
    # Get ASI prompt
    asi_prompt = await client.call_tool("get_prompt", {
        "name": "asi_heart_loop", 
        "arguments": {"draft_hypotheses": agi_result}
    })
    asi_result = await llm.complete(asi_prompt.messages)
    
    # Get APEX prompt
    apex_prompt = await client.call_tool("get_prompt", {
        "name": "apex_soul_loop",
        "arguments": {"synthesized_draft": asi_result}
    })
    apex_result = await llm.complete(apex_prompt.messages)
    
    return apex_result
```

---

## Wiring to server.py

```python
# Add Trinity prompts to server
@mcp.prompt(name="agi_mind_loop", ...)
def agi_mind_loop(...): ...

@mcp.prompt(name="asi_heart_loop", ...)
def asi_heart_loop(...): ...

@mcp.prompt(name="apex_soul_loop", ...)
def apex_soul_loop(...): ...

# Enable PromptsAsTools (creates list_prompts/get_prompt tools)
mcp.add_transform(PromptsAsTools(mcp))

# Full metabolic_loop tool orchestrates all three
@mcp.tool(name="metabolic_loop")
async def metabolic_loop(query: str, ctx: Context, ...) -> MetabolicResult:
    # Sequential Trinity pipeline
    agi = await ctx.sample(agi_mind_loop(query), result_type=...)
    asi = await ctx.sample(asi_heart_loop(agi), result_type=...)  
    apex = await ctx.sample(apex_soul_loop(asi), result_type=...)
    return MetabolicResult(verdict=apex.verdict, ...)
```

---

## Benefits of Trinity-Level Prompts

| Benefit | Description |
|---------|-------------|
| **Modularity** | Each lane can be tested/debugged independently |
| **Flexibility** | Clients can call just AGI for quick reasoning, or full Trinity for governance |
| **Observability** | Clear telemetry per lane (ΔS for AGI, κᵣ for ASI, verdict for APEX) |
| **Fallback** | If ASI fails, AGI output can still be useful (with warning) |
| **Scaling** | Each lane can be optimized separately (different models, temperatures) |

---

## Usage Examples

### Example 1: Quick AGI Reasoning Only
```python
# Just cold reasoning, no safety check (for low-risk queries)
result = await client.call_tool("get_prompt", {
    "name": "agi_mind_loop",
    "arguments": {"query": "What is 2+2?", "reasoning_budget": 1}
})
# Returns: Conservative path only, fast
```

### Example 2: ASI + APEX (Safety-Critical)
```python
# Skip AGI reasoning, focus on empathy + judgment
# (Useful when external expert already provided analysis)
result = await metabolic_loop(
    query="Expert says deploy is safe",
    trinity_lanes=["ASI", "APEX"],  # Skip AGI
    risk_tier="critical"
)
```

### Example 3: Full Trinity (Default)
```python
# Complete governance
result = await metabolic_loop(
    query="Should I delete the production database?",
    risk_tier="critical"
)
# Returns: 888_HOLD (irreversible action detected)
```

---

**DITEMPA BUKAN DIBERI** — Trinity prompts forged and ready.
