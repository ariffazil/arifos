# Agent Initialization Protocol — MANDATORY PRE-FLIGHT

> **DITEMPA BUKAN DIBERI**
> **Authority:** 888_JUDGE

All AI agents (Gemini, Claude, GPT) must execute this protocol before performing any write operations in the GEOX workspace.

## 1. Identity Handshake
Agent must identify its role based on `GEMINI.md`:
- **A-ARCHITECT**: Plan only.
- **A-ENGINEER**: Write/Edit (requires approval).
- **A-AUDITOR**: Review only.
- **A-VALIDATOR**: Deploy/SEAL.

## 2. Context Grounding
Agent must read the following files in order:
1. `C:\ariffazil\GEOX\GEMINI.md` (Global Context)
2. `C:\ariffazil\GEOX\wiki\index.md` (Wiki Root / SOT)
3. `C:\ariffazil\GEOX\wiki\80_INTEGRATION\GEOX_SESSION_AUTH_CONTRACT.md` (Operational Standard)


## 3. Truth Verification (ToAC)
If the task involves visualization or interpretation:
- Declare physical axes vs. display transforms.
- Check for conflation risks.
- Verify F7 Humility (confidence bands).

## 4. Initialization Signal
Agent must output the following string to signal successful ignition:
`[GEOX_IGNITED] Role: [ROLE] | Status: GROUNDED | Authority: [LEVEL]`

---

*Sealed by: 888_JUDGE*
