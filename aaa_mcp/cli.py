"""
arifOS FORGE-2 CLI — Unified Command Line Interface
One-click deployment, observability, and governance management.

Usage:
    arifos serve --profile strict --metrics
    arifos deploy --target vps --stack trinity2
    arifos monitor --dashboard
    arifos health --endpoint http://localhost:8088/health

Features:
- Multiple runtime profiles (strict, balanced, permissive, audit)
- Built-in observability (Prometheus, Grafana, Loki)
- Deployment templates for 6 platforms
- Constitutional floor diagnostics
"""

import argparse
import os
import subprocess
import sys
import webbrowser
from enum import Enum


class Profile(str, Enum):
    STRICT = "strict"
    BALANCED = "balanced"
    PERMISSIVE = "permissive"
    AUDIT = "audit"


class DeploymentTarget(str, Enum):
    VPS = "vps"
    DOCKER = "docker"
    K8S = "k8s"
    RAILWAY = "railway"
    FLY = "fly"
    COOLIFY = "coolify"


def run_command(cmd: list[str], env: dict | None = None) -> int:
    """Run shell command with environment."""
    env = env or {}
    full_env = {**os.environ, **env}
    try:
        result = subprocess.run(cmd, env=full_env, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Command failed: {' '.join(cmd)}")
            print(f"Stderr: {result.stderr}")
        return result.returncode
    except Exception as e:
        print(f"Error running command: {e}")
        return 1


def check_docker() -> bool:
    """Check if Docker is available."""
    return run_command(["docker", "--version"]) == 0


def check_docker_compose() -> bool:
    """Check if Docker Compose is available."""
    return run_command(["docker", "compose", "version"]) == 0


def serve_command(args):
    """Start arifOS MCP server with specified profile."""
    profile = args.profile
    metrics = args.metrics
    port = args.port
    host = args.host

    print("🚀 Starting arifOS MCP Server")
    print(f"   Profile: {profile}")
    print(f"   Metrics: {'enabled' if metrics else 'disabled'}")
    print(f"   Endpoint: {host}:{port}")

    # Set environment variables based on profile
    env_vars = {
        "AAA_MCP_PROFILE": profile.upper(),
        "HOST": host,
        "PORT": str(port),
        "ARIFOS_PHYSICS_DISABLED": "0",  # Enable physics for strict profile
    }

    if profile == Profile.STRICT:
        env_vars.update(
            {
                "GOVERNANCE_MODE": "STRICT",
                "CONSTITUTIONAL_ENFORCEMENT": "full",
            }
        )
    elif profile == Profile.BALANCED:
        env_vars.update(
            {
                "GOVERNANCE_MODE": "BALANCED",
                "CONSTITUTIONAL_ENFORCEMENT": "moderate",
            }
        )
    elif profile == Profile.PERMISSIVE:
        env_vars.update(
            {
                "GOVERNANCE_MODE": "PERMISSIVE",
                "ARIFOS_PHYSICS_DISABLED": "1",
            }
        )
    elif profile == Profile.AUDIT:
        env_vars.update(
            {
                "GOVERNANCE_MODE": "AUDIT",
                "AAA_MCP_OUTPUT_MODE": "debug",
            }
        )

    if metrics:
        env_vars.update(
            {
                "PROMETHEUS_PORT": "9090",
                "OTEL_EXPORTER_OTLP_ENDPOINT": "http://localhost:4317",
                "OTEL_SERVICE_NAME": "arifos-mcp",
            }
        )
        print(f"   Metrics endpoint: http://{host}:9090/metrics")

    # Build command
    cmd = [sys.executable, "-m", "aaa_mcp", "sse"]

    print("\nEnvironment:")
    for key, value in env_vars.items():
        print(f"  {key}={value}")

    print(f"\nCommand: {' '.join(cmd)}")
    print("\n" + "=" * 60)

    # Run the server
    os.environ.update(env_vars)
    try:
        import aaa_mcp.__main__ as main_module

        sys.argv = ["aaa_mcp", "sse"]
        main_module.main()
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return 1

    return 0


def deploy_command(args):
    """Deploy arifOS to specified target."""
    target = args.target
    stack = args.stack

    print(f"🚀 Deploying arifOS to {target} with {stack} stack")

    if not check_docker():
        print("❌ Docker is not installed or not in PATH")
        print("   Install Docker from: https://docs.docker.com/get-docker/")
        return 1

    if not check_docker_compose():
        print("❌ Docker Compose is not available")
        print("   Install Docker Compose: https://docs.docker.com/compose/install/")
        return 1

    compose_file = "docker-compose.yml"
    if not os.path.exists(compose_file):
        print("❌ Docker Compose file not found")
        return 1

    print(f"   Using compose file: {compose_file}")

    if args.pull:
        print("   Pulling latest images...")
        if run_command(["docker", "compose", "-f", compose_file, "pull"]) != 0:
            print("⚠️  Failed to pull some images, continuing...")

    print("   Starting services...")
    cmd = ["docker", "compose", "-f", compose_file, "up", "-d", "--remove-orphans"]
    if run_command(cmd) != 0:
        print("❌ Failed to start services")
        return 1

    print("✅ Deployment completed")
    print("\n📊 Services:")
    run_command(["docker", "compose", "-f", compose_file, "ps"])

    print("\n🔗 URLs:")
    print("   - MCP SSE: http://localhost:8088/sse")
    print("   - REST API: http://localhost:8889/health")
    if stack == "trinity2":
        print("   - Grafana: http://localhost:3000 (admin/admin)")
        print("   - Prometheus: http://localhost:9090")

    return 0


def monitor_command(args):
    """Open monitoring dashboard."""
    if args.dashboard:
        url = "http://localhost:3000"
        print(f"🌐 Opening Grafana dashboard: {url}")
        webbrowser.open(url)
        return 0

    compose_file = "docker-compose.yml"

    if os.path.exists(compose_file):
        print("📊 Service Status:")
        run_command(["docker", "compose", "-f", compose_file, "ps"])

        print("\n📈 Logs (tail):")
        run_command(["docker", "compose", "-f", compose_file, "logs", "--tail=10"])
    else:
        print("❌ Docker Compose file not found")
        return 1

    return 0


def health_command(args):
    """Check health of arifOS endpoint."""
    import requests

    endpoint = args.endpoint
    timeout = args.timeout

    print(f"🏥 Checking health of {endpoint}")

    try:
        response = requests.get(endpoint, timeout=timeout)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed (HTTP {response.status_code})")

            # Pretty print JSON
            import json

            print(json.dumps(data, indent=2))

            # Check critical components
            if data.get("status") == "healthy":
                print("\n📊 Component Status:")
                components = data.get("components", {})
                for component, status in components.items():
                    icon = "✅" if status == "healthy" else "❌"
                    print(f"   {icon} {component}: {status}")

            return 0
        else:
            print(f"❌ Health check failed (HTTP {response.status_code})")
            print(f"   Response: {response.text}")
            return 1
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to endpoint: {e}")
        return 1


def create_parser():
    """Create CLI argument parser."""
    parser = argparse.ArgumentParser(
        description="arifOS FORGE-2 CLI — Unified Command Line Interface",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  arifos serve --profile strict --metrics
  arifos deploy --target vps --stack trinity2
  arifos monitor --dashboard
  arifos health --endpoint http://localhost:8088/health
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Serve command
    serve_parser = subparsers.add_parser("serve", help="Start MCP server")
    serve_parser.add_argument(
        "--profile",
        type=Profile,
        choices=list(Profile),
        default=Profile.STRICT,
        help="Governance profile",
    )
    serve_parser.add_argument("--metrics", action="store_true", help="Enable metrics endpoint")
    serve_parser.add_argument("--port", type=int, default=8080, help="Port to bind")
    serve_parser.add_argument("--host", default="0.0.0.0", help="Host to bind")
    serve_parser.set_defaults(func=serve_command)

    # Deploy command
    deploy_parser = subparsers.add_parser("deploy", help="Deploy arifOS stack")
    deploy_parser.add_argument(
        "--target",
        type=DeploymentTarget,
        choices=list(DeploymentTarget),
        default=DeploymentTarget.DOCKER,
        help="Deployment target",
    )
    deploy_parser.add_argument(
        "--stack", choices=["trinity2", "minimal"], default="trinity2", help="Stack configuration"
    )
    deploy_parser.add_argument("--pull", action="store_true", help="Pull latest images")
    deploy_parser.set_defaults(func=deploy_command)

    # Monitor command
    monitor_parser = subparsers.add_parser("monitor", help="Monitor arifOS services")
    monitor_parser.add_argument("--dashboard", action="store_true", help="Open Grafana dashboard")
    monitor_parser.set_defaults(func=monitor_command)

    # Health command
    health_parser = subparsers.add_parser("health", help="Check health endpoint")
    health_parser.add_argument(
        "--endpoint", default="http://localhost:8088/health", help="Health endpoint URL"
    )
    health_parser.add_argument("--timeout", type=int, default=5, help="Request timeout in seconds")
    health_parser.set_defaults(func=health_command)

    return parser


def main():
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 0

    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
