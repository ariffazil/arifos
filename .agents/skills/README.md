# arifOS Agent Skills

**Location:** `.agents/skills/`  
**Purpose:** Reusable skill templates for arifOS agents

---

## Skill Categories

### core-arifos/ (MANDATORY)
Essential skills for all arifOS agents:

| Skill | Purpose | Constitutional Floor |
|-------|---------|---------------------|
| **arifos-orchestration** | 000-999 loop management | F3, F4 |
| **governance-audit** | F1-F13 verification | All |
| **injection-defense** | F12 pattern detection | F12 |
| **thermo-planning** | Resource budgeting | F4 |
| **truth-logging** | Audit trail maintenance | F1, F2 |

---

## Skill Structure

Each skill is a directory containing:

```
skills/core-arifos/skill-name/
├── SKILL.md          # Skill definition and usage
├── examples/         # Example invocations
└── tests/            # Validation tests
```

---

## Using Skills

Skills are referenced in workflows and MCP tool calls:

```json
{
  "tool": "agi_reason",
  "params": {
    "query": "Analyze deployment safety",
    "skills": ["governance-audit", "thermo-planning"]
  }
}
```

---

**DITEMPA BUKAN DIBERI — Forged, Not Given**
