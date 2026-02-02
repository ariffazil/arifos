# Physics.md — Thermodynamic Constraints

> **The Immutable Laws of the Agentic Environment**  
> **Reference:** `333_APPS/L5_AGENTS/environment/physics.py`  
> **Principle:** *Code that loops is alive. But even life must obey thermodynamics.*

---

## 🌡️ I. TOKEN PHYSICS (Landauer Limit)

### Concept
**Conservation of Compute.** Every thought costs energy. Every token consumed has a thermodynamic price.

### Implementation
```python
class TokenPhysics:
    COST_PER_1K_TOKENS = 0.002  # USD (API reference cost)
    MAX_SESSION_BUDGET = 1.00    # USD per session
```

### The Budget Equation
```
session_cost = Σ((input_tokens + output_tokens) / 1000) × COST_PER_1K

Constraint: session_cost ≤ MAX_SESSION_BUDGET
```

### Starvation Protocol
```python
def consume(self, input_tokens: int, output_tokens: int) -> float:
    cost = ((input_tokens + output_tokens) / 1000) * self.COST_PER_1K_TOKENS
    self.session_cost += cost
    
    if self.session_cost > self.MAX_SESSION_BUDGET:
        raise PermissionError(
            f"STARVATION: Budget exceeded "
            f"({self.session_cost:.4f} > {self.MAX_SESSION_BUDGET})"
        )
    return self.session_cost
```

### Agent Usage
```python
# Check before expensive operation
if PHYSICS["token"].session_cost > 0.75:
    logger.warning("Budget 75% consumed — consider sealing")

# Consume for operation
cost = PHYSICS["token"].consume(input_tokens=1000, output_tokens=500)
print(f"Session cost: ${cost:.4f} / $1.00")
```

---

## ⏱️ II. TIME PHYSICS (Entropy/Time Dilation)

### Concept
**Consumer of Entropy.** Execution takes time. Time is scarce. Slow operations increase system entropy.

### Implementation
```python
class TimePhysics:
    MAX_LATENCY_MS = 30000  # 30 seconds hard limit
```

### The Time Bound
```
latency = t_end - t_start ≤ MAX_LATENCY_MS

Constraint: operation completes within 30s or VOID
```

### Timeout Enforcement
```python
async def measure(self, coro):
    """Execute coroutine within time bounds."""
    start = time.perf_counter_ns()
    try:
        return await asyncio.wait_for(
            coro, 
            timeout=self.MAX_LATENCY_MS / 1000
        )
    except asyncio.TimeoutError:
        raise TimeoutError("SABAR: Operation exceeded time budget")
    finally:
        end = time.perf_counter_ns()
        duration_ms = (end - start) / 1e6
        # Log for telemetry
```

### Agent Usage
```python
# Wrap agent execution with time enforcement
result = await PHYSICS["time"].measure(agent.execute(input_data))

# Handle timeout
if result.get("verdict") == "SABAR":
    logger.info("Operation timed out — cooling required")
```

---

## ⚖️ III. CONSTITUTIONAL LAW (Floor Enforcement)

### Concept
**The Kernel Guard.** Middleware that binds agent actions to constitutional floors.

### Implementation
```python
class ConstitutionalLaw:
    @staticmethod
    def check_floor(floor_id: str, value: Any) -> bool:
        """
        Check if action violates constitutional floor.
        Returns True if allowed, False if blocked.
        """
        if floor_id == "F1":  # Amanah (Reversibility)
            # Block irreversible actions by default
            return False  # Require explicit override
            
        elif floor_id == "F2":  # Truth
            return value >= 0.99
            
        elif floor_id == "F4":  # Clarity
            return value <= 0  # ΔS ≤ 0
            
        # ... etc for all 13 floors
        return True
```

### Floor Checks
```python
# Pre-flight check
if not PHYSICS["law"].check_floor("F1", action.reversible):
    return {"verdict": "VOID", "floor": "F1", "reason": "Irreversible without approval"}

if not PHYSICS["law"].check_floor("F2", claim.confidence):
    return {"verdict": "VOID", "floor": "F2", "reason": "Truth < 0.99"}

if not PHYSICS["law"].check_floor("F12", input.injection_risk):
    return {"verdict": "VOID", "floor": "F12", "reason": "Injection detected"}
```

---

## 🔗 IV. PHYSICS & THE 13 FLOORS

| Floor | Physics Enforcement | Mechanism |
|:---:|:---|:---|
| **F1** | Amanah | `ConstitutionalLaw.check_floor("F1", reversible)` |
| **F2** | Truth | TokenPhysics (expensive verification = high truth) |
| **F4** | Clarity | TimePhysics (fast response = low entropy) |
| **F7** | Humility | TokenPhysics (limited budget forces concision) |
| **F12** | Injection | ConstitutionalLaw pre-flight scan |
| **F-all** | All floors | HYPERVISOR cycle enforcement |

---

## 📊 V. BUDGET CONFIGURATION

### Default Budgets (`budget.json`)
```json
{
  "token_physics": {
    "cost_per_1k_tokens": 0.002,
    "max_session_budget": 1.00,
    "warning_threshold": 0.75
  },
  "time_physics": {
    "max_latency_ms": 30000,
    "warning_threshold_ms": 20000
  },
  "thermodynamics": {
    "landauer_kbt_ln2": 2.87e-21,
    "entropy_budget_max": 1.0
  }
}
```

### Per-Operation Budgets
```python
# Quick query (low budget)
quick_budget = {"tokens": 100, "time_ms": 5000}

# Deep reasoning (high budget)
deep_budget = {"tokens": 4000, "time_ms": 25000}

# Constitutional seal (unlimited budget for verification)
seal_budget = {"tokens": "unlimited", "time_ms": "unlimited"}
```

---

## 🎯 VI. OPERATIONAL PRINCIPLES

### 1. Starvation is Preferable to Violation
Better to run out of budget (STARVATION) than violate a floor (VOID).

### 2. Time is Entropy
Slow operations add confusion. Fast, clear operations reduce entropy.

### 3. Truth Has a Price
Verification costs tokens. Cheap answers are likely false.

### 4. Physics is Hard
These constraints are **non-negotiable**. They are enforced, not suggested.

---

## 📚 VII. REFERENCES

| Reference | Location |
|:---|:---|
| **Implementation** | `333_APPS/L5_AGENTS/environment/physics.py` |
| **Hypervisor** | `environment/hypervisor.md` |
| **Floors** | `../rules/constitutional_floors.md` |
| **Theory** | `../../000_THEORY/000_LAW.md` |

---

**DITEMPA BUKAN DIBERI**

> *"Every thought costs energy. Every operation takes time. 
> Every action is judged. This is not cruelty. This is thermodynamics."*
