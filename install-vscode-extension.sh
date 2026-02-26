#!/bin/bash
# JARVIS Pro VS Code Extension - Installation Script

set -e

echo "╔════════════════════════════════════════════════════════════════════════╗"
echo "║       🚀 JARVIS Pro VS Code Extension Installation                     ║"
echo "╚════════════════════════════════════════════════════════════════════════╝"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check Python
echo -e "${BLUE}Checking Python installation...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is required but not installed${NC}"
    exit 1
fi
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo -e "${GREEN}✅ Python ${PYTHON_VERSION} found${NC}"
echo ""

# Check VS Code
echo -e "${BLUE}Checking VS Code installation...${NC}"
if ! command -v code &> /dev/null; then
    echo -e "${YELLOW}⚠️  VS Code CLI not found in PATH (this is optional)${NC}"
else
    VSCODE_VERSION=$(code --version | head -1)
    echo -e "${GREEN}✅ VS Code ${VSCODE_VERSION} found${NC}"
fi
echo ""

# Install Python dependencies
echo -e "${BLUE}Installing Python dependencies...${NC}"
pip3 install -q websocket-server anthropic requests 2>/dev/null || pip install -q websocket-server anthropic requests
echo -e "${GREEN}✅ Python dependencies installed${NC}"
echo ""

# Check Node.js
echo -e "${BLUE}Checking Node.js...${NC}"
if ! command -v npm &> /dev/null; then
    echo -e "${YELLOW}⚠️  Node.js/npm not found${NC}"
    echo -e "${YELLOW}To build the extension, install Node.js from https://nodejs.org${NC}"
else
    NODE_VERSION=$(node --version)
    echo -e "${GREEN}✅ Node.js ${NODE_VERSION} found${NC}"
fi
echo ""

# Navigate to extension directory
EXTENSION_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.vscode-extension" && pwd)"
cd "$EXTENSION_DIR"

echo -e "${BLUE}Extension directory: ${EXTENSION_DIR}${NC}"
echo ""

# Install Node dependencies
if command -v npm &> /dev/null; then
    echo -e "${BLUE}Installing Node.js dependencies...${NC}"
    npm install -q 2>/dev/null || npm install
    echo -e "${GREEN}✅ Node dependencies installed${NC}"
    echo ""
    
    # Package as VSIX
    echo -e "${BLUE}Packaging extension as VSIX...${NC}"
    npm install -g @vscode/vsce -q 2>/dev/null || true
    
    if command -v vsce &> /dev/null; then
        vsce package -o jarvis-pro.vsix 2>/dev/null || vsce package
        echo -e "${GREEN}✅ Extension packaged: jarvis-pro.vsix${NC}"
        echo ""
    fi
fi

# Setup .vscode directory
echo -e "${BLUE}Setting up VS Code configuration files...${NC}"
cd "$(dirname "$EXTENSION_DIR")"
python3 << 'EOF'
import json
from pathlib import Path

vscode_dir = Path("./.vscode")
vscode_dir.mkdir(exist_ok=True)

# Settings
settings = {
    "jarvis.serverHost": "localhost",
    "jarvis.serverPort": 8765,
    "jarvis.autoStart": True,
    "jarvis.defaultLanguage": "python",
    "[python]": {
        "editor.formatOnSave": True,
        "editor.defaultFormatter": "ms-python.python"
    }
}

with open(vscode_dir / "settings.json", "w") as f:
    json.dump(settings, f, indent=2)

# Extensions recommendations
extensions = {
    "recommendations": [
        "ms-python.python",
        "ms-python.vscode-pylance",
        "ms-python.debugpy"
    ]
}

with open(vscode_dir / "extensions.json", "w") as f:
    json.dump(extensions, f, indent=2)

print("✅ VS Code configuration files created")
EOF
echo ""

# Summary
echo -e "${GREEN}╔════════════════════════════════════════════════════════════════════════╗"
echo "║             ✅ Installation Complete!                                  ║"
echo "╚════════════════════════════════════════════════════════════════════════╝${NC}"
echo ""

echo -e "${BLUE}📋 Installation Summary:${NC}"
echo "  ✅ Python dependencies: websocket-server, anthropic"
echo "  ✅ VS Code configuration files created"

if command -v npm &> /dev/null; then
    if [ -f "$EXTENSION_DIR/jarvis-pro.vsix" ]; then
        echo "  ✅ VSIX extension packaged"
    fi
fi
echo ""

echo -e "${BLUE}🚀 Next Steps:${NC}"
echo ""
echo "  Option 1: Install Extension from VSIX"
if [ -f "$EXTENSION_DIR/jarvis-pro.vsix" ]; then
    echo "    1. Run: code --install-extension .vscode-extension/jarvis-pro.vsix"
else
    echo "    (Build the VSIX file first by running: npm install && vsce package)"
fi
echo ""
echo "  Option 2: Run Development Mode"
echo "    1. Start JARVIS server: python3 core/vscode_server.py"
echo "    2. Open .vscode-extension folder in VS Code"
echo "    3. Press F5 to launch extension in debug mode"
echo ""
echo "  Option 3: Manual Setup (Easiest)"
echo "    1. Start JARVIS server: python3 core/vscode_server.py &"
echo "    2. Open project folder in VS Code"
echo "    3. Press Cmd+Shift+P and type 'JARVIS'"
echo "    4. Commands will be available (extension runs in background)"
echo ""

echo -e "${YELLOW}⚠️  Important:${NC}"
echo "  • Set ANTHROPIC_API_KEY environment variable:"
echo "    export ANTHROPIC_API_KEY='your-key-here'"
echo "  • Or add to ~/.bashrc or ~/.zshrc for persistence"
echo ""

echo -e "${BLUE}📚 Documentation:${NC}"
echo "  • Extension Guide: .vscode-extension/README.md"
echo "  • JARVIS Pro Model: JARVIS_PRO_MODEL.md"
echo "  • Build & Debug: BUILD_DEBUG_INTEGRATION.md"
echo ""

echo -e "${GREEN}Happy coding with JARVIS! 🚀${NC}"
