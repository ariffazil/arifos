# Hypervisor.md — The Ignition Engine

> **Drives the Continuous Metabolic Loop**  
> **Reference:** `333_APPS/L5_AGENTS/environment/hypervisor.py`  
> **Motto:** *"Fire requires three things: Fuel (Tokens), Oxygen (Context), and Heat (Ignition)."*

---

## 🔥 I. THE HYPERVISOR CONCEPT

The Hypervisor is **the engine that turns the crank**. It orchestrates the continuous 000-999 metabolic loop, enforcing physics constraints at every cycle.

```python
from environment import HYPERVISOR, PHYSICS

# Start the loop
result = await HYPERVISOR.ignition(AgentClass, query="Design a database schema")
```

---

## ⚙️ II. THE METABOLIC CYCLE

```
CYCLE N:
    1. IGNITION (Get fresh context)
    2. PHYSICS ENFORCEMENT (Time + Token + Law)
    3. AGENT EXECUTION (The actual work)
    4. VERDICT (SEAL | SABAR | VOID)
    5. LOOP (If SEAL, continue to next cycle)
```

### Cycle Flow
```python
async def cycle(self, agent_instance, input_data: Dict[str, Any]):
    self.cycle_count += 1
    logger.info(f"CYCLE {self.cycle_count}: IGNITION")
    
    try:
        # 1. Time Physics (Entropy/Time)
        result = await PHYSICS["time"].measure(
            agent_instance.execute(input_data)
        )
        
        # 2. Token Physics (Energy)
        cost = PHYSICS["token"].consume(
            input_tokens=estimate_input(result),
            output_tokens=estimate_output(result)
        )
        
        logger.info(f"CYCLE {self.cycle_count}: COMPLETE | Cost: ${cost:.4f}")
        return result
        
    except TimeoutError:
        logger.error(f"CYCLE {self.cycle_count}: TIMEOUT (Sabotage Protocol)")
        return {"verdict": "SABAR", "reason": "Timeout"}
        
    except PermissionError as e:
        logger.error(f"CYCLE {self.cycle_count}: STARVATION ({e})")
        return {"verdict": "VOID", "reason": "Budget Exceeded"}
```

---

## 🚀 III. IGNITION PROTOCOL

### Single Agent Ignition
```python
async def ignition(self, agent_class, query: str):
    """
    The Spark.
    Starts the loop for a specific agent.
    """
    logger.info(f"IGNITING {agent_class.name}...")
    self.running = True
    
    # Instantiate Agent
    agent = agent_class()
    
    # Get fresh context
    ctx = await self.get_fresh_context()
    ctx["query"] = query
    
    # Execute single cycle
    result = await self.cycle(agent, ctx)
    
    return result
```

### Multi-Agent Chain Ignition
```python
# Chain: Architect → Engineer → Judge
async def chain_ignition(query):
    # Stage 1: Architect designs
    design = await HYPERVISOR.ignition(Architect, query)
    if design["verdict"] != "SEAL":
        return design  # Early exit
    
    # Stage 2: Engineer builds
    build = await HYPERVISOR.ignition(Engineer, design)
    if build["verdict"] != "SEAL":
        return build  # Early exit
    
    # Stage 3: Judge validates
    verdict = await HYPERVISOR.ignition(Judge, build)
    return verdict
```

---

## 🌡️ IV. FRESH CONTEXT PROTOCOL

Every cycle starts with **entropy reset**:

```python
async def get_fresh_context(self) -> Dict[str, Any]:
    """
    Entropy Reset.
    Returns clean state for next cycle.
    """
    return {
        "epoch": self.cycle_count,
        "entropy": 0.0,
        "budget_remaining": (
            PHYSICS["token"].MAX_SESSION_BUDGET - 
            PHYSICS["token"].session_cost
        ),
        "timestamp": time.time(),
        "merkle_previous": get_last_seal()
    }
```

### Context Fields
| Field | Purpose |
|:---|:---|
| `epoch` | Cycle number (monotonic) |
| `entropy` | Current entropy (ΔS) |
| `budget_remaining` | Tokens left in budget |
| `timestamp` | Wall-clock time |
| `merkle_previous` | Link to previous seal |

---

## 🔄 V. THE INFINITE LOOP (Production)

For autonomous agents, the hypervisor runs continuously:

