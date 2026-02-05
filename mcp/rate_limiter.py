"""Rate limiter for MCP server."""
from typing import Optional

class RateLimiter:
    def __init__(self):
        self.requests = {}
    
    def allow_request(self, session_id: str) -> bool:
        # Simple rate limiting - allow all for now
        return True

def get_rate_limiter():
    return RateLimiter()