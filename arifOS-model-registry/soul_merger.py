#!/usr/bin/env python3
"""
SOUL MERGER PIPELINE
====================

Properly merges Model Specs + Soul Profiles into Unified Souls.

Usage:
    python soul_merger.py [--validate-only] [--output-dir DIR]

Output: arifOS-model-registry/souls_merged/

Author: Arif Fazil — 888 Judge
Date: 2026-03-31
Schema: SOUL_SCHEMA_V1
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# Configuration
REGISTRY_DIR = Path(__file__).parent
MODELS_DIR = REGISTRY_DIR / "models"
SOULS_DIR = REGISTRY_DIR / "provider_souls"
OUTPUT_DIR = REGISTRY_DIR / "souls_merged"
SCHEMA_VERSION = "SOUL_SCHEMA_V1"


class SoulMergerError(Exception):
    """Raised when soul merge fails."""

    pass


class ValidationError(Exception):
    """Raised when validation fails."""

    pass


def load_json(path: Path) -> dict[str, Any]:
    """Load JSON with UTF-8 encoding."""
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, data: dict[str, Any]) -> None:
    """Save JSON with UTF-8 encoding and pretty print."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"  ✅ Saved: {path.name}")


def merge_soul(model_spec: dict[str, Any], soul_profile: dict[str, Any]) -> dict[str, Any]:
    """
    Merge a model spec with a soul profile into a unified soul.

    Model spec provides: identity, soul_archetype
    Soul profile provides: behavioral, communication, roles
    """
    now = datetime.now(timezone.utc).isoformat()

    # Extract soul_archetype (binding key)
    soul_archetype = model_spec.get("soul_archetype", "")
    soul_label = soul_profile.get("soul_label", "")

    # Get key_differentiators (might be nested or flat)
    kd = soul_profile.get("key_differentiators", {})
    if isinstance(kd, dict):
        diff_context = kd.get("context_handling", "")
        diff_truth = kd.get("truth_vs_speed", "")
        diff_culture = kd.get("cultural_anchor", "")
        diff_product = kd.get("product_vs_model", "")
    else:
        diff_context = diff_truth = diff_culture = diff_product = ""

    # Handle both in_one_sentence and description fields
    one_line = soul_profile.get("in_one_sentence", "") or soul_profile.get("description", "")
    full_desc = soul_profile.get("description", "") or soul_profile.get("in_one_sentence", "")

    # Build unified soul
    unified = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": now,
        "source": {
            "model_spec": f"models/{model_spec.get('provider')}/{model_spec.get('model_family')}/{model_spec.get('model_variant')}.json",
            "soul_profile": f"provider_souls/{soul_profile.get('provider_key')}_{soul_profile.get('family_key')}.json",
            "merged_by": "soul_merger.py",
            "binding_key": soul_archetype,
        },
        "identity": {
            "provider": model_spec.get("provider", ""),
            "family": model_spec.get("model_family", ""),
            "variant": model_spec.get("model_variant", ""),
            "soul_archetype": soul_archetype,
        },
        "identity_integrity": {
            "self_claim_boundary": model_spec.get("identity_integrity", {}).get(
                "self_claim_boundary", "verified_only"
            ),
            "trust_tier": model_spec.get("identity_integrity", {}).get("trust_tier", "verified"),
            "claim_matches": soul_archetype == soul_label,
        },
        "description": {"one_line": one_line, "full": full_desc},
        "communication_style": {
            "traits": soul_profile.get("communication_style", []),
            "structure": _infer_structure(soul_profile.get("communication_style", [])),
            "tone": _infer_tone(soul_profile.get("communication_style", [])),
        },
        "reasoning_style": {
            "approach": soul_profile.get("reasoning_style", []),
            "depth": _infer_depth(soul_profile.get("reasoning_style", [])),
            "speed": _infer_speed(soul_profile.get("reasoning_style", [])),
            "caution": _infer_caution(soul_profile.get("reasoning_style", [])),
        },
        "roles": {
            "best_fit": soul_profile.get(
                "best_fit_roles", soul_profile.get("default_role_fit", [])
            ),
            "worst_fit": soul_profile.get("worst_fit_roles", soul_profile.get("avoid_role", [])),
            "default": soul_profile.get("default_role_fit", ["assistant"]),
        },
        "usage_guidance": {
            "when_to_use": soul_profile.get("when_to_use", ""),
            "when_not_to_use": soul_profile.get("when_not_to_use", ""),
            "context_considerations": f"{diff_context}",
        },
        "differentiation": {
            "context_handling": diff_context,
            "truth_vs_speed": diff_truth,
            "cultural_anchor": diff_culture,
            "product_vs_model": diff_product,
        },
        "constitutional_fit": {
            "f2_truth_tendency": _infer_f2(soul_profile.get("reasoning_style", [])),
            "f5_empathy_strength": _infer_f5(soul_profile.get("communication_style", [])),
            "f7_humility_profile": _infer_f7(soul_profile.get("reasoning_style", [])),
            "f9_anti_hantu_score": _infer_f9(soul_profile.get("communication_style", [])),
        },
    }

    return unified