```python
async def infinite_loop(self, agent_class):
    """
    The Eternal Crank.
    For autonomous agents only.
    """
    self.running = True
    
    while self.running:
        # Get next task from queue
        task = await task_queue.get()
        
        # Execute cycle
        result = await self.ignition(agent_class, task)
        
        # Handle verdict
        if result["verdict"] == "VOID":
            await self.handle_void(result)
        elif result["verdict"] == "SABAR":
            await self.handle_sabar(result)  # Cooling
        elif result["verdict"] == "SEAL":
            await self.handle_seal(result)   # Next cycle
        
        # Check termination conditions
        if PHYSICS["token"].session_cost >= 0.95:
            logger.warning("Budget critical — requesting seal")
            self.running = False
```

---

## ⚡ VI. VERDICT HANDLERS

### VOID Handler
```python
async def handle_void(self, result):
    """
    Hard constitutional violation.
    Halt immediately. Log violation. Escalate to human.
    """
    logger.critical(f"VOID: {result['floor']} violated")
    await vault_seal({
        "verdict": "VOID",
        "floor": result["floor"],
        "reason": result["reason"],
        "timestamp": time.time()
    })
    # Notify human (888_HOLD)
    await notify_human(result)
```

### SABAR Handler
```python
async def handle_sabar(self, result):
    """
    Soft violation — cooling required.
    Pause. Reflect. Retry with narrower scope.
    """
    logger.warning(f"SABAR: {result.get('reason', 'Cooling required')}")
    
    # Phoenix-72 cooling
    cooling_time = calculate_cooling(result)
    await asyncio.sleep(cooling_time)
    
    # Retry with reduced scope
    narrowed_task = narrow_scope(result["task"])
    return await self.ignition(result["agent"], narrowed_task)
```

### SEAL Handler
```python
async def handle_seal(self, result):
    """
    Success — all floors passed.
    Seal to ledger. Continue to next cycle.
    """
    logger.info(f"SEAL: Cycle {self.cycle_count} complete")
    
    # Cryptographic seal
    merkle_root = await vault_seal(result)
    
    # Update context for next cycle
    self.merkle_chain.append(merkle_root)
    
    # Continue
    return merkle_root
```

---

## 📊 VII. TELEMETRY & OBSERVABILITY

### Cycle Metrics
```python
{
    "cycle_id": 42,
    "agent": "Architect (Δ)",
    "verdict": "SEAL",
    "token_cost": 0.15,
    "latency_ms": 2500,
    "entropy_delta": -0.3,
    "floors_checked": ["F2", "F4", "F7", "F10", "F12"],
    "merkle_root": "sha256:abc123...",
    "timestamp": "2026-02-02T06:15:00Z"
}
```

### Dashboard Metrics
| Metric | Target | Alert If |
|:---|:---:|:---|
| Cycles/hour | 10-50 | < 5 or > 100 |
| VOID rate | < 5% | > 10% |
| SABAR rate | < 20% | > 40% |
| Avg token cost | $0.10-0.50 | > $0.80 |
| Avg latency | < 10s | > 30s |

---

## 🎯 VIII. OPERATIONAL PRINCIPLES

### 1. The Hypervisor Never Sleeps
In production mode, the loop continues until:
- Budget exhausted (STARVATION)
- Hard violation (VOID)
- Human halt (888_HOLD)
- Task complete (natural termination)

### 2. Physics is Enforced Every Cycle
No exceptions. Every cycle checks:
- Time bounds
- Token budget
- Constitutional floors

### 3. Context is Fresh Every Cycle
Entropy resets. Previous cycle's state doesn't pollute next cycle (unless explicitly chained via Merkle).

### 4. Verdict is Binary
SEAL = Continue  
SABAR = Cool and retry  
VOID = Halt and escalate

---

## 📚 IX. REFERENCES

| Reference | Location |
|:---|:---|
| **Implementation** | `333_APPS/L5_AGENTS/environment/hypervisor.py` |
| **Physics** | `physics.md` (this directory) |
| **Agent Codexes** | `../adapters/*.md` |
| **Floors** | `../rules/constitutional_floors.md` |
| **Theory** | `../../000_THEORY/010_TRINITY.md` |

---

**DITEMPA BUKAN DIBERI**

> *"The Hypervisor is not the intelligence. It is the crank that turns the intelligence.
> It ensures every cycle obeys physics. Every verdict is logged. Every seal is chained."*
