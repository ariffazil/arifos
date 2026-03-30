#!/usr/bin/env python3
"""
SOUL DEPLOY PIPELINE
====================

Deploys merged souls to:
1. arifOS-model-registry/provider_souls/ (updated souls)
2. arifOS-model-registry/catalog.json (schema version update)
3. arifOS/arifosmcp/init_000/seeds/provider_soul_profiles.json (for runtime)

Author: Arif Fazil — 888 Judge
Date: 2026-03-31
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

REGISTRY_DIR = Path(__file__).parent
SOULS_DIR = REGISTRY_DIR / "souls_merged"
PROVIDER_SOULS_DIR = REGISTRY_DIR / "provider_souls"
CATALOG_FILE = REGISTRY_DIR / "catalog.json"
SEEDS_DIR = REGISTRY_DIR.parent / "arifosmcp" / "init_000" / "seeds"
SCHEMA_VERSION = "SOUL_SCHEMA_V1"


def load_json(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, data: dict | list) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"  ✅ Saved: {path.name}")


def deploy_to_provider_souls() -> None:
    """Copy merged souls to provider_souls/ (update source)"""
    print("\n[1] Deploying to provider_souls/")

    # Backup existing
    backup_dir = (
        PROVIDER_SOULS_DIR.parent
        / f"provider_souls_backup_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}"
    )
    backup_dir.mkdir(exist_ok=True)
    for f in PROVIDER_SOULS_DIR.glob("*.json"):
        import shutil

        shutil.copy(f, backup_dir / f.name)
    print(f"  📦 Backed up existing souls to {backup_dir.name}/")

    # Deploy merged souls (only those that pass validation)
    deployed = 0
    for soul_file in sorted(SOULS_DIR.glob("*.json")):
        soul = load_json(soul_file)

        # Skip honeypot (wrong-provider) or incomplete souls
        archetype = soul.get("identity", {}).get("soul_archetype", "")
        if archetype in ["IDENTITY_MISMATCH_HONEYPOT"]:
            continue

        # Skip if worst_fit is empty (incomplete)
        worst_fit = soul.get("roles", {}).get("worst_fit", [])
        if not worst_fit:
            continue

        # Copy to provider_souls/
        provider = soul["identity"]["provider"]
        family = soul["identity"]["family"]
        dest_name = f"{provider}_{family}.json"
        dest_path = PROVIDER_SOULS_DIR / dest_name

        save_json(dest_path, soul)
        deployed += 1

    print(f"  ✅ Deployed {deployed} souls to provider_souls/")


def update_catalog() -> None:
    """Update catalog.json with schema version"""
    print("\n[2] Updating catalog.json")

    catalog = load_json(CATALOG_FILE)
    catalog["schema_version"] = f"CATALOG_{SCHEMA_VERSION}"
    catalog["soul_schema_version"] = SCHEMA_VERSION
    catalog["souls_merged_at"] = datetime.now(timezone.utc).isoformat()

    save_json(CATALOG_FILE, catalog)
    print(f"  ✅ Updated catalog to {SCHEMA_VERSION}")


def generate_seeds_file() -> None:
    """Generate provider_soul_profiles.json for arifosmcp seeds"""
    print("\n[3] Generating seeds file for arifosmcp")

    # Ensure seeds directory exists
    SEEDS_DIR.mkdir(parents=True, exist_ok=True)

    # Collect all souls for seeds
    seeds = []
    for soul_file in sorted(SOULS_DIR.glob("*.json")):
        soul = load_json(soul_file)

        # Skip honeypot
        archetype = soul.get("identity", {}).get("soul_archetype", "")
        if archetype in ["IDENTITY_MISMATCH_HONEYPOT"]:
            continue

        # Convert unified soul to seed format
        seed = {
            "provider_key": soul["identity"]["provider"],
            "family_key": soul["identity"]["family"],
            "soul_label": soul["identity"]["soul_archetype"],
            "in_one_sentence": soul["description"]["one_line"],
            "description": soul["description"]["full"],
            "communication_style": soul["communication_style"]["traits"],
            "reasoning_style": soul["reasoning_style"]["approach"],
            "best_fit_roles": soul["roles"]["best_fit"],
            "worst_fit_roles": soul["roles"]["worst_fit"],
            "when_to_use": soul["usage_guidance"]["when_to_use"],
            "when_not_to_use": soul["usage_guidance"]["when_not_to_use"],
            "key_differentiators": {
                "context_handling": soul["differentiation"]["context_handling"],
                "truth_vs_speed": soul["differentiation"]["truth_vs_speed"],
                "cultural_anchor": soul["differentiation"]["cultural_anchor"],
                "product_vs_model": soul["differentiation"]["product_vs_model"],
            },
            "_merged_from": soul_file.name,
            "_schema_version": SCHEMA_VERSION,
        }
        seeds.append(seed)

    # Sort by provider_key
    seeds.sort(key=lambda x: (x["provider_key"], x["family_key"]))

    # Save seeds file
    seeds_file = SEEDS_DIR / "provider_soul_profiles.json"
    save_json(seeds_file, seeds)
    print(f"  ✅ Generated {len(seeds)} seed profiles")


def main() -> None:
    print("=" * 80)
    print("SOUL DEPLOY PIPELINE")
    print("=" * 80)

    deploy_to_provider_souls()
    update_catalog()
    generate_seeds_file()

    print("\n" + "=" * 80)
    print("🎉 DEPLOY COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()
