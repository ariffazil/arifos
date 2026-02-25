"""
aclip_cai/mcp_server.py — The Tool Registry
Exposes the 9 triad tools + sensory tools.
"""

from fastmcp import FastMCP

from .tools.fs_inspector import fs_inspect
from .tools.system_monitor import get_system_health
from .triad.delta.anchor import anchor
from .triad.delta.integrate import integrate
from .triad.delta.reason import reason
from .triad.omega.align import align
from .triad.omega.respond import respond
from .triad.omega.validate import validate
from .triad.psi.audit import audit
from .triad.psi.forge import forge
from .triad.psi.seal import seal

mcp = FastMCP("arifOS_Console", instructions="The Sovereign Infrastructure Console (aclip_cai).")


# Δ TRIAD — Mind
@mcp.tool()
async def triad_anchor(session_id: str, user_id: str, context: str):
    """000_INIT: Session ignition + Defense."""
    return await anchor(session_id, user_id, context)


@mcp.tool()
async def triad_reason(session_id: str, hypothesis: str, evidence: list[str]):
    """222_REASON: Logical causal tracing."""
    return await reason(session_id, hypothesis, evidence)


@mcp.tool()
async def triad_integrate(session_id: str, bundle: dict, gap: bool = False):
    """333_MAP: Context grounding."""
    return await integrate(session_id, bundle, gap)


# Ω TRIAD — Heart
@mcp.tool()
async def triad_respond(session_id: str, draft: str):
    """444_DRAFT: Plan generation."""
    return await respond(session_id, draft)


@mcp.tool()
async def triad_validate(session_id: str, action: str):
    """555_ASI: Empathy audit."""
    return await validate(session_id, action)


@mcp.tool()
async def triad_align(session_id: str, action: str):
    """666_ETHICS: Ethics alignment."""
    return await align(session_id, action)


# Ψ TRIAD — Soul
@mcp.tool()
async def triad_forge(session_id: str, plan: str):
    """777_FORGE: Solution synthesis."""
    return await forge(session_id, plan)


@mcp.tool()
async def triad_audit(session_id: str, action: str, token: str = ""):
    """888_JUDGE: Final verdict."""
    return await audit(session_id, action, token)


@mcp.tool()
async def triad_seal(session_id: str, summary: str):
    """999_VAULT: Immutable seal."""
    return await seal(session_id, summary)


# Sensory Perception
@mcp.tool()
async def sense_health():
    """C0: System health telemetry."""
    return get_system_health()


@mcp.tool()
async def sense_fs(path: str = ".", depth: int = 1):
    """C2: Filesystem traversal."""
    return fs_inspect(path=path, depth=depth)
