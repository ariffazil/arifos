import os
import shutil
import fnmatch
from aclip_cai.tools.fs_inspector import fs_inspect

def test():
    base = "test_fs_inspect"
    if os.path.exists(base):
        shutil.rmtree(base)
    os.makedirs(base)
    
    (open(os.path.join(base, "a.py"), "w")).close()
    (open(os.path.join(base, "b.txt"), "w")).close()
    (open(os.path.join(base, "c.py"), "w")).close()
    
    res_pat = fs_inspect(path=base, pattern="*.py", depth=1)
    print("Pattern *.py result:", res_pat)
    
    items = res_pat.get("tree", [])
    files = [i["name"] for i in items if i["type"] == "file"]
    print("Files found:", files)

if __name__ == "__main__":
    test()
