# VAULT999 Railway Migration Script
# Double-click to run, or right-click -> "Run with PowerShell"

$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  VAULT999 Railway Migration Tool" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Railway CLI is installed
try {
    $railwayVersion = railway --version 2>$null
    Write-Host "OK Railway CLI found: $railwayVersion" -ForegroundColor Green
} catch {
    Write-Host "Railway CLI not found. Installing..." -ForegroundColor Yellow
    try {
        npm install -g @railway/cli
        Write-Host "OK Railway CLI installed" -ForegroundColor Green
    } catch {
        Write-Host "ERROR: Failed to install Railway CLI. Please install Node.js first from https://nodejs.org" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
}

Write-Host ""
Write-Host "Step 1: Checking Railway login..." -ForegroundColor Yellow

# Check if logged in
try {
    $projects = railway projects 2>$null
    Write-Host "OK Already logged in to Railway" -ForegroundColor Green
} catch {
    Write-Host "Please login to Railway (this will open a browser)..." -ForegroundColor Yellow
    railway login
}

Write-Host ""
Write-Host "Step 2: Linking to your arifOS project..." -ForegroundColor Yellow

try {
    railway link
    Write-Host "OK Project linked" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Could not link project. Make sure you're in the arifOS directory." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "Step 3: Running database migration..." -ForegroundColor Yellow
Write-Host "This creates the vault_ledger and vault_head tables" -ForegroundColor Gray
Write-Host ""

# Save migration to temp file
$tempFile = [System.IO.Path]::GetTempFileName() + ".sql"
$migrationSQL = @"
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
"@

$migrationSQL | Out-File -FilePath $tempFile -Encoding utf8
Write-Host "Migration SQL created" -ForegroundColor Gray

# Run the migration
try {
    Write-Host "Executing migration on Railway PostgreSQL..." -ForegroundColor Yellow
    
    # Create Python script
    $pyScript = @"
import asyncio, asyncpg, pathlib, os

dsn = os.environ['DATABASE_URL']
sql = pathlib.Path('$tempFile').read_text()
stmts = [s.strip() for s in sql.split(';') if s.strip()]

async def main():
    conn = await asyncpg.connect(dsn)
    for s in stmts:
        await conn.execute(s)
    tables = await conn.fetch("SELECT tablename FROM pg_tables WHERE schemaname = 'public' AND tablename IN ('vault_ledger', 'vault_head')")
    await conn.close()
    print('Created tables:', [t['tablename'] for t in tables])
    print('Migration completed successfully!')

asyncio.run(main())
"@

    $pyFile = [System.IO.Path]::GetTempFileName() + ".py"
    $pyScript | Out-File -FilePath $pyFile -Encoding utf8
    
    railway run python $pyFile
    
    Remove-Item $tempFile -ErrorAction SilentlyContinue
    Remove-Item $pyFile -ErrorAction SilentlyContinue
    
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "  MIGRATION COMPLETE!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Your VAULT999 PostgreSQL tables are ready." -ForegroundColor White
    
} catch {
    Write-Host ""
    Write-Host "ERROR: Migration failed" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "Step 4: Verifying setup..." -ForegroundColor Yellow

# Run verification
$verifyScript = @"
import asyncio, asyncpg, os

async def main():
    dsn = os.environ['DATABASE_URL']
    conn = await asyncpg.connect(dsn)
    ledger = await conn.fetchval('SELECT COUNT(*) FROM vault_ledger')
    head = await conn.fetch('SELECT * FROM vault_head WHERE id = 1')
    await conn.close()
    print(f'vault_ledger entries: {ledger}')
    print(f'vault_head record: {"Yes" if head else "No"}')
    print('Verification complete!')

asyncio.run(main())
"@

$verifyFile = [System.IO.Path]::GetTempFileName() + ".py"
$verifyScript | Out-File -FilePath $verifyFile -Encoding utf8

railway run python $verifyFile
Remove-Item $verifyFile -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  ALL DONE!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Your arifOS VAULT999 is now configured." -ForegroundColor White
Write-Host ""
Write-Host "Next: Deploy your app with 'railway up'" -ForegroundColor Yellow
Write-Host ""

Read-Host "Press Enter to close"
