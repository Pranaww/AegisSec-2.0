"""
AegisSec v2.0 — Non-Interactive Scan Test
Accepts a target as a CLI argument and runs a two-tool scan through the full pipeline.
"""

import sys
sys.path.insert(0, '.')

from src.automation_engine import AutomationEngine
from src.report_generator import ReportGenerator
from src.config_manager import ConfigManager
from rich.console import Console
from datetime import datetime
import os

console = Console()


def main():
    if len(sys.argv) < 2:
        console.print("[red]Usage: python test_scan.py <target>[/red]")
        console.print("[dim]Example: python test_scan.py 127.0.0.1[/dim]")
        sys.exit(1)

    target = sys.argv[1]
    console.print(f"[bold cyan]AegisSec Non-Interactive Scan Test[/bold cyan]")
    console.print(f"[bold]Target: {target}[/bold]\n")

    engine = AutomationEngine()
    report_gen = ReportGenerator()

    # Simple 2-tool test
    tools = [
        {"name": "nmap", "command": f"nmap -sn {target}"},
        {"name": "ping", "command": f"ping -c 3 {target}"},
    ]

    results = {
        "target": target,
        "scan_type": "test",
        "timestamp": datetime.now().isoformat(),
        "tools_used": tools,
        "educational_insights": [],
        "tool_outputs": {},
        "ai_analysis": {},
        "executive_summary": "Non-interactive test scan completed."
    }

    for tool in tools:
        tool_name = tool["name"]
        console.print(f"[bold]Running {tool_name}...[/bold]")
        result = engine.run_single_tool(tool_name, tool["command"], target)
        results["tool_outputs"][tool_name] = result

        if result["success"]:
            console.print(f"  [green]✓ {tool_name} succeeded ({result['execution_time']}s)[/green]")
        else:
            console.print(f"  [red]✗ {tool_name} failed: {result.get('error', '')}[/red]")

    # Generate reports
    output_dir = os.path.join(os.path.dirname(__file__), "test_reports")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_target = target.replace(".", "_")
    base = f"test_scan_{safe_target}_{timestamp}"

    for fmt in ['html', 'json']:
        path = report_gen.generate_report(results, output_dir, base, fmt)
        if path:
            console.print(f"  [green]✓ {fmt.upper()} report: {path}[/green]")

    console.print("\n[bold green]Test scan complete![/bold green]")


if __name__ == "__main__":
    main()
