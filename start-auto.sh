#!/bin/bash

# 🤖 JARVIS AUTO-START - One Command to Start Everything

PROJECT_ROOT="/Volumes/Akash SSD/repos/jarvis-brain"

# Start backend if not running
if ! ps aux | grep -q '[p]ython.*app.py'; then
    echo "📡 Starting backend on port 8001..."
    cd "$PROJECT_ROOT"
    source jarvis_env/bin/activate
    FLASK_PORT=8001 python backend/app.py > backend.log 2>&1 &
    sleep 2
    echo "✅ Backend started"
fi

# Open VS Code
echo "📂 Opening VS Code with Auto-Pilot enabled..."
cd "$PROJECT_ROOT"
code .

echo ""
echo "✨ Jarvis System Started!"
echo "   🤖 Auto-Pilot: ON"
echo "   🔧 Auto-Fix: ON" 
echo "   📊 Real-Time Analysis: ON"
echo "   📡 Backend: Running (port 8001)"
echo ""
echo "Status Bar should show: 🤖 Auto-Pilot ON"
echo ""
