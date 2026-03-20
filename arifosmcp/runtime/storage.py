"""
arifosmcp/runtime/storage.py — Hardened Storage Backends (Redis + Encryption)
Wired for arifOS VPS Environment: srv1325122.hstgr.cloud
"""

import os
import logging
from typing import Any, Optional

from cryptography.fernet import Fernet
from key_value.aio.stores.redis import RedisStore
from key_value.aio.wrappers.encryption import FernetEncryptionWrapper

logger = logging.getLogger(__name__)

def build_encrypted_redis_store() -> Any:
    """
    Build a Fernet-encrypted Redis store for FastMCP/arifOS.
    
    Wired to reach 'arifos_redis:6379' (Docker container name).
    Requires STORAGE_ENCRYPTION_KEY environment variable.
    """
    redis_host = os.getenv("REDIS_HOST", "arifos_redis")
    redis_port = int(os.getenv("REDIS_PORT", "6379"))
    encryption_key = os.getenv("STORAGE_ENCRYPTION_KEY")
    
    if not encryption_key:
        logger.warning("STORAGE_ENCRYPTION_KEY not set. Falling back to ephemeral in-memory key.")
        encryption_key = Fernet.generate_key().decode()
    
    try:
        redis_store = RedisStore(
            host=redis_host,
            port=redis_port,
            db=int(os.getenv("REDIS_DB", "0")),
        )
        
        # Wrap in Fernet encryption for F11/F12 compliance
        encrypted_store = FernetEncryptionWrapper(
            key_value=redis_store,
            fernet=Fernet(encryption_key.encode())
        )
        
        logger.info(f"✅ FastMCP Redis storage initialised: {redis_host}:{redis_port}")
        return encrypted_store
        
    except Exception as exc:
        logger.error(f"❌ Failed to initialise Redis storage: {exc}")
        # Return None to allow FastMCP to fall back to 'memory' if needed, 
        # or it can be used to raise a Hard Error.
        return None

def get_storage() -> Any:
    """Return the primary storage backend for FastMCP."""
    backend = os.getenv("ARIFOS_STORAGE_BACKEND", "redis").lower()
    if backend == "redis":
        return build_encrypted_redis_store()
    return "memory"
