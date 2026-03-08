# arifOS MCP Naming Guide
## For Non-Coders

---

### THE SIMPLE RULE

**Use `arifosmcp.runtime`**  
**Ignore `arifosmcp.transport`**

That is it. That is the whole guide.

---

### WHY ARE THERE TWO NAMES?

Think of it like a restaurant:

```
FRONT OF HOUSE (Customers see)
  arifosmcp.runtime
  - Waiters, menu, dining room
  - This is what you interact with
        |
        v
BACK OF HOUSE (Kitchen)
  arifosmcp.transport
  - Chefs, ovens, recipes  
  - Works behind the scenes
```

---

### WHEN TO USE WHICH

| If you want to... | Use this | Example |
|-------------------|----------|---------|
| Start the server | arifosmcp.runtime | python -m arifosmcp.runtime http |
| Connect from GitHub | arifosmcp.runtime | Already configured |
| Check health | arifosmcp.runtime | curl localhost:8080/health |
| Fix something inside | arifosmcp.transport | Only if AGI tells you to |

---

### DOCKER COMPOSE CHEAT SHEET

Your server runs this command:
```yaml
# In docker-compose.arifos.yml
CMD: ["python", "-m", "arifosmcp.runtime", "http"]
          ↑
          USE THIS ONE
```

---

### COMMON CONFUSION

WRONG:
```
python -m arifosmcp.transport        ← Old way, do not use
```

RIGHT:
```
python -m arifosmcp.runtime ← New way, use this
```

---

### FILE LOCATIONS

| Path | Purpose |
|------|---------|
| /srv/arifOS/arifosmcp.runtime/ | **Public API** ← You care about this |
| /srv/arifOS/arifosmcp.transport/ | **Internal code** ← Ignore this |

---

### WHAT IF I SEE BOTH?

**Example:** You see two files:
- arifosmcp.runtime/server.py ✅
- arifosmcp.transport/server.py ⚠️

**What to do:**  
Use the one with **arifos_** prefix. Ignore the shorter one.

---

### QUICK CHECKLIST

Before running any command:

- [ ] Does it say arifosmcp.runtime? → ✅ Good to go
- [ ] Does it only say arifosmcp.transport? → ❌ Stop, ask first
- [ ] Are you unsure? → ❌ Ask AGI-Opencode

---

### FOR FUTURE AGENTS

If an AI agent (like me) is working on your VPS:

**Tell them:**
> Use arifosmcp.runtime as the canonical surface. arifosmcp.transport is legacy internal.

---

### SUMMARY

| Name | Role | Use? |
|------|------|------|
| arifosmcp.runtime | Public interface | ✅ YES |
| arifosmcp.transport | Internal implementation | ❌ NO |

---

**Created:** 2026-03-05  
**By:** AGI-Opencode  
**For:** Arif Fazil  
**Purpose:** Prevent confusion about MCP naming
