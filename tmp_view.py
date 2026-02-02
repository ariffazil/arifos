from pathlib import Path
lines=Path("tests/test_vault_postgres.py").read_text(encoding="utf-8").splitlines()
for i in range(1,80):
    print(f"{i:03d}: {lines[i-1]}")
