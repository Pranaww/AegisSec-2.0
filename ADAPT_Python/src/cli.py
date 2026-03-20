"""
AegisSec v2.0 — CLI Interface
The main orchestrator. Owns the full user-facing workflow logic for all operation modes.
"""

import re
import os
from datetime import datetime
from typing import List, Dict, Optional

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.syntax import Syntax

from src.config_manager import ConfigManager
from src.deepseek_client import DeepSeekClient
from src.automation_engine import AutomationEngine
from src.report_generator import ReportGenerator


class AegisSecCLI:
    """Main orchestrator — owns the full user-facing workflow logic for all operation modes."""

    def __init__(self):
        self.console = Console()
        self.config_manager = ConfigManager()
        self.ai_client: Optional[DeepSeekClient] = None
        self.engine: Optional[AutomationEngine] = None
        self.report_gen = ReportGenerator()
        self.setup_ai_client()

    def setup_ai_client(self):
        """Reads API key from config; creates DeepSeekClient or sets None."""
        api_key = self.config_manager.get_api_key()
        if api_key:
            self.ai_client = DeepSeekClient(api_key)
            self.engine = AutomationEngine(self.ai_client)
        else:
            self.ai_client = None
            self.engine = AutomationEngine()

    # ──────────────────────── Mode 1: Quick Scan ────────────────────────

    def quick_scan(self):
        """Skips AI selection; uses top-3 Kali tools directly."""
        self.console.print(Panel("[bold cyan]Quick Automated Scan[/bold cyan]",
                                  subtitle="Mode 1"))

        target = self._prompt_target()
        if not target:
            return

        self.console.print(f"\n[bold green]Target:[/bold green] {target}")
        self.console.print("[dim]Using default Kali tools: nmap, nikto, dirb[/dim]\n")

        tools = self._get_fallback_tools(target)
        results = self._execute_and_collect(target, tools, "quick_scan")

        self.show_executive_summary(results, target, "quick_scan")
        self.generate_reports(results, target, "quick_scan")

    # ──────────────────────── Mode 2: AI-Guided Pentest ────────────────────────

    def run_pentest_workflow(self):
        """Full AI-guided pentest: target → tool select → execute → summary → reports."""
        self.console.print(Panel("[bold cyan]AI-Guided Penetration Test[/bold cyan]",
                                  subtitle="Mode 2"))

        if not self.ai_client:
            self.console.print("[bold red]AI client not configured. Please set up your API key first (Option 4).[/bold red]")
            return

        target = self._prompt_target()
        if not target:
            return

        # Ask for scan type
        self.console.print("\n[bold yellow]Select scan type:[/bold yellow]")
        self.console.print("  1. Reconnaissance")
        self.console.print("  2. Vulnerability Assessment")
        self.console.print("  3. Comprehensive")
        self.console.print("  4. Educational Demo")

        scan_choice = self.console.input("\n[bold]Choose (1-4) [default: 3]: [/bold]").strip() or "3"
        scan_types = {
            "1": "reconnaissance",
            "2": "vulnerability_assessment",
            "3": "comprehensive",
            "4": "educational_demo"
        }
        scan_type = scan_types.get(scan_choice, "comprehensive")

        # Get AI recommendations
        self.console.print(f"\n[bold green]Target:[/bold green] {target}")
        self.console.print(f"[bold green]Scan Type:[/bold green] {scan_type}\n")

        tools = []
        with Progress(SpinnerColumn(), TextColumn("[bold cyan]Consulting AI for tool recommendations..."),
                       console=self.console) as progress:
            task = progress.add_task("", total=None)
            tools = self.ai_client.get_tool_recommendations(target, scan_type)

        if not tools:
            self.console.print("[yellow]AI returned no recommendations, using fallback tools.[/yellow]")
            tools = self._get_fallback_tools(target)

        selected_tools = self.show_tool_recommendations_and_select(tools)
        if not selected_tools:
            self.console.print("[yellow]No tools selected. Aborting.[/yellow]")
            return

        results = self._execute_and_collect(target, selected_tools, scan_type)
        self.show_executive_summary(results, target, scan_type)
        self.generate_reports(results, target, scan_type)

    # ──────────────────────── Mode 3: Educational Mode ────────────────────────

    def educational_mode(self):
        """Interactive Q&A loop via DeepSeekClient.get_ai_advisor_response."""
        self.console.print(Panel("[bold cyan]Educational Mode — AI Cybersecurity Mentor[/bold cyan]",
                                  subtitle="Mode 3"))

        if not self.ai_client:
            self.console.print("[bold red]AI client not configured. Please set up your API key first (Option 4).[/bold red]")
            return

        self.console.print("[dim]Ask any cybersecurity question. Type 'exit' to return to main menu.[/dim]\n")

        while True:
            question = self.console.input("[bold green]You:[/bold green] ").strip()
            if question.lower() in ['exit', 'quit', 'q', 'back']:
                self.console.print("[dim]Returning to main menu...[/dim]")
                break
            if not question:
                continue

            with Progress(SpinnerColumn(), TextColumn("[bold cyan]Thinking..."),
                           console=self.console) as progress:
                task = progress.add_task("", total=None)
                response = self.ai_client.get_ai_advisor_response(question)

            self.console.print(Panel(response, title="[bold cyan]Educational Guidance[/bold cyan]",
                                      border_style="cyan"))
            self.console.print()

    # ──────────────────────── Mode 5: View Reports ────────────────────────

    def view_reports(self):
        """Lists saved reports; opens HTML or displays JSON."""
        self.console.print(Panel("[bold cyan]Saved Reports[/bold cyan]",
                                  subtitle="Mode 5"))

        output_dir = self.config_manager.get_output_dir()

        if not os.path.exists(output_dir):
            self.console.print("[yellow]No reports directory found.[/yellow]")
            return

        # Collect report files
        reports = []
        for f in os.listdir(output_dir):
            if f.endswith(('.html', '.json', '.md')):
                filepath = os.path.join(output_dir, f)
                mtime = os.path.getmtime(filepath)
                reports.append((f, filepath, mtime))

        if not reports:
            self.console.print(f"[yellow]No reports found in {output_dir}[/yellow]")
            return

        # Sort newest first
        reports.sort(key=lambda x: x[2], reverse=True)

        table = Table(title="Available Reports")
        table.add_column("#", style="cyan", width=4)
        table.add_column("Filename", style="green")
        table.add_column("Type", style="yellow")
        table.add_column("Modified", style="dim")

        for i, (name, path, mtime) in enumerate(reports, 1):
            ext = name.rsplit('.', 1)[-1].upper()
            modified = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M")
            table.add_row(str(i), name, ext, modified)

        self.console.print(table)

        choice = self.console.input("\n[bold]Enter report number to view (or 'back'): [/bold]").strip()
        if choice.lower() in ['back', 'exit', 'q']:
            return

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(reports):
                name, filepath, _ = reports[idx]
                if filepath.endswith('.json'):
                    with open(filepath, 'r') as f:
                        content = f.read()
                    syntax = Syntax(content, "json", theme="monokai", line_numbers=True)
                    self.console.print(syntax)
                elif filepath.endswith('.md'):
                    with open(filepath, 'r') as f:
                        content = f.read()
                    self.console.print(Panel(content, title=name))
                else:
                    # Open HTML in default browser
                    import platform
                    system = platform.system()
                    if system == "Windows":
                        os.system(f'start "{filepath}"')
                    elif system == "Darwin":
                        os.system(f'open "{filepath}"')
                    else:
                        os.system(f'xdg-open "{filepath}" 2>/dev/null || sensible-browser "{filepath}"')
                    self.console.print(f"[green]Opened {name} in browser.[/green]")
            else:
                self.console.print("[red]Invalid selection.[/red]")
        except ValueError:
            self.console.print("[red]Please enter a number.[/red]")

    # ──────────────────────── Tool Selection UI ────────────────────────

    def show_tool_recommendations_and_select(self, tools: List[Dict]) -> List[Dict]:
        """Displays Rich table; parses user selection string."""
        # Sort: Kali pre-installed first, then by priority
        tools.sort(key=lambda t: (not t.get("kali_preinstalled", False),
                                   t.get("priority", 99)))

        table = Table(title="[bold]Recommended Security Tools[/bold]")
        table.add_column("#", style="cyan", width=4)
        table.add_column("Tool", style="green", min_width=12)
        table.add_column("Priority", style="yellow", width=8)
        table.add_column("Category", style="magenta", min_width=15)
        table.add_column("Purpose", style="white", min_width=30)
        table.add_column("Kali", style="green", width=6)

        for i, tool in enumerate(tools, 1):
            kali = "✓" if tool.get("kali_preinstalled") else "✗"
            kali_style = "[green]✓[/green]" if tool.get("kali_preinstalled") else "[red]✗[/red]"
            table.add_row(
                str(i),
                tool.get("name", "?"),
                str(tool.get("priority", "?")),
                tool.get("category", "?"),
                tool.get("educational_purpose", "")[:60],
                kali_style
            )

        self.console.print(table)

        self.console.print("\n[bold yellow]Selection options:[/bold yellow]")
        self.console.print("  [cyan]top3[/cyan]  — First 3 tools (Kali-prioritized) [default]")
        self.console.print("  [cyan]all[/cyan]   — First 5 tools (top-3 Kali + 2 additional)")
        self.console.print("  [cyan]kali[/cyan]  — Only Kali pre-installed tools")
        self.console.print("  [cyan]1,2,4[/cyan] — Specific tools by number")

        choice = self.console.input("\n[bold]Select tools [default: top3]: [/bold]").strip().lower() or "top3"

        if choice == "top3":
            return tools[:3]
        elif choice == "all":
            return tools[:5]
        elif choice == "kali":
            return [t for t in tools if t.get("kali_preinstalled")]
        else:
            try:
                indices = [int(x.strip()) - 1 for x in choice.split(",")]
                return [tools[i] for i in indices if 0 <= i < len(tools)]
            except (ValueError, IndexError):
                self.console.print("[yellow]Invalid selection, using top 3.[/yellow]")
                return tools[:3]

    # ──────────────────────── Execution Helper ────────────────────────

    def _execute_and_collect(self, target: str, tools: List[Dict],
                              scan_type: str) -> dict:
        """Execute tools and collect results into a structured dict."""
        results = {
            "target": target,
            "scan_type": scan_type,
            "timestamp": datetime.now().isoformat(),
            "tools_used": tools,
            "educational_insights": [],
            "tool_outputs": {},
            "ai_analysis": {}
        }

        self.console.print(f"\n[bold cyan]Executing {len(tools)} tool(s)...[/bold cyan]\n")

        for i, tool in enumerate(tools, 1):
            tool_name = tool.get("name", "unknown")
            command = tool.get("command", "")
            edu_purpose = tool.get("educational_purpose", "")

            self.console.print(f"[bold]({i}/{len(tools)}) Running {tool_name}...[/bold]")
            if edu_purpose:
                self.console.print(f"[dim]  Purpose: {edu_purpose}[/dim]")

            with Progress(SpinnerColumn(), TextColumn(f"[cyan]Executing {tool_name}..."),
                           console=self.console) as progress:
                task = progress.add_task("", total=None)
                result = self.engine.run_single_tool(tool_name, command, target)

            results["tool_outputs"][tool_name] = result

            if result["success"]:
                self.console.print(f"  [green]✓ {tool_name} completed ({result['execution_time']}s)[/green]")

                # Get AI analysis if available
                if self.ai_client and result.get("output"):
                    with Progress(SpinnerColumn(),
                                   TextColumn(f"[cyan]AI analyzing {tool_name} output..."),
                                   console=self.console) as progress:
                        task = progress.add_task("", total=None)
                        analysis = self.ai_client.analyze_tool_output(
                            tool_name, result["output"], target
                        )
                    results["ai_analysis"][tool_name] = analysis
                    self.console.print(Panel(analysis[:500],
                                              title=f"[cyan]AI Analysis — {tool_name}[/cyan]",
                                              border_style="blue"))
            else:
                self.console.print(
                    f"  [red]✗ {tool_name} failed: {result.get('error', 'Unknown error')}[/red]"
                )

            self.console.print()

        return results

    # ──────────────────────── Summary & Reports ────────────────────────

    def show_executive_summary(self, results: dict, target: str, scan_type: str):
        """Stats table + AI executive summary panel."""
        tool_outputs = results.get("tool_outputs", {})
        total = len(tool_outputs)
        successful = sum(1 for r in tool_outputs.values() if r.get("success"))
        failed = total - successful

        # Stats table
        table = Table(title="[bold]Session Statistics[/bold]")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        table.add_row("Target", target)
        table.add_row("Scan Type", scan_type)
        table.add_row("Tools Executed", str(total))
        table.add_row("Successful", f"[green]{successful}[/green]")
        table.add_row("Failed", f"[red]{failed}[/red]" if failed else "0")
        table.add_row("Success Rate",
                       f"{(successful/total*100):.0f}%" if total else "N/A")
        self.console.print(table)

        # Executive summary from AI
        if self.ai_client:
            with Progress(SpinnerColumn(),
                           TextColumn("[cyan]Generating executive summary..."),
                           console=self.console) as progress:
                task = progress.add_task("", total=None)
                summary = self.ai_client.generate_executive_summary(results)
            results["executive_summary"] = summary
            self.console.print(Panel(summary, title="[bold cyan]Executive Summary[/bold cyan]",
                                      border_style="cyan"))
        else:
            results["executive_summary"] = "AI executive summary unavailable."

    def generate_reports(self, results: dict, target: str, scan_type: str):
        """Loops configured formats; calls ReportGenerator."""
        formats = self.config_manager.get_report_formats()
        output_dir = self.config_manager.get_output_dir()

        # Build filename
        safe_target = target.replace(".", "_").replace("/", "_").replace(":", "_")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_filename = f"aegissec_{safe_target}_{scan_type}_{timestamp}"

        self.console.print(f"\n[bold cyan]Generating reports...[/bold cyan]")
        for fmt in formats:
            filepath = self.report_gen.generate_report(results, output_dir,
                                                        base_filename, fmt)
            if filepath:
                self.console.print(f"  [green]✓ {fmt.upper()} report saved: {filepath}[/green]")
            else:
                self.console.print(f"  [yellow]⊘ {fmt.upper()} report: not yet implemented[/yellow]")

    # ──────────────────────── Helpers ────────────────────────

    def _prompt_target(self) -> Optional[str]:
        """Prompt and validate target."""
        target = self.console.input(
            "\n[bold yellow]Enter target IP or domain: [/bold yellow]"
        ).strip()
        if not target:
            self.console.print("[red]No target provided.[/red]")
            return None
        if not self._validate_target(target):
            self.console.print("[red]Invalid target format. Use an IP address or domain name.[/red]")
            return None
        return target

    def _validate_target(self, target: str) -> bool:
        """Regex check: valid IPv4 / domain / localhost."""
        # IPv4
        ipv4 = re.compile(
            r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}'
            r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
        )
        # Domain
        domain = re.compile(
            r'^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$'
        )
        # Localhost
        if target in ('localhost', '127.0.0.1'):
            return True
        return bool(ipv4.match(target) or domain.match(target))

    def _get_fallback_tools(self, target: str) -> List[Dict]:
        """Returns 3-tool hardcoded list when AI unavailable."""
        return [
            {
                "name": "nmap",
                "command": f"nmap -sV -sC {target}",
                "educational_purpose": "Network reconnaissance and port scanning",
                "category": "reconnaissance",
                "kali_preinstalled": True,
                "priority": 1
            },
            {
                "name": "nikto",
                "command": f"nikto -h {target}",
                "educational_purpose": "Web server vulnerability scanning",
                "category": "vulnerability_analysis",
                "kali_preinstalled": True,
                "priority": 2
            },
            {
                "name": "dirb",
                "command": f"dirb http://{target}",
                "educational_purpose": "Directory and file enumeration",
                "category": "enumeration",
                "kali_preinstalled": True,
                "priority": 3
            }
        ]
