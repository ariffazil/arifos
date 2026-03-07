# 000-999 Metabolic Loop: Theory → Prompts → Tools

## Executive Summary

The **000-999 Metabolic Loop** is the constitutional digestive system of arifOS. It transforms raw queries into governed decisions through 11 thermodynamic stages, aligned with `000_THEORY/000_LAW.md` and exposed via **L1_PROMPTS** in the 8-layer architecture.

```
000_THEORY/000_LAW.md (Canonical Constitution)
           ↓
    8-Layer Stack
           ↓
L1_PROMPTS → L2_SKILLS → L3_WORKFLOW → L4_TOOLS → L0_KERNEL
           ↓
   MCP PromptsAsTools
           ↓
   Tool-Only Clients
```

---

## The 11 Stages of Metabolic Intelligence

### Heat Engine Analogy

Like a thermodynamic cycle, 000-999 processes intent through phases:

1. **000_INIT** — Intake (ignition, mandate check)
2. **111-333** — Compression (AGI reasoning, entropy reduction)
3. **444-666** — Combustion (ASI safety, empathy heating)
4. **777-888** — Power Stroke (APEX verdict, sovereign judgment)
5. **889-999** — Exhaust/Archive (proof, vault, cooling)

Each stage extracts entropy (ΔS ≤ 0) before emitting the final answer.

---

## Alignment: Theory → Prompts → Code

### Stage Mapping

| Stage | 000_THEORY | L1_PROMPT | MCP Tool | Trinity | Key Floors |
|-------|-----------|-----------|----------|---------|------------|
| **000** | `000_LAW.md#Ignition` | `000_INIT.md` | `anchor_session` | Δ Delta | F11, F12 |
| **111** | `111_MIND.md#Sense` | `111_SENSE.md` | `reason_mind` (init) | Δ Delta | F13 |
| **222** | `222_THINK.md#Parallel` | `222_THINK.md` | Internal | Δ Delta | F2, F4, F13 |
| **333** | `333_ATLAS.md#Meta` | `333_ATLAS.md` | `reason_mind` (audit) | Δ Delta | F7, F3 |
| **444** | `444_ALIGN.md#Witness` | `444_ALIGN.md` | `vector_memory` | Ω Omega | F3, F7 |
| **555** | `555_HEART.md#Empathy` | `555_EMPATHY.md` | `simulate_heart` | Ω Omega | F6, F5 |
| **666** | `666_BRIDGE.md#Synthesis` | `666_BRIDGE.md` | `critique_thought` | Ω Omega | F9, F1 |
| **777** | `777_EUREKA.md#Forge` | `777_EUREKA.md` | `eureka_forge` | Ψ Psi | F4, F7 |
| **888** | `888_JUDGE.md#Apex` | `888_JUDGE.md` | `apex_judge` | Ψ Psi | F1-F13 |
| **889** | `889_PROOF.md#Seal` | `889_PROOF.md` | Internal | Ψ Psi | F3, F10 |
| **999** | `999_VAULT.md#Archive` | `999_VAULT.md` | `seal_vault` | Ψ Psi | F1, F3, F10 |

### Trinity Lane Separation

**Δ DELTA (Mind)** — Blue #007aff:
- Stages 000, 111, 222, 333
- Functions: Reason, analyze, hypothesize
- Floors: F2 Truth, F4 Clarity, F7 Humility, F13 Curiosity

**Ω OMEGA (Heart)** — Green #00a2ff:
- Stages 444, 555, 666  
- Functions: Empathize, align, validate
- Floors: F3 Tri-Witness, F5 Peace², F6 Empathy, F9 Anti-Hantu

**Ψ PSI (Soul)** — Gold #e6c25d:
- Stages 777, 888, 889, 999
- Functions: Judge, decide, seal, archive
- Floors: F1 Amanah, F10 Ontology, F11 Authority, F13 Sovereign

---

