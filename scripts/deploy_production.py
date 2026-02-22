"""
arifOS Production Deployment Script
====================================

Automated deployment to Railway/Docker with validation.

Usage:
    python scripts/deploy_production.py --platform railway
    python scripts/deploy_production.py --platform docker
    python scripts/deploy_production.py --validate-only

DITEMPA BUKAN DIBERI
"""

import argparse
import asyncio
import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


class Colors:
    """ASCII-only color codes (Windows-safe)"""

    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BLUE = "\033[94m"
    RESET = "\033[0m"


def log_ok(msg):
    print(f"{Colors.GREEN}[OK]{Colors.RESET} {msg}")


def log_warn(msg):
    print(f"{Colors.YELLOW}[WARN]{Colors.RESET} {msg}")


def log_err(msg):
    print(f"{Colors.RED}[ERR]{Colors.RESET} {msg}")


def log_info(msg):
    print(f"{Colors.BLUE}[INFO]{Colors.RESET} {msg}")


async def validate_environment():
    """Validate environment before deployment."""
    print("=" * 60)
    print("PRODUCTION DEPLOYMENT VALIDATION")
    print("=" * 60)
    print()

    checks_passed = 0
    checks_failed = 0

    # 1. Python version
    version = sys.version_info
    if version >= (3, 10):
        log_ok(f"Python {version.major}.{version.minor}.{version.micro}")
        checks_passed += 1
    else:
        log_err(f"Python {version.major}.{version.minor} (need >= 3.10)")
        checks_failed += 1

    # 2. Core imports
    try:
        from core.organs import agi, apex, asi, init, vault
        from core.pipeline import forge
        from core.organs import init, agi, asi, apex, vault

        log_ok("Core organs importable")
        checks_passed += 1
    except Exception as e:
        log_err(f"Core import failed: {e}")
        checks_failed += 1

    # 3. AAA MCP imports
    try:
        from aaa_mcp.server import mcp

        log_ok("AAA MCP server importable")
        checks_passed += 1
    except Exception as e:
        log_err(f"AAA MCP import failed: {e}")
        checks_failed += 1

    # 4. Pipeline execution
    try:
        result = await forge("Validation test", actor_id="deploy")
        log_ok(f"Pipeline executes ({result.verdict})")
        checks_passed += 1
    except Exception as e:
        log_err(f"Pipeline execution failed: {e}")
        checks_failed += 1

    # 5. Environment file
    env_prod = Path(__file__).parent.parent / ".env.production"
    if env_prod.exists():
        log_ok("Production env template exists")
        checks_passed += 1
    else:
        log_warn("No .env.production template")

    # 6. Dockerfile
    dockerfile = Path(__file__).parent.parent / "Dockerfile"
    if dockerfile.exists():
        log_ok("Dockerfile present")
        checks_passed += 1
    else:
        log_err("Dockerfile missing")
        checks_failed += 1

    # 7. Railway config
    railway_toml = Path(__file__).parent.parent / "railway.toml"
    if railway_toml.exists():
        log_ok("railway.toml present")
        checks_passed += 1
    else:
        log_warn("railway.toml missing")

    print()
    print("=" * 60)
    log_info(f"Checks: {checks_passed} passed, {checks_failed} failed")

    if checks_failed > 0:
        log_err("VALIDATION FAILED - Fix errors before deployment")
        return False

    log_ok("VALIDATION PASSED - Ready for production")
    return True


