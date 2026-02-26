#!/bin/bash
# Start JARVIS VS Code Integration Server

cd "$(dirname "$0")" || exit 1

echo "🚀 Starting JARVIS VS Code Integration Server..."
echo ""

# Activate venv if needed
if [ -d "jarvis_env" ]; then
    source jarvis_env/bin/activate
fi

# Start server
echo "📡 Starting WebSocket server on port 8765..."
python3 -u core/vscode_server.py

echo ""
echo "Server stopped."
