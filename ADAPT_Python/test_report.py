"""
AegisSec v2.0 — Report Generator Test
Tests ReportGenerator for all formats (HTML, JSON, Markdown).
"""

import sys
import os
sys.path.insert(0, '.')

from src.report_generator import ReportGenerator
from rich.console import Console
from datetime import datetime

console = Console()


def test_reports():
    console.print("[bold cyan]Testing Report Generator[/bold cyan]\n")

    gen = ReportGenerator()

    # Create sample results
    results = {
        "target": "192.168.1.1",
        "scan_type": "comprehensive",
        "timestamp": datetime.now().isoformat(),
        "tools_used": [
            {"name": "nmap", "kali_preinstalled": True, "priority": 1},
            {"name": "nikto", "kali_preinstalled": True, "priority": 2},
        ],
        "educational_insights": [
            "Port scanning reveals the attack surface of a target system.",
            "Web vulnerability scanning identifies common misconfigurations."
        ],
        "tool_outputs": {
            "nmap": {
                "tool": "nmap",
                "command": "nmap -sV -sC 192.168.1.1",
                "success": True,
                "output": "PORT   STATE SERVICE VERSION\n22/tcp open  ssh     OpenSSH 8.2\n80/tcp open  http    Apache 2.4.41\n443/tcp open  https   nginx 1.18",
                "error": None,
                "execution_time": 12.5,
                "educational_note": "Nmap discovered 3 open ports on the target."
            },
            "nikto": {
                "tool": "nikto",
                "command": "nikto -h 192.168.1.1",
                "success": True,
                "output": "- Server: Apache/2.4.41\n+ /admin: Admin directory found\n+ X-Frame-Options header not set",
                "error": None,
                "execution_time": 25.3,
                "educational_note": "Nikto found potential web misconfigurations."
            }
        },
        "ai_analysis": {
            "nmap": "The scan reveals SSH on port 22 and web services on ports 80/443. This is a common configuration for web servers.",
            "nikto": "The exposed /admin directory and missing X-Frame-Options header are security concerns to investigate."
        },
        "executive_summary": "This penetration test scanned the target and discovered open ports and web vulnerabilities demonstrating key security concepts."
    }

    output_dir = os.path.join(os.path.dirname(__file__), "test_reports")
    base = f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    for fmt in ['html', 'json', 'markdown']:
        path = gen.generate_report(results, output_dir, base, fmt)
        if path:
            console.print(f"  [green]✓ {fmt.upper()}: {path}[/green]")
        else:
            console.print(f"  [red]✗ {fmt.upper()}: Failed[/red]")

    console.print("\n[bold green]Report generation test complete![/bold green]")


if __name__ == "__main__":
    test_reports()
