#!/bin/bash
# JARVIS AI Backend Switcher
# Easily switch between Claude and Ollama

set -e

WORKSPACE="/Volumes/Akash SSD/repos/jarvis-brain"
ENV_FILE="$WORKSPACE/.env"

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║          JARVIS AI Backend Switcher (Claude ↔ Ollama)          ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Check if .env exists
if [ ! -f "$ENV_FILE" ]; then
    echo "❌ .env file not found at $ENV_FILE"
    exit 1
fi

# Get current backend
CURRENT_BACKEND=$(grep "^AI_BACKEND=" "$ENV_FILE" | cut -d'=' -f2 | tr -d ' ')
echo "Current Backend: $CURRENT_BACKEND"
echo ""

if [ "$1" = "claude" ]; then
    echo "🔄 Switching to Claude (Cloud AI)..."
    
    # Check if API key is set
    API_KEY=$(grep "^ANTHROPIC_API_KEY=" "$ENV_FILE" | cut -d'=' -f2 | tr -d ' ')
    if [ "$API_KEY" = "your_api_key_here" ]; then
        echo "❌ API key not set!"
        echo "   Please edit .env and add your Claude API key:"
        echo "   nano .env"
        echo "   Change: ANTHROPIC_API_KEY=your_api_key_here"
        echo "   To: ANTHROPIC_API_KEY=sk-proj-your-actual-key"
        exit 1
    fi
    
    # Update .env
    sed -i.bak "s/^AI_BACKEND=.*/AI_BACKEND=claude/" "$ENV_FILE"
    
    echo "✅ Switched to Claude!"
    echo "   Restart JARVIS to apply changes"
    echo ""
    echo "   pkill -f vscode_server.py"
    echo "   python3 core/vscode_server.py"
    echo ""

elif [ "$1" = "ollama" ]; then
    echo "🔄 Switching to Ollama (Free Local AI)..."
    
    # Check if Ollama is running
    if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        echo "⚠️  Ollama server not running!"
        echo "   Start it in another terminal:"
        echo "   ollama serve"
        echo ""
    fi
    
    # Update .env
    sed -i.bak "s/^AI_BACKEND=.*/AI_BACKEND=ollama/" "$ENV_FILE"
    
    echo "✅ Switched to Ollama!"
    echo "   Make sure Ollama is running:"
    echo "   ollama serve"
    echo ""
    echo "   Restart JARVIS to apply changes:"
    echo "   pkill -f vscode_server.py"
    echo "   python3 core/vscode_server.py"
    echo ""

elif [ "$1" = "status" ]; then
    echo "📊 Backend Status:"
    echo ""
    echo "Configuration:"
    grep "^AI_BACKEND\|^ANTHROPIC_API_KEY\|^OLLAMA_" "$ENV_FILE" | sed 's/^/  /'
    echo ""
    
    echo "Claude Status:"
    if grep -q "^ANTHROPIC_API_KEY=sk-proj" "$ENV_FILE"; then
        echo "  ✅ API key configured"
    else
        echo "  ❌ API key not configured"
    fi
    echo ""
    
    echo "Ollama Status:"
    if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        MODELS=$(curl -s http://localhost:11434/api/tags | grep -o '"name":"[^"]*"' | wc -l)
        echo "  ✅ Ollama is running"
        echo "  📦 Models available: $MODELS"
    else
        echo "  ❌ Ollama not running (start with: ollama serve)"
    fi
    echo ""

elif [ "$1" = "models" ]; then
    echo "🦙 Checking Ollama models..."
    echo ""
    
    if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        echo "Installed models:"
        curl -s http://localhost:11434/api/tags | python3 -m json.tool | grep -A1 '"name"' | sed 's/^/  /'
        echo ""
        echo "To download more models:"
        echo "  ollama pull llama2"
        echo "  ollama pull mistral"
        echo "  ollama pull neural-chat"
    else
        echo "❌ Ollama not running"
        echo "Start it with: ollama serve"
    fi
    echo ""

else
    echo "Usage:"
    echo "  $0 claude    - Switch to Claude (cloud AI)"
    echo "  $0 ollama    - Switch to Ollama (free local AI)"
    echo "  $0 status    - Show configuration and status"
    echo "  $0 models    - List Ollama models"
    echo ""
    echo "Example:"
    echo "  # Switch to free local AI"
    echo "  bash switch-ai.sh ollama"
    echo ""
    echo "  # Check status"
    echo "  bash switch-ai.sh status"
    echo ""
    echo "  # Switch back to Claude"
    echo "  bash switch-ai.sh claude"
    echo ""
fi
