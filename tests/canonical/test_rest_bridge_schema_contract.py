"""Static contract checks for legacy REST bridge schemas.

These checks prevent schema drift where REST advertises stricter inputs
than the canonical callable signatures exposed by `arifosmcp.runtime.server`.
"""

from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REST_FILE = ROOT / "arifosmcp.transport" / "rest.py"


def _load_tool_schemas() -> dict[str, dict]:
    mod = ast.parse(REST_FILE.read_text(encoding="utf-8"))
    for node in mod.body:
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == "TOOL_SCHEMAS":
                return ast.literal_eval(node.value)
    raise AssertionError("TOOL_SCHEMAS not found in arifosmcp.transport/rest.py")


def test_rest_schema_inspect_file_matches_public_signature() -> None:
    schemas = _load_tool_schemas()
    inspect_args = schemas["inspect_file"]["args"]

    assert "session_id" not in inspect_args
    assert inspect_args["path"]["required"] is False
    assert inspect_args["depth"]["default"] == 1
    assert inspect_args["max_files"]["default"] == 100


def test_rest_schema_check_vital_matches_public_signature() -> None:
    schemas = _load_tool_schemas()
    vital_args = schemas["check_vital"]["args"]

    assert "session_id" not in vital_args
    assert vital_args["include_swap"]["default"] is True
    assert vital_args["include_io"]["default"] is False
    assert vital_args["include_temp"]["default"] is False
