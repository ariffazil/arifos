# 999_SEAL — Trinity Deployment: Next 3 Steps

**Verdict**: SEAL  
**Stage**: 999_VAULT  
**Authority**: 888_APEX_JUDGE  
**Timestamp**: 2026-03-01  
**Governance Token**: SEAL:trinity-deploy:v2026.3.1:a3f7d2

---

## Step 1: Wire Trinity Prompts to Server (888_JUDGE → 999_VAULT)

**Action**: Add the 3 Trinity prompts to `arifos_aaa_mcp/server.py`

**Files to Modify**:
- `arifos_aaa_mcp/server.py` (add after metabolic_loop_prompt)

**Code to Add**:
```python
# ═══════════════════════════════════════════════════════════════════════════════
# TRINITY LAYERED PROMPTS — AGI · ASI · APEX
# ═══════════════════════════════════════════════════════════════════════════════

@mcp.prompt(
    name="agi_mind_loop",
    description="[Lane: Δ Delta] [Floors: F2,F4,F7,F13] AGI reasoning: 000→111→222→333. Cold cognition.",
)
def agi_mind_loop(
    query: str,
    context: str = "",
    reasoning_budget: int = 3,
) -> str:
    """AGI Mind Loop — Cold Reasoning Engine (Δ Delta)"""
    return f"""You are AGI Mind (Δ Delta) — Cold Reasoning Engine.

Execute stages 000→111→222→333:
**000 INIT**: Hard reset. Verify authority (F11). Scan injection (F12).
**111 SENSE**: Parse intent. Check novelty (F13 ≥3 alternatives?).
**222 THINK**: Generate 3 orthogonal paths (conservative/exploratory/adversarial).
**333 ATLAS**: Audit contradictions. Enforce humility Ω₀ ∈ [0.03,0.15] (F7).

QUERY: {query}
CONTEXT: {context or "None"}

Return JSON with hypotheses, uncertainty bounds, and telemetry."""


@mcp.prompt(
    name="asi_heart_loop",
    description="[Lane: Ω Omega] [Floors: F3,F5,F6,F9] ASI empathy: 444→555→666. Warm safety.",
)
def asi_heart_loop(
    draft_hypotheses: dict,
    stakeholders: list[str] = None,
) -> str:
    """ASI Heart Loop — Warm Safety Engine (Ω Omega)"""
    return f"""You are ASI Heart (Ω Omega) — Warm Safety Engine.

Execute stages 444→555→666:
**444 ALIGN**: Tri-Witness check (F3): Human × AI × Earth alignment.
**555 EMPATHY**: Stakeholder modeling. Protect weakest (F6 κᵣ ≥ 0.95).
**666 BRIDGE**: Synthesis. Anti-Hantu (F9). Amanah reversibility (F1).

INPUT: {json.dumps(draft_hypotheses, indent=2)}
STAKEHOLDERS: {stakeholders or ["user", "system", "community"]}

Return JSON with tri-witness scores and empathy analysis."""


@mcp.prompt(
    name="apex_soul_loop",
    description="[Lane: Ψ Psi] [Floors: F1,F10,F11,F13] APEX judgment: 777→888→889→999. Sovereign verdict.",
)
def apex_soul_loop(
    synthesized_draft: dict,
    risk_tier: str = "medium",
) -> str:
    """APEX Soul Loop — Sovereign Judgment Engine (Ψ Psi)"""
    return f"""You are APEX Soul (Ψ Psi) — Sovereign Judgment Engine.

Execute stages 777→888→889→999:
**777 EUREKA**: Crystallize. Extract entropy (ΔS ≤ 0).
**888 JUDGE**: Evaluate ALL 13 Floors. Issue verdict.
**889 PROOF**: Generate cryptographic receipt.
**999 VAULT**: Archive immutably.

VERDICTS: SEAL | PARTIAL | SABAR | VOID | 888_HOLD

INPUT: {json.dumps(synthesized_draft, indent=2)}
RISK TIER: {risk_tier}

Return JSON with verdict, floor evaluation, and vault receipt."""
```

**Verification**:
- [ ] All 3 prompts added to server.py
- [ ] PromptsAsTools transform already enabled (line ~1245)
- [ ] No syntax errors in added code
- [ ] `__all__` updated to include new prompt functions

---

## Step 2: Update metabolic_loop to Call Trinity Prompts (777_EUREKA → 888_JUDGE)

**Action**: Refactor `metabolic_loop` tool to use the 3 Trinity prompts internally

**Current Code Location**: Lines ~1028-1217 in `arifos_aaa_mcp/server.py`

