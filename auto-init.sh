#!/bin/bash
# JARVIS Auto-Setup and Auto-Start
# This script sets up everything automatically on system startup

set -e

WORKSPACE="/Volumes/Akash SSD/repos/jarvis-brain"
VENV="$WORKSPACE/jarvis_env"
LOG_DIR="$WORKSPACE/.jarvis_logs"
PID_FILE="$WORKSPACE/.jarvis_server.pid"

# Create log directory
mkdir -p "$LOG_DIR"

echo "🚀 JARVIS Auto-Initialization Starting..."
echo "Timestamp: $(date)" >> "$LOG_DIR/auto_init.log"

# 1. Activate virtual environment
if [ -d "$VENV" ]; then
    source "$VENV/bin/activate" 2>/dev/null || true
    echo "✅ Virtual environment activated" | tee -a "$LOG_DIR/auto_init.log"
fi

# 2. Check and set API key
if [ -z "$ANTHROPIC_API_KEY" ]; then
    if [ -f "$WORKSPACE/.env" ]; then
        set -a
        source "$WORKSPACE/.env"
        set +a
        echo "✅ Loaded environment from .env" | tee -a "$LOG_DIR/auto_init.log"
    else
        echo "⚠️  No ANTHROPIC_API_KEY set" | tee -a "$LOG_DIR/auto_init.log"
    fi
fi

# 3. Kill any existing server
pkill -f "core/vscode_server.py" 2>/dev/null || true
sleep 1

# 4. Start JARVIS server
cd "$WORKSPACE"
nohup python3 -u core/vscode_server.py > "$LOG_DIR/server.log" 2>&1 &
SERVER_PID=$!
echo $SERVER_PID > "$PID_FILE"

echo "✅ Server started (PID: $SERVER_PID)" | tee -a "$LOG_DIR/auto_init.log"

# 5. Wait for server to be ready
sleep 2

# 6. Verify server is running
if ps -p $SERVER_PID > /dev/null 2>&1; then
    echo "✅ JARVIS server is running!" | tee -a "$LOG_DIR/auto_init.log"
    echo "📡 WebSocket: ws://localhost:8765" | tee -a "$LOG_DIR/auto_init.log"
    echo "🎯 Ready to use in VS Code!" | tee -a "$LOG_DIR/auto_init.log"
else
    echo "❌ Server failed to start" | tee -a "$LOG_DIR/auto_init.log"
    exit 1
fi

echo "✅ Auto-initialization complete!" | tee -a "$LOG_DIR/auto_init.log"
