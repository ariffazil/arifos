# VPS Infrastructure Integration — Job 1 Complete
**Redis as Primary VAULT999 Backend**

---

## What Was Done

### 1. Created Redis Vault Store (`arifosmcp/runtime/vault_redis.py`)

New module providing:
- **Async Redis connection** to `arifos_redis:6379` (Docker network)
- **Merkle chain storage** in Redis list (`vault999:chain`)
- **Session indexing** via Redis sets (`vault999:sessions:{session_id}`)
- **Optional Fernet encryption** for at-rest data (via `STORAGE_ENCRYPTION_KEY` env var)
- **Chain verification** with hash linkage validation
- **Graceful fallback** to file-based vault if Redis unavailable

### 2. Updated Dependencies (`pyproject.toml`)

Added:
```toml
"cryptography>=42.0.0",  # Fernet encryption for vault at-rest
```

Redis was already present: `"redis>=5.0.0"`

### 3. Wired Redis into Bridge (`arifosmcp/runtime/bridge.py`)

Modified:
- **Vault seal operation**: Now writes to Redis with Merkle chain
- **Vault verify operation**: Checks Redis chain integrity
- **Trace replay**: Reads session entries from Redis
- **Backend indicator**: Returns `"backend": "redis"` in responses

### 4. Backward Compatibility

File-based vault (`VAULT999/vault999.jsonl`) remains as fallback:
- If Redis unavailable → automatic fallback to file
- If `STORAGE_ENCRYPTION_KEY` not set → stores unencrypted (development mode)
- All existing code paths preserved

---

## Docker Compose Integration

The VPS already has:
```yaml
services:
  arifos_redis:
    image: redis:7-alpine
    container_name: arifos_redis
    ports:
      - "6379:6379"
    networks:
      - arifos_network

  arifosmcp_server:
    # ... existing config
    environment:
      - STORAGE_ENCRYPTION_KEY=${STORAGE_ENCRYPTION_KEY}
    networks:
      - arifos_network  # Same network = can reach arifos_redis by hostname
```

**No changes needed to Docker Compose** — the containers are already connected via `arifos_network`.

---

## Environment Variables Required

Add to `.env` or Docker Compose:
```bash
# Generate once: python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
STORAGE_ENCRYPTION_KEY=your-fernet-key-here
```

Optional (Redis connection defaults):
```bash
REDIS_HOST=arifos_redis  # Already the default
REDIS_PORT=6379          # Already the default
```

---

## Testing After Deploy

```bash
# 1. Verify Redis is reachable
docker exec arifosmcp_server python -c "
from arifosmcp.runtime.vault_redis import get_vault_store
import asyncio

async def test():
    store = get_vault_store()
    r = await store._get_redis()
    await r.ping()
    print('Redis connected ✅')

asyncio.run(test())
"

# 2. Test vault seal
curl -X POST http://localhost:8080/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "vault_ledger",
      "arguments": {
        "mode": "verify"
      }
    }
  }'

# Expected: {"backend": "redis", "status": "INTACT"}
```

---

## What's Next (Job 2-7)

| Job | Task | Status |
|-----|------|--------|
| **1** | ✅ **Redis Vault** (DONE) | Complete |
| 2 | Qdrant for engineering_memory | Pending |
| 3 | Postgres for structured audit | Pending |
| 4 | BRAVE_API_KEY for physics_reality | Pending |
| 5 | Prometheus metrics endpoint | Pending |
| 6 | Clean up deprecated tools | Pending |
| 7 | Smoke test verification | Pending |

---

## Files Modified

1. `arifosmcp/runtime/vault_redis.py` — NEW
2. `arifosmcp/runtime/bridge.py` — MODIFIED (Redis integration)
3. `pyproject.toml` — MODIFIED (cryptography dependency)

---

*Ditempa Bukan Diberi* 🔨💎
