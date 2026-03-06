"""Verify VAULT999 ledger integrity (chain continuity + JSON validity).

Usage:
    python scripts/verify_vault_integrity.py
    python scripts/verify_vault_integrity.py --vault-path VAULT999/BBB_LEDGER/vault.jsonl

Exit codes:
    0 — Vault OK or empty (acceptable for fresh install)
    1 — Chain integrity violation detected
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def verify(vault_path: Path) -> bool:
    """Return True if vault is valid (or empty). Print findings to stderr."""
    if not vault_path.exists():
        print(f"VAULT: {vault_path} not found — OK for fresh install", file=sys.stderr)
        return True

    entries: list[dict] = []
    with vault_path.open() as fh:
        for lineno, raw in enumerate(fh, start=1):
            raw = raw.strip()
            if not raw:
                continue
            try:
                entries.append(json.loads(raw))
            except json.JSONDecodeError as exc:
                print(f"VAULT ERROR: line {lineno} is not valid JSON: {exc}", file=sys.stderr)
                return False

    if not entries:
        print("VAULT: empty ledger — OK for fresh install", file=sys.stderr)
        return True

    # Verify hash chain continuity
    for i, entry in enumerate(entries):
        if i == 0:
            continue
        prev = entries[i - 1]
        expected_prev = prev.get("entry_hash") or prev.get("current_hash", "")
        actual_prev = entry.get("prev_hash") or entry.get("previous_hash", "")
        if expected_prev and actual_prev and expected_prev != actual_prev:
            print(
                f"VAULT ERROR: chain break at sequence {entry.get('sequence', i + 1)}: "
                f"expected prev_hash={expected_prev!r}, got {actual_prev!r}",
                file=sys.stderr,
            )
            return False

    print(
        f"VAULT OK: {len(entries)} entries, chain continuous ({vault_path})",
        file=sys.stderr,
    )
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify VAULT999 ledger integrity")
    parser.add_argument(
        "--vault-path",
        default="VAULT999/BBB_LEDGER/vault.jsonl",
        help="Path to the vault JSONL ledger file",
    )
    args = parser.parse_args()

    vault_path = Path(args.vault_path)
    ok = verify(vault_path)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
