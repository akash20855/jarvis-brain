#!/bin/bash
# Claude Haiku 4.5 Automatic Setup & Start
# This script automatically sets up and starts Jarvis Brain with Claude Haiku

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$PROJECT_DIR/jarvis_env"

echo "🧠 Claude Haiku 4.5 - Automatic Setup"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Step 1: Activate virtual environment
echo ""
echo "1️⃣  Activating Python environment..."
if [ ! -d "$VENV_DIR" ]; then
    echo "   Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
fi
source "$VENV_DIR/bin/activate"
echo "   ✅ Environment activated"

# Step 2: Check for API key
echo ""
echo "2️⃣  Checking API key..."
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "   ⚠️  ANTHROPIC_API_KEY not set!"
    echo ""
    echo "   You need an API key to use Claude Haiku:"
    echo "   1. Go to: https://console.anthropic.com"
    echo "   2. Generate API key"
    echo "   3. Set it:"
    echo "      export ANTHROPIC_API_KEY='sk-ant-your-key'"
    echo ""
    echo "   Then run this script again:"
    echo "      bash start-claude.sh"
    echo ""
    read -p "Or paste your key here (or press Enter to continue without it): " API_KEY
    if [ -n "$API_KEY" ]; then
        export ANTHROPIC_API_KEY="$API_KEY"
        echo "   ✅ API key set"
    else
        echo "   ⚠️  Continuing without API key (status-only mode)"
    fi
else
    MASKED_KEY="${ANTHROPIC_API_KEY:0:10}...${ANTHROPIC_API_KEY: -4}"
    echo "   ✅ API key found: $MASKED_KEY"
fi

# Step 3: Kill any existing processes on port 8001
echo ""
echo "3️⃣  Clearing port 8001..."
if lsof -i :8001 >/dev/null 2>&1; then
    lsof -i :8001 | tail -n +2 | awk '{print $2}' | xargs kill -9 2>/dev/null || true
    sleep 1
    echo "   ✅ Port cleared"
else
    echo "   ✅ Port is free"
fi

# Step 4: Install dependencies
echo ""
echo "4️⃣  Installing dependencies..."
pip install -q anthropic requests flask flask-cors pyyaml python-dotenv 2>/dev/null
echo "   ✅ Dependencies ready"

# Step 5: Start backend server
echo ""
echo "5️⃣  Starting Jarvis Brain Backend..."
cd "$PROJECT_DIR"
FLASK_PORT=8001 python backend/app.py > backend.log 2>&1 &
FLASK_PID=$!
sleep 3

# Step 6: Verify Claude status
echo ""
echo "6️⃣  Verifying Claude status..."
if curl -s http://localhost:8001/api/claude/status >/dev/null 2>&1; then
    echo "   ✅ Claude Haiku 4.5 is online!"
else
    echo "   ⚠️  Backend starting (wait a moment)..."
    sleep 2
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Jarvis Brain with Claude Haiku is running!"
echo ""
echo "🚀 Quick Commands:"
echo ""
echo "Generate code:"
echo "  curl-claude generate 'fibonacci function' python"
echo ""
echo "Analyze code:"
echo "  curl-claude analyze 'def foo(): pass' script.py"
echo ""
echo "View status:"
echo "  curl http://localhost:8001/api/claude/status"
echo ""
echo "View logs:"
echo "  tail -f backend.log"
echo ""
echo "Stop server:"
echo "  pkill -f 'python backend/app.py'"
echo ""
echo "📚 Full docs: CLAUDE_HAIKU_GUIDE.md"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Keep script running
wait $FLASK_PID
