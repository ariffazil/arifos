from typing import Any

from arifosmcp.prompts import PROMPTS
from arifosmcp.resources import RESOURCES
from arifosmcp.tools import (
    forge,
    gateway,
    heart_666,
    init_000,
    judge_888,
    kernel_444,
    memory_555,
    mind_333,
    ops_777,
    sabar,
    sense_111,
    vault_999,
    witness_222,
)


def register_all(server: Any) -> None:
    server.tool(name="arifos_000_init")(init_000)
    server.tool(name="arifos_111_sense")(sense_111)
    server.tool(name="arifos_222_witness")(witness_222)
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
            def prompt_fn() -> str:
                return text
            return prompt_fn

        server.prompt(name=name)(_make_prompt(template))

    for uri, resource_fn in RESOURCES.items():
        server.resource(uri)(resource_fn)
