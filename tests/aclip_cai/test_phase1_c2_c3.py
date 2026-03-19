from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path

from aclip_cai.console_tools import fs_inspect, log_tail


async def test_fs_inspect_depth_and_hidden(tmp_path: Path) -> None:
    (tmp_path / "visible.txt").write_text("ok", encoding="utf-8")
    hidden_dir = tmp_path / ".hidden"
    hidden_dir.mkdir()
    (hidden_dir / "secret.txt").write_text("x", encoding="utf-8")
    nested = tmp_path / "nested"
    nested.mkdir()
    (nested / "child.py").write_text("print('x')", encoding="utf-8")

    result = await fs_inspect(path=str(tmp_path), depth=1, include_hidden=False)

    assert result.status == "ok"
    assert result.data["root"] == str(tmp_path.resolve())
    names = {Path(f["relative"]).name for f in result.data["files"]}
    assert "visible.txt" in names
    assert "secret.txt" not in names


async def test_fs_inspect_max_depth_alias(tmp_path: Path) -> None:
    level1 = tmp_path / "level1"
    level1.mkdir()
    (level1 / "x.txt").write_text("x", encoding="utf-8")

    result = await fs_inspect(path=str(tmp_path), max_depth=1)

    assert result.status == "ok"
    assert result.data["traversal_depth"] == 1


async def test_log_tail_since_minutes_filter(tmp_path: Path) -> None:
    now = datetime.now(timezone.utc)
    old_ts = (now - timedelta(minutes=30)).isoformat().replace("+00:00", "Z")
    new_ts = (now - timedelta(minutes=1)).isoformat().replace("+00:00", "Z")
    log_file = tmp_path / "app.log"
    log_file.write_text(
        f"{old_ts} INFO old event\n" f"{new_ts} ERROR recent event\n" "line without timestamp\n",
        encoding="utf-8",
    )

    result = await log_tail(log_file=str(log_file), lines=50, since_minutes=5)

    assert result.status == "ok"
    entries = result.data["entries"]
    assert len(entries) == 1
    assert "recent event" in entries[0]["raw"]


async def test_log_tail_pattern_alias_and_log_path_alias(tmp_path: Path) -> None:
    log_file = tmp_path / "match.log"
    log_file.write_text("INFO alpha\nERROR bravo\n", encoding="utf-8")

    result = await log_tail(log_path=str(log_file), pattern="ERROR")

    assert result.status == "ok"
    assert result.data["lines_returned"] == 1
    assert "ERROR" in result.data["entries"][0]["raw"]
