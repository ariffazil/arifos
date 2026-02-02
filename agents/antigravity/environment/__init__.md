# Environment Initialization

> **The Physics Layer of .antigravity**  
> **Imports:** HYPERVISOR, PHYSICS  
> **Purpose:** Thermodynamic enforcement for agent operations

---

## 🌡️ The Three Physics Engines

```python
from environment import HYPERVISOR, PHYSICS

PHYSICS = {
    "token": TokenPhysics(),   # Energy budget (Landauer Limit)
    "time": TimePhysics(),     # Entropy/Time (Latency bounds)
    "law": ConstitutionalLaw() # Floor enforcement (F1-F13)
}

HYPERVISOR = Hypervisor()  # Ignition engine
```

---

## ⚡ Quick Start

```python
# 1. Check budget before operation
if PHYSICS["token"].session_cost < 0.50:
    proceed()
else:
    raise PermissionError("STARVATION: Budget critical")

# 2. Enforce time bounds
result = await PHYSICS["time"].measure(agent.execute(input))

# 3. Check constitutional floor
if PHYSICS["law"].check_floor("F1", action):
    proceed()
else:
    return {"verdict": "VOID", "reason": "F1 Amanah violated"}

# 4. Run full metabolic cycle
result = await HYPERVISOR.ignition(AgentClass, query)
```

---

## 📚 Documentation

| File | Purpose |
|:---|:---|
| `physics.md` | TokenPhysics, TimePhysics, ConstitutionalLaw |
| `hypervisor.md` | Ignition, metabolic cycle, loop orchestration |
| `__init__.md` | This file — quick reference |

---

**DITEMPA BUKAN DIBERI**
