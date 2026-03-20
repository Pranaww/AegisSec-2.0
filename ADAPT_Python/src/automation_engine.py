"""
AegisSec v2.0 — Automation Engine
Handles subprocess-level execution of security tools with timeout management,
availability checking, and optional AI-guided intelligent chaining.
"""

import subprocess
import time
from typing import Dict, List, Optional


class AutomationEngine:
    """Handles subprocess execution of security tools."""

    def __init__(self, ai_client=None):
        self.ai_client = ai_client
        self.timeout_default = 300
        self.session_results: Dict[str, dict] = {}
        self.tool_check_commands = {
            'nmap': ['nmap', '--version'],
            'nikto': ['nikto', '-Version'],
            'dirb': ['dirb'],
            'gobuster': ['gobuster', 'version'],
            'sqlmap': ['sqlmap', '--version'],
            'hydra': ['hydra', '-h'],
            'john': ['john', '--version'],
            'metasploit': ['msfconsole', '--version'],
            'burpsuite': ['burpsuite', '--version'],
            'wpscan': ['wpscan', '--version']
        }

    def _check_tool_availability(self, tool_name: str) -> bool:
        """Runs tool --version with 10s timeout; returns bool."""
        check_cmd = self.tool_check_commands.get(tool_name)
        if not check_cmd:
            # Try generic --version
            check_cmd = [tool_name, '--version']

        try:
            result = subprocess.run(
                check_cmd,
                capture_output=True,
                timeout=10,
                text=True
            )
            return True  # If it doesn't throw, the tool exists
        except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
            return False
        except subprocess.CalledProcessError:
            # Some tools return non-zero even for --version but still exist
            return True

    def run_single_tool(self, tool_name: str, command: str, target: str,
                        timeout: int = None) -> dict:
        """Checks availability → executes → returns result dict."""
        if timeout is None:
            timeout = self.timeout_default

        result = {
            "tool": tool_name,
            "command": command,
            "success": False,
            "output": "",
            "error": None,
            "execution_time": 0.0,
            "educational_note": ""
        }

        # Step 1: Check availability
        if not self._check_tool_availability(tool_name):
            result["error"] = (
                f"Tool '{tool_name}' is not installed on this system. "
                f"Install it using your package manager (e.g., apt install {tool_name})."
            )
            result["educational_note"] = (
                f"The tool '{tool_name}' was not found. On Kali Linux, most security "
                "tools come pre-installed. On other systems, you may need to install them manually."
            )
            return result

        # Step 2: Execute
        start_time = time.time()
        try:
            proc = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            result["execution_time"] = round(time.time() - start_time, 2)

            if proc.returncode == 0:
                result["success"] = True
                result["output"] = proc.stdout or ""
                result["educational_note"] = (
                    f"Successfully executed {tool_name} for cybersecurity learning. "
                    "Review the output to understand what the tool discovered."
                )
            else:
                result["output"] = proc.stdout or ""
                result["error"] = proc.stderr or f"Tool exited with code {proc.returncode}"
                result["educational_note"] = (
                    f"{tool_name} returned a non-zero exit code. This sometimes indicates "
                    "partial results or an error. Check the output and error messages."
                )
                # Some tools return non-zero but still produce useful output
                if result["output"]:
                    result["success"] = True

        except subprocess.TimeoutExpired:
            result["execution_time"] = round(time.time() - start_time, 2)
            result["error"] = f"Tool timed out after {timeout} seconds."
            result["educational_note"] = (
                f"{tool_name} exceeded the {timeout}s timeout. This can happen with "
                "thorough scans on large networks. Try reducing the scan scope."
            )
        except subprocess.CalledProcessError as e:
            result["execution_time"] = round(time.time() - start_time, 2)
            result["error"] = str(e)
        except Exception as e:
            result["execution_time"] = round(time.time() - start_time, 2)
            result["error"] = f"Unexpected error: {str(e)}"

        self.session_results[tool_name] = result
        return result

    def run_tools(self, tools: List[Dict], target: str) -> List[dict]:
        """Sequential execution of tool list; accumulates stats."""
        results = []
        for tool in tools:
            tool_name = tool.get("name", "unknown")
            command = tool.get("command", "")
            result = self.run_single_tool(tool_name, command, target)
            results.append(result)
        return results

    def run_intelligent_tools(self, tools: List[Dict], target: str) -> List[dict]:
        """Like run_tools but calls AI analysis after each successful tool."""
        results = []
        for tool in tools:
            tool_name = tool.get("name", "unknown")
            command = tool.get("command", "")
            result = self.run_single_tool(tool_name, command, target)

            if result["success"] and self.ai_client and result["output"]:
                try:
                    analysis = self.ai_client.analyze_tool_output(
                        tool_name, result["output"], target
                    )
                    result["ai_analysis"] = analysis
                except Exception:
                    result["ai_analysis"] = "AI analysis unavailable."

            results.append(result)
        return results

    def get_session_summary(self) -> dict:
        """Returns count and results of all tools run this session."""
        total = len(self.session_results)
        successful = sum(1 for r in self.session_results.values() if r.get("success"))
        return {
            "total_tools_run": total,
            "successful": successful,
            "failed": total - successful,
            "results": dict(self.session_results)
        }

    def _get_available_tools(self) -> List[str]:
        """Checks all 10 known tools; returns available list."""
        available = []
        for tool in self.tool_check_commands:
            if self._check_tool_availability(tool):
                available.append(tool)
        return available

    def cleanup_session(self):
        """Clears session_results."""
        self.session_results.clear()
