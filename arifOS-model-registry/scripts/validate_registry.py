#!/usr/bin/env python3
"""
Registry Validation Script
Low-risk, high-reward: Catches inconsistencies before they break init_anchor.
"""

import json
import os
import sys
from pathlib import Path

def load_json(path):
    """Load JSON file with proper encoding."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def validate_provider_soul(file_path):
    """Validate a single provider soul file."""
    errors = []
    data = load_json(file_path)
    filename = Path(file_path).stem
    
    # Skip validation for test fixtures (files starting with 'wrong_')
    if filename.startswith("wrong_"):
        return []
    
    # Required fields
    required = ["provider_key", "family_key", "soul_label"]
    for field in required:
        if field not in data:
            errors.append(f"Missing required field: {field}")
    
    # Check provider_key doesn't contain underscore (should be clean)
    provider_key = data.get("provider_key", "")
    if "_" in provider_key:
        errors.append(f"Provider key '{provider_key}' contains underscore")
    
    # Check arrays are actually arrays
    array_fields = ["communication_style", "reasoning_style", "default_role_fit", "avoid_role"]
    for field in array_fields:
        if field in data and not isinstance(data[field], list):
            errors.append(f"Field '{field}' should be an array")
    
    return errors

def validate_catalog():
    """Validate catalog.json matches provider_souls/*.json."""
    errors = []
    
    registry_dir = Path(__file__).parent.parent
    souls_dir = registry_dir / "provider_souls"
    catalog_path = registry_dir / "catalog.json"
    
    # Load catalog
    catalog = load_json(catalog_path)
    catalog_archetypes = set(catalog.get("soul_archetypes", []))
    
    # Get actual files
    actual_files = set()
    for f in souls_dir.glob("*.json"):
        actual_files.add(f.stem)
    
    # Check for mismatches
    in_catalog_not_files = catalog_archetypes - actual_files
    in_files_not_catalog = actual_files - catalog_archetypes
    
    if in_catalog_not_files:
        errors.append(f"In catalog but no file: {in_catalog_not_files}")
    if in_files_not_catalog:
        errors.append(f"Has file but not in catalog: {in_files_not_catalog}")
    
    return errors, catalog

def validate_simplified_registry():
    """Check simplified registry has all providers."""
    errors = []
    
    registry_dir = Path(__file__).parent.parent
    simplified_path = registry_dir.parent / "arifosmcp" / "data" / "MODEL_REGISTRY.json"
    
    if not simplified_path.exists():
        errors.append(f"Simplified registry not found: {simplified_path}")
        return errors
    
    simplified = load_json(simplified_path)
    models = simplified.get("models", {})
    
    # Expected providers (from comprehensive registry)
    expected_providers = {
        "openai", "anthropic", "google", "xai", "deepseek", 
        "mistral", "alibaba", "meta", "cohere", "moonshot", "minimax"
    }
    
    # Extract providers from simplified registry
    actual_providers = set()
    for model_id in models:
        if model_id.startswith("_"):
            continue
        parts = model_id.split("/")
        if len(parts) >= 1:
            actual_providers.add(parts[0])
    
    missing = expected_providers - actual_providers
    if missing:
        errors.append(f"Simplified registry missing providers: {missing}")
    
    return errors

def main():
    """Run all validations."""
    registry_dir = Path(__file__).parent.parent
    souls_dir = registry_dir / "provider_souls"
    
    all_errors = []
    
    print("🔍 Validating arifOS Model Registry...\n")
    
    # Validate each provider soul
    print("1. Checking provider_souls/*.json files...")
    for soul_file in sorted(souls_dir.glob("*.json")):
        errors = validate_provider_soul(soul_file)
        if errors:
            all_errors.append(f"\n❌ {soul_file.name}:")
            for err in errors:
                all_errors.append(f"   - {err}")
        else:
            print(f"   ✅ {soul_file.name}")
    
    # Validate catalog
    print("\n2. Checking catalog.json consistency...")
    errors, catalog = validate_catalog()
    if errors:
        all_errors.append(f"\n❌ catalog.json:")
        for err in errors:
            all_errors.append(f"   - {err}")
    else:
        count = len(catalog.get('soul_archetypes', []))
        print(f"   ✅ catalog.json matches provider_souls/ ({count} archetypes)")
    
    # Validate simplified registry
    print("\n3. Checking simplified registry...")
    errors = validate_simplified_registry()
    if errors:
        all_errors.append(f"\n❌ Simplified registry:")
        for err in errors:
            all_errors.append(f"   - {err}")
    else:
        print(f"   ✅ Simplified registry has all providers")
    
    # Summary
    print("\n" + "="*50)
    if all_errors:
        error_count = len([e for e in all_errors if e.startswith(chr(10))])
        print(f"❌ VALIDATION FAILED: {error_count} files with errors")
        for err in all_errors:
            print(err)
        return 1
    else:
        print("✅ ALL VALIDATIONS PASSED")
        simplified = load_json(registry_dir.parent / "arifosmcp" / "data" / "MODEL_REGISTRY.json")
        print(f"   - {len(list(souls_dir.glob('*.json')))} provider souls")
        print(f"   - {len(catalog.get('soul_archetypes', []))} archetypes")
        print(f"   - {len(simplified.get('models', {}))} models")
        return 0

if __name__ == "__main__":
    sys.exit(main())
