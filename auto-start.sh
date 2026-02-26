#!/bin/bash

# 🤖 Jarvis Auto-Start Script
# This starts everything automatically

PROJECT_ROOT="/Volumes/Akash SSD/repos/jarvis-brain"

echo "🚀 Starting Jarvis Brain System..."

# Start backend if not running
if ! ps aux | grep -q '[p]ython.*app.py'; then
    echo "📡 Starting backend API (port 8001)..."
    cd "$PROJECT_ROOT"
    source jarvis_env/bin/activate
    FLASK_PORT=8001 python backend/app.py > backend.log 2>&1 &
    sleep 2
    echo "✅ Backend started"
else
    echo "✅ Backend already running"
fi

# Open VS Code
echo "📂 Opening VS Code..."
cd "$PROJECT_ROOT"
code .

echo "✨ Jarvis is ready!"
echo "   • Auto-Pilot: ON"
echo "   • Auto-Fix: ON"
echo "   • Real-Time Analysis: ON"
echo "   • Backend: Running on port 8001"
