"""Minimal L5 token physics guards used by contract tests."""

from __future__ import annotations


class TokenPhysics:
    """Apply simple budget checks for token consumption."""

    def consume(self, requested_tokens: int, remaining_budget: int) -> int:
        if requested_tokens < 0:
            raise ValueError("requested_tokens must be non-negative")
        if remaining_budget < 0:
            raise ValueError("remaining_budget must be non-negative")
        if requested_tokens > remaining_budget:
            raise PermissionError("STARVATION: token budget exceeded")
        return remaining_budget - requested_tokens