def deploy_railway():
    """Deploy to Railway."""
    print()
    print("=" * 60)
    print("RAILWAY DEPLOYMENT")
    print("=" * 60)
    print()

    root = Path(__file__).parent.parent

    # Check Railway CLI
    result = subprocess.run(["railway", "--version"], capture_output=True, text=True)
    if result.returncode != 0:
        log_err("Railway CLI not found")
        print()
        print("Install Railway CLI:")
        print("  npm install -g @railway/cli")
        print()
        print("Or use Railway Dashboard:")
        print("  https://railway.app/new/template/arifos")
        return False

    log_ok(f"Railway CLI: {result.stdout.strip()}")

    # Check if logged in
    result = subprocess.run(["railway", "whoami"], capture_output=True, text=True)
    if result.returncode != 0:
        log_warn("Not logged in to Railway")
        print("Run: railway login")
        return False

    log_ok(f"Logged in as: {result.stdout.strip()}")

    # Check if project is linked
    result = subprocess.run(["railway", "status"], capture_output=True, text=True, cwd=str(root))
    if result.returncode != 0:
        log_warn("Project not linked to Railway")
        print()
        print("Options:")
        print("  1. Link existing project: railway link")
        print("  2. Create new project: railway init")
        print()
        return False

    log_ok("Project linked to Railway")

    # Set environment variables if not present
    log_info("Checking environment variables...")
    env_vars = {
        "PORT": "8080",
        "HOST": "0.0.0.0",
        "AAA_MCP_TRANSPORT": "sse",
        "ARIFOS_CONSTITUTIONAL_MODE": "AAA",
    }

    for key, default in env_vars.items():
        result = subprocess.run(
            ["railway", "variables", "get", key], capture_output=True, text=True, cwd=str(root)
        )
        if result.returncode != 0:
            log_warn(f"Setting {key}={default}")
            subprocess.run(
                ["railway", "variables", "set", key, default], cwd=str(root), capture_output=True
            )

    # Deploy
    print()
    log_info("Starting deployment...")
    print()

    subprocess.run(["railway", "up"], cwd=str(root))

    print()
    log_ok("Deployment complete!")
    print()
    print("View logs: railway logs")
    print("Open app:  railway open")

    return True


def deploy_docker():
    """Deploy using Docker."""
    print()
    print("=" * 60)
    print("DOCKER DEPLOYMENT")
    print("=" * 60)
    print()

    root = Path(__file__).parent.parent

    # Check Docker
    result = subprocess.run(["docker", "--version"], capture_output=True, text=True)
    if result.returncode != 0:
        log_err("Docker not found")
        return False

    log_ok(f"Docker: {result.stdout.strip()}")

    # Build image
    log_info("Building Docker image...")
    result = subprocess.run(
        ["docker", "build", "-t", "arifos-mcp:latest", "."],
        cwd=str(root),
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        log_err("Docker build failed")
        print(result.stderr)
        return False

    log_ok("Image built: arifos-mcp:latest")

    # Run container
    print()
    log_info("Starting container...")
    print()

    subprocess.run(
        [
            "docker",
            "run",
            "-p",
            "8080:8080",
            "-e",
            "PORT=8080",
            "-e",
            "HOST=0.0.0.0",
            "-e",
            "AAA_MCP_TRANSPORT=sse",
            "--name",
            "arifos-mcp",
            "arifos-mcp:latest",
        ]
    )

    return True


def generate_railway_template():
    """Generate Railway template for sharing."""
    template = {
        "$schema": "https://railway.app/railway.schema.json",
        "build": {"builder": "DOCKERFILE", "dockerfilePath": "Dockerfile"},
        "deploy": {
            "startCommand": "python scripts/start_server.py",
            "healthcheckPath": "/health",
            "healthcheckTimeout": 30,
            "restartPolicyType": "on_failure",
            "restartPolicyMaxRetries": 3,
        },
        "variables": {
            "PORT": "8080",
            "HOST": "0.0.0.0",
            "AAA_MCP_TRANSPORT": "sse",
            "ARIFOS_CONSTITUTIONAL_MODE": "AAA",
        },
    }

    output = Path(__file__).parent.parent / "railway.template.json"
    with open(output, "w") as f:
        json.dump(template, f, indent=2)

    log_ok(f"Railway template generated: {output}")
    print()
    print("Deploy via template:")
    print("  https://railway.app/new/template/arifos")


def main():
    parser = argparse.ArgumentParser(description="Deploy arifOS to production")
    parser.add_argument(
        "--platform",
        "-p",
        choices=["railway", "docker", "validate"],
        default="validate",
        help="Deployment platform",
    )
    parser.add_argument(
        "--generate-template", "-t", action="store_true", help="Generate Railway template"
    )

    args = parser.parse_args()

    if args.generate_template:
        generate_railway_template()
        return

    if args.platform == "validate":
        success = asyncio.run(validate_environment())
        sys.exit(0 if success else 1)
    elif args.platform == "railway":
        success = deploy_railway()
        sys.exit(0 if success else 1)
    elif args.platform == "docker":
        success = deploy_docker()
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
