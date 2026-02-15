# VAULT999 Railway Setup (No Terminal Required!)

## What This Does
Sets up VAULT999 PostgreSQL tables on Railway so your seals survive container restarts.

## Prerequisites
1. **Node.js** installed (for Railway CLI) - Download from https://nodejs.org
2. **Railway account** with your arifOS project deployed

## Step 1: Run the Migration

### Double-Click (Easiest)
1. Open File Explorer to `scripts/` folder  
2. **Double-click** `RUN_MIGRATION.bat`
3. Follow the prompts (it will open browser for Railway login)

## What Happens
1. Checks if Railway CLI is installed
2. Logs you into Railway (browser opens)
3. Links to your arifOS project
4. Creates `vault_ledger` and `vault_head` tables
5. Verifies the setup

## Step 2: Verify (Optional)
After migration, run:
- Double-click `VERIFY_VAULT.bat` to test that seals work

## Troubleshooting

### "npm not found" or "railway not found"
Install Node.js: https://nodejs.org (LTS version)

### "Not authorized" or login fails
Make sure you're logged into Railway in the browser that opens.

### "Could not link project"
Run this in PowerShell first:
```powershell
cd C:\Users\User\arifOS
railway link
```
Then select your arifOS project.

## Success Indicators
You'll see:
```
OK Railway CLI found
OK Project linked
Created tables: ['vault_ledger', 'vault_head']
Migration completed successfully!
OK vault_ledger entries: 0
OK vault_head record: No (empty)
```

Empty is OK! Tables are created and ready.

## That's It!
Your VAULT999 will now persist seals to PostgreSQL automatically.
