---
name: ai-memory
description: AI gateway + vector memory + thermo-ops safety — OpenClaw, Qdrant, BGE embeddings, 888_HOLD gates
---

# ai-memory

## Scope
Consolidated AI layer — AI gateway (OpenClaw), vector memory (Qdrant + BGE embeddings), and thermodynamic safety operations (888_HOLD gates).

**Merged from:** `ai-gateway` + `memory-vectors` + `thermo-ops`

## Constitutional Alignment
| Floor | Role | Threshold |
|-------|------|-----------|
| F1 | Amanah | LOCKED (888_HOLD gates) |
| F4 | Clarity | ΔS ≤ 0 (embedding quality) |
| F7 | Humility | Ω₀ ∈ [0.03, 0.05] |
| F8 | Genius | G ≥ 0.80 (model selection) |
| F13 | Sovereign | HUMAN (final approval) |

## Key Components
- **AI Gateway**: OpenClaw model routing, load balancing, MCP integration
- **Vector Memory**: Qdrant collection, BGE embeddings, semantic search
- **Thermo-Ops**: 888_HOLD safety gates, risk classification, F1 Amanah enforcement
- **Embeddings**: BGE-M3 or BGE-large for semantic encoding

## Backend Path
- `aclip_cai/embeddings/bge_embedder.py`
- `aaa_mcp/external_gateways/` — OpenClaw, Ollama clients
- Safety: `core/shared/guards.py`, `core/kernel/constitutional_decorator.py`

## Operational Rules

**Trigger When:**
- Vector memory search/recall needed
- AI model routing/gateway operations
- Dangerous operation requiring 888_HOLD
- Risk tier classification
- Thermodynamic calculations

**Allowed Operations:**
- Semantic search via BGE embeddings
- Model routing through OpenClaw gateway
- Memory band assignment (L0-L5)
- Risk classification (LOW/MODERATE/CRITICAL)
- 888_HOLD gate enforcement

**888_HOLD Required:**
- **DANGEROUS**: rm -rf, mkfs, dd, etc.
- **DATABASE**: migrations, production schema changes
- **DEPLOYMENT**: production releases
- **CREDENTIALS**: secret handling, key exposure
- **MASS OPS**: >10 files or containers
- **CONFLICTING EVIDENCE**: across source tiers

## Memory Bands
| Band | Duration | Use Case |
|------|----------|----------|
| L0 (Hot) | 0-24h | Active sessions |
| L1 (Warm) | 24-72h | Recent context |
| L2 (Phoenix) | 72h-7d | Cooling decisions |
| L3 (Cool) | 7-30d | Historical reference |
| L4 (Cold) | 30-365d | Archive |
| L5 (Eternal) | 365d+ | Constitutional law |

## Quick Reference
```python
# Vector memory recall
from aclip_cai.embeddings.bge_embedder import recall_context
results = await recall_context(query_vector, top_k=5)

# AI Gateway
from aaa_mcp.external_gateways.openclaw_client import route_request
response = await route_request(model="claude", query=prompt)

# Risk classification
from core.shared.guards import classify_risk
tier = classify_risk("deploy", scope="production")
```

## Verification
```bash
# Check Qdrant
curl http://localhost:6333/collections

# Check embeddings
python -c "from aclip_cai.embeddings.bge_embedder import BGEEmbedder; print('BGE ready')"
```
