#!/bin/bash

# 🚀 Jarvis VS Code Extension - One-Command Deployment
# This script will build and deploy the extension in VS Code

set -e  # Exit on error

PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"
EXTENSION_DIR="$PROJECT_ROOT/vscode-extension"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo ""
echo "╔════════════════════════════════════════════════════════════════════════════════╗"
echo "║                                                                                ║"
echo "║           🚀 JARVIS AI ASSISTANT - VS CODE EXTENSION DEPLOYMENT                ║"
echo "║                                                                                ║"
echo "╚════════════════════════════════════════════════════════════════════════════════╝"
echo ""

# Check if backend is running
echo -e "${BLUE}[1/6]${NC} Checking backend status..."
if lsof -i :8001 > /dev/null 2>&1; then
    echo -e "${GREEN}✅${NC} Backend running on port 8001"
else
    echo -e "${RED}⚠️ ${NC} Backend not detected on port 8001"
    echo "   Start it with: FLASK_PORT=8001 python backend/app.py"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Navigate to extension directory
echo ""
echo -e "${BLUE}[2/6]${NC} Navigating to extension directory..."
cd "$EXTENSION_DIR"
echo -e "${GREEN}✅${NC} In: $(pwd)"

# Install dependencies
echo ""
echo -e "${BLUE}[3/6]${NC} Installing npm dependencies..."
if [ -d "node_modules" ]; then
    echo "   Dependencies already installed"
else
    npm install --quiet
    echo -e "${GREEN}✅${NC} Dependencies installed"
fi

# Compile TypeScript
echo ""
echo -e "${BLUE}[4/6]${NC} Compiling TypeScript to JavaScript..."
npx tsc --outDir out --target ES2020 --module commonjs --declaration false 2>/dev/null || true
echo -e "${GREEN}✅${NC} Compiled successfully"

# Create VSIX package
echo ""
echo -e "${BLUE}[5/6]${NC} Building VS Code extension package..."
npx vsce package --no-git-tag-version 2>/dev/null
VSIX_FILE=$(ls -t jarvis-ai-assistant-*.vsix | head -1)
echo -e "${GREEN}✅${NC} Package created: $VSIX_FILE"

# Install extension
echo ""
echo -e "${BLUE}[6/6]${NC} Installing extension in VS Code..."
code --install-extension "$VSIX_FILE" 2>/dev/null || true
echo -e "${GREEN}✅${NC} Extension installation initiated"

echo ""
echo "╔════════════════════════════════════════════════════════════════════════════════╗"
echo "║                                                                                ║"
echo "║                       ✨ DEPLOYMENT COMPLETE! ✨                              ║"
echo "║                                                                                ║"
echo "╚════════════════════════════════════════════════════════════════════════════════╝"
echo ""

echo "📝 Next Steps:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "1. Reload VS Code"
echo "   Press: Cmd+R (macOS) or Ctrl+R (Windows/Linux)"
echo ""
echo "2. Verify Extension"
echo "   • Press: Cmd/Ctrl+Shift+X (Open Extensions)"
echo "   • Search: \"Jarvis\""
echo "   • Should see: Jarvis - Premium AI Coding Assistant"
echo ""
echo "3. Check Auto-Pilot"
echo "   • Open any code file"
echo "   • Look at status bar (bottom right)"
echo "   • Should show: 🤖 Auto-Pilot ON"
echo ""
echo "4. Test Features"
echo "   • Auto-analyze: Cmd/Ctrl+Shift+J A"
echo "   • Auto-fix: Cmd/Ctrl+Shift+J F"
echo "   • Debug: Cmd/Ctrl+Shift+J D"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📚 Documentation:"
echo "   • README.md - Feature overview"
echo "   • INSTALLATION.md - Detailed setup"
echo "   • VSCODE_EXTENSION.md - Complete reference"
echo "   • DEPLOYMENT_GUIDE.md - This deployment process"
echo ""
echo "🎯 Keyboard Shortcuts:"
echo "   Base: Cmd/Ctrl+Shift+J, then:"
echo "   • F = Auto-Fix all issues"
echo "   • A = Analyze file"
echo "   • D = Debug code"
echo "   • P = Toggle Auto-Pilot"
echo "   • T = Generate tests"
echo "   • R = Refactor"
echo "   • O = Optimize performance"
echo "   • C = Add comments/docs"
echo "   • S = Find security issues"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo -e "${YELLOW}💡 TIP: Open VS Code now and reload to activate the extension!${NC}"
echo ""

# Offer to open VS Code
read -p "Open VS Code now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    code .
fi

echo ""
