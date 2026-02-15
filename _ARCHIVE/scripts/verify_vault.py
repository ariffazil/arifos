#!/usr/bin/env python3
"""
Vault 999 Chain Verification CLI

Usage:
    python scripts/verify_vault.py
    python scripts/verify_vault.py --dsn postgresql://user:pass@host:5432/arifos

Reads DATABASE_URL from environment if --dsn not provided.
"""

import argparse
import asyncio
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


async def verify(dsn: str) -> int:
    from codebase.vault.persistent_ledger import PersistentVaultLedger

    ledger = PersistentVaultLedger(dsn=dsn)
    try:
        await ledger.connect()
    except Exception as e:
        print(f"[ERROR] Failed to connect: {e}")
        return 1

    try:
        result = await ledger.verify_chain()
        count = result.get("entries", 0)

        if count == 0:
            print("[INFO] Vault ledger is empty (no entries to verify).")
            return 0

        if result["valid"]:
            print(f"[OK] Chain verification PASSED ({count} entries)")
            print(f"  Merkle root: {result.get('merkle_root', 'N/A')[:32]}...")
            return 0
        else:
            print(f"[FAIL] Chain verification FAILED")
            print(f"  Reason: {result.get('reason', 'unknown')}")
            if result.get("first_invalid_seq"):
                print(f"  First invalid sequence: {result['first_invalid_seq']}")
            return 2

    finally:
        await ledger.close()


def main():
    parser = argparse.ArgumentParser(description="Vault 999 Chain Verification")
    parser.add_argument(
        "--dsn",
        default=os.environ.get("DATABASE_URL") or os.environ.get("VAULT_POSTGRES_DSN"),
        help="PostgreSQL DSN (default: $DATABASE_URL)",
    )
    args = parser.parse_args()

    if not args.dsn:
        print("[ERROR] No DSN provided. Set DATABASE_URL or use --dsn.")
        sys.exit(1)

    exit_code = asyncio.run(verify(args.dsn))
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
