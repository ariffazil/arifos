import asyncio
import json
import os
import subprocess
import sys

PYTHON_EXE = r"C:\Users\User\arifOS\.venv313\Scripts\python.exe"
ENV = os.environ.copy()
ENV["PYTHONPATH"] = r"C:\Users\User\arifOS"
ENV["PYTHONIOENCODING"] = "utf-8"
ENV["ARIFOS_VAULT_PATH"] = r"C:\Users\User\arifOS\VAULT999"
ENV["ARIFOS_CONSTITUTIONAL_MODE"] = "AAA"


async def test_server(name, args):
    print(f"\n--- Testing {name} ---")
    cmd = [PYTHON_EXE] + args
    print(f"Command: {' '.join(cmd)}")

    try:
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env=ENV,
        )

        init_req = {
            "jsonrpc": "2.0",
            "method": "initialize",
            "params": {
                "clientInfo": {"name": "test", "version": "1.0"},
                "protocolVersion": "2024-11-05",
                "capabilities": {},
            },
            "id": 1,
        }

        try:
            input_bytes = (json.dumps(init_req) + "\n").encode()
            stdout, stderr = await asyncio.wait_for(
                proc.communicate(input=input_bytes), timeout=5.0
            )

            if proc.returncode is not None and proc.returncode != 0:
                print(f"❌ FAILED with code {proc.returncode}")
                print(f"STDERR: {stderr.decode()}")
                return False

            if not stdout:
                print("❌ FAILED: No output received")
                if stderr:
                    print(f"STDERR: {stderr.decode()}")
                return False

            resp = json.loads(stdout.decode().split("\n")[0])
            if "result" in resp:
                print(
                    f"✅ SUCCESS: Server responded with protocol version {resp['result']['protocolVersion']}"
                )
                return True
            else:
                print(f"❌ FAILED: Unexpected response: {stdout.decode()[:100]}")
                return False

        except asyncio.TimeoutError:
            print("❌ FAILED: Timeout waiting for response")
            proc.kill()
            stdout, stderr = await proc.communicate()
            if stderr:
                print(f"STDERR: {stderr.decode()}")
            return False

    except Exception as e:
        print(f"❌ FAILED: Exception: {e}")
        return False


async def main():
    s1 = await test_server("aaa-mcp (Brain)", ["-m", "aaa_mcp", "stdio"])
    s2 = await test_server("aclip-cai (Senses)", ["-m", "aclip_cai.server"])

    if s1 and s2:
        print("\n🎉 ALL CHECKS PASSED: Kimi is safe to launch.")
        sys.exit(0)
    else:
        print("\n⚠️ CHECKS FAILED: Fix required.")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