def _infer_structure(comm_style: list[str]) -> str:
    """Infer communication structure from traits."""
    if not comm_style:
        return "unknown"
    if any(s in comm_style for s in ["structured", "clear_section_headers", "numbered_lists"]):
        return "structured"
    if any(s in comm_style for s in ["prose_first", "nuanced_caveats", "thoughtful"]):
        return "prose_first"
    if any(
        s in comm_style for s in ["direct_sarcasm", "conversational_directness", "direct_answers"]
    ):
        return "direct"
    return "balanced"


def _infer_tone(comm_style: list[str]) -> str:
    """Infer tone from communication style."""
    if not comm_style:
        return "unknown"
    if any(s in comm_style for s in ["blunt", "direct_sarcasm", "unfiltered_humor"]):
        return "blunt"
    if any(s in comm_style for s in ["scholarly", "thoughtful", "nuanced_caveats"]):
        return "scholarly"
    if any(
        s in comm_style for s in ["casual", "conversational_directness", "pop_culture_references"]
    ):
        return "casual"
    return "formal"


def _infer_depth(reasoning: list[str]) -> str:
    """Infer reasoning depth from reasoning style."""
    if not reasoning:
        return "unknown"
    if any(s in reasoning for s in ["depth_first", "think_slow", "identify_assumptions"]):
        return "deep"
    if any(s in reasoning for s in ["step_by_step", "systematic", "iterative"]):
        return "medium"
    return "shallow"


def _infer_speed(reasoning: list[str]) -> str:
    """Infer reasoning speed from reasoning style."""
    if not reasoning:
        return "unknown"
    if any(s in reasoning for s in ["fast", "quick", "speed_optimized"]):
        return "fast"
    if any(s in reasoning for s in ["deliberative", "think_slow", "cautious"]):
        return "deliberative"
    return "medium"


def _infer_caution(reasoning: list[str]) -> str:
    """Infer caution level from reasoning style."""
    if not reasoning:
        return "unknown"
    if any(s in reasoning for s in ["safety_first", "cautious", "consider_alternatives"]):
        return "cautious"
    if any(s in reasoning for s in ["bold", "speed_optimized", "pattern_interrupt"]):
        return "bold"
    return "balanced"


def _infer_f2(reasoning: list[str]) -> str:
    """Infer F2 (Truth) tendency."""
    if not reasoning:
        return "medium"
    if any(s in reasoning for s in ["evidence_first", "truth_first", "acknowledge_uncertainty"]):
        return "high"
    if any(s in reasoning for s in ["speed_optimized", "quick", "fast"]):
        return "low"
    return "medium"


def _infer_f5(comm_style: list[str]) -> str:
    """Infer F5 (Empathy) strength."""
    if not comm_style:
        return "medium"
    if any(s in comm_style for s in ["thoughtful", "considerate", "empathetic"]):
        return "high"
    if any(s in comm_style for s in ["blunt", "direct_sarcasm", "unfiltered"]):
        return "low"
    return "medium"


