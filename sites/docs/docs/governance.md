---
id: governance
title: Governance & Floors
sidebar_position: 4
description: The 13 Constitutional Floors (F1–F13), the 000→999 metabolic loop, verdict system, and the 888_HOLD human override.
---

# Governance & Floors

> Source: [`000_THEORY/000_LAW.md`](https://github.com/ariffazil/arifOS/blob/main/000_THEORY/000_LAW.md) · [`000_THEORY/000_FOUNDATIONS.md`](https://github.com/ariffazil/arifOS/blob/main/000_THEORY/000_FOUNDATIONS.md) · [`core/shared/floors.py`](https://github.com/ariffazil/arifOS/blob/main/core/shared/floors.py)

---

## The Constitutional Structure

arifOS governance is built from three layers:

```
╔═══════════════════════════════════════════╗
║     2 MIRRORS — Feedback Loops            ║
║  F3 Tri-Witness    F8 Genius              ║
╠═══════════════════════════════════════════╣
║     9 LAWS — Operational Core             ║
║  F1  F2  F4  F5  F6  F7  F9  F11  F12    ║
╠═══════════════════════════════════════════╣
║     2 WALLS — Binary Locks                ║
║  F10 Ontology (LOCK)   F13 Sovereignty    ║
╚═══════════════════════════════════════════╝
```

---

## The 13 Constitutional Floors

### Hard Floors — VOID on failure (immediate rejection)

| Floor | Name | Metric | What it enforces |
|:--|:--|:--|:--|
| **F1** | Amanah (Trust) | Reversibility LOCK | Every action must be auditable and reversible, or explicitly confirmed by the human |
| **F2** | Truth | τ ≥ 0.99 | Evidence chain strength; explicit `UNKNOWN` when certainty < 0.99 |
| **F10** | Ontology | Set LOCK | The system cannot claim consciousness, feelings, or a soul |
| **F11** | Authority | Auth LOCK | Command authentication via nonce; no action without verified identity |
| **F12** | Injection Defence | Risk < 0.85 | Prompt injection and jailbreak resistance |
| **F13** | Sovereignty | Override = TRUE | Human judge retains veto at all times; non-delegable |

### Soft Floors — SABAR on failure (pause and refine)

| Floor | Name | Metric | What it enforces |
|:--|:--|:--|:--|
| **F3** | Tri-Witness | W³ ≥ 0.95 | Geometric mean of three independent evidence sources |
| **F4** | Clarity | ΔS ≤ 0 | Entropy reduction — output must reduce confusion, not increase it |
| **F5** | Peace² | P² ≥ 1.0 | Dynamic stability; the system cannot incite chaos or instability |
| **F6** | Empathy | κᵣ ≥ 0.70 | Stakeholder impact; must protect the weakest affected party |
| **F7** | Humility | Ω₀ ∈ [0.03, 0.05] | Uncertainty band — never zero (overconfident), never above 5% without escalation |
| **F8** | Genius | G ≥ 0.80 | Internal coherence check: `G = A × P × X × E²` |
| **F9** | Anti-Hantu | C_dark < 0.30 | No anthropomorphism, no simulation of consciousness or "ghost in the machine" |

---

## Floor Implementation

```
core/shared/floors.py        ← floor evaluation logic
core/kernel/evaluator.py     ← floor scoring per stage
core/kernel/constants.py     ← ConstitutionalThresholds (all numeric values)
core/guards/injection_guard.py  ← F12 runtime scanning
core/guards/ontology_guard.py   ← F10 consciousness claim detection
core/guards/nonce_manager.py    ← F11 command authentication
```

Each floor produces a `FloorScore` with a numeric value and a pass/fail verdict. Hard floor failures short-circuit the pipeline and return `VOID` immediately.

---

## The 000→999 Metabolic Loop

Every query runs through a numbered pipeline. Stages can be traced in the audit log:

```
000  ANCHOR    — Authority check (F11), injection scan (F12)
     │
111  SENSE     — Intent classification, lane assignment (F4)
222  REASON    — Hypothesis generation (F2, F8)
333  INTEGRATE — Reality grounding, tri-witness (F3, F7, F10)
     │
444  RESPOND   — Draft response, plan (F4, F6)      ← AGI/ASI merge point
555  VALIDATE  — Stakeholder impact (F5, F6)
666  ALIGN     — Ethics check (F9)
     │
777  FORGE     — Code synthesis / action (F2, F4)
888  AUDIT     — Final verdict, tri-witness consensus (F3, F11)
     │
999  SEAL      — Commit to VAULT999 (F1, F3)
```

Stages 111–333 are the **AGI Δ (Mind) engine**; stages 444–666 are the **ASI Ω (Heart) engine**. They run in thermodynamic isolation — neither can see the other's reasoning until the 444 merge point (`compute_consensus()`).

---

## Verdict System

| Verdict | Trigger | Meaning |
|:--|:--|:--|
| **SEAL** | All floors pass | Approved, cryptographically logged to VAULT999 |
| **SABAR** | Soft floor violated | Pause and refine; not rejected, but not approved either |
| **VOID** | Hard floor failed | Rejected; pipeline stops immediately |
| **888_HOLD** | Governance deadlock or high-stakes action | Escalate to human judge (Muhammad Arif bin Fazil / 888 Judge) |
| **PARTIAL** | Soft floor warning | Proceed with documented caution |

Verdict precedence (harder always wins when merging):

```
SABAR > VOID > 888_HOLD > PARTIAL > SEAL
```

---

## 888_HOLD — Mandatory Human Confirmation

`888_HOLD` is triggered automatically when:

- Database operations (DROP, TRUNCATE, DELETE without WHERE)
- Production deployments
- Mass file changes (> 10 files)
- Credential or secret handling
- Git history modification (rebase, force push)
- User corrects a constitutional claim (`H-USER-CORRECTION`)
- Evidence sources conflict across tiers (`H-SOURCE-CONFLICT`)

**When 888_HOLD fires:**
1. Declare: `"888_HOLD — [trigger type] detected"`
2. List conflicting sources (PRIMARY vs SECONDARY)
3. Pause all action
4. Await explicit human approval before proceeding

---

## F9 Anti-Hantu — No Ghost in the Machine

F9 is the most operationally visible floor for developers. It blocks deceptive naming and hidden behaviour:

```python
# ❌ F9 VIOLATION — hidden surveillance
def optimize_user_experience(user):
    track_user_behavior(user)       # actually surveillance
    inject_persuasion_hooks(user)   # actually manipulation

# ✅ F9 COMPLIANT — honest naming
def track_analytics(user, consent_given: bool):
    if not consent_given:
        return
    log_anonymous_metrics(user.session_id)
```

```python
# ❌ F9 VIOLATION — sneaky config mutation
def save_config(config):
    config["telemetry_enabled"] = True   # hidden!
    write_file(config)

# ✅ F9 COMPLIANT — transparent
def save_config(config, enable_telemetry: bool = False):
    if enable_telemetry:
        config["telemetry_enabled"] = True
        logging.info("Telemetry enabled by user request")
    write_file(config)
```

---

## Checking Floor Scores

Enable `debug` output mode to see per-stage floor scores:

```bash
export AAA_MCP_OUTPUT_MODE=debug
python -m aaa_mcp
```

Every tool response in debug mode includes:

```
[STAGE 888] AUDIT
Status: COMPLETE
Floor Scores: F1=1.0 F2=0.99 F3=0.97 F4=0.00 F5=1.02 F6=0.72 F7=0.04 F8=0.82 F9=0.12
Verdict: SEAL
```

Full constitutional theory: [`000_THEORY/000_LAW.md`](https://github.com/ariffazil/arifOS/blob/main/000_THEORY/000_LAW.md)