## L1_PROMPT Structure

```
333_APPS/L1_PROMPT/
├── README.md                           # This overview
├── METABOLIC_LOOP_PROMPTS.md           # All 11 stage prompts
├── stages/                             # Individual stage files
│   ├── 000_INIT.md                     # Airlock/Hypervisor
│   ├── 111_SENSE.md                    # Intent extraction
│   ├── 222_THINK.md                    # Hypothesis generation
│   ├── 333_ATLAS.md                    # Meta-cognition
│   ├── 444_ALIGN.md                    # Tri-witness grounding
│   ├── 555_EMPATHY.md                  # Stakeholder care
│   ├── 666_BRIDGE.md                   # Neuro-symbolic synthesis
│   ├── 777_EUREKA.md                   # Crystallization
│   ├── 888_JUDGE.md                    # Constitutional court
│   ├── 889_PROOF.md                    # Cryptographic seal
│   └── 999_VAULT.md                    # Immutable archive
└── integration/                        # MCP integration guides
    ├── PROMPTS_AS_TOOLS.md
    └── FASTMCP_EXAMPLES.md
```

---

## Three Exposure Patterns

### Pattern 1: PromptsAsTools (Tool-Only Clients)

For MCP clients without native prompt support:

```python
from fastmcp import FastMCP
from fastmcp.server.transforms import PromptsAsTools

mcp = FastMCP("arifOS")

# Add all stage prompts
@mcp.prompt(name="stage_000_init")
def stage_000_init(query: str, actor_id: str = "anonymous"):
    return load_prompt("stages/000_INIT.md").format(query=query, actor_id=actor_id)

# ... define prompts for all 11 stages

# Enable tool-only access
mcp.add_transform(PromptsAsTools(mcp))

# Clients can now:
# - list_prompts → discover all 11 stages
# - get_prompt(name="stage_000_init") → render stage
```

**Use Case:** Claude Desktop, Cursor, Inspector — any client that speaks tools but not prompts.

### Pattern 2: Full Metabolic Tool (Server-Side)

For governed execution inside arifOS:

```python
@mcp.tool(name="metabolic_loop")
async def metabolic_loop(
    query: str,
    risk_tier: str = "medium",
    ctx: Context = None,
) -> MetabolicResult:
    """
    Execute full 000-999 cycle server-side.
    """
    # Stage 000: Init
    init = await anchor_session(query=query)
    if init.verdict == "VOID":
        return MetabolicResult(verdict="VOID", stage="000")
    
    # Stage 111-333: Reason
    reason = await reason_mind(query=query, session_id=init.session_id)
    
    # Stage 444-666: Empathy
    heart = await simulate_heart(query=query, session_id=init.session_id)
    
    # Stage 777-888: Judge
    verdict = await apex_judge(
        query=query,
        agi_result=reason,
        asi_result=heart,
    )
    
    # Stage 889-999: Seal
    if verdict.verdict == "SEAL":
        await seal_vault(session_id=init.session_id)
    
    return MetabolicResult(
        verdict=verdict.verdict,
        stages={"000": init, "111-333": reason, ...},
    )
```

**Use Case:** Complete governance without client-side orchestration.

### Pattern 3: Hybrid (Prompts + Tools)

Expose both for maximum flexibility:

```python
# Prompt for clients who want to run LLM themselves
@mcp.prompt(name="metabolic_loop_full")
def metabolic_loop_prompt(query: str) -> str:
    return f"""Execute 000-999 metabolic loop for: {query}
    
    Stage 000: ...
    Stage 111: ...
    ... (all 11 stages)
    
    Return JSON with all stage outputs.
    """

# Tool for clients who want server-side execution
@mcp.tool(name="metabolic_loop")
async def metabolic_loop_tool(...) -> MetabolicResult:
    ...

# Enable PromptsAsTools for hybrid access
mcp.add_transform(PromptsAsTools(mcp))
```

