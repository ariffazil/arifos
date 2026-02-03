#!/usr/bin/env python3
"""
Fix test imports: arifos.* → codebase.*
Repairs 34 broken test files
"""
from pathlib import Path
import sys

def fix_imports(file_path: Path):
    """Replace arifos. imports with codebase."""
    if not file_path.exists():
        print(f"⚠️  Skipping (not found): {file_path}")
        return
        
    content = file_path.read_text()
    
    # Count replacements
    old_content = content
    
    # Replace imports
    replacements = [
        ("from arifos.", "from codebase."),
        ("import arifos.", "import codebase."),
        ("from arifos_core.", "from codebase."),
        ("import arifos_core.", "import codebase."),
    ]
    
    for old, new in replacements:
        content = content.replace(old, new)
    
    if content != old_content:
        file_path.write_text(content)
        print(f"✅ Fixed: {file_path}")
    else:
        print(f"⏭️  No changes: {file_path}")

def main():
    test_dir = Path("tests/")
    
    if not test_dir.exists():
        print(f"❌ Test directory not found: {test_dir}")
        sys.exit(1)
    
    print("🔧 Fixing test imports...")
    print("=" * 50)
    
    fixed_count = 0
    for test_file in test_dir.rglob("*.py"):
        fix_imports(test_file)
        fixed_count += 1
    
    print("=" * 50)
    print(f"✅ Processed {fixed_count} test files")
    print("\nNext: Run 'pytest tests/ -v' to verify fixes")

if __name__ == "__main__":
    main()
