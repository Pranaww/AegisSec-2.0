#!/bin/bash
echo "=== AegisSec v2.0 Launcher ==="

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed."
    exit 1
fi

# Create venv if not exists
if [ ! -d "venv" ]; then
    echo "[*] Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate

echo "[*] Installing dependencies..."
pip install -r requirements.txt -q

echo "[*] Launching AegisSec..."
python main.py
