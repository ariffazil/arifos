import asyncio
import os
import shutil
import tempfile
from pathlib import Path
from aclip_cai.console_tools import fs_inspect

async def main():
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        d = tmp_path / "sub"
        d.mkdir()
        f = d / "test.txt"
        f.write_text("content")
        
        res = await fs_inspect(path=str(tmp_path), max_depth=1)
        print(f"Tool: {res.tool}")
        print(f"Status: {res.status}")
        data = res.data
        if "directories" in data and data["directories"]:
            first = data["directories"][0]
            print(f"First directory type: {type(first)}")
            print(f"First directory content: {first}")
            print(f"Path in first dir: {first['path']}")

if __name__ == "__main__":
    asyncio.run(main())
