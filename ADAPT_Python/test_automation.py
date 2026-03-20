"""
AegisSec v2.0 — Automation Engine Test
Tests tool execution via AutomationEngine.
"""

import sys
sys.path.insert(0, '.')

from src.automation_engine import AutomationEngine
from rich.console import Console
from rich.table import Table

console = Console()


def test_automation():
    engine = AutomationEngine()

    console.print("[bold cyan]Testing Automation Engine[/bold cyan]\n")

    # Test tool availability
    console.print("[bold]Checking available tools...[/bold]")
    available = engine._get_available_tools()
    console.print(f"Available tools: {', '.join(available) if available else 'None found'}\n")

    # Test running a simple tool
    tools = [
        {"name": "nmap", "command": "nmap -sn 127.0.0.1"},
        {"name": "ping", "command": "ping -c 2 127.0.0.1"},
    ]

    results = engine.run_tools(tools, "127.0.0.1")

    table = Table(title="Test Results")
    table.add_column("Tool", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Time", style="yellow")
    table.add_column("Output Preview", style="dim", max_width=50)

    for result in results:
        status = "[green]✓ Pass[/green]" if result["success"] else "[red]✗ Fail[/red]"
        output_preview = (result.get("output", "") or result.get("error", ""))[:50]
        table.add_row(
            result["tool"],
            status,
            f"{result['execution_time']}s",
            output_preview
        )

    console.print(table)

    # Session summary
    summary = engine.get_session_summary()
    console.print(f"\n[bold]Session: {summary['successful']}/{summary['total_tools_run']} tools succeeded[/bold]")


if __name__ == "__main__":
    test_automation()
