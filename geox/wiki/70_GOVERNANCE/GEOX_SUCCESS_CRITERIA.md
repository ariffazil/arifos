# GEOX Success Criteria
**"DITEMPA BUKAN DIBERI" — Forged, Not Given.**

> **Version:** v0.4.1 — April 1, 2026
> **Authority:** 999 SEAL | Floors F1 F4 F7
> **Confidence:** CLAIM | P2 1.0 | HOLD CLEAR

---

## Executive Summary

**GEOX Phase-1 Definition:**
> AI-operable geoscience context and interpretation platform for image-first seismic and cross-section workflows inside MCP-enabled chat interfaces.

**GEOX is not "the LLM"** — GEOX is the governed Earth-model and visualization layer that receives intent, resolves assets, computes results, and renders views.

**Success Definition:**
GEOX succeeds if a geologist can start from a chat prompt, open a map or section, inspect geologically meaningful overlays, read bounded insights, and understand uncertainty without needing SEG-Y or vendor-locked interpretation software.

---

## Scope Freeze

### In-Scope (Now)
- Map context app
- Cross-section app
- Seismic section app
- Image ingest and QC
- Reflector/fault/facies overlays from images
- Geological reasoning and audit
- Memory and provenance

### Out-of-Scope (Now)
- SEG-Y-first workflows
- 3D seismic cube interpretation
- AVO/inversion-grade quantitative analysis
- Final economic or drilling decisions from image-only evidence

---

## Six-Axis Success Framework

| Axis | What It Measures |
|------|-----------------|
| **Usability** | Speed, workflow completion, learnability |
| **Geological Quality** | Scale disclosure, provenance, overlay usefulness |
| **Governance** | Hold triggers, irreversibility, audit completeness |
| **Interoperability** | Host portability, schema stability, structured fallback |
| **Performance** | Render latency, QC speed, determinism |
| **Repo Maturity** | Test coverage, version pinning, tool visibility |

---

## Usability Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Fresh query → first rendered map/section | < 60 sec (dev/staging) | E2E timer |
| Selected map feature → linked section | < 10 sec | E2E timer |
| First-time pilot geologist completion rate | > 80% | User study |
| Clicks from spatial context to section view | ≤ 3 after search | UI audit |

---

## Geological Quality Metrics

| Metric | Target | Enforcement |
|--------|--------|-------------|
| 100% of views display scale or `SCALE UNKNOWN` | Mandatory | F4 + DisplayState badge |
| 100% of views display provenance, display type, confidence | Mandatory | F11 + AuditState |
| Reflector/fault overlays rated "useful starting point" | ≥ 70% benchmark cases | User review |
| Cross-sections distinguish observed vs inferred | 100% | CrossSectionState `is_observed` |

---

## Governance Metrics

| Metric | Target | Enforcement |
|--------|--------|-------------|
| Out-of-scope requests trigger warning or 888 HOLD | 100% | CrossSectionHoldTriggers |
| Image-only outputs prohibit quantitative claims when scale/polarity/control insufficient | 100% | F4 + QC badges |
| Zero irreversible recommendations without human signoff | 100% | F1 + F13 |
| 100% of stored interpretations include audit metadata + uncertainty band | 100% | GeoXAuditState |

---

## Interoperability Metrics

| Metric | Target | Method |
|--------|--------|--------|
| Same canonical state for same request across ≥2 MCP hosts | 100% | Cross-host test |
| Full app mode works in FastMCP dev + ≥1 production host | Yes | Integration test |
| Structured fallback mode when host ignores rich rendering | Works | Graceful degradation test |
| No direct dependency on any one provider's vision API | Yes | Dependency audit |

---

## Performance Metrics

| Metric | Target | Environment |
|--------|--------|-------------|
| Map app initial render | < 5 sec | Ordinary AOI context |
| Section app base image render | < 8 sec | CPU-class deployment |
| Overlay toggle (cached) | < 2 sec | Cached layers |
| Overlay toggle (uncached) | < 10 sec | Fresh compute |
| QC run per ordinary image | < 5 sec | CPU-class deployment |

---

## Repo Maturity Metrics

| Metric | Target | Method |
|--------|--------|--------|
| Deterministic rerun consistency | > 99% | Same asset, params, version |
| Automated test coverage (schemas, routing, QC, audit) | > 80% | Coverage report |
| Zero backend app tools visible to model tool list | 100% | Tool audit |
| Version-pinned FastMCP and major deps | Yes | Lock file + CI |

---

## App-by-App Success Criteria

### Map App

**Must Render:**
- [ ] Basemap
- [ ] Basin/AOI features
- [ ] Seismic lines
- [ ] Wells
- [ ] Linked asset drawer
- [ ] Scale bar and legend

**Success Metrics:**
| Metric | Target |
|--------|--------|
| Feature search accuracy | Acceptable for pilot dataset |
| Linked section open success rate | > 95% |
| Coordinate + feature metadata on 100% of selectable features | 100% |
| Snapshot export for selected context | Works |

---

### Cross-Section App

**Must Render:**
- [ ] Profile line
- [ ] Horizontal and vertical scales
- [ ] Unit polygons
- [ ] Borehole/well columns (if available)
- [ ] Faults
- [ ] Uncertainty zones
- [ ] Vertical exaggeration badge (if used)

**Must Disclose:**
- [ ] Datum and vertical exaggeration state (100%)
- [ ] Observed vs inferred areas (100%)

