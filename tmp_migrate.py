import asyncio, os, asyncpg, pathlib

async def main():
    dsn = os.environ['DATABASE_URL']
    sql_path = pathlib.Path('codebase/vault/migrations/001_create_vault_ledger.sql')
    parts = [s.strip() for s in sql_path.read_text(encoding='utf-8').split(';') if s.strip()]
    conn = await asyncpg.connect(dsn)
    try:
        for stmt in parts:
            await conn.execute(stmt)
        print(f"migration_ok {len(parts)} statements")
    finally:
        await conn.close()

if __name__ == '__main__':
    asyncio.run(main())
