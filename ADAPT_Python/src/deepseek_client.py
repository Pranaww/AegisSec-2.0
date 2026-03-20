"""
AegisSec v2.0 — DeepSeek AI Client
Handles all communication with OpenRouter's API using the DeepSeek model.
"""

import json
import requests
from typing import List, Dict, Optional


class DeepSeekClient:
    """Handles all communication with OpenRouter's API using deepseek/deepseek-chat-v3.1:free."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://openrouter.ai/api/v1"
        self.model = "deepseek/deepseek-chat-v3.1:free"
        self.kali_priority_tools = ["nmap", "nikto", "dirb"]
        self.extended_tools = [
            "gobuster", "sqlmap", "hydra", "metasploit",
            "burpsuite", "wpscan", "john"
        ]

    def _make_api_call(self, messages: list, temperature: float = 0.7,
                       max_tokens: int = 1500, timeout: int = 30) -> Optional[str]:
        """Makes a POST request to the OpenRouter API."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://aegissec.local",
            "X-Title": "AegisSec v2.0"
        }
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=timeout
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
        except requests.exceptions.Timeout:
            print("[AI] Request timed out.")
            return None
        except requests.exceptions.HTTPError as e:
            print(f"[AI] HTTP error: {e}")
            return None
        except Exception as e:
            print(f"[AI] Unexpected error: {e}")
            return None

    def get_tool_recommendations(self, target: str, scan_type: str = "comprehensive") -> List[Dict]:
        """Sends structured prompt; parses JSON array of 10 tool objects."""
        system_prompt = (
            "You are AegisSec, an expert cybersecurity AI assistant designed for educational penetration testing. "
            "You recommend security tools and explain their educational value. Always prioritize Kali Linux pre-installed tools. "
            "Respond ONLY with a valid JSON array of tool objects."
        )
        user_prompt = f"""Recommend up to 10 security tools for scanning target: {target}
Scan type: {scan_type}

Return a JSON array where each object has these exact keys:
- "name": tool name (string)
- "command": full command to run against the target (string)
- "educational_purpose": what the student learns from this tool (string)
- "learning_value": deeper educational context (string)
- "category": one of "reconnaissance", "vulnerability_analysis", "enumeration", "exploitation" (string)
- "kali_preinstalled": whether the tool comes with Kali Linux (boolean)
- "priority": priority rank 1-10, lower is higher priority (integer)

Prioritize these Kali pre-installed tools: nmap, nikto, dirb.
Then include extended tools like: gobuster, sqlmap, hydra, wpscan, john.

Respond with ONLY the JSON array, no markdown, no explanation."""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        response = self._make_api_call(messages, temperature=0.7,
                                        max_tokens=2000, timeout=30)
        if response:
            try:
                # Try to extract JSON from the response
                text = response.strip()
                if text.startswith("```"):
                    # Strip markdown code fences
                    lines = text.split("\n")
                    text = "\n".join(lines[1:-1])
                tools = json.loads(text)
                if isinstance(tools, list) and len(tools) > 0:
                    return tools
            except json.JSONDecodeError:
                pass

        return self._get_fallback_tools(target)

    def analyze_tool_output(self, tool_name: str, output: str, target: str) -> str:
        """Sends first 1000 chars of output; returns plain-text technical analysis."""
        truncated = output[:1000] if output else "No output captured."
        system_prompt = (
            "You are a cybersecurity education AI. Analyze the following security tool output "
            "and provide: 1) what was found, 2) security implications, 3) educational explanation, "
            "4) recommended next steps. Keep the response concise and educational."
        )
        user_prompt = f"""Tool: {tool_name}
Target: {target}
Output (truncated):
{truncated}

Provide a concise educational analysis of this output."""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        response = self._make_api_call(messages, temperature=0.6,
                                        max_tokens=800, timeout=25)
        return response or "AI analysis unavailable — review the raw output above for findings."

    def generate_executive_summary(self, results: dict) -> str:
        """Generates full learning-focused summary from complete results dict."""
        tools_summary = []
        for tool_name, result in results.get("tool_outputs", {}).items():
            status = "✓ Success" if result.get("success") else "✗ Failed"
            tools_summary.append(f"- {tool_name}: {status}")

        system_prompt = (
            "You are a cybersecurity education AI. Generate a comprehensive executive summary "
            "of a penetration test. Include 5 sections: 1) Learning Achievements, "
            "2) Key Findings, 3) Security Insights, 4) Hands-On Experience Gained, "
            "5) Recommended Next Steps. Make it educational and encouraging."
        )
        user_prompt = f"""Penetration test completed against: {results.get('target', 'unknown')}
Scan type: {results.get('scan_type', 'comprehensive')}
Tools run:
{chr(10).join(tools_summary)}

Generate a comprehensive educational executive summary."""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        response = self._make_api_call(messages, temperature=0.8,
                                        max_tokens=1500, timeout=30)
        return response or self._get_fallback_summary()

    def get_ai_advisor_response(self, query: str, context: str = "") -> str:
        """Open Q&A endpoint; cybersecurity mentor role."""
        system_prompt = (
            "You are AegisSec, a friendly and knowledgeable cybersecurity mentor. "
            "You help students learn about ethical hacking, security tools, techniques, "
            "and concepts. Always frame your answers in an educational context. "
            "Provide practical examples when possible."
        )
        user_prompt = query
        if context:
            user_prompt = f"Context: {context}\n\nQuestion: {query}"

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        response = self._make_api_call(messages, temperature=0.7,
                                        max_tokens=1000, timeout=20)
        return response or "I'm unable to reach the AI service right now. Please check your internet connection and API key."

    def _get_fallback_tools(self, target: str) -> List[Dict]:
        """Returns 5 hardcoded tool dicts when AI is unavailable."""
        return [
            {
                "name": "nmap",
                "command": f"nmap -sV -sC -O {target}",
                "educational_purpose": "Learn network reconnaissance and port scanning fundamentals",
                "learning_value": "Foundation of all penetration testing — discover open ports, running services, and OS fingerprinting",
                "category": "reconnaissance",
                "kali_preinstalled": True,
                "priority": 1
            },
            {
                "name": "nikto",
                "command": f"nikto -h {target}",
                "educational_purpose": "Learn web server vulnerability scanning",
                "learning_value": "Understand common web server misconfigurations and vulnerabilities",
                "category": "vulnerability_analysis",
                "kali_preinstalled": True,
                "priority": 2
            },
            {
                "name": "dirb",
                "command": f"dirb http://{target}",
                "educational_purpose": "Learn directory and file enumeration on web servers",
                "learning_value": "Discover hidden directories and files that may expose sensitive information",
                "category": "enumeration",
                "kali_preinstalled": True,
                "priority": 3
            },
            {
                "name": "gobuster",
                "command": f"gobuster dir -u http://{target} -w /usr/share/wordlists/dirb/common.txt",
                "educational_purpose": "Learn advanced directory/DNS/vhost enumeration",
                "learning_value": "Modern alternative to dirb with concurrent scanning capabilities",
                "category": "enumeration",
                "kali_preinstalled": False,
                "priority": 4
            },
            {
                "name": "sqlmap",
                "command": f"sqlmap -u http://{target} --batch --crawl=2",
                "educational_purpose": "Learn SQL injection detection and exploitation",
                "learning_value": "Understand how SQL injection works and how to detect it automatically",
                "category": "vulnerability_analysis",
                "kali_preinstalled": False,
                "priority": 5
            }
        ]

    def _get_fallback_summary(self) -> str:
        """Returns hardcoded encouraging educational summary text."""
        return """## Executive Summary

### Learning Achievements
You've completed a penetration testing exercise, gaining hands-on experience with real security tools.

### Key Findings
Review the individual tool outputs above for specific findings about your target.

### Security Insights
Every scan reveals information about the target's security posture. Even "no findings" is valuable — it means the target has good defenses in that area.

### Hands-On Experience
Running these tools in a controlled environment builds the practical skills needed for cybersecurity careers.

### Recommended Next Steps
1. Analyze each tool's output carefully
2. Research any vulnerabilities found
3. Try different scan types and tool combinations
4. Practice on authorized targets like HackTheBox or TryHackMe"""