**888 HOLD Triggers:**
- [ ] Borehole spacing > 10km — continuity unreliable
- [ ] Unit correlation confidence < 0.6
- [ ] VE > 2x but not disclosed
- [ ] Fault geometry not seismic-constrained
- [ ] Pinchout/truncation in interpreted zone
- [ ] Zero well control in interval of interest

---

### Seismic Section App

**Must Render:**
- [ ] Seismic image
- [ ] Axis labels and units
- [ ] Legend/display badge
- [ ] QC badges
- [ ] Reflector/fault/facies overlays
- [ ] Insight panel

**Success Metrics:**
| Metric | Target |
|--------|--------|
| QC catches contaminated images | Above agreed threshold |
| Images with unknown scale disable measurement tools | 100% |
| ROI analysis returns bounded hypotheses | Not freeform speculation |
| Overlay usefulness rating | > 70% pilot set |

---

## IO/State Success Criteria

**One canonical ingress-egress model** — host model differences must not change core behavior.

| Requirement | Target |
|-------------|--------|
| All model-visible tools accept normalized intent envelopes | 100% |
| All app/backend tools emit standard JSON envelope | 100% |
| All rendered views originate from canonical display state | 100% |
| Integration tests confirm stable schema validation | > 95% |

**ToolOutputEnvelope Contract:**
```python
{
    "success": bool,
    "state_delta": dict,
    "structuredContent": dict,
    "text_summary": str,
    "warnings": list[str],
    "hold_status": HoldStatus,
    "tool_name": str,
    "execution_time_ms": float | None
}
```

---

## Benchmark Packs

### Map Pack
- [ ] Basins, lines, wells, AOIs
- [ ] ≥ 20 representative cases
- [ ] Expected QC result per case
- [ ] Expected hold/no-hold result per case
- [ ] Expected minimum metadata per case

### Cross Section Pack
- [ ] Profiles, wells, tops, faults, uncertainty examples
- [ ] ≥ 20 representative cases
- [ ] Expected QC result per case
- [ ] Expected hold/no-hold result per case
- [ ] Expected minimum metadata per case

### Seismic Image Pack
- [ ] Clean, noisy, annotated, scale-unknown images
- [ ] ≥ 20 representative cases
- [ ] Expected QC result per case
- [ ] Expected hold/no-hold result per case
- [ ] Expected minimum metadata per case

---

## Delivery Milestones

| Milestone | Contents | Definition of Done |
|-----------|----------|-------------------|
| **M1** | Canonical schemas + shared registry + health + pinned deps | Schemas validate, health check works, deps locked |
| **M2** | Map app functional with asset linking | Can search, select, open linked sections |
| **M3** | Seismic section app with QC + base overlays | Image loads, QC runs, overlays render |
| **M4** | Cross-section app with uncertainty | Profile renders, observed/inferred distinguished, HOLD works |
| **M5** | Reasoning + audit + memory integrated | End-to-end with provenance chain |
| **M6** | Host compatibility + benchmark hardening | ≥2 hosts, benchmark packs >80% pass rate |

---

## North-Star KPI Set

| KPI | Initial Target | Long-Term Target |
|-----|---------------|------------------|
| **Workflow Completion Rate** | > 80% | > 95% |
| **Geologist Utility Rating** | > 4.0/5 | > 4.5/5 |
| **Governance Compliance Rate** | 100% mandatory fields + hold | 100% all fields |
| **Structured Render Success Rate** | > 95% supported hosts | > 99% |
| **Same-Input Determinism** | > 99% | > 99.9% |
| **Host Portability Score** | Validated in 2 MCP clients | Validated in 4+ clients |

---

## What "Not Success" Looks Like

- [ ] GEOX depends on one LLM vendor's vision behavior
- [ ] UI renders but lacks scale, legend, or uncertainty
- [ ] Geological claims exceed image/control evidence
- [ ] Cross sections present inferred geology as fact
- [ ] Tools are monolithic and non-deterministic
- [ ] Model-visible tool list is cluttered with backend internals

---

## Strategic Status

> **CLAIM:** GEOX should be considered a **forgable systems architecture with strong strategic direction but incomplete execution**, not yet a finished product.

> **CLAIM:** The immediate objective is not bigger model complexity; it is sharper architecture, canonical schemas, app/tool separation, benchmark packs, and governance-hardening.

> **CLAIM:** If you hit the metrics above, GEOX becomes a serious open geoscience MCP platform, even before SEG-Y enters the picture.

---

## Anti-Patterns to Avoid

| Anti-Pattern | Why It Fails |
|--------------|--------------|
| Pass raw screenshot to LLM and trust prose | Fragile, non-reproducible |
| Let LLM invent axis labels or legends | Violates F4 Clarity |
| Let provider vision decide fault existence | Violates F2 Truth |
| Couple UI state to one vendor's JSON format | Violates Host Portability |
| Build Petrel clone with AI | Wrong battle, too large |
| Skip uncertainty disclosure | Violates F7 Humility |

---

## Architectural Guards

| Guard | Implementation |
|-------|---------------|
| GEOX owns visual semantics, not LLM | GeoXDisplayState → UI render |
| LLM handles intent, GEOX handles execution | GeoXIntent → Tool call |
| Vision models are optional adapters | VisionAdapterLayer with normalized output |
| All tools emit ToolOutputEnvelope | Envelope pattern enforced |
| Cross Section ≠ Seismic Section | Separate state types, different confidence semantics |
| Observed vs Inferred always distinguished | `is_observed: bool` on all features |

---

*Ditempa Bukan Diberi* [ΔΩΨ | 888 | 999]
*Document Version: v0.4.1*
*Last Updated: April 1, 2026*
*Status: FORGE-READY | 999 SEAL PENDING