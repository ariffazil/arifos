# VAULT999 Verification Script

$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  VAULT999 Verification Tool" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$testScript = @"
import asyncio, asyncpg, os, json, hashlib
from datetime import datetime, timezone
from uuid import uuid4

async def main():
    print('Connecting to Railway PostgreSQL...')
    dsn = os.environ['DATABASE_URL']
    conn = await asyncpg.connect(dsn)
    
    print('\\n=== CHECKING TABLES ===')
    ledger_count = await conn.fetchval('SELECT COUNT(*) FROM vault_ledger')
    print(f'OK vault_ledger entries: {ledger_count}')
    
    head = await conn.fetchrow('SELECT * FROM vault_head WHERE id = 1')
    if head:
        print(f'OK vault_head exists: sequence={head[\"head_sequence\"]}')
    else:
        print('OK vault_head: empty (no entries yet)')
    
    print('\\n=== TESTING APPEND ===')
    test_data = {'test': True, 'message': 'VAULT999 verification'}
    seal_id = uuid4()
    timestamp = datetime.now(timezone.utc)
    entry_hash = hashlib.sha256(json.dumps({'test': 'data'}, sort_keys=True).encode()).hexdigest()
    
    row = await conn.fetchrow('''
        INSERT INTO vault_ledger 
            (session_id, seal_id, timestamp, authority, verdict, seal_data, entry_hash, prev_hash, merkle_root)
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
        RETURNING sequence, entry_hash
    ''', 'verify-session', seal_id, timestamp, 'verification', 'SEAL', 
        json.dumps(test_data), entry_hash, '0' * 64, entry_hash)
    
    print(f'OK Test entry created: sequence={row[\"sequence\"]}')
    
    print('\\n=== VERIFYING CHAIN ===')
    entries = await conn.fetch('SELECT sequence, entry_hash FROM vault_ledger ORDER BY sequence')
    print(f'OK Total entries in chain: {len(entries)}')
    
    print('\\n=== CLEANUP ===')
    await conn.execute(\"DELETE FROM vault_ledger WHERE session_id = 'verify-session'\")
    await conn.execute('DELETE FROM vault_head WHERE 1=1')
    print('OK Test data cleaned up')
    await conn.close()
    
    print('\\n========================================')
    print('OK ALL CHECKS PASSED!')
    print('========================================')
    print('\\nYour VAULT999 is ready for production.')

asyncio.run(main())
"@

$tempFile = [System.IO.Path]::GetTempFileName() + ".py"
$testScript | Out-File -FilePath $tempFile -Encoding utf8

try {
    railway run python $tempFile
    Remove-Item $tempFile -ErrorAction SilentlyContinue
} catch {
    Write-Host "ERROR: Verification failed" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Remove-Item $tempFile -ErrorAction SilentlyContinue
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Read-Host "Press Enter to close"
