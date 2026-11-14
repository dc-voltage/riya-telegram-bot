#!/bin/bash
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

echo "=== Starting DC VOLTAGE AI Helper Telegram Bot ==="
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    venv/bin/pip install --upgrade pip python-telegram-bot google-genai
fi

exec venv/bin/python3 bot.py
