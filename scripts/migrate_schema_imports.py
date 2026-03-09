#!/usr/bin/env python3
"""
Schema Migration Script
Migrate old motto_schema and protocol.schemas imports to core.schema

Usage:
    python scripts/migrate_schema_imports.py
"""

import re
from pathlib import Path

OLD_IMPORTS = {
    "arifosmcp.transport.core.motto_schema": "core.schema.output",
    "arifosmcp.transport.protocol.schemas": "core.schema",
}


def migrate_file(file_path: Path) -> None:
    """Migrate a single file's imports."""
    with open(file_path, "r") as f:
        content = f.read()

    # Replace old imports with new
    for old_import, new_import in OLD_IMPORTS.items():
        # Handle different import styles
        patterns = [
            f"from {old_import} import",
            f"from {old_import} import ",
        ]
        for pattern in patterns:
            content = content.replace(pattern, f"from {new_import} import")

    with open(file_path, "w") as f:
        f.write(content)

    print(f"Migrated: {file_path}")


def find_files_with_old_imports(root_dir: Path) -> list[Path]:
    """Find all Python files with old schema imports."""
    files_to_migrate = []

    for py_file in root_dir.rglob("**/*.py"):
        try:
            with open(py_file, "r") as f:
                content = f.read()
                for old_import in OLD_IMPORTS.keys():
                    if f"from {old_import}" in content:
                        files_to_migrate.append(py_file)
                        break
        except Exception:
            continue

    return files_to_migrate


def main():
    root = Path("/srv/arifOS")

    print("=" * 60)
    print("SCHEMA IMPORT MIGRATION")
    print("=" * 60)

    files = find_files_with_old_imports(root)

    if not files:
        print("No files with old schema imports found.")
        return

    print(f"Found {len(files)} files with old schema imports")

    for file_path in files:
        migrate_file(file_path)

    print("\nMigration complete!")
    print("\nNext steps:")
    print("1. Run tests to verify everything still works")
    print("2. Archive old schema files if no longer needed")
    print("3. Update DEPLOY.md with schema migration notes")


if __name__ == "__main__":
    main()
