#!/bin/bash
# JARVIS Quick Start Script
# Automatically starts JARVIS server with full setup and verification

set -e

WORKSPACE="/Volumes/Akash SSD/repos/jarvis-brain"
VENV="$WORKSPACE/jarvis_env"
ENV_FILE="$WORKSPACE/.env"
LOG_FILE="$WORKSPACE/.jarvis_logs/startup.log"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║          🚀 JARVIS Quick Start (Auto Setup)                    ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Create log directory
mkdir -p "$WORKSPACE/.jarvis_logs"

# Log function
log() {
    echo "$@" >> "$LOG_FILE"
}

log "=== JARVIS Startup at $(date) ==="

# Step 1: Check workspace
echo -e "${YELLOW}1️⃣  Checking workspace...${NC}"
if [ ! -d "$WORKSPACE" ]; then
    echo -e "${RED}✗ Workspace not found: $WORKSPACE${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Workspace found${NC}"
log "✓ Workspace found: $WORKSPACE"

# Step 2: Check venv
echo -e "${YELLOW}2️⃣  Checking virtual environment...${NC}"
if [ ! -d "$VENV" ]; then
    echo -e "${RED}✗ Virtual environment not found${NC}"
    echo "Create it with: python3 -m venv $VENV"
    log "✗ Virtual environment not found"
    exit 1
fi
echo -e "${GREEN}✓ Virtual environment exists${NC}"
log "✓ Virtual environment exists"

# Step 3: Activate venv
echo -e "${YELLOW}3️⃣  Activating virtual environment...${NC}"
source "$VENV/bin/activate"
echo -e "${GREEN}✓ Virtual environment activated${NC}"
log "✓ Virtual environment activated"

# Step 4: Check .env
echo -e "${YELLOW}4️⃣  Checking configuration (.env)...${NC}"
if [ ! -f "$ENV_FILE" ]; then
    echo -e "${YELLOW}⚠ .env not found, creating from template...${NC}"
    if [ -f "$WORKSPACE/.env.template" ]; then
        cp "$WORKSPACE/.env.template" "$ENV_FILE"
        echo -e "${GREEN}✓ Created .env from template${NC}"
        echo -e "${YELLOW}⚠ Edit .env and add your API key:${NC}"
        echo -e "  nano $ENV_FILE"
        log "✓ Created .env from template"
    else
        echo -e "${RED}✗ .env.template not found${NC}"
        log "✗ .env.template not found"
        exit 1
    fi
else
    echo -e "${GREEN}✓ Configuration file (.env) exists${NC}"
    log "✓ Configuration file exists"
fi

# Step 5: Check Python
echo -e "${YELLOW}5️⃣  Checking Python...${NC}"
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo -e "${GREEN}✓ Python $PYTHON_VERSION${NC}"
log "✓ Python $PYTHON_VERSION"

# Step 6: Check dependencies
echo -e "${YELLOW}6️⃣  Checking dependencies...${NC}"
MISSING=0

if ! python3 -c "import websocket_server" 2>/dev/null; then
    echo -e "${RED}✗ websocket-server not installed${NC}"
    MISSING=1
    log "✗ websocket-server not installed"
else
    echo -e "${GREEN}✓ websocket-server${NC}"
    log "✓ websocket-server"
fi

if ! python3 -c "import anthropic" 2>/dev/null; then
    echo -e "${YELLOW}⚠ anthropic not installed (needed for Claude)${NC}"
    log "⚠ anthropic not installed"
else
    echo -e "${GREEN}✓ anthropic${NC}"
    log "✓ anthropic"
fi

if ! python3 -c "import requests" 2>/dev/null; then
    echo -e "${YELLOW}⚠ requests not installed${NC}"
    log "⚠ requests not installed"
else
    echo -e "${GREEN}✓ requests${NC}"
    log "✓ requests"
fi

if [ $MISSING -eq 1 ]; then
    echo -e "${RED}Missing critical dependencies. Install with:${NC}"
    echo "pip install websocket-server anthropic requests"
    log "✗ Missing critical dependencies"
    exit 1
fi

# Step 7: Load environment
echo -e "${YELLOW}7️⃣  Loading environment variables...${NC}"
if [ -f "$ENV_FILE" ]; then
    set -a
    source "$ENV_FILE"
    set +a
    echo -e "${GREEN}✓ Environment loaded${NC}"
    log "✓ Environment variables loaded"
fi

# Step 8: Check for old processes
echo -e "${YELLOW}8️⃣  Checking for old processes...${NC}"
if pgrep -f "vscode_server.py" > /dev/null; then
    echo -e "${YELLOW}⚠ Old server running, killing...${NC}"
    pkill -f "vscode_server.py" || true
    sleep 1
    echo -e "${GREEN}✓ Old process killed${NC}"
    log "✓ Killed old server process"
fi

# Step 9: Start JARVIS server
echo -e "${YELLOW}9️⃣  Starting JARVIS server...${NC}"
echo ""

# Start in background
cd "$WORKSPACE"
python3 core/vscode_server.py > "$LOG_FILE" 2>&1 &
SERVER_PID=$!
echo $SERVER_PID > "$WORKSPACE/.jarvis_server.pid"

sleep 2

# Step 10: Verify server is running
echo -e "${YELLOW}🔟 Verifying server...${NC}"
if ps -p $SERVER_PID > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Server is running (PID: $SERVER_PID)${NC}"
    log "✓ Server started with PID: $SERVER_PID"
else
    echo -e "${RED}✗ Server failed to start${NC}"
    echo -e "${RED}Check logs:${NC}"
    tail -20 "$LOG_FILE"
    log "✗ Server failed to start"
    exit 1
fi

# Check WebSocket port
if lsof -i :8765 >/dev/null 2>&1; then
    echo -e "${GREEN}✓ WebSocket listening on port 8765${NC}"
    log "✓ WebSocket listening on 8765"
else
    echo -e "${YELLOW}⚠ Port 8765 not responding yet, waiting...${NC}"
    sleep 2
    if lsof -i :8765 >/dev/null 2>&1; then
        echo -e "${GREEN}✓ WebSocket listening on port 8765${NC}"
        log "✓ WebSocket listening on 8765"
    else
        echo -e "${RED}✗ WebSocket not responding${NC}"
        log "✗ WebSocket not responding"
    fi
fi

echo ""
echo -e "${GREEN}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                    ✅ JARVIS IS READY!                         ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}What to do now:${NC}"
echo ""
echo -e "  1️⃣  Open VS Code:"
echo -e "      ${YELLOW}code .${NC}"
echo ""
echo -e "  2️⃣  Use JARVIS:"
echo -e "      ${YELLOW}Cmd+Shift+P → type 'jarvis' → select command${NC}"
echo ""
echo -e "  3️⃣  Watch server logs:"
echo -e "      ${YELLOW}tail -f $LOG_FILE${NC}"
echo ""
echo -e "${GREEN}Server running on: ws://localhost:8765${NC}"
echo -e "${GREEN}Server PID: $SERVER_PID${NC}"
echo -e "${GREEN}Logs: $LOG_FILE${NC}"
echo ""

log "=== JARVIS Startup Complete ==="
log "Server ready at: ws://localhost:8765"
log "All checks passed!"
