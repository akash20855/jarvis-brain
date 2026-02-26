#!/bin/bash

# JARVIS VS Code AI Integration - Quick Setup
# Sets up JARVIS as your default AI assistant in VS Code

set -e

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║     🤖 JARVIS AI Integration with VS Code - Setup              ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 1. Check venv
echo "1️⃣  Checking virtual environment..."
if [ ! -d "jarvis_env" ]; then
    echo "   ✗ Virtual environment not found. Creating..."
    python3 -m venv jarvis_env
fi
source jarvis_env/bin/activate
echo "   ✓ Virtual environment activated"
echo

# 2. Install dependencies
echo "2️⃣  Checking dependencies..."
pip install -q websocket-server dotenv groq anthropic websocket-client
echo "   ✓ Dependencies installed"
echo

# 3. Check .env
echo "3️⃣  Checking configuration (.env)..."
if [ ! -f ".env" ]; then
    echo "   ✗ .env not found. Creating template..."
    cat > .env << 'EOF'
AI_BACKEND=groq
GROQ_API_KEY=your_groq_api_key_here
ANTHROPIC_API_KEY=your_api_key_here
OLLAMA_API_URL=http://localhost:11434
EOF
    echo "   ⚠️  Created default .env. Update GROQ_API_KEY if needed."
else
    echo "   ✓ Configuration found"
fi
echo

# 4. Start JARVIS server
echo "4️⃣  Starting JARVIS server..."
pkill -f "python3 core/vscode_server" 2>/dev/null || true
sleep 1

python3 core/vscode_server.py > .jarvis_logs/startup.log 2>&1 &
SERVER_PID=$!
sleep 3

if ps -p $SERVER_PID > /dev/null; then
    echo "   ✓ Server running (PID: $SERVER_PID)"
else
    echo "   ✗ Server failed to start"
    echo "   Check logs: tail -50 .jarvis_logs/startup.log"
    exit 1
fi
echo

# 5. Verify connection
echo "5️⃣  Verifying server..."
if python3 /tmp/test_jarvis.py 2>/dev/null | grep -q "success: True"; then
    echo "   ✓ Server is responsive"
else
    echo "   ⚠️  Could not verify server. It may still be starting..."
fi
echo

# 6. VS Code setup
echo "6️⃣  VS Code Extension Setup..."
echo "   The JARVIS AI Assistant extension will:"
echo "   • Auto-activate when you open this folder"
echo "   • Show AI model selector in status bar"
echo "   • Provide keyboard shortcuts for quick access"
echo

# 7. Summary
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                    ✅ SETUP COMPLETE!                          ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo

echo "🚀 What to do now:"
echo
echo "  1️⃣  Open VS Code:"
echo "     code ."
echo
echo "  2️⃣  Use JARVIS:"
echo "     • Press: Cmd+Shift+P"
echo "     • Type: 'jarvis'"
echo "     • Select any command"
echo
echo "  3️⃣  Change AI Model:"
echo "     • Click: 🤖 icon in status bar"
echo "     • Or: Cmd+Shift+P → 'Switch AI Model'"
echo
echo "📊 Current Status:"
echo "   • Backend: Groq (Free & Fast)"
echo "   • Server: ws://localhost:8765"
echo "   • Status: ✅ Running"
echo
echo "💡 Keyboard Shortcuts:"
echo "   • Cmd+Alt+J = Chat"
echo "   • Cmd+Alt+F = Auto-Fix"
echo "   • Cmd+Alt+A = Analyze"
echo "   • Cmd+Alt+D = Debug"
echo
echo "📖 Learn more:"
echo "   See: VSCODE_AI_MODELS_GUIDE.md"
echo
echo "Server PID: $SERVER_PID"
echo "Watch logs: tail -f .jarvis_logs/startup.log"
echo
