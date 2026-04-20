# arifosmcp/runtime/registry.py
import os
import importlib.util
from fastmcp import FastMCP

def register_canonical_tools(mcp: FastMCP, tools_dir: str):
    """
    Dynamically registers all 13 tools from the canonical tools directory.
    Naming follows: arifos_<stage>_<name>
    """
    if not os.path.exists(tools_dir):
        print(f"ERROR: Tools directory {tools_dir} not found.")
        return

    # Metabolic Plane Mapping (Canonical Names)
    STAGE_MAP = {
        "_000_init.py": "arifos_000_init",
        "_111_sense.py": "arifos_111_sense",
        "_222_witness.py": "arifos_222_witness",
        "_333_mind.py": "arifos_333_mind",
        "_444_kernel.py": "arifos_444_kernel",
        "_555_memory.py": "arifos_555_memory",
        "_666_heart.py": "arifos_666_heart",
        "_777_ops.py": "arifos_777_ops",
        "_888_judge.py": "arifos_888_judge",
        "_999_vault.py": "arifos_999_vault",
        "_forge.py": "arifos_forge",
        "_gateway.py": "arifos_gateway",
        "_sabar.py": "arifos_sabar",
    }

    for filename, tool_name in STAGE_MAP.items():
        file_path = os.path.join(tools_dir, filename)
        
        if os.path.exists(file_path):
            # Load module dynamically
            spec = importlib.util.spec_from_file_location(tool_name, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Register the execute function as the tool
            if hasattr(module, "execute"):
                mcp.tool(name=tool_name)(module.execute)
                print(f"REGISTERED: {tool_name} from {filename}")
            else:
                print(f"WARNING: {filename} missing execute() function.")
        else:
            # Register a cooling placeholder for missing tools
            @mcp.tool(name=tool_name)
            async def placeholder(*args, **kwargs):
                return {
                    "status": "AWAIT_FORGE",
                    "error": f"Tool {tool_name} is not yet forged in the execution plane."
                }
            print(f"PLACEHOLDER: {tool_name} (File not found)")
