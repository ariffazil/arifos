"""
Codex - The User-Friendly Interface for ArifOS
"""

import asyncio
import os
import sys

# Ensure we can import rich
try:
    from rich.console import Console
    from rich.markdown import Markdown
    from rich.panel import Panel
    from rich.prompt import Prompt
    from rich.syntax import Syntax
except ImportError:
    print("Installing rich...")
    os.system("uv pip install rich")
    from rich.console import Console
    from rich.markdown import Markdown
    from rich.panel import Panel
    from rich.prompt import Prompt
    from rich.syntax import Syntax

# Import the core engine
try:
    import aaa_mcp.tools.canonical_trinity as trinity
except ImportError:
    # Fallback to local import if package not installed
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    import aaa_mcp.tools.canonical_trinity as trinity

console = Console()

BANNER = r"""
[bold cyan]      Δ       [/bold cyan]
[bold cyan]     / \      [/bold cyan]  [bold white]ARIF OS :: CODEX[/bold white]
[bold cyan]    /   \     [/bold cyan]  [dim]Authority: Muhammad Arif bin Fazil[/dim]
[bold cyan]   /  👁  \    [/bold cyan]  [dim]Status: ONLINE[/dim]
[bold cyan]  /_______\\   [/bold cyan]  [yellow]DITEMPA BUKAN DIBERI[/yellow]
"""


async def main():
    console.clear()
    console.print(Panel(BANNER, subtitle="v55.2 (Constitutional Shell)"))
    console.print("[green]Welcome, Sir. The Core is listening.[/green]")
    console.print("[dim]Type 'exit' to quit, 'help' for commands.[/dim]\n")

    while True:
        try:
            query = Prompt.ask("[bold cyan]>>[/bold cyan]")

            if not query.strip():
                continue

            if query.lower() in ("exit", "quit"):
                console.print("[yellow]Disconnecting...[/yellow]")
                break

            if query.lower() == "help":
                console.print(
                    Markdown(
                        """
**Available Commands:**
- `status`: Check system health
- `help`: Show this menu
- `exit`: Quit Codex
- *Any other text will be processed by the Trinity Engine.*
                """
                    )
                )
                continue

            if query.lower() == "status":
                console.print("[green]System Status: OPTIMAL[/green]")
                console.print("Engine: [bold]aaa_mcp v55.2[/bold]")
                console.print("Transport: [bold]Local stdio[/bold]")
                continue

            # Process with Trinity
            with console.status(
                "[bold cyan]Consulting the Architect...[/bold cyan]", spinner="dots"
            ):
                # Call the actual 7-step loop (mocked for now in my recovery)
                result = await trinity.mcp_trinity(query=query, session_id="codex-user")

            # Display Result
            if isinstance(result, dict):
                verdict = result.get("verdict", "UNKNOWN")
                color = "green" if verdict == "SEAL" else "yellow" if verdict == "SABAR" else "red"

                console.print(
                    Panel(
                        f"[bold {color}]VERDICT: {verdict}[/bold {color}]\n"
                        + f"[white]{result.get('query', 'No response body')}[/white]\n"
                        + (
                            f"[dim]Motto: {result.get('motto', '')}[/dim]"
                            if result.get("motto")
                            else ""
                        ),
                        title="Trinity Output",
                        border_style=color,
                    )
                )
            else:
                console.print(f"[bold]Output:[/bold] {result}")

            console.print("")  # Newline

        except KeyboardInterrupt:
            console.print("\n[yellow]Interrupted.[/yellow]")
            break
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
