"""
AegisSec v2.0 — AI Advisor Test
Tests the DeepSeekClient.get_ai_advisor_response() function.
"""

import sys
sys.path.insert(0, '.')

from src.config_manager import ConfigManager
from src.deepseek_client import DeepSeekClient
from rich.console import Console
from rich.panel import Panel

console = Console()


def test_ai_advisor():
    config = ConfigManager()
    api_key = config.get_api_key()

    if not api_key:
        console.print("[red]No API key configured. Run main.py first to set up.[/red]")
        return

    client = DeepSeekClient(api_key)

    test_questions = [
        "What is nmap and how is it used in penetration testing?",
        "Explain the difference between active and passive reconnaissance.",
        "What are the OWASP Top 10 vulnerabilities?"
    ]

    for question in test_questions:
        console.print(f"\n[bold yellow]Question:[/bold yellow] {question}")
        response = client.get_ai_advisor_response(question)
        console.print(Panel(response, title="AI Response", border_style="cyan"))


if __name__ == "__main__":
    test_ai_advisor()
