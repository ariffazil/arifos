"""Public arifOS AAA MCP package (canonical 13-tool surface)."""

# Lazy — do not eagerly import server here.
# FastMCP tool registration fires on server import; importing arifosmcp.runtime
# sub-modules (e.g. contracts) must not trigger that side-effect.
__all__ = ["create_aaa_mcp_server"]


def create_aaa_mcp_server():  # noqa: ANN201
    from .server import create_aaa_mcp_server as _fn
    return _fn()
