# ADAPT in Python

This is a Python rewrite of the C-based ADAPT (Automated Dynamic Analysis and Penetration Testing) framework. It implements the core **MAPE-K** (Monitor, Analyze, Plan, Execute, Knowledge) autonomous loop.

## Architecture

- **`models.py`:** Contains dataclasses for Targets, Scans, Attacks, and utility scoring.
- **`knowledge_base.py`:** The central store for states and available tools.
- **`monitor.py`:** Tracks the current status of progress and determines when the system should re-analyze.
- **`analyzer.py`:** Computes "Utility Scores" for various targets and actions. 
- **`planner.py`:** Chooses the highest utility plans based on system states and action guards.
- **`executor.py`:** Asynchronously executes the chosen plans using `asyncio`.
- **`mape_k.py`:** Wires everything together in a continuous `while` loop.
- **`plugins/`:** Extensible scanner and attacker modules (e.g., `nmap_scan.py`).

## How to Run

Just execute the main script using Python 3:

```bash
python main.py
```

The system will automatically initialize targets, scan them to find vulnerabilities, and then use the findings to launch simulated attacks!
