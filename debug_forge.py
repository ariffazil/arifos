import asyncio
from aclip_cai.console_tools import forge_guard

async def main():
    res = await forge_guard(
        action="delete",
        target="/important/data",
        session_id="test-session",
        risk_level="high",
        dry_run=True,
    )
    print(f"Tool: {res.tool}")
    print(f"Status: {res.status}")
    print(f"Verdict in data: {res.data.get('verdict')}")
    print(f"Gate in data: {res.data.get('gate')}")
    print(f"Reason Code: {res.data.get('reason_code')}")

if __name__ == "__main__":
    asyncio.run(main())
