"""
Redis Mind Vault — Session State Persistence
arifOS v55.5-HARDENED

Persists session state across ephemeral tool calls.
ChatGPT audit: "Persist 'mind' in vault/DB, not local env/processes"
"""

import json
import os
from datetime import datetime
from typing import Any, Dict, Optional

import redis

# Parse Railway Redis URL
# redis://default:PASSWORD@redis.railway.internal:6379
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")


def get_redis_client() -> Optional[redis.Redis]:
    """Initialize Redis client from Railway connection string."""
    try:
        # Parse redis://username:password@host:port
        # Strip redis:// prefix
        url = REDIS_URL.replace("redis://", "")

        # Split auth and host
        if "@" in url:
            auth, host_port = url.split("@")
        else:
            auth, host_port = "", url

        # Parse username:password
        if ":" in auth:
            username, password = auth.split(":", 1)
        else:
            username, password = "default", ""

        # Parse host:port
        if ":" in host_port:
            host, port_str = host_port.rsplit(":", 1)
            port = int(port_str)
        else:
            host, port = host_port, 6379

        client = redis.Redis(
            host=host,
            port=port,
            username=username or None,
            password=password or None,
            decode_responses=True,
            socket_connect_timeout=5,
            socket_timeout=5,
        )

        # Test connection
        client.ping()
        return client

    except Exception as e:
        print(f"Redis connection failed: {e}")
        return None


class MindVault:
    """
    Session state manager backed by Redis.

    Key pattern: arifos:session:{session_id}
    TTL: 24 hours (configurable)
    """

    KEY_PREFIX = "arifos:session"
    DEFAULT_TTL = 86400  # 24 hours

    def __init__(self):
        self._redis = get_redis_client()
        self._local_fallback: Dict[str, Any] = {}  # Fallback if Redis unavailable

    def _key(self, session_id: str) -> str:
        return f"{self.KEY_PREFIX}:{session_id}"

    def load(self, session_id: str) -> Dict[str, Any]:
        """Hydrate session state from Redis."""
        if not self._redis:
            return self._local_fallback.get(session_id, {})

        try:
            data = self._redis.get(self._key(session_id))
            if data:
                return json.loads(data)
            return {}
        except Exception as e:
            print(f"Redis load error: {e}")
            return self._local_fallback.get(session_id, {})

    def save(self, session_id: str, state: Dict[str, Any], ttl: int = None) -> bool:
        """Persist session state to Redis."""
        if not self._redis:
            self._local_fallback[session_id] = state
            return True

        try:
            # Add metadata
            state["_last_saved"] = datetime.utcnow().isoformat()
            state["_ttl"] = ttl or self.DEFAULT_TTL

            self._redis.setex(self._key(session_id), ttl or self.DEFAULT_TTL, json.dumps(state))
            return True
        except Exception as e:
            print(f"Redis save error: {e}")
            self._local_fallback[session_id] = state
            return False

    def update(self, session_id: str, updates: Dict[str, Any]) -> bool:
        """Merge updates into existing session state."""
        state = self.load(session_id)
        state.update(updates)
        return self.save(session_id, state)

    def delete(self, session_id: str) -> bool:
        """Delete session state."""
        if not self._redis:
            self._local_fallback.pop(session_id, None)
            return True

        try:
            self._redis.delete(self._key(session_id))
            return True
        except Exception as e:
            print(f"Redis delete error: {e}")
            self._local_fallback.pop(session_id, None)
            return False

    def health_check(self) -> Dict[str, Any]:
        """Check Redis connectivity."""
        if not self._redis:
            return {"status": "unavailable", "mode": "local_fallback"}

        try:
            self._redis.ping()
            info = self._redis.info("server")
            return {
                "status": "connected",
                "version": info.get("redis_version"),
                "mode": "redis",
            }
        except Exception as e:
            return {"status": "error", "error": str(e), "mode": "local_fallback"}


# Singleton instance
_mind_vault: Optional[MindVault] = None


def get_mind_vault() -> MindVault:
    """Get or create MindVault singleton."""
    global _mind_vault
    if _mind_vault is None:
        _mind_vault = MindVault()
    return _mind_vault


# ============ USAGE EXAMPLE ============
"""
Example: Using MindVault in tool execution

from aaa_mcp.redis_client import get_mind_vault

vault = get_mind_vault()
state = vault.load(session_id)  # Hydrate across ephemeral runs
state.update(new_data)
vault.save(session_id, state, ttl=86400)  # Persist for 24h
"""
