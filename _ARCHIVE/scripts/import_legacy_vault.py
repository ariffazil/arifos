#!/usr/bin/env python3
"""
Import legacy VAULT999 filesystem entries into PostgreSQL.

One-time migration script. Safe to re-run (idempotent via entry_hash uniqueness).

Usage:
    python scripts/import_legacy_vault.py --dry-run
    python scripts/import_legacy_vault.py --execute

Options:
    --dry-run    Show what would be imported, don't write
    --execute    Actually import to Postgres
    --verbose    Show detailed progress
"""

import argparse
import asyncio
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

# Add repo root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from codebase.vault.persistent_ledger import PersistentVaultLedger


LEGACY_PATHS = [
    "VAULT999/BBB_LEDGER/entries",
    "VAULT999/BBB_LEDGER/refusal_audit.jsonl",
    ".arifos/ledger.jsonl",
]


def parse_iso_timestamp(ts: str) -> datetime:
    """Parse various timestamp formats to datetime."""
    if ts.endswith('Z'):
        ts = ts[:-1] + '+00:00'
    try:
        return datetime.fromisoformat(ts)
    except ValueError:
        # Fallback to epoch if unparseable
        return datetime(2026, 1, 1)


def load_jsonl_entries(path: Path) -> List[Dict[str, Any]]:
    """Load entries from JSONL file."""
    entries = []
    if not path.exists():
        return entries
    
    with open(path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
                entry['_source_file'] = str(path)
                entry['_line_num'] = line_num
                entries.append(entry)
            except json.JSONDecodeError as e:
                print(f"  Warning: JSON parse error in {path}:{line_num}: {e}")
    
    return entries


def load_json_entries(path: Path) -> List[Dict[str, Any]]:
    """Load entries from individual JSON files in directory."""
    entries = []
    if not path.exists():
        return entries
    
    for json_file in path.glob("*.json"):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                entry = json.load(f)
                entry['_source_file'] = str(json_file)
                entries.append(entry)
        except (json.JSONDecodeError, IOError) as e:
            print(f"  Warning: Failed to read {json_file}: {e}")
    
    return entries


def normalize_entry(entry: Dict[str, Any]) -> Dict[str, Any]:
    """Convert legacy entry format to standardized format for import."""
    
    # Handle various timestamp formats
    ts = entry.get('timestamp') or entry.get('created_at') or entry.get('time')
    if isinstance(ts, (int, float)):
        from datetime import timezone
        dt = datetime.fromtimestamp(ts, tz=timezone.utc)
    elif isinstance(ts, str):
        dt = parse_iso_timestamp(ts)
    else:
        dt = datetime.utcnow()
    
    # Extract verdict
    verdict = entry.get('verdict', 'SEAL')
    if verdict not in ('SEAL', 'VOID', 'SABAR', 'PARTIAL', '888_HOLD'):
        verdict = 'SEAL'  # Default for unknown legacy formats
    
    # Extract session_id
    session_id = entry.get('session_id') or entry.get('session') or f"legacy-{entry.get('_line_num', '0')}"
    
    # Extract authority
    authority = entry.get('authority') or entry.get('auth') or 'legacy_import'
    
    # Build seal_data with original preserved
    seal_data = {
        'original_entry': entry,
        'source': 'legacy_import',
        'source_file': entry.get('_source_file', 'unknown'),
    }
    
    # Try to extract meaningful data
    for key in ['query', 'reasoning', 'response', 'payload', 'data', 'trace_id', 
                'refusal_type', 'risk_domain', 'policy_codes']:
        if key in entry:
            seal_data[key] = entry[key]
    
    return {
        'session_id': session_id,
        'timestamp': dt,
        'authority': authority,
        'verdict': verdict,
        'seal_data': seal_data,
    }


async def scan_legacy_entries() -> List[Dict[str, Any]]:
    """Scan all legacy locations and return normalized entries."""
    all_entries = []
    
    repo_root = Path(__file__).parent.parent
    
    for rel_path in LEGACY_PATHS:
        path = repo_root / rel_path
        
        if not path.exists():
            print(f"Skipping (not found): {path}")
            continue
        
        if path.is_dir():
            print(f"Scanning directory: {path}")
            entries = load_json_entries(path)
        else:
            print(f"Scanning JSONL: {path}")
            entries = load_jsonl_entries(path)
        
        print(f"  Found {len(entries)} entries")
        
        for entry in entries:
            normalized = normalize_entry(entry)
            all_entries.append(normalized)
    
    return all_entries


async def import_entries(entries: List[Dict[str, Any]], dry_run: bool = True, verbose: bool = False) -> Dict[str, Any]:
    """Import entries to PostgreSQL."""
    
    stats = {
        'scanned': len(entries),
        'skipped': 0,
        'imported': 0,
        'errors': [],
    }
    
    if dry_run:
        print(f"\n[DRY RUN] Would import {len(entries)} entries")
        for i, entry in enumerate(entries[:5], 1):
            print(f"  {i}. {entry['session_id'][:40]:<40} | {entry['verdict']:<8} | {entry['timestamp']}")
        if len(entries) > 5:
            print(f"  ... and {len(entries) - 5} more")
        return stats
    
    # Actual import
    dsn = (
        os.environ.get("VAULT_POSTGRES_DSN") 
        or os.environ.get("DATABASE_URL") 
        or "postgresql://postgres:postgres@localhost:5432/arifos"
    )
    
    ledger = PersistentVaultLedger(dsn)
    await ledger.connect()
    
    try:
        for i, entry in enumerate(entries):
            try:
                receipt = await ledger.append(
                    session_id=entry['session_id'],
                    verdict=entry['verdict'],
                    seal_data=entry['seal_data'],
                    authority=entry['authority'],
                )
                stats['imported'] += 1
                
                if verbose:
                    print(f"  Imported {i+1}/{len(entries)}: seq={receipt['sequence_number']} {entry['session_id'][:30]}")
                elif (i + 1) % 100 == 0:
                    print(f"  Progress: {i+1}/{len(entries)} imported...")
                    
            except Exception as e:
                # Likely duplicate entry_hash (already imported)
                if "unique constraint" in str(e).lower() or "duplicate" in str(e).lower():
                    stats['skipped'] += 1
                    if verbose:
                        print(f"  Skipped (duplicate): {entry['session_id'][:30]}")
                else:
                    stats['errors'].append(f"{entry['session_id']}: {e}")
                    print(f"  Error importing {entry['session_id'][:30]}: {e}")
    
    finally:
        await ledger.close()
    
    return stats


async def main():
    parser = argparse.ArgumentParser(description='Import legacy VAULT999 entries to PostgreSQL')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be imported')
    parser.add_argument('--execute', action='store_true', help='Actually perform import')
    parser.add_argument('--verbose', action='store_true', help='Show detailed progress')
    args = parser.parse_args()
    
    if not args.dry_run and not args.execute:
        print("Error: Specify --dry-run or --execute")
        parser.print_help()
        sys.exit(1)
    
    print("=" * 60)
    print("VAULT999 Legacy Import Tool")
    print("=" * 60)
    
    # Scan legacy entries
    print("\nScanning legacy storage...")
    entries = await scan_legacy_entries()
    
    if not entries:
        print("\nNo legacy entries found. Nothing to import.")
        sys.exit(0)
    
    print(f"\nTotal legacy entries found: {len(entries)}")
    
    # Import
    stats = await import_entries(entries, dry_run=args.dry_run, verbose=args.verbose)
    
    # Summary
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"Scanned:   {stats['scanned']}")
    print(f"Imported:  {stats['imported']}")
    print(f"Skipped:   {stats['skipped']} (duplicates)")
    print(f"Errors:    {len(stats['errors'])}")
    
    if stats['errors']:
        print("\nErrors encountered:")
        for err in stats['errors'][:10]:
            print(f"  - {err}")
        if len(stats['errors']) > 10:
            print(f"  ... and {len(stats['errors']) - 10} more")
    
    if args.dry_run:
        print("\nThis was a DRY RUN. No data was written.")
        print("Run with --execute to perform actual import.")
    else:
        print("\nImport complete.")
        print("Verify with: SELECT COUNT(*) FROM vault_ledger;")
    
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
