"""
ACLIP CAI — Console for AI on arifOS

The local ops surface for AI agents.
What a CLI is for humans, ACLIP is for the AI.

aaa-mcp  = The Constitution (governance, floors, Trinity pipeline)
aclip-cai = The Console    (system health, memory, platform ops)

Transport: MCP (implementation detail)
Identity:  ACLIP — arifOS Console for AI

Entry: python -m aclip_cai [stdio|sse|http]
"""

from fastmcp import FastMCP

mcp = FastMCP(
    "aclip-cai",
    instructions="""ACLIP — Console for AI on arifOS

The ops surface for AI agents on this machine.
Agents use this console to see and operate the local environment.

Console tools:
  system_health  - Read RAM, CPU, disk, top processes (like 'top' for AI)
  chroma_query   - Query persistent vector memory (like 'grep' for AI memory)

What a CLI is for humans, ACLIP is for the AI.
Constitutional governance remains in aaa-mcp.
""",
)


@mcp.tool()
async def system_health(
    mode: str = "full",
    filter_process: str = "",
    top_n: int = 15,
) -> dict:
    """Read system health from the ACLIP console.

    The AI equivalent of opening Task Manager or running 'top'.

    Args:
        mode: "full" (health + processes + warnings) |
              "resources" (RAM/CPU/disk only) |
              "processes" (process list only)
        filter_process: Substring filter on process name (e.g. "python").
        top_n: Max processes to return (default 15).
    """
    from aclip_cai.tools.system_monitor import (
        get_resource_usage,
        get_system_health,
        list_processes,
    )

    if mode == "resources":
        return get_resource_usage()
    if mode == "processes":
        return list_processes(filter_name=filter_process, top_n=top_n)
    return get_system_health()


@mcp.tool()
async def chroma_query(
    query: str,
    collection: str = "default",
    top_k: int = 5,
    list_only: bool = False,
) -> dict:
    """Query the ACLIP memory console (Chroma vector store).

    The AI equivalent of 'grep' or 'search' over persistent memory.
    Reads from C:\\Users\\User\\chroma_memory.

    Args:
        query: Natural language search query.
        collection: Chroma collection name (default: "default").
        top_k: Number of results to return (default 5).
        list_only: If True, list available collections instead of searching.
    """
    from aclip_cai.tools.chroma_query import list_collections, query_memory

    if list_only:
        return list_collections()
    return query_memory(query=query, collection=collection, top_k=top_k)
