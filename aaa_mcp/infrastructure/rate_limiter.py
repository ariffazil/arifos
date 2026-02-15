"""
Rate Limiter for arifOS MCP Server (v55.5-HARDENED)

Implements token bucket algorithm for constitutional rate limiting.
Enforces F12 (Defense) by preventing request floods.
"""

import time
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class TokenBucket:
    """Token bucket for rate limiting."""

    capacity: int  # Maximum tokens
    tokens: float  # Current tokens
    refill_rate: float  # Tokens per second
    last_refill: float  # Timestamp of last refill


class RateLimiter:
    """
    Constitutional rate limiter with token bucket algorithm.

    F12 Defense: Prevents request flooding and abuse.
    Default: 60 requests/minute per session.
    """

    DEFAULT_CAPACITY = 60  # requests
    DEFAULT_REFILL_RATE = 1.0  # tokens/second (60/min)

    def __init__(self, capacity: int = DEFAULT_CAPACITY, refill_rate: float = DEFAULT_REFILL_RATE):
        self.capacity = capacity
        self.refill_rate = refill_rate
        self._buckets: Dict[str, TokenBucket] = {}

    def _get_bucket(self, session_id: str) -> TokenBucket:
        """Get or create token bucket for session."""
        if session_id not in self._buckets:
            self._buckets[session_id] = TokenBucket(
                capacity=self.capacity,
                tokens=float(self.capacity),
                refill_rate=self.refill_rate,
                last_refill=time.time(),
            )
        return self._buckets[session_id]

    def _refill(self, bucket: TokenBucket) -> None:
        """Refill tokens based on elapsed time."""
        now = time.time()
        elapsed = now - bucket.last_refill
        refill_amount = elapsed * bucket.refill_rate
        bucket.tokens = min(bucket.capacity, bucket.tokens + refill_amount)
        bucket.last_refill = now

    def allow_request(self, session_id: str, cost: float = 1.0) -> bool:
        """
        Check if request is allowed under rate limit.

        Args:
            session_id: Session identifier
            cost: Token cost for this request (default 1.0)

        Returns:
            True if request is allowed, False if rate limited
        """
        bucket = self._get_bucket(session_id)
        self._refill(bucket)

        if bucket.tokens >= cost:
            bucket.tokens -= cost
            return True
        return False

    def get_remaining(self, session_id: str) -> int:
        """Get remaining tokens for session."""
        bucket = self._get_bucket(session_id)
        self._refill(bucket)
        return int(bucket.tokens)

    def reset(self, session_id: str) -> None:
        """Reset rate limit for session."""
        if session_id in self._buckets:
            del self._buckets[session_id]

    def get_stats(self, session_id: str) -> Dict:
        """Get rate limit statistics for session."""
        bucket = self._get_bucket(session_id)
        self._refill(bucket)
        return {
            "session_id": session_id,
            "tokens_remaining": int(bucket.tokens),
            "capacity": bucket.capacity,
            "refill_rate": bucket.refill_rate,
            "f12_status": "PASS" if bucket.tokens > 0 else "LIMIT",
        }


# Singleton instance
_rate_limiter: Optional[RateLimiter] = None


def get_rate_limiter() -> RateLimiter:
    """Get or create the rate limiter singleton."""
    global _rate_limiter
    if _rate_limiter is None:
        _rate_limiter = RateLimiter()
    return _rate_limiter