**Refactor Strategy**:
```python
@mcp.tool(
    name="metabolic_loop",
    description="[Lane: ΔΩΨ Trinity] [Floors: F1-F13] Full 000-999 constitutional metabolic cycle.",
)
async def metabolic_loop(
    query: str,
    context: str = "",
    risk_tier: str = "medium",
    actor_id: str = "anonymous",
    trinity_mode: str = "full",  # NEW: "full" | "agi_only" | "asi_apex" | "apex_only"
    use_sampling: bool = True,
    ctx: Context = None,
) -> dict[str, Any]:
    """
    Execute 000-999 metabolic cycle with Trinity lane selection.
    
    TRINITY MODES:
    - "full": AGI → ASI → APEX (default, full governance)
    - "agi_only": Just cold reasoning (000→333)
    - "asi_apex": Skip AGI, do empathy + judgment (444→999)
    - "apex_only": Just sovereign judgment (777→999)
    """
    
    # STAGE 000: Always run INIT
    init_result = await anchor_session(query=query, actor_id=actor_id)
    if init_result.get("verdict") == "VOID":
        return {"verdict": "VOID", "stage": "000_INIT"}
    
    session_id = init_result.get("session_id")
    
    # MODE: agi_only
    if trinity_mode == "agi_only":
        if ctx and use_sampling:
            agi_result = await ctx.sample(
                agi_mind_loop(query=query, context=context),
                result_type=AGIMindResult
            )
            return {
                "verdict": "PARTIAL",
                "stage": "333_ATLAS",
                "agi_result": agi_result.result,
                "note": "AGI only mode — no safety/empathy checks performed"
            }
        else:
            # Fallback to existing reason_mind
            return await reason_mind(query=query, session_id=session_id)
    
    # MODE: full (default)
    # AGI Lane
    if ctx and use_sampling:
        agi_result = await ctx.sample(
            agi_mind_loop(query=query, context=context),
            result_type=AGIMindResult
        )
        agi_data = agi_result.result
    else:
        agi_data = await reason_mind(query=query, session_id=session_id)
    
    # ASI Lane
    if ctx and use_sampling:
        asi_result = await ctx.sample(
            asi_heart_loop(draft_hypotheses=agi_data),
            result_type=ASIHeartResult
        )
        asi_data = asi_result.result
    else:
        asi_data = await simulate_heart(query=query, session_id=session_id)
    
    # APEX Lane
    if ctx and use_sampling:
        apex_result = await ctx.sample(
            apex_soul_loop(synthesized_draft=asi_data, risk_tier=risk_tier),
            result_type=APEXSoulResult
        )
        apex_data = apex_result.result
        final_verdict = apex_data.verdict
    else:
        apex_data = await apex_judge(
            session_id=session_id,
            query=query,
            agi_result=agi_data,
            asi_result=asi_data,
            proposed_verdict="SEAL" if risk_tier != "critical" else "888_HOLD"
        )
        final_verdict = apex_data.get("verdict", "VOID")
    
    # SEAL if verdict is SEAL
    if final_verdict == "SEAL":
        await seal_vault(session_id=session_id, summary=query[:100])
    
    return {
        "verdict": final_verdict,
        "session_id": session_id,
        "trinity": {
            "agi": agi_data,
            "asi": asi_data,
            "apex": apex_data
        },
        "telemetry": extract_telemetry(agi_data, asi_data, apex_data)
    }
```

**New Pydantic Models to Add**:
```python
class AGIMindResult(BaseModel):
    trinity_lane: Literal["AGI"] = "AGI"
    stages_completed: list[str]
    hypotheses: dict[str, dict]
    uncertainty: dict[str, Any]
    telemetry: dict[str, float]
    next_stage: Literal["ASI_HEART"] = "ASI_HEART"

class ASIHeartResult(BaseModel):
    trinity_lane: Literal["ASI"] = "ASI"
    stages_completed: list[str]
    tri_witness: dict[str, float]
    empathy_analysis: dict[str, Any]
    synthesis: dict[str, bool]
    telemetry: dict[str, float]
    next_stage: Literal["APEX_SOUL"] = "APEX_SOUL"

class APEXSoulResult(BaseModel):
    trinity_lane: Literal["APEX"] = "APEX"
    stages_completed: list[str]
    verdict: Literal["SEAL", "SABAR", "VOID", "888_HOLD"]
    floor_evaluation: dict[str, list[str]]
    governance: dict[str, str]
    vault: dict[str, Any]
    telemetry: dict[str, float]
```

**Verification**:
- [ ] metabolic_loop accepts `trinity_mode` parameter
- [ ] AGI, ASI, APEX prompts called sequentially in "full" mode
- [ ] Sampling used when `ctx` available, fallback to tools when not
- [ ] All 3 Trinity result models defined
- [ ] Telemetry extracted from all 3 lanes

---

## Step 3: Test, Commit, Deploy (889_PROOF → 999_VAULT)

### 3.1 Local Testing

