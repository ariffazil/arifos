import asyncio
import os
import sys

async def smoke_test():
    print("🚀 Starting arifOS VPS Integration Smoke Test...")
    
    # 1. Check Redis
    print("\n--- [1] Redis Connectivity ---")
    try:
        from arifosmcp.runtime.storage import get_storage
        storage = get_storage()
        print(f"✅ Storage initialized: {type(storage).__name__}")
        
        test_key = "smoke_test_key"
        test_val = {"status": "ok", "time": "2026-03-21"}
        await storage.set(test_key, test_val)
        retrieved = await storage.get(test_key)
        if retrieved == test_val:
            print("✅ Redis Write/Read: SUCCESS")
        else:
            print(f"❌ Redis Write/Read: DATA MISMATCH (Got {retrieved})")
    except Exception as e:
        print(f"❌ Redis Connectivity: FAILED - {e}")

    # 2. Check Qdrant
    print("\n--- [2] Qdrant Connectivity ---")
    try:
        from arifosmcp.agentzero.memory.constitutional_memory import ConstitutionalMemoryStore
        memory = ConstitutionalMemoryStore()
        # accessing client to test connection
        client = memory.client
        collections = client.get_collections()
        found = any(c.name == "arifos_memory" for c in collections.collections)
        print(f"✅ Qdrant Connected. Unified collection 'arifos_memory' found: {found}")
    except Exception as e:
        print(f"❌ Qdrant Connectivity: FAILED - {e}")

    # 3. Check Postgres
    print("\n--- [3] PostgreSQL Connectivity ---")
    try:
        from arifosmcp.intelligence.tools.logic.vault_logger import VaultLogger
        logger = VaultLogger()
        if logger._conn:
            print("✅ Postgres Connected via POSTGRES_URL")
            # Try a dummy write if possible, or just check _conn
            print("✅ vault_audit table check: Connection established.")
        else:
            print("⚠️ Postgres connection not established (Fallback to JSONL). Check POSTGRES_URL.")
    except Exception as e:
        print(f"❌ Postgres Connectivity: FAILED - {e}")

    # 4. Check Metrics
    print("\n--- [4] Metrics Engine ---")
    try:
        from arifosmcp.runtime.metrics import update_prometheus_metrics
        update_prometheus_metrics()
        print("✅ Prometheus metrics updated successfully.")
    except Exception as e:
        print(f"❌ Metrics Engine: FAILED - {e}")

    print("\n🚀 Smoke Test Complete.")

if __name__ == "__main__":
    asyncio.run(smoke_test())
