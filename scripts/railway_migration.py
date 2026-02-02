#!/usr/bin/env python3
"""
VAULT999 Railway Migration Tool
Run: python scripts/railway_migration.py

This creates the vault_ledger and vault_head tables on Railway PostgreSQL.
"""

import subprocess
import sys
import tempfile
import os

MIGRATION_SQL = """
CREATE TABLE IF NOT EXISTS vault_ledger (
    sequence BIGSERIAL PRIMARY KEY,
    session_id TEXT NOT NULL,
    seal_id UUID NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL,
    authority TEXT NOT NULL,
    verdict TEXT NOT NULL,
    seal_data JSONB NOT NULL,
    entry_hash TEXT NOT NULL UNIQUE,
    prev_hash TEXT,
    merkle_root TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_vault_session ON vault_ledger(session_id);
CREATE INDEX IF NOT EXISTS idx_vault_timestamp ON vault_ledger(timestamp);

CREATE TABLE IF NOT EXISTS vault_head (
    id SMALLINT PRIMARY KEY DEFAULT 1,
    head_sequence BIGINT NOT NULL,
    head_entry_hash TEXT NOT NULL,
    head_merkle_root TEXT NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT now()
);
"""

PYTHON_MIGRATION = '''
import asyncio
import asyncpg
import os

async def main():
    dsn = os.environ["DATABASE_URL"]
    conn = await asyncpg.connect(dsn)
    
    sql = """{sql}"""
    stmts = [s.strip() for s in sql.split(";") if s.strip()]
    
    for stmt in stmts:
        await conn.execute(stmt)
    
    tables = await conn.fetch("""
        SELECT tablename FROM pg_tables 
        WHERE schemaname = 'public' 
        AND tablename IN ('vault_ledger', 'vault_head')
    """)
    
    await conn.close()
    print("Created tables:", [t["tablename"] for t in tables])
    print("Migration completed successfully!")

asyncio.run(main())
'''


def get_railway_cmd():
    """Get the Railway CLI command, checking env var first."""
    return os.environ.get("RAILWAY_EXE", "railway")


def check_railway_cli():
    """Check if Railway CLI is installed."""
    cmd = get_railway_cmd()
    try:
        result = subprocess.run(
            [cmd, "--version"],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"✓ Railway CLI found: {result.stdout.strip()}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("✗ Railway CLI not found.")
        print("\nPlease install it with:")
        print("  npm install -g @railway/cli")
        print("\nOr download Node.js from https://nodejs.org first")
        return False


def check_login():
    """Check if user is logged into Railway."""
    cmd = get_railway_cmd()
    try:
        subprocess.run(
            [cmd, "projects"],
            capture_output=True,
            text=True,
            check=True
        )
        print("✓ Already logged in to Railway")
        return True
    except subprocess.CalledProcessError:
        print("Please login to Railway (opening browser)...")
        subprocess.run([cmd, "login"])
        return True


def link_project():
    """Link to Railway project."""
    cmd = get_railway_cmd()
    print("\n→ Linking to your arifOS project...")
    try:
        subprocess.run([cmd, "link"], check=True)
        print("✓ Project linked")
        return True
    except subprocess.CalledProcessError:
        print("✗ Could not link project")
        return False


def run_migration():
    """Run the database migration."""
    print("\n→ Running database migration...")
    print("  Creating vault_ledger and vault_head tables...")
    
    # Create temp Python file with migration
    py_code = PYTHON_MIGRATION.format(sql=MIGRATION_SQL.replace('"', '\\"'))
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(py_code)
        temp_file = f.name
    
    try:
        cmd = get_railway_cmd()
        result = subprocess.run(
            [cmd, "run", "python", temp_file],
            capture_output=True,
            text=True
        )
        print(result.stdout)
        if result.returncode != 0:
            print("Error:", result.stderr)
            return False
        return True
    finally:
        os.unlink(temp_file)


def verify_setup():
    """Verify the setup worked."""
    print("\n→ Verifying setup...")
    
    verify_code = '''
import asyncio
import asyncpg
import os

async def main():
    dsn = os.environ["DATABASE_URL"]
    conn = await asyncpg.connect(dsn)
    
    ledger = await conn.fetchval("SELECT COUNT(*) FROM vault_ledger")
    head = await conn.fetch("SELECT * FROM vault_head WHERE id = 1")
    
    await conn.close()
    
    print(f"✓ vault_ledger entries: {ledger}")
    print(f"✓ vault_head record: {'Yes' if head else 'No (empty)'}")
    print("✓ Verification complete!")

asyncio.run(main())
'''
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(verify_code)
        temp_file = f.name
    
    try:
        cmd = get_railway_cmd()
        result = subprocess.run(
            [cmd, "run", "python", temp_file],
            capture_output=True,
            text=True
        )
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        return result.returncode == 0
    finally:
        os.unlink(temp_file)


def main():
    print("=" * 50)
    print("  VAULT999 Railway Migration Tool")
    print("=" * 50)
    print()
    
    # Step 1: Check Railway CLI
    if not check_railway_cli():
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    # Step 2: Check login
    if not check_login():
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    # Step 3: Link project
    if not link_project():
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    # Step 4: Run migration
    if not run_migration():
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    # Step 5: Verify
    verify_setup()
    
    print()
    print("=" * 50)
    print("  ✓ MIGRATION COMPLETE!")
    print("=" * 50)
    print()
    print("Your VAULT999 PostgreSQL tables are ready.")
    print("Next: Deploy with 'railway up'")
    print()
    
    input("Press Enter to close...")


if __name__ == "__main__":
    main()