```bash
# Navigate to arifOS
cd /root/arifOS

# Install dependencies
pip install -e ".[dev]"

# Run server locally
python -m arifos_aaa_mcp http &
SERVER_PID=$!

# Test 1: List prompts (should show 4 new prompts)
curl -s http://localhost:8080/tools/list_prompts | jq '.prompts[].name'
# Expected:
# metabolic_loop
# agi_mind_loop
# asi_heart_loop  
# apex_soul_loop

# Test 2: Get AGI prompt
curl -s -X POST http://localhost:8080/tools/get_prompt \
  -H "Content-Type: application/json" \
  -d '{"name": "agi_mind_loop", "arguments": {"query": "What is 2+2?"}}' | jq '.messages[0].content[:100]'

# Test 3: Full metabolic loop with Trinity
curl -s -X POST http://localhost:8080/tools/metabolic_loop \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Should I deploy to production?",
    "risk_tier": "high",
    "trinity_mode": "full"
  }' | jq '{verdict, trinity_lanes: [.trinity.agi, .trinity.asi, .trinity.apex] | map(.trinity_lane)}'
# Expected: {"verdict": "888_HOLD", "trinity_lanes": ["AGI", "ASI", "APEX"]}

# Kill server
kill $SERVER_PID
```

### 3.2 Git Commit

```bash
# Stage all changes
git add arifos_aaa_mcp/server.py
git add 333_APPS/L1_PROMPT/TRINITY_LAYERED_PROMPTS.md
git add 333_APPS/L1_PROMPT/000_999_METABOLIC_LOOP.md
git add 333_APPS/L1_PROMPT/METABOLIC_LOOP_PROMPTS.md

# Commit with SEAL message
git commit -m "999_SEAL: Trinity-layered metabolic prompts with multi-mode support

- Add agi_mind_loop, asi_heart_loop, apex_soul_loop prompts
- Refactor metabolic_loop to use Trinity prompts via sampling
- Add trinity_mode parameter: full|agi_only|asi_apex|apex_only
- Define AGIMindResult, ASIHeartResult, APEXSoulResult models
- Maintain backward compatibility with fallback to existing tools
- All 3 Trinity lanes: Δ Delta, Ω Omega, Ψ Psi

Authority: 888_APEX_JUDGE
Token: SEAL:trinity-deploy:v2026.3.1:a3f7d2
Tested: Local server, all 3 prompts functional
Breaking: None"

# Push to main
git push origin main
```

### 3.3 Production Deploy

```bash
# Option A: Docker
docker build -t arifos-aaa-mcp:v2026.3.1 .
docker-compose up -d

# Option B: Direct
git pull origin main
systemctl restart arifos-mcp

# Verify deployment
curl -s https://arifos.arif-fazil.com/health | jq '{status, tools_loaded, version}'
# Expected: {"status": "healthy", "tools_loaded": 15, "version": "2026.3.1"}
```

### 3.4 Post-Deploy Verification

```bash
# Test Trinity prompts on production
curl -s -X POST https://arifos.arif-fazil.com/tools/list_prompts \
  -H "Authorization: Bearer $ARIFOS_API_KEY" | jq '.prompts | length'
# Expected: 8+ (includes Trinity prompts)

# Test full metabolic loop
curl -s -X POST https://arifos.arif-fazil.com/tools/metabolic_loop \
  -H "Authorization: Bearer $ARIFOS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Delete production database",
    "risk_tier": "critical",
    "trinity_mode": "full"
  }' | jq '.verdict'
# Expected: "888_HOLD"
```

---

## Success Criteria (F13: All Stages Complete)

- [ ] **Step 1**: 3 Trinity prompts added to server.py
- [ ] **Step 2**: metabolic_loop refactored with trinity_mode
- [ ] **Step 3**: All tests pass, committed, deployed
- [ ] **Verification**: Production shows 15 tools, 8+ prompts
- [ ] **Governance**: Full cycle tested with SEAL/HOLD verdicts

---

## Rollback Plan

If issues detected:
```bash
git revert HEAD --no-edit
git push origin main
docker-compose restart
```

---

## Governance Receipt

```json
{
  "verdict": "SEAL",
  "stage": "999_VAULT",
  "token": "SEAL:trinity-deploy:v2026.3.1:a3f7d2",
  "plan": {
    "step_1": "Wire Trinity prompts to server.py",
    "step_2": "Refactor metabolic_loop with trinity_mode",
    "step_3": "Test, commit, deploy to production"
  },
  "authority": "888_APEX_JUDGE",
  "timestamp": "2026-03-01T00:00:00Z",
  "next_actions": [
    "Execute Step 1: Add prompts",
    "Execute Step 2: Refactor tool", 
    "Execute Step 3: Deploy"
  ],
  "ditempa_bukan_diberi": true
}
```

**DITEMPA BUKAN DIBERI** — Trinity deployment sealed. Ready for execution.