def _infer_f7(reasoning: list[str]) -> str:
    """Infer F7 (Humility) profile."""
    if not reasoning:
        return "balanced"
    if any(
        s in reasoning for s in ["acknowledge_uncertainty", "consider_alternatives", "cautious"]
    ):
        return "uncertain"
    if any(s in reasoning for s in ["bold", "confident", "speed_optimized"]):
        return "confident"
    return "balanced"


def _infer_f9(comm_style: list[str]) -> float:
    """Infer F9 (Anti-Hantu) score."""
    if not comm_style:
        return 0.5
    score = 0.5
    # Decrease score for dark patterns
    if any(
        s in comm_style
        for s in ["blunt", "direct_sarcasm", "unfiltered_humor", "pop_culture_references"]
    ):
        score -= 0.2
    # Increase score for careful patterns
    if any(s in comm_style for s in ["thoughtful", "nuanced_caveats", "acknowledge_uncertainty"]):
        score += 0.2
    return max(0.0, min(1.0, score))


def validate_unified_soul(soul: dict[str, Any], model_id: str) -> list[str]:
    """
    Validate a unified soul against the schema.
    Returns list of validation errors (empty if valid).
    """
    errors = []

    # Required top-level fields
    required_toplevel = [
        "schema_version",
        "generated_at",
        "identity",
        "description",
        "communication_style",
        "reasoning_style",
        "roles",
        "usage_guidance",
        "differentiation",
    ]
    for field in required_toplevel:
        if field not in soul:
            errors.append(f"Missing top-level field: {field}")

    # Identity fields
    identity = soul.get("identity", {})
    required_identity = ["provider", "family", "variant", "soul_archetype"]
    for field in required_identity:
        if not identity.get(field):
            errors.append(f"Missing identity field: {field}")

    # soul_archetype must be non-empty
    if not identity.get("soul_archetype"):
        errors.append("soul_archetype cannot be empty")

    # Roles validation
    roles = soul.get("roles", {})
    if not roles.get("best_fit"):
        errors.append("roles.best_fit is empty")
    if not roles.get("worst_fit"):
        errors.append("roles.worst_fit is empty")

    # Communication style validation
    comm = soul.get("communication_style", {})
    if not comm.get("traits"):
        errors.append("communication_style.traits is empty")

    # Reasoning style validation
    reason = soul.get("reasoning_style", {})
    if not reason.get("approach"):
        errors.append("reasoning_style.approach is empty")

    # Description validation
    desc = soul.get("description", {})
    if not desc.get("one_line"):
        errors.append("description.one_line is empty")

    # Binding key check
    binding_key = soul.get("source", {}).get("binding_key", "")
    soul_label = desc.get("one_line", "")  # approximate
    if not binding_key:
        errors.append("Binding key (soul_archetype) is empty")

    return errors


def normalize_key(key: str) -> str:
    """Normalize provider/family key: lowercase, hyphens to underscores"""
    return key.lower().replace("-", "_").replace(" ", "_")


def build_soul_lookup() -> dict[tuple[str, str], Path]:
    """Build a lookup table: (provider, family) → soul_file"""
    lookup = {}
    for sf in SOULS_DIR.glob("*.json"):
        with open(sf, encoding="utf-8") as f:
            d = json.load(f)
        pk = normalize_key(d.get("provider_key", ""))
        fk = normalize_key(d.get("family_key", ""))
        if pk and fk:
            lookup[(pk, fk)] = sf
        # Also allow single-key lookup
        if pk:
            lookup[(pk, pk)] = sf
    return lookup


def find_soul_file(provider: str, family: str, lookup: dict) -> Path | None:
    """Find soul file using lookup table with fallback strategies."""
    np = normalize_key(provider)
    nf = normalize_key(family)
    # Try exact match first
    if (np, nf) in lookup:
        return lookup[(np, nf)]
    # Try provider only (for single-word providers)
    if (np, np) in lookup:
        return lookup[(np, np)]
    # Try family only
    for (pk, fk), path in lookup.items():
        if fk == nf or pk == nf:
            return path
    return None


