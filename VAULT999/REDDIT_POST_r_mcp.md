# arifOS — I built an Intelligence Kernel for Constitutional AI (MCP-native, pip installable)

**TL;DR:** `pip install arifos` — A governance kernel that sits between AI models and users, enforcing 13 constitutional safety floors through 9 MCP tools. Every decision is cryptographically sealed. Would love feedback from the MCP community.

---

## What is arifOS?

I kept hitting the same problem: AI gives dangerous advice confidently, admits no uncertainty, and leaves no audit trail when things go wrong.

Existing solutions felt like guardrails made of cardboard:
- **Prompt engineering** — "Be safe!" (bypassed instantly)
- **Post-moderation** — Harm already generated (too late)
- **3-5 rule frameworks** — Not enough granularity

So I built something different: **an Intelligence Kernel** — not middleware, but the substrate that determines whether AI cognition is permitted to exist.

---

## Why MCP-Native Was Non-Negotiable

I rejected building a Python SDK. Here's why:

| SDK Approach | MCP Protocol Approach |
|:-------------|:----------------------|
| `pip install arifos-sdk` + wrapper | Direct MCP tool calls |
| Language-locked (Python only) | **Any language** (JS, Go, Rust, etc.) |
| Can bypass governance (wrapper hides behavior) | **Must speak protocol directly** |
| Tourist (needs translation) | **Indigenous** (native speaker) |

MCP isn't just transport — it's the **driver interface** to the kernel. Like USB for hardware, but for AI governance.

---

## The 9 MCP Tools (System Calls for Governed Cognition)

```
anchor(000)   → Session init + injection scan
reason(222)   → Logical analysis + truth check
integrate(333)→ Context grounding
validate(555) → Stakeholder impact (empathy ≥ 0.95)
align(666)    → Ethics check
forge(777)    → Solution synthesis
audit(888)    → Final verdict (SEAL/VOID/SABAR)
seal(999)     → Cryptographic commit to VAULT999
```

Every request runs 000→999. Fail a hard floor (F1, F2, F4, F7, F12) → **VOID** (blocked). Fail a soft floor (F5, F6, F9) → **SABAR** (pause + warn).

---

## The 13 Constitutional Floors

Not arbitrary rules. Load-bearing structure:

| Floor | Enforces | Fail Action |
|:------|:---------|:------------|
| F1 Amanah | Reversibility | VOID |
| F2 Truth | Grounded evidence | VOID |
| F7 Humility | Uncertainty ∈ [0.03, 0.05] | VOID |
| F12 Defense | Injection attacks | VOID |
| F6 Empathy | Vulnerable stakeholder protection | SABAR |
| F13 Sovereign | Human veto (888_HOLD) | Human review |

Full spec: [github.com/ariffazil/arifOS/blob/main/000_THEORY/000_LAW.md](https://github.com/ariffazil/arifOS/blob/main/000_THEORY/000_LAW.md)

---

## Quick Start

```bash
pip install arifos
python -m aaa_mcp          # stdio (Claude Desktop, Cursor)
python -m aaa_mcp sse      # SSE endpoint
python -m aaa_mcp http     # Streamable HTTP
```

Or connect to live server:
```bash
curl https://arifosmcp.arif-fazil.com/health
```

---

## The "Intelligence Kernel" Claim

I'm claiming arifOS is an **operating system for AI cognition**, not just middleware. Here's the precise distinction:

| Traditional OS | arifOS Intelligence Kernel |
|:---------------|:---------------------------|
| Controls whether a **program runs** | Controls whether a **thought is permitted** |
| Manages CPU/memory | Manages **thermodynamic cognitive budget** |
| Schedules processes | Schedules **000→999 governance pipeline** |
| Memory protection | **13 constitutional floors** as isolation |

It doesn't replace Linux (hardware). It **runs alongside it**, governing the AI layer.

---

## Honest State (Reality Index: 0.95)

Not going to oversell:

✅ **SEALED (Production)**
- 9 MCP tools operational
- 13 floors enforced
- Triple transport (STDIO/SSE/HTTP)
- Live: [arifosmcp.arif-fazil.com/health](https://arifosmcp.arif-fazil.com/health)

🟡 **SABAR (Pilot)**
- Multi-agent federation (L5)
- Ω₀ calibration needs production data

🔴 **VOID/Research**
- Institutional consensus (L6) — stubs only
- Recursive AGI (L7) — pure theory

---

## Why I'm Posting Here

The MCP community is building the "USB for AI." I think governance should be **native to that protocol**, not an afterthought.

**Questions for you:**

1. Is "protocol-native governance" something you'd want for your MCP servers?
2. Do the 13 floors feel like over-engineering, or necessary granularity?
3. Would you trust a kernel that can block your AI's cognition, or is that too much control?

**Repo:** [github.com/ariffazil/arifOS](https://github.com/ariffazil/arifOS)  
**Docs:** [arifos.arif-fazil.com](https://arifos.arif-fazil.com)

---

**Motto:** *DITEMPA BUKAN DIBERI* — Forged, Not Given 🔥💎🧠

Built by a geoscientist who got tired of AI giving confident bad advice. Would genuinely appreciate technical feedback from this community.
