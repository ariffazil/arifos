# Horizon 2026 Q2: MCP-First, Governance-Core

> **Strategic Priority:** Optimize GEOX as the subsurface MCP server and governance brain  
> **Timeline:** 2-week sprints  
> **Seal:** DITEMPA BUKAN DIBERI  
> **Applies to:** GEOX, arifOS, AF-FORGE

---

## The Bet

**GEOX wins not by having more buttons than Petrel, but by being the only subsurface tool with epistemic risk as first-class.**

Subsurface teams will adopt GEOX not for visualization, but for **decision discipline** that their existing tools cannot provide.

---

## Sprint Breakdown

### Week 1: MCP Server Hardening — "Drop-in Reliability"

**Goal:** Any MCP-capable agent can discover, introspect, and use GEOX without reading our minds.

| Deliverable | Status | Definition of Done |
|-------------|--------|-------------------|
| Unified Tool Registry | 🟡 In Progress | Single source of truth with metadata, schemas, error codes |
| `list_tools` Endpoint | 🟡 In Progress | Rich metadata for UI generation and auto-wiring |
| Standard Workflows (3) | 🔴 Not Started | Seismic, Map, AC_Risk Console flows documented and tested |
| Error Standardization | 🔴 Not Started | Normalized codes: validation, physics, governance |
| Client Sanity Check | 🔴 Not Started | Verified with Claude Desktop or equivalent |

**Key Decisions:**
- Tool status levels: `production` | `preview` | `scaffold`
- Error codes: `GEOX_4xx_*` validation, `GEOX_403_*` governance, `GEOX_422_*` physics
- All vision tools must emit AC_Risk and verdict

---

### Week 2: AC_Risk Console — "The Flagship MCP App"

**Goal:** One high-value MCP App that proves the pattern and delivers unique value.

**Why AC_Risk Console:**
- Light UI (sliders, fields, text) — no heavy graphics
- Works across all use-cases (seismic, maps, digitization)
- Shows what Petrel/DG/PaleoScan **DON'T** have: in-chat risk exploration
- Minimal dependencies: HTML + JS + MCP bridge

**Features:**
```
UI Components:
├── U_phys slider (0.0 - 1.0)
├── D_transform multi-select (transform checklist)
├── B_cog selector (expertise level dropdown)
├── Calculate button
├── Result panel:
│   ├── AC_Risk score (big number, color-coded)
│   ├── Verdict badge (SEAL/QUALIFY/HOLD/VOID)
│   ├── Component breakdown bars
│   ├── Explanation text
│   └── Suggested mitigations
├── History panel: previous calculations
└── Export: JSON/CSV of risk assessment
```

**Technical Stack:**
- Vanilla JS (no framework bloat)
- MCP App SDK host adapter
- Hosted at: `geox.arif-fazil.com/apps/ac-risk-console/`

**Success Criteria:**
- [ ] Runs inline in Claude Desktop
- [ ] Runs inline in goose
- [ ] External fallback works
- [ ] 3 demo videos recorded

---

## Defer: Web UI and WebMCP

**Condition for Re-activation:**
1. MCP server is rock-solid (measured: 99% tool success rate)
2. AC_Risk Console is live and used (measured: 50+ sessions/week)
3. Clear EMV from web surface (measured: customer request with budget)

**Rationale:**
- WebMCP spec is still evolving
- Web site without working MCP = "sudo features"
- Agents don't browse websites; they use tools

---

## Decision Principles

### 1. Better Tools Over More Tools

**DO:**
- Harden existing tools with schemas, error handling, versioning
- Document clear workflows
- Test with real clients

**DON'T:**
- Add new half-baked tools
- Expand surface before depth
- Build tools nobody asked for

### 2. Governance and Risk Over GUI Features

**DO:**
- Route everything through AC_Risk
- Emit verdicts (SEAL/QUALIFY/HOLD/VOID)
- Explain why something is risky

**DON'T:**
- Chase Petrel's visualization
- Build pretty dashboards without risk calc
- Hide uncertainty behind UI polish

### 3. Integration Over Cloning

**DO:**
- Accept Petrel exports → return AC_Risk audits
- Build bridges to DSG, PaleoScan, OpendTect
- Position as "governance layer on top"

**DON'T:**
- Try to replicate Petrel's GUI
- Compete on 3D visualization
- Build standalone interpretation suite

---

## Comparative Positioning

| Capability | Petrel/DG/PaleoScan | GEOX |
|------------|-------------------|------|
| 3D Visualization | ✅ Industry standard | ❌ Out of scope |
| Attribute Libraries | ✅ Hundreds | 🟡 Selective, physics-grounded |
| Auto-Interpretation | ✅ RGT, chronostrat | 🟡 VLM + consistency check |
| **Epistemic Risk** | ❌ None | ✅ **AC_Risk first-class** |
| **Governance (F1-F13)** | ❌ None | ✅ **Constitutional** |
| **Agent Interface** | ❌ None | ✅ **MCP Native** |
| **ToAC Discipline** | ❌ None | ✅ **Core Theory** |

**GEOX = The governance and risk brain that sits on top of existing interpretation stacks.**

---

## Integration Targets

### Phase 1: Export Bridges (Immediate)
```
Petrel → export horizons/grids → GEOX → AC_Risk audit → Decision support
DSG → export interpretation → GEOX → ToAC validation → Risk report
PaleoScan → export RGT → GEOX → Alternative hypotheses → Confidence bands
```

### Phase 2: Live Connections (Later)
- Well-known data formats (SEGY, LAS, XYZ)
- Standard APIs (WMS, WFS)
- Webhook notifications

---

## Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| MCP tool success rate | 99% | Server telemetry |
| Tool discovery time | <30s | Client integration test |
| AC_Risk Console usage | 50+ sessions/week | App analytics |
| Error clarity | 100% coded | Error registry coverage |
| Client integrations | 3+ types | Claude, goose, custom |
| Petrel bridge value | 1 case study | Customer validation |

---

## Prompt Directive for Agents

```markdown
You are optimizing GEOX for maximum EMV/NPV versus legacy subsurface software.

ABSOLUTE FOCUS:
1. Harden MCP server: schemas, errors, workflows, client testing
2. Ship AC_Risk Console: one flagship MCP App done well
3. Build bridges: accept exports from Petrel/DSG/PaleoScan, return risk audits

HARD CONSTRAINTS:
- Never propose features exceeding existing capacity
- Never promise parity with Petrel UX
- Always route through AC_Risk and ToAC
- Prefer governance over aesthetic appeal

DEFAULT RULE: Choose work that increases marginal value of GEOX as an 
MCP-integrated subsurface governance engine over standalone UX.
```

---

## Document History

| Date | Version | Change |
|------|---------|--------|
| 2026-04-10 | 1.0 | Initial horizon definition |

---

*DITEMPA BUKAN DIBERI — Forged, Not Given*  
*Applies across: GEOX, arifOS, AF-FORGE*
