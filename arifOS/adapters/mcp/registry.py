"""arifOS MCP registry — uses arifOS namespace tools (Phase 1 full implementations)"""
from typing import Any
from fastmcp.tools import FunctionTool
from arifOS.prompts import PROMPTS
from arifOS.resources import RESOURCES
from arifOS.tools import (
    forge, gateway, heart_666, init_000, judge_888, kernel_444,
    memory_555, mind_333, ops_777, sabar, sense_111, vault_999, witness_222,
)

def register_all(server: Any) -> None:
    server.tool(name="arifos_000_init")(init_000)
    _register_sense_111(server)
    _register_witness_222(server)
    server.tool(name="arifos_333_mind")(mind_333)
    server.tool(name="arifos_444_kernel")(kernel_444)
    server.tool(name="arifos_555_memory")(memory_555)
    server.tool(name="arifos_666_heart")(heart_666)
    server.tool(name="arifos_777_ops")(ops_777)
    server.tool(name="arifos_888_judge")(judge_888)
    server.tool(name="arifos_999_vault")(vault_999)
    server.tool(name="arifos_forge")(forge)
    server.tool(name="arifos_gateway")(gateway)
    server.tool(name="arifos_sabar")(sabar)
    for name, template in PROMPTS.items():
        def _make_prompt(text: str):
            def prompt_fn() -> str: return text
            return prompt_fn
        server.prompt(name=name)(_make_prompt(template))
    for uri, resource_fn in RESOURCES.items():
        server.resource(uri)(resource_fn)

def _register_sense_111(server):
    """Explicit schema for sense_111"""
    async def sense_111_fn(**kwargs): return await sense_111(**kwargs)
    server.tool(name="arifos_111_sense",
        description="arifOS sense — discover and verify external signals",
        annotations={"author":"arifOS","version":"1.0"})(sense_111_fn)

def _register_witness_222(server):
    """Explicit schema for witness_222"""
    async def witness_222_fn(**kwargs): return await witness_222(**kwargs)
    server.tool(name="arifos_222_witness",
        description="arifOS witness — honest cross-validation against external reality",
        annotations={"author":"arifOS","version":"1.0"})(witness_222_fn)
