#!/usr/bin/env python3
"""
Entropy Audit Script — Measure repository chaos
Lower entropy = cleaner codebase
"""
from pathlib import Path
from collections import defaultdict
import json

def count_files(directory: Path) -> dict:
    """Count files by category"""
    counts = defaultdict(int)
    sizes = defaultdict(int)
    
    for file in directory.rglob("*"):
        if not file.is_file():
            continue
            
        # Skip __pycache__
        if "__pycache__" in str(file):
            continue
            
        size = file.stat().st_size
        
        # Categorize
        if "archive/" in str(file):
            counts["archive"] += 1
            sizes["archive"] += size
        elif "tests/" in str(file) or file.name.startswith("test_"):
            counts["tests"] += 1
            sizes["tests"] += size
        elif file.suffix == ".py":
            if "codebase/" in str(file):
                counts["production_code"] += 1
                sizes["production_code"] += size
            else:
                counts["scripts"] += 1
                sizes["scripts"] += size
        elif file.suffix in [".md", ".txt", ".rst"]:
            counts["docs"] += 1
            sizes["docs"] += size
        elif file.suffix in [".yml", ".yaml", ".json", ".toml"]:
            counts["config"] += 1
            sizes["config"] += size
        else:
            counts["other"] += 1
            sizes["other"] += size
    
    return dict(counts), dict(sizes)

def calculate_entropy_score(counts: dict, sizes: dict) -> dict:
    """Calculate entropy metrics"""
    total_files = sum(counts.values())
    total_size = sum(sizes.values())
    
    # Entropy factors (lower is better)
    archive_ratio = counts.get("archive", 0) / max(total_files, 1)
    test_ratio = counts.get("tests", 0) / max(counts.get("production_code", 1), 1)
    
    # Score 0-100 (0 = perfect, 100 = chaos)
    entropy_score = (
        archive_ratio * 50 +  # Archive bloat
        test_ratio * 20 +      # Test coverage
        (1 if counts.get("other", 0) > 100 else 0) * 10  # Uncategorized files
    )
    
    return {
        "total_files": total_files,
        "total_size_mb": total_size / (1024 * 1024),
        "archive_ratio": f"{archive_ratio:.1%}",
        "test_coverage_ratio": f"{test_ratio:.1%}",
        "entropy_score": min(100, int(entropy_score)),
    }

def main():
    print("🔥 arifOS Entropy Audit")
    print("=" * 50)
    
    root = Path(".")
    counts, sizes = count_files(root)
    metrics = calculate_entropy_score(counts, sizes)
    
    # File breakdown
    print("\n📊 File Breakdown:")
    for category, count in sorted(counts.items(), key=lambda x: -x[1]):
        size_mb = sizes[category] / (1024 * 1024)
        print(f"   {category:20} {count:5} files ({size_mb:6.1f} MB)")
    
    # Metrics
    print("\n📈 Metrics:")
    print(f"   Total files:     {metrics['total_files']}")
    print(f"   Total size:      {metrics['total_size_mb']:.1f} MB")
    print(f"   Archive ratio:   {metrics['archive_ratio']}")
    print(f"   Test ratio:      {metrics['test_coverage_ratio']}")
    
    # Entropy score
    score = metrics['entropy_score']
    status = "🟢 CLEAN" if score < 20 else "🟡 MODERATE" if score < 50 else "🔴 CHAOS"
    
    print(f"\n🎯 Entropy Score: {score}/100 {status}")
    
    # Recommendations
    print("\n💡 Recommendations:")
    if score > 30:
        print("   • Compress archive/ folders to tar.gz")
    if score > 40:
        print("   • Remove duplicate engine implementations")
    if score > 50:
        print("   • Consolidate scattered documentation")
    
    if score <= 20:
        print("   • Repository is well-organized!")
        print("   • Continue current practices")
    
    print("\n" + "=" * 50)
    print("DITEMPA BUKAN DIBERI 💎🔥🧠")
    
    # Save metrics
    with open("entropy_metrics.json", "w") as f:
        json.dump({"counts": counts, "sizes": {k: v for k, v in sizes.items()}, "metrics": metrics}, f, indent=2)

if __name__ == "__main__":
    main()
