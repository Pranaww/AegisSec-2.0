# AegisSec v2.0

**AI-Powered Educational Penetration Testing Platform**
*By RunTime Terrors Team*

---

## Overview

AegisSec is an AI-powered, educational penetration testing automation platform that integrates the **DeepSeek AI model** (via OpenRouter API) with standard Kali Linux security tools to create an end-to-end guided cybersecurity learning environment.

## Features

- **AI-Guided Scanning** — DeepSeek AI recommends and prioritizes security tools
- **Automated Execution** — Tools run as real system processes with captured output
- **Educational Analysis** — AI explains every tool output in plain language
- **Multi-Format Reports** — HTML, JSON, and Markdown with AI insights embedded
- **Interactive Mentor** — Free-form cybersecurity Q&A with AI
- **Cross-Platform** — Windows, Linux, and Kali Linux support

## Quick Start

### Prerequisites
- Python 3.10+
- OpenRouter API key (free at [openrouter.ai](https://openrouter.ai))
- Recommended: Kali Linux for full tool availability

### Installation

```bash
git clone https://github.com/Pranaww/AegisSec-2.0.git
cd AegisSec-2.0/ADAPT_Python
pip install -r requirements.txt
python main.py
```

Or use the launcher scripts:

```bash
# Linux / Kali
chmod +x run.sh && ./run.sh

# Windows
run.bat
```

## Project Structure

```
AegisSec/
├── main.py                    # Entry point — banner, menu, bootstrap
├── requirements.txt           # Python dependencies
├── run.bat / run.sh           # One-click launchers
├── src/
│   ├── __init__.py
│   ├── cli.py                 # All user-facing workflows and menus
│   ├── deepseek_client.py     # AI engine (OpenRouter / DeepSeek)
│   ├── automation_engine.py   # Tool executor (subprocess)
│   ├── report_generator.py    # Report builder (HTML/JSON/MD)
│   └── config_manager.py      # Persistent configuration
├── test_ai.py                 # AI advisor test
├── test_automation.py         # Automation engine test
├── test_report.py             # Report generator test
└── test_scan.py               # Non-interactive scan test
```

## Operation Modes

| Mode | Description |
|------|-------------|
| 1. Quick Scan | Runs nmap + nikto + dirb automatically |
| 2. AI-Guided Test | AI picks and ranks tools for your target |
| 3. Educational Mode | Interactive cybersecurity Q&A with AI |
| 4. Settings | Configure API key, output dir, preferences |
| 5. View Reports | Browse and open saved reports |
| 6. Exit | Clean exit |

## Tool Arsenal

| Tool | Category | Kali Pre-installed |
|------|----------|-------------------|
| nmap | Reconnaissance | ✓ |
| nikto | Vulnerability Analysis | ✓ |
| dirb | Enumeration | ✓ |
| gobuster | Enumeration | ✗ |
| sqlmap | Vulnerability Analysis | ✗ |
| hydra | Exploitation | ✗ |
| metasploit | Exploitation | ✗ |
| wpscan | WordPress Scanning | ✗ |
| john | Password Cracking | ✗ |

## License

For educational purposes only. Always obtain proper authorization before testing.
