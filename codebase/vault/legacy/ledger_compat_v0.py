"""
VAULT999 Compatibility Layer

Provides read-only access to legacy filesystem-based vault entries.
All new writes go to PostgreSQL; this module allows reading historical data.

Migration strategy: Option B (leave legacy read-only, document clearly)
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class LegacyVaultReader:
    """
    Read-only access to legacy filesystem vault entries.
    
    Supports:
    - entries/{session_id}.json (vault_tool.py format)
    - refusal_audit.jsonl (ledger_native.py format)
    """
    
    def __init__(self, base_path: str = "VAULT999"):
        self.base_path = Path(base_path)
        
    def read_session_json(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Read from legacy entries/{session_id}.json format.
        
        Returns None if not found.
        """
        file_path = self.base_path / "BBB_LEDGER" / "entries" / f"{session_id}.json"
        
        if not file_path.exists():
            return None
        
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            logger.warning(f"Failed to read legacy entry {session_id}: {e}")
            return None
    
    def list_session_jsons(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        List legacy entries from BBB_LEDGER/entries/ directory.
        
        Returns list of entries (newest first by mtime).
        """
        entries_dir = self.base_path / "BBB_LEDGER" / "entries"
        
        if not entries_dir.exists():
            return []
        
        entries = []
        for json_file in entries_dir.glob("*.json"):
            try:
                with open(json_file, 'r') as f:
                    data = json.load(f)
                    data["_legacy_source"] = str(json_file)
                    data["_legacy_mtime"] = json_file.stat().st_mtime
                    entries.append(data)
            except (json.JSONDecodeError, IOError) as e:
                logger.warning(f"Failed to read legacy file {json_file}: {e}")
        
        # Sort by mtime descending
        entries.sort(key=lambda x: x.get("_legacy_mtime", 0), reverse=True)
        return entries[:limit]
    
    def read_refusal_jsonl(self, session_id: str) -> List[Dict[str, Any]]:
        """
        Read entries from legacy refusal_audit.jsonl for a session.
        """
        jsonl_path = self.base_path / "BBB_LEDGER" / "refusal_audit.jsonl"
        
        if not jsonl_path.exists():
            return []
        
        entries = []
        try:
            with open(jsonl_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        entry = json.loads(line)
                        if entry.get("session_id") == session_id:
                            entry["_legacy_source"] = str(jsonl_path)
                            entries.append(entry)
                    except json.JSONDecodeError:
                        continue
        except IOError as e:
            logger.warning(f"Failed to read legacy jsonl {jsonl_path}: {e}")
        
        return entries
    
    def get_legacy_stats(self) -> Dict[str, Any]:
        """
        Get statistics about legacy vault data.
        """
        stats = {
            "session_json_count": 0,
            "refusal_jsonl_entries": 0,
            "legacy_base_path": str(self.base_path),
        }
        
        # Count session JSONs
        entries_dir = self.base_path / "BBB_LEDGER" / "entries"
        if entries_dir.exists():
            stats["session_json_count"] = len(list(entries_dir.glob("*.json")))
        
        # Count refusal JSONL lines
        jsonl_path = self.base_path / "BBB_LEDGER" / "refusal_audit.jsonl"
        if jsonl_path.exists():
            try:
                with open(jsonl_path, 'r') as f:
                    stats["refusal_jsonl_entries"] = sum(1 for line in f if line.strip())
            except IOError:
                pass
        
        return stats


async def migrate_legacy_to_postgres(
    legacy_reader: LegacyVaultReader,
    dry_run: bool = True
) -> Dict[str, Any]:
    """
    One-time migration script from legacy filesystem to PostgreSQL.
    
    Args:
        legacy_reader: Legacy vault reader instance
        dry_run: If True, only count what would be migrated
        
    Returns:
        Migration statistics
    """
    from codebase.vault.persistent_ledger import get_vault_ledger

    stats = {
        "session_jsons_found": 0,
        "session_jsons_migrated": 0,
        "refusal_entries_found": 0,
        "refusal_entries_migrated": 0,
        "errors": [],
        "dry_run": dry_run,
    }
    
    # Count legacy entries
    session_entries = legacy_reader.list_session_jsons(limit=10000)
    stats["session_jsons_found"] = len(session_entries)
    
    jsonl_path = legacy_reader.base_path / "BBB_LEDGER" / "refusal_audit.jsonl"
    if jsonl_path.exists():
        try:
            with open(jsonl_path, 'r') as f:
                stats["refusal_entries_found"] = sum(1 for line in f if line.strip())
        except IOError:
            pass
    
    if dry_run:
        return stats
    
    # Actual migration
    ledger = get_vault_ledger()
    await ledger.connect()
    
    for entry in session_entries:
        try:
            # Map legacy format to new format
            await ledger.append(
                session_id=entry.get("session_id", "unknown"),
                authority="legacy_migration",
                verdict=entry.get("verdict", "SEAL"),
                seal_data={"legacy_data": entry, "legacy_source": entry.get("_legacy_source")},
            )
            stats["session_jsons_migrated"] += 1
        except Exception as e:
            stats["errors"].append(f"Failed to migrate {entry.get('session_id')}: {e}")
    
    return stats