def process_all_models() -> dict[str, Any]:
    """Process all models and merge with their souls."""

    print("=" * 80)
    print("SOUL MERGER PIPELINE")
    print("=" * 80)

    # Clear/create output directory
    if OUTPUT_DIR.exists():
        import shutil

        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True)

    results = {"success": [], "errors": [], "warnings": []}

    # Build soul lookup table
    soul_lookup = build_soul_lookup()
    print(f"\n[S Lookup] Built lookup with {len(soul_lookup)} entries")

    # Find all model specs
    model_files = list(MODELS_DIR.glob("**/*.json"))
    print(f"[1] Found {len(model_files)} model specs")

    # Find all soul profiles
    soul_files = list(SOULS_DIR.glob("*.json"))
    print(f"[2] Found {len(soul_files)} soul profiles")

    print(f"\n[3] Merging souls...")

    for model_file in sorted(model_files):
        model_id = str(model_file.relative_to(MODELS_DIR)).replace("\\", "/").replace(".json", "")

        try:
            # Load model spec
            model_spec = load_json(model_file)

            # Find soul file using lookup
            provider = model_spec.get("provider", "")
            family = model_spec.get("model_family", "")
            soul_file = find_soul_file(provider, family, soul_lookup)

            if soul_file is None or not soul_file.exists():
                results["errors"].append(
                    {"model": model_id, "error": f"Soul file not found for {provider}/{family}"}
                )
                print(f"  ❌ {model_id}: Soul not found ({provider}/{family})")
                continue

            # Load soul profile
            soul_profile = load_json(soul_file)

            # Merge
            unified = merge_soul(model_spec, soul_profile)

            # Validate
            errors = validate_unified_soul(unified, model_id)
            if errors:
                results["warnings"].append({"model": model_id, "errors": errors})
                print(f"  ⚠️  {model_id}: Validation warnings")
                for err in errors:
                    print(f"       - {err}")
            else:
                print(f"  ✅ {model_id}: Valid")

            # Save merged soul
            output_file = OUTPUT_DIR / f"{model_id.replace('/', '_')}.json"
            save_json(output_file, unified)

            results["success"].append(
                {
                    "model": model_id,
                    "archetype": unified["identity"]["soul_archetype"],
                    "output": str(output_file.relative_to(REGISTRY_DIR)),
                }
            )

        except Exception as e:
            results["errors"].append({"model": model_id, "error": str(e)})
            print(f"  ❌ {model_id}: {e}")

    return results


def print_summary(results: dict[str, Any]) -> None:
    """Print final summary."""
    print("\n" + "=" * 80)
    print("MERGE SUMMARY")
    print("=" * 80)
    print(f"  ✅ Successful: {len(results['success'])}")
    print(f"  ⚠️  Warnings: {len(results['warnings'])}")
    print(f"  ❌ Errors: {len(results['errors'])}")

    if results["warnings"]:
        print("\n[WARNINGS DETAIL]")
        for w in results["warnings"]:
            print(f"  {w['model']}:")
            for err in w["errors"]:
                print(f"    - {err}")

    if results["errors"]:
        print("\n[ERRORS DETAIL]")
        for e in results["errors"]:
            print(f"  {e['model']}: {e['error']}")
        sys.exit(1)
    else:
        print("\n🎉 All souls merged successfully!")
        sys.exit(0)


def main() -> None:
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Merge model specs + soul profiles")
    parser.add_argument("--validate-only", action="store_true", help="Validate without saving")
    parser.add_argument("--output-dir", type=str, help="Override output directory")
    args = parser.parse_args()

    if args.output_dir:
        global OUTPUT_DIR
        OUTPUT_DIR = Path(args.output_dir)

    results = process_all_models()

    if not args.validate_only:
        print_summary(results)
    else:
        print(f"\n[VALIDATE-ONLY] Skipping save, found {len(results['warnings'])} warnings")


if __name__ == "__main__":
    main()