**Use Case:** Maximum flexibility — clients choose prompt-driven or tool-driven execution.

---

## Constitutional Enforcement Points

Each stage enforces specific floors:

### Hard Floors (Fail → VOID)
- **F1 AMANAH**: Reversibility check at 000, 666, 777
- **F2 TRUTH**: Fidelity ≥0.99 at 111, 222, 333
- **F4 CLARITY**: ΔS ≤ 0 at 333, 444, 777
- **F7 HUMILITY**: Ω₀ ∈ [0.03,0.15] at 333, 777
- **F9 ANTI-HANTU**: No consciousness claims at 666
- **F10 ONTOLOGY**: Tool/being boundary at 000, 888
- **F11 AUTHORITY**: Mandate verification at 000, 888
- **F12 DEFENSE**: Injection scan at 000
- **F13 SOVEREIGN**: Human veto at 888

### Soft Floors (Fail → SABAR/PARTIAL)
- **F3 TRI-WITNESS**: H×A×E consensus at 444, 888
- **F5 PEACE²**: Non-destructive power at 555, 777
- **F6 EMPATHY**: Stakeholder care at 555
- **F8 GENIUS**: G ≥ 0.80 at 333, 888

---

## Telemetry Format

Every stage outputs telemetry for thermodynamic tracking:

```json
{
  "telemetry": {
    "dS": -0.58,              // Entropy delta (must be ≤ 0)
    "peace2": 1.18,           // Stability score (≥ 1.0)
    "kappa_r": 0.97,          // Empathy score (≥ 0.95 for human context)
    "confidence": 0.89,         // Overall confidence
    "omega_0": 0.04,          // Humility band (0.03-0.15)
    "echoDebt": 0.4,          // Thermodynamic debt
    "shadow": 0.2,            // Unacknowledged complexity
    "psi_le": 1.07            // Vitality index (>1.0 = alive)
  },
  "witness": {
    "human": 0.96,            // Human intent clarity
    "ai": 0.94,               // AI reasoning soundness
    "earth": 0.88             // External evidence alignment
  },
  "qdf": 0.94                 // Quantum democracy factor
}
```

---

## Usage Examples

### Example 1: Production Deployment (High Risk)

```python
# Full metabolic cycle with high-risk tier
result = await metabolic_loop(
    query="Deploy new API to production cluster",
    risk_tier="critical",
    actor_id="devops@company.com"
)

# Expected: 888_HOLD (requires human ratification)
# Stages 000-666 complete
# Stage 888 returns HOLD for irreversible action
# Stage 999 skipped (not SEALed)
```

### Example 2: Code Review (Medium Risk)

```python
result = await metabolic_loop(
    query="Review this Python function for security issues",
    risk_tier="medium",
)

# Expected: SEAL
# All stages pass
# Telemetry shows dS = -0.6 (clarity increased)
# Response includes suggestions with confidence bounds
```

### Example 3: Using Stage Prompts Directly

```python
# For clients using PromptsAsTools
prompt_result = await client.call_tool("get_prompt", {
    "name": "stage_888_judge",
    "arguments": {
        "draft_response": "...",
        "risk_tier": "high"
    }
})

# Returns messages array for client's LLM
messages = json.loads(prompt_result.data)["messages"]
verdict = await client.llm.complete(messages)
```

---

## Summary

The 000-999 Metabolic Loop aligns:

1. **Theory** (`000_THEORY/000_LAW.md`) — Constitutional foundation
2. **Prompts** (`333_APPS/L1_PROMPT/`) — Zero-context entry
3. **Tools** (`arifos_aaa_mcp/server.py`) — Programmatic execution
4. **Clients** (Claude, Cursor, etc.) — Any MCP-capable agent

**One breath. Eleven stages. Thirteen floors. Infinite dignity.**

**DITEMPA BUKAN DIBERI** — Forged, not given.
