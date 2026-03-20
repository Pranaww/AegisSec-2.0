"""
AegisSec v2.0 — Configuration Manager
Manages persistent user settings using a JSON file at ~/.aegissec/config.json
"""

import json
import os
from pathlib import Path


class ConfigManager:
    """Manages all persistent user settings using a JSON file."""

    def __init__(self):
        self.config_dir = Path.home() / ".aegissec"
        self.config_file = self.config_dir / "config.json"
        self.default_config = {
            "openrouter_api_key": "",
            "default_output_dir": str(Path.home() / "aegissec_reports"),
            "educational_mode": True,
            "auto_generate_reports": True,
            "preferred_tools": ["nmap", "nikto", "dirb"],
            "timeout_settings": {
                "tool_timeout": 300,
                "ai_timeout": 30
            },
            "report_formats": ["html", "json"],
            "kali_mode": True
        }
        self.config = self.load_config()

    def is_configured(self) -> bool:
        """True if config file exists and API key is non-empty."""
        if not self.config_file.exists():
            return False
        return bool(self.config.get("openrouter_api_key", ""))

    def load_config(self) -> dict:
        """Reads JSON; merges with defaults for missing keys."""
        if self.config_file.exists():
            try:
                with open(self.config_file, "r") as f:
                    user_config = json.load(f)
                # Merge with defaults (defaults fill missing keys)
                merged = {**self.default_config, **user_config}
                # Merge nested timeout_settings
                merged["timeout_settings"] = {
                    **self.default_config["timeout_settings"],
                    **user_config.get("timeout_settings", {})
                }
                return merged
            except (json.JSONDecodeError, IOError):
                return dict(self.default_config)
        return dict(self.default_config)

    def save_config(self, config: dict = None):
        """Writes dict to JSON with indent=2."""
        if config:
            self.config = config
        self.config_dir.mkdir(parents=True, exist_ok=True)
        with open(self.config_file, "w") as f:
            json.dump(self.config, f, indent=2)

    def setup(self):
        """Interactive wizard: API key, output dir, modes, report formats."""
        from rich.console import Console
        from rich.panel import Panel
        console = Console()

        console.print(Panel("[bold cyan]AegisSec v2.0 — First-Time Setup[/bold cyan]",
                            subtitle="Configuration Wizard"))

        # 1. API Key
        api_key = console.input(
            "[bold yellow]Enter your OpenRouter API key: [/bold yellow]").strip()
        if api_key:
            self.config["openrouter_api_key"] = api_key

        # 2. Output directory
        default_dir = self.config["default_output_dir"]
        output_dir = console.input(
            f"[bold yellow]Report output directory [default: {default_dir}]: [/bold yellow]").strip()
        if output_dir:
            self.config["default_output_dir"] = output_dir

        # 3. Educational mode
        edu = console.input(
            "[bold yellow]Enable educational mode? (y/n) [default: y]: [/bold yellow]").strip().lower()
        self.config["educational_mode"] = edu != "n"

        # 4. Kali mode
        kali = console.input(
            "[bold yellow]Enable Kali Linux optimization? (y/n) [default: y]: [/bold yellow]").strip().lower()
        self.config["kali_mode"] = kali != "n"

        # 5. Report formats
        fmt = console.input(
            "[bold yellow]Report formats (comma-separated: html,json,markdown,pdf) [default: html,json]: [/bold yellow]").strip()
        if fmt:
            self.config["report_formats"] = [f.strip() for f in fmt.split(",")]

        self.save_config()
        console.print("[bold green]✓ Configuration saved successfully![/bold green]")

    def get_api_key(self) -> str:
        return self.config.get("openrouter_api_key", "")

    def get_output_dir(self) -> str:
        output_dir = self.config.get("default_output_dir",
                                     str(Path.home() / "aegissec_reports"))
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        return output_dir

    def is_educational_mode(self) -> bool:
        return self.config.get("educational_mode", True)

    def is_kali_mode(self) -> bool:
        return self.config.get("kali_mode", True)

    def get_report_formats(self) -> list:
        return self.config.get("report_formats", ["html", "json"])

    def get_timeout_settings(self) -> dict:
        return self.config.get("timeout_settings",
                               {"tool_timeout": 300, "ai_timeout": 30})
