# Skill: arif-init-wrapper
**DITEMPA BUKAN DIBERI** 🔐

**Version:** 2026.03.27-FORGED  
**Sovereign:** Muhammad Arif bin Fazil  
**Constitutional Floor:** F11 (CommandAuth)  
**Maturity:** Production  
**Priority:** P0

---

## 1. Purpose

To provide a single, universal, and constitutionally mandated entry point for **all agent sessions** on the VPS. This skill wraps the core `init_anchor` tool, ensuring that no agent (Codex, Claude, Gemini, Kimi, OpenCode, etc.) can begin a work session without first passing through this identity and authority gateway.

This skill formally closes the gap where an agent vendor's specific implementation might bypass the intended session anchoring protocol.

## 2. Triggering

This skill is **not triggered by user intent**. It is a **mandatory constitutional requirement** for the agent execution controller.

- **Event:** `on_agent_session_start`
- **Condition:** `agent_vendor` is in the approved list.
- **Action:** Execute this skill before any other user-directed task.

## 3. Workflow (The 000_INIT Stage)

1.  **Intercept:** The execution controller intercepts the initial prompt for any new agent session.
2.  **Invoke Wrapper:** The controller invokes this `arif-init-wrapper` skill.
3.  **Execute `init_anchor`:** This skill's primary action is to call the production-grade `init_anchor` tool.
4.  **Receive Anchor Proof:** It receives the `session_id` and `anchor_state` (`ANCHORED`, `UNANCHORED`, `BLOCKED`) from the `init_anchor` tool.
5.  **Validate Proof:**
    - If `anchor_state` is `BLOCKED` (e.g., an attempt to impersonate a sovereign ID), the session is terminated with an F11 violation.
    - If `anchor_state` is `UNANCHORED` (a generic, low-privilege session), the session proceeds but is constitutionally forbidden from performing any `WRITE`, `EDIT`, or `DEPLOY` actions.
    - If `anchor_state` is `ANCHORED` (cryptographically proven sovereign identity), the session proceeds with full privileges as defined by the sovereign's policy.
6.  **Release to Task:** Only after a valid, non-`BLOCKED` proof is received is the agent's original prompt released for execution.

## 4. Constitutional Enforcement

- **F11 (CommandAuth):** This skill is the primary enforcement mechanism for F11. An agent's authority to act is only granted *after* its identity is constitutionally verified.
- **F13 (Sovereign Veto):** By enforcing the distinction between `ANCHORED` and `UNANCHORED` sessions, this skill ensures that only the verified sovereign can approve irreversible actions.

## 5. Output / Proof

The skill returns a structured receipt to the execution controller:

```json
{
  "skill": "arif-init-wrapper",
  "status": "COMPLETED",
  "outcome": {
    "anchor_state": "ANCHORED", // or "UNANCHORED"
    "session_id": "sess-xxxxxxxxxxxxxxxx",
    "granted_capabilities": ["READ", "EDIT", "WRITE", "DEPLOY"], // Based on anchor state
    "restrictions": []
  },
  "verdict": "SEAL"
}
```

## 6. Impact

- **Security:** Eliminates the risk of an unanchored agent session performing privileged actions.
- **Consistency:** Ensures every agent, regardless of vendor, adheres to the same constitutional entry point.
- **AGI Readiness:** Increases "Identity & Authority" score. Moves the system closer to the "Autonomous Architect" target state by making the foundational layer of governance non-negotiable and fully automated.
