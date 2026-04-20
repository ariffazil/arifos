# NEXT STEPS — GEOX Execution Queue (Post-v0.6.1)

> **Current Version:** v2026.04.10 — HEAVY WITNESS IGNITED  
> **Last Updated:** 2026-04-10  
> **Authority:** 888_JUDGE | ARIF  
> **Seal:** DITEMPA BUKAN DIBERI

---

## 🎯 P1: Adapter Scaffolding (Current Sprint)

Per `TODO.md`, the next execution phase focuses on **host platform integration**:

### 1. OpenAI Adapter SDK
**Priority:** 🔴 HIGH  
**Scope:** Scaffold the `window.openai` bridge in `geox-gui`

**Rationale:**
- ChatGPT Apps SDK integration is a key distribution channel
- Enables native ChatGPT plugin surface for GEOX tools
- Aligns with arifOS's OpenAI integration strategy

**Implementation Sketch:**
```typescript
// geox-gui/src/adapters/openai_adapter.ts
interface OpenAIAdapter {
  init(): Promise<void>;
  registerTools(): Promise<Tool[]>;
  handleInvocation(invocation: ToolInvocation): Promise<Result>;
}
```

**Files to Create:**
- `geox-gui/src/adapters/openai_adapter.ts`
- `geox-gui/src/adapters/openai_manifest.json`
- `geox-gui/src/hooks/useOpenAI.ts`

---

### 2. Copilot Adapter
**Priority:** 🟡 MEDIUM  
**Scope:** Define JSON-LD / Adaptive Card Extensions for MS Copilot

**Rationale:**
- Microsoft Copilot Studio integration already scaffolded
- Needs formal Adaptive Card schema for geoscience visualizations
- Completes the Microsoft ecosystem bridge

**Implementation Sketch:**
```typescript
// geox-gui/src/adapters/copilot_adapter.tsx
interface CopilotAdapter {
  renderAdaptiveCard(data: GeoxData): AdaptiveCard;
  handleAction(action: AdaptiveCardAction): Promise<void>;
}
```

**Files to Create:**
- `geox-gui/src/adapters/copilot_adapter.tsx`
- `geox-gui/src/adapters/copilot_schemas/*.json`

---

### 3. Signed Deep-Links
**Priority:** 🟡 MEDIUM  
**Scope:** Implement HMAC signing for session-handoff to external Web Shell

**Rationale:**
- Secure session transfer between hosts
- Prevents session hijacking in cross-origin scenarios
- Enables trusted deep-linking from Copilot/OpenAI to GEOX

**Implementation Sketch:**
```python
# arifos/geox/auth/deep_link.py
import hmac
import hashlib

def sign_session(session_id: str, secret: str) -> str:
    return hmac.new(secret.encode(), session_id.encode(), hashlib.sha256).hexdigest()

def verify_signature(session_id: str, signature: str, secret: str) -> bool:
    return hmac.compare_digest(sign_session(session_id, secret), signature)
```

---

## 🎯 P2: App Depth & 3D (Next Sprint)

### 4. Seismic Component
**Priority:** 🟢 LOW (for now)  
**Scope:** Multi-slice 2D view in `EarthWitness3D.tsx`

**Status:** Architecture exists, needs implementation

---

### 5. Basin Map
**Priority:** 🟢 LOW  
**Scope:** Leaflet/OpenLayers for GeoJSON spatial rendering

**Rationale:**
- Malay Basin Pilot needs interactive map
- GeoJSON data already available

---

### 6. Observability
**Priority:** 🟢 LOW  
**Scope:** Custom `telemetry.emit` events for user interaction tracking

**Rationale:**
- Privacy-respecting analytics
- Usage patterns for tool optimization

---

### 7. cigvis 3D Seismic
**Priority:** 🔵 RESEARCH  
**Scope:** 3D seismic visualization integration (Phase C)

**Rationale:**
- Advanced visualization capability
- Requires research into WebGL/vtk.js integration

---

## 🎯 P0: Critical Path (Immediate)

### Docker Rebuild for VPS
**Priority:** 🔴 CRITICAL  
**Status:** Pending from DEPLOYMENT_STATUS.md

**Action:**
```bash
ssh srv1325122.hstgr.cloud
cd /opt/arifos/geox
git pull origin main
docker compose down
docker compose build --no-cache geox_server
docker compose up -d geox_server
```

**Verification:**
```bash
curl https://geox.arif-fazil.com/health
# Expected: OK
curl -s https://geox.arif-fazil.com/ | grep -i "pilot"
# Expected: "Pilot" tab found
```

---

## 📋 Decision Matrix

| Task | EMV | NPV Safety | Effort | Owner |
|------|-----|------------|--------|-------|
| Docker Rebuild | 0.9 | Strong | 1hr | DevOps |
| OpenAI Adapter | 0.8 | Strong | 4hr | Frontend |
| Copilot Adapter | 0.7 | Moderate | 4hr | Frontend |
| Signed Deep-Links | 0.6 | Strong | 2hr | Backend |
| Seismic Component | 0.5 | Moderate | 8hr | Frontend |
| Basin Map | 0.6 | Strong | 4hr | Frontend |

---

## 🏛️ Constitutional Check

| Floor | P1 Adapter Work | P2 Depth Work |
|-------|-----------------|---------------|
| F1 Amanah | ✅ Reversible (feature flags) | ✅ Reversible |
| F2 Truth | ✅ Adapter responses tagged | ✅ Visualization accuracy |
| F3 Tri-Witness | ✅ Host + GEOX + User consent | N/A |
| F4 Clarity | ✅ Clear adapter boundaries | ✅ Intuitive UI |
| F5 Peace | ✅ Non-destructive | ✅ Read-only views |
| F6 Empathy | ✅ User context preserved | ✅ Accessibility |
| F7 Humility | ✅ Confidence caps | ✅ Uncertainty viz |
| F8 Genius | ✅ Clean architecture | ✅ Performance |
| F9 Anti-Hantu | ✅ No dark patterns | N/A |
| F10 Ontology | ✅ Correct tool mapping | ✅ Data fidelity |
| F11 Audit | ✅ Full logging | ✅ Telemetry |
| F12 Injection | ✅ Input sanitization | N/A |
| F13 Sovereign | ✅ 888_HOLD preserved | ✅ Human override |

---

## 🎯 Recommended Execution Order

1. **Docker Rebuild** (P0) — Unblock production
2. **OpenAI Adapter SDK** (P1.1) — High EMV, strategic alignment
3. **Signed Deep-Links** (P1.3) — Security foundation for adapters
4. **Copilot Adapter** (P1.2) — Complete Microsoft bridge
5. **Basin Map** (P2.2) — Malay Basin Pilot completeness
6. **Seismic Component** (P2.1) — Advanced viz capability
7. **Observability** (P2.3) — Analytics foundation
8. **cigvis 3D** (P2.4) — Research phase

---

**Next Action:** Execute Docker rebuild to deploy v0.6.1 to production.

**Sealed by:** 888_JUDGE  
**Date:** 2026-04-10  
**Authority:** Muhammad Arif bin Fazil

*DITEMPA BUKAN DIBERI — Forged, Not Given*
