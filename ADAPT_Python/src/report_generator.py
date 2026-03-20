"""
AegisSec v2.0 — Report Generator
Generates polished output reports in multiple formats: HTML, JSON, Markdown, PDF.
"""

import json
import html
import os
from datetime import datetime
from pathlib import Path
from typing import Optional


class ReportGenerator:
    """Generates polished output reports in multiple formats."""

    def __init__(self):
        self.supported_formats = ['html', 'json', 'markdown', 'pdf']

    def generate_report(self, results: dict, output_dir: str,
                        base_filename: str, format_type: str) -> Optional[str]:
        """Dispatcher: routes to format-specific method."""
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        if format_type == 'html':
            return self._generate_enhanced_html_report(results, output_dir, base_filename)
        elif format_type == 'json':
            return self._generate_json_report(results, output_dir, base_filename)
        elif format_type == 'markdown':
            return self._generate_markdown_report(results, output_dir, base_filename)
        elif format_type == 'pdf':
            return self._generate_pdf_report(results, output_dir, base_filename)
        return None

    def _generate_enhanced_html_report(self, results: dict, output_dir: str,
                                        base_filename: str) -> str:
        """Full-featured CSS-styled HTML with sections."""
        filepath = os.path.join(output_dir, f"{base_filename}.html")

        target = results.get("target", "Unknown")
        scan_type = results.get("scan_type", "comprehensive")
        timestamp = results.get("timestamp", datetime.now().isoformat())
        tool_outputs = results.get("tool_outputs", {})
        ai_analysis = results.get("ai_analysis", {})
        exec_summary = results.get("executive_summary", "")

        # Build tool cards HTML
        tools_html = self._generate_tools_html(tool_outputs, ai_analysis)
        summary_html = self._generate_executive_summary_html(exec_summary)
        insights_html = self._generate_educational_insights_html(results)
        stats_html = self._generate_stats_html(results)

        template = self._get_enhanced_html_template()
        final_html = template.format(
            target=html.escape(target),
            scan_type=html.escape(scan_type),
            timestamp=html.escape(str(timestamp)),
            stats_section=stats_html,
            executive_summary_section=summary_html,
            educational_insights_section=insights_html,
            tools_section=tools_html
        )

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(final_html)
        return filepath

    def _generate_json_report(self, results: dict, output_dir: str,
                               base_filename: str) -> str:
        """Serializes results dict to indented JSON."""
        filepath = os.path.join(output_dir, f"{base_filename}.json")
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, default=str)
        return filepath

    def _generate_markdown_report(self, results: dict, output_dir: str,
                                   base_filename: str) -> str:
        """Structured Markdown with tables and code blocks."""
        filepath = os.path.join(output_dir, f"{base_filename}.md")
        target = results.get("target", "Unknown")
        scan_type = results.get("scan_type", "comprehensive")
        timestamp = results.get("timestamp", datetime.now().isoformat())

        md = f"""# AegisSec Penetration Test Report

**Target:** {target}
**Scan Type:** {scan_type}
**Timestamp:** {timestamp}

---

## Executive Summary

{results.get("executive_summary", "No executive summary available.")}

---

## Tool Results

| Tool | Status | Execution Time |
|------|--------|---------------|
"""
        tool_outputs = results.get("tool_outputs", {})
        for tool_name, result in tool_outputs.items():
            status = "✓ Success" if result.get("success") else "✗ Failed"
            exec_time = f"{result.get('execution_time', 0)}s"
            md += f"| {tool_name} | {status} | {exec_time} |\n"

        md += "\n---\n\n## Detailed Results\n\n"
        ai_analysis = results.get("ai_analysis", {})

        for tool_name, result in tool_outputs.items():
            md += f"### {tool_name}\n\n"
            md += f"**Command:** `{result.get('command', 'N/A')}`\n\n"

            if result.get("output"):
                md += f"**Output:**\n```\n{result['output'][:2000]}\n```\n\n"
            if result.get("error"):
                md += f"**Error:** {result['error']}\n\n"
            if tool_name in ai_analysis:
                md += f"**AI Analysis:**\n{ai_analysis[tool_name]}\n\n"
            md += "---\n\n"

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(md)
        return filepath

    def _generate_pdf_report(self, results: dict, output_dir: str,
                              base_filename: str) -> Optional[str]:
        """Planned/stubbed."""
        # PDF generation requires additional libraries (reportlab, weasyprint, etc.)
        # This is stubbed for future implementation.
        return None

    def _get_enhanced_html_template(self) -> str:
        """Returns the full HTML+CSS template string."""
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AegisSec Report — {target}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #0a0e17;
            color: #e0e6ed;
            line-height: 1.6;
        }}
        .header {{
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            padding: 40px;
            text-align: center;
            border-bottom: 3px solid #00d4ff;
        }}
        .header h1 {{
            font-size: 2.5em;
            color: #00d4ff;
            text-shadow: 0 0 20px rgba(0,212,255,0.3);
        }}
        .header .subtitle {{ color: #8892b0; margin-top: 10px; font-size: 1.1em; }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 30px; }}
        .overview {{
            background: #1a1a2e;
            border-radius: 10px;
            padding: 25px;
            margin: 20px 0;
            border: 1px solid #2a2a4a;
        }}
        .overview h2 {{ color: #00d4ff; margin-bottom: 15px; }}
        .overview-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
        }}
        .overview-item {{ background: #0d1117; padding: 15px; border-radius: 8px; }}
        .overview-item .label {{ color: #8892b0; font-size: 0.9em; }}
        .overview-item .value {{ color: #e6f1ff; font-size: 1.1em; font-weight: bold; margin-top: 5px; }}
        .stat-cards {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }}
        .stat-card {{
            background: linear-gradient(135deg, #1a1a2e, #16213e);
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            border: 1px solid #2a2a4a;
            transition: transform 0.2s;
        }}
        .stat-card:hover {{ transform: translateY(-3px); }}
        .stat-card .number {{ font-size: 2em; font-weight: bold; color: #00d4ff; }}
        .stat-card .label {{ color: #8892b0; margin-top: 5px; }}
        .section {{ margin: 30px 0; }}
        .section h2 {{
            color: #00d4ff;
            font-size: 1.5em;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 1px solid #2a2a4a;
        }}
        .summary-box {{
            background: #1a1a2e;
            border-radius: 10px;
            padding: 25px;
            border-left: 4px solid #00d4ff;
            white-space: pre-wrap;
        }}
        .tool-card {{
            background: #1a1a2e;
            border-radius: 10px;
            margin: 20px 0;
            border: 1px solid #2a2a4a;
            overflow: hidden;
            transition: transform 0.2s;
        }}
        .tool-card:hover {{ transform: translateY(-2px); box-shadow: 0 5px 20px rgba(0,0,0,0.3); }}
        .tool-card-header {{
            background: #16213e;
            padding: 15px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .tool-card-header h3 {{ color: #e6f1ff; }}
        .tool-status {{
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: bold;
        }}
        .status-success {{ background: #1a4731; color: #4ade80; }}
        .status-failed {{ background: #4a1a1a; color: #f87171; }}
        .tool-card-body {{ padding: 20px; }}
        .command-box {{
            background: #0d1117;
            padding: 12px 15px;
            border-radius: 6px;
            font-family: 'Courier New', monospace;
            color: #79c0ff;
            margin: 10px 0;
            overflow-x: auto;
        }}
        .output-box {{
            background: #0d1117;
            padding: 15px;
            border-radius: 6px;
            font-family: 'Courier New', monospace;
            color: #4ade80;
            margin: 10px 0;
            max-height: 300px;
            overflow-y: auto;
            white-space: pre-wrap;
            font-size: 0.85em;
        }}
        .analysis-box {{
            background: #0d1117;
            padding: 15px;
            border-radius: 6px;
            border-left: 3px solid #3b82f6;
            margin: 10px 0;
            color: #93c5fd;
            white-space: pre-wrap;
        }}
        .learning-box {{
            background: #1a1a0d;
            padding: 15px;
            border-radius: 6px;
            border-left: 3px solid #fbbf24;
            margin: 10px 0;
            color: #fde68a;
        }}
        .footer {{
            text-align: center;
            padding: 30px;
            color: #8892b0;
            border-top: 1px solid #2a2a4a;
            margin-top: 40px;
        }}
        @media (max-width: 768px) {{
            .header h1 {{ font-size: 1.8em; }}
            .container {{ padding: 15px; }}
            .stat-cards {{ grid-template-columns: repeat(2, 1fr); }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🛡️ AegisSec Report</h1>
        <div class="subtitle">AI-Powered Penetration Testing Platform — Educational Report</div>
    </div>
    <div class="container">
        <div class="overview">
            <h2>Assessment Overview</h2>
            <div class="overview-grid">
                <div class="overview-item">
                    <div class="label">Target</div>
                    <div class="value">{target}</div>
                </div>
                <div class="overview-item">
                    <div class="label">Scan Type</div>
                    <div class="value">{scan_type}</div>
                </div>
                <div class="overview-item">
                    <div class="label">Timestamp</div>
                    <div class="value">{timestamp}</div>
                </div>
            </div>
        </div>

        {stats_section}

        <div class="section">
            <h2>📋 Executive Summary</h2>
            {executive_summary_section}
        </div>

        <div class="section">
            <h2>📚 Educational Insights</h2>
            {educational_insights_section}
        </div>

        <div class="section">
            <h2>🔧 Tool Results</h2>
            {tools_section}
        </div>
    </div>
    <div class="footer">
        <p>Generated by AegisSec v2.0 — RunTime Terrors Team</p>
        <p>For educational purposes only. Always obtain proper authorization before testing.</p>
    </div>
</body>
</html>"""

    def _generate_tools_html(self, tool_outputs: dict, ai_analysis: dict) -> str:
        """Renders per-tool cards with command, output, AI analysis."""
        cards = []
        for tool_name, result in tool_outputs.items():
            success = result.get("success", False)
            status_class = "status-success" if success else "status-failed"
            status_text = "✓ Success" if success else "✗ Failed"

            command = html.escape(result.get("command", "N/A"))
            output = html.escape(result.get("output", "No output.")[:3000])
            error = result.get("error", "")
            exec_time = result.get("execution_time", 0)
            edu_note = result.get("educational_note", "")

            analysis = html.escape(ai_analysis.get(tool_name, ""))

            card = f"""<div class="tool-card">
    <div class="tool-card-header">
        <h3>🔹 {html.escape(tool_name)}</h3>
        <span class="tool-status {status_class}">{status_text} ({exec_time}s)</span>
    </div>
    <div class="tool-card-body">
        <strong>Command:</strong>
        <div class="command-box">$ {command}</div>
        <strong>Output:</strong>
        <div class="output-box">{output}</div>"""

            if error:
                card += f'\n        <strong>Error:</strong>\n        <div class="output-box" style="color: #f87171;">{html.escape(error)}</div>'

            if analysis:
                card += f'\n        <strong>AI Analysis:</strong>\n        <div class="analysis-box">{analysis}</div>'

            if edu_note:
                card += f'\n        <div class="learning-box">📖 <strong>Learning Note:</strong> {html.escape(edu_note)}</div>'

            card += "\n    </div>\n</div>"
            cards.append(card)

        return "\n".join(cards)

    def _generate_executive_summary_html(self, summary: str) -> str:
        """Renders executive summary section."""
        if summary:
            return f'<div class="summary-box">{html.escape(summary)}</div>'
        return '<div class="summary-box">No executive summary available.</div>'

    def _generate_educational_insights_html(self, results: dict) -> str:
        """Renders learning callout boxes."""
        insights = results.get("educational_insights", [])
        if not insights:
            return '<div class="learning-box">📖 Complete the scan to see educational insights.</div>'

        boxes = []
        for insight in insights:
            boxes.append(f'<div class="learning-box">📖 {html.escape(str(insight))}</div>')
        return "\n".join(boxes)

    def _generate_stats_html(self, results: dict) -> str:
        """Renders stat cards for quick metrics."""
        tool_outputs = results.get("tool_outputs", {})
        total = len(tool_outputs)
        successful = sum(1 for r in tool_outputs.values() if r.get("success"))
        failed = total - successful
        success_rate = f"{(successful/total*100):.0f}%" if total > 0 else "0%"

        kali_tools = sum(1 for t in results.get("tools_used", [])
                         if isinstance(t, dict) and t.get("kali_preinstalled"))

        return f"""<div class="stat-cards">
    <div class="stat-card">
        <div class="number">{total}</div>
        <div class="label">Tools Run</div>
    </div>
    <div class="stat-card">
        <div class="number">{successful}</div>
        <div class="label">Successful</div>
    </div>
    <div class="stat-card">
        <div class="number">{failed}</div>
        <div class="label">Failed</div>
    </div>
    <div class="stat-card">
        <div class="number">{success_rate}</div>
        <div class="label">Success Rate</div>
    </div>
    <div class="stat-card">
        <div class="number">{kali_tools}</div>
        <div class="label">Kali Tools</div>
    </div>
</div>"""
