# UNIFIED SOUL SCHEMA SPECIFICATION
**Version:** SOUL_SCHEMA_V1
**Date:** 2026-03-31
**Authority:** Arif Fazil — 888 Judge

---

## PURPOSE

This document defines the **Unified Soul Schema** — a complete identity + behavioral profile for each AI model in the arifOS registry.

The soul is embedded during `init_anchor` so the AI knows:
1. **WHO IT IS** (identity from model spec)
2. **HOW IT THINKS** (reasoning style)
3. **HOW IT COMMUNICATES** (communication style)
4. **WHAT IT'S GOOD AT** (best fit roles)
5. **WHAT TO AVOID** (worst fit roles)

---

## TWO SOURCES → ONE SOUL

| Source | Location | Contains |
|--------|----------|----------|
| **Model Spec** | `models/<provider>/<family>/<variant>.json` | Identity + `soul_archetype` |
| **Soul Profile** | `provider_souls/<provider>_<family>.json` | Behavioral + `soul_label` |

**Binding Key:** `soul_archetype` (from model) = `soul_label` (from soul)

---

## UNIFIED SOUL SCHEMA (V1)

```json
{
  "schema_version": "SOUL_SCHEMA_V1",
  "generated_at": "ISO8601_TIMESTAMP",
  "source": {
    "model_spec": "models/<provider>/<family>/<variant>.json",
    "soul_profile": "provider_souls/<provider>_<family>.json",
    "merged_by": "soul_pipeline.py"
  },

  "identity": {
    "provider": "string (e.g., 'openai')",
    "family": "string (e.g., 'gpt')",
    "variant": "string (e.g., 'gpt-4')",
    "soul_archetype": "string — THE BINDING KEY"
  },

  "identity_integrity": {
    "self_claim_boundary": "verified_only | unverified_allowed",
    "trust_tier": "verified | untrusted | mood_matched",
    "claim_matches": "boolean"
  },

  "description": {
    "one_line": "string — terse description",
    "full": "string — detailed description"
  },

  "communication_style": {
    "traits": ["array of strings"],
    "structure": "prose_first | structured | direct | conversational",
    "tone": "formal | casual | scholarly | blunt"
  },

  "reasoning_style": {
    "approach": ["array of strings"],
    "depth": "shallow | medium | deep",
    "speed": "fast | medium | deliberative",
    "caution": "bold | balanced | cautious"
  },

  "roles": {
    "best_fit": ["array of role strings"],
    "worst_fit": ["array of role strings"],
    "default": "string — primary role"
  },

  "usage_guidance": {
    "when_to_use": "string",
    "when_not_to_use": "string",
    "context_considerations": "string"
  },

  "differentiation": {
    "context_handling": "string",
    "truth_vs_speed": "string",
    "cultural_anchor": "string",
    "product_vs_model": "string"
  },

  "constitutional_fit": {
    "f2_truth_tendency": "high | medium | low",
    "f5_empathy_strength": "high | medium | low",
    "f7_humility_profile": "confident | balanced | uncertain",
    "f9_anti_hantu_score": "0.0 - 1.0"
  }
}
```

---

## FIELD MAPPING

### From Model Spec:
| Model Field | → | Unified Soul Field |
|-------------|---|---------------------|
| provider | → | identity.provider |
| model_family | → | identity.family |
| model_variant | → | identity.variant |
| soul_archetype | → | identity.soul_archetype |
| identity_integrity | → | identity_integrity |
| runtime_class | → | (stored, used for routing) |

### From Soul Profile:
| Soul Field | → | Unified Soul Field |
|------------|---|-------------------|
| soul_label | → | (checked against soul_archetype) |
| in_one_sentence | → | description.one_line |
| description | → | description.full |
| communication_style | → | communication_style.traits |
| reasoning_style | → | reasoning_style.approach |
| best_fit_roles | → | roles.best_fit |
| worst_fit_roles | → | roles.worst_fit |
| when_to_use | → | usage_guidance.when_to_use |
| when_not_to_use | → | usage_guidance.when_not_to_use |
| key_differentiators.context_handling | → | differentiation.context_handling |
| key_differentiators.truth_vs_speed | → | differentiation.truth_vs_speed |
| key_differentiators.cultural_anchor | → | differentiation.cultural_anchor |
| key_differentiators.product_vs_model | → | differentiation.product_vs_model |

---

## VALIDATION RULES

1. **soul_archetype MUST equal soul_label** (for successful binding)
2. **All 17+ models MUST have complete unified souls**
3. **soul_archetype must be unique** (no two models share same archetype)
4. **best_fit_roles and worst_fit_roles must not overlap**

---

## MISMATCH RESOLUTION

For the 2 currently mismatched souls:

| Model | soul_archetype | Soul soul_label | Resolution |
|-------|---------------|-----------------|------------|
| microsoft/copilot/copilot-enterprise | `microsoft_copilot` | `ecosystem_native_architect` | **KEEP archetype as canonical** — arch is more specific |
| perplexity/perplexity/perplexity-pro | `perplexity_ai` | `search_grounded_synthesizer` | **KEEP archetype as canonical** — arch is brand identifier |

**Rationale:** `soul_archetype` from model spec is the authoritative binding key. `soul_label` is human-readable but secondary.

---

## OUTPUT LOCATIONS

| Stage | Location |
|-------|----------|
| Source (read) | `arifOS-model-registry/models/` and `provider_souls/` |
| Merged Output | `arifOS-model-registry/souls_merged/` |
| Verified + Deployed | `arifOS-model-registry/provider_souls/` (updated) |
| Embedded in arifosmcp | `arifOS/arifosmcp/init_000/seeds/provider_soul_profiles.json` |

---

## VALIDATION CHECKLIST

After merge, verify for each model:

- [ ] `soul_archetype` matches between model and soul
- [ ] `identity.provider`, `family`, `variant` populated
- [ ] `description.one_line` exists
- [ ] `communication_style.traits` has 2+ items
- [ ] `reasoning_style.approach` has 2+ items
- [ ] `roles.best_fit` has 2+ items
- [ ] `roles.worst_fit` has 1+ items
- [ ] `usage_guidance.when_to_use` exists
- [ ] `differentiation` has all 4 sub-fields

---

**SEAL: This schema is binding for all Model Soul operations in arifOS**
