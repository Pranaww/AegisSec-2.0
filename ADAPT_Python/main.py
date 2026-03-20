"""
AegisSec v2.0 — Entry Point
Application bootstrap, banner display, top-level mode routing.
"""

import sys
from rich.console import Console
from rich.panel import Panel

from src.config_manager import ConfigManager
from src.cli import AegisSecCLI

console = Console()


def display_banner():
    """Renders the cyan ASCII art banner in a Rich Panel."""
    banner = """
    ╔═══════════════════════════════════════════════════════════╗
    ║           _    _____ ____ ___ ____  ____  _____ ____      ║
    ║          / \\  | ____/ ___|_ _/ ___||  __)/ ____|  __|    ║
    ║         / _ \\ |  _|| |  _ | |\\___ \\| |__ | |    | |__    ║
    ║        / ___ \\| |__| |_| || | ___) |  __|| |____|  __|   ║
    ║       /_/   \\_\\____\\____|___|____/|____| \\_____|____|    ║
    ║                                                           ║
    ║           AI-Powered Penetration Testing Platform          ║
    ║                      Version 2.0                          ║
    ║                   RunTime Terrors Team                     ║
    ╚═══════════════════════════════════════════════════════════╝
    """
    console.print(Panel(banner, style="bold cyan", border_style="cyan",
                         subtitle="[dim]Educational Cybersecurity Platform[/dim]"))


def main():
    """Initializes ConfigManager, checks first-run, shows menu, dispatches to CLI."""
    display_banner()

    config = ConfigManager()

    # First-time setup check
    if not config.is_configured():
        console.print("\n[bold yellow]⚙  First-time setup required![/bold yellow]\n")
        config.setup()

    cli = AegisSecCLI()

    while True:
        console.print("\n[bold cyan]═══ Main Menu ═══[/bold cyan]")
        console.print("  [green]1.[/green] Quick Automated Scan")
        console.print("  [green]2.[/green] AI-Guided Penetration Test")
        console.print("  [green]3.[/green] Educational Mode (AI Mentor)")
        console.print("  [green]4.[/green] Settings")
        console.print("  [green]5.[/green] View Reports")
        console.print("  [green]6.[/green] Exit")

        try:
            choice = console.input("\n[bold]Select an option (1-6): [/bold]").strip()
        except (KeyboardInterrupt, EOFError):
            console.print("\n[dim]Goodbye![/dim]")
            break

        if choice == "1":
            cli.quick_scan()
        elif choice == "2":
            cli.run_pentest_workflow()
        elif choice == "3":
            cli.educational_mode()
        elif choice == "4":
            config.setup()
            cli.setup_ai_client()  # Refresh AI client after settings change
        elif choice == "5":
            cli.view_reports()
        elif choice == "6":
            console.print("\n[bold cyan]Thank you for using AegisSec! Stay ethical, stay curious. 🛡️[/bold cyan]")
            break
        else:
            console.print("[red]Invalid option. Please choose 1-6.[/red]")


if __name__ == "__main__":
    main()