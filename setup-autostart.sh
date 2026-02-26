#!/bin/bash
# Setup JARVIS Auto-Start on macOS using launchd

WORKSPACE="/Volumes/Akash SSD/repos/jarvis-brain"
PLIST_SRC="$WORKSPACE/com.jarvis.vscode.server.plist"
PLIST_DEST="$HOME/Library/LaunchAgents/com.jarvis.vscode.server.plist"
PLIST_SYSTEM="/Library/LaunchDaemons/com.jarvis.vscode.server.plist"

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║        🚀 JARVIS Auto-Start Setup for macOS                    ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Check if running setup or install
if [ "$1" = "install" ]; then
    echo "📦 Installing JARVIS auto-start service..."
    echo ""
    
    # Copy plist to user LaunchAgents
    mkdir -p "$HOME/Library/LaunchAgents"
    cp "$PLIST_SRC" "$PLIST_DEST"
    
    echo "✅ Plist copied to: $PLIST_DEST"
    echo ""
    
    # Load the service
    launchctl load "$PLIST_DEST"
    
    if launchctl list | grep -q "com.jarvis.vscode.server"; then
        echo "✅ JARVIS auto-start service installed!"
        echo "✅ Server will auto-start on next login or system restart"
        echo ""
        echo "📋 Service Details:"
        echo "   • Service: com.jarvis.vscode.server"
        echo "   • Location: $PLIST_DEST"
        echo "   • Status: Loaded and running"
        echo ""
    else
        echo "❌ Failed to load service"
        exit 1
    fi

elif [ "$1" = "uninstall" ]; then
    echo "🔄 Uninstalling JARVIS auto-start service..."
    echo ""
    
    launchctl unload "$PLIST_DEST" 2>/dev/null || true
    rm -f "$PLIST_DEST"
    
    echo "✅ Auto-start service removed"
    echo ""

elif [ "$1" = "status" ]; then
    echo "📊 JARVIS Auto-Start Status:"
    echo ""
    
    if [ -f "$PLIST_DEST" ]; then
        echo "✅ Service installed"
        
        if launchctl list | grep -q "com.jarvis.vscode.server"; then
            echo "✅ Service is loaded and active"
        else
            echo "❌ Service is not loaded"
        fi
        
        echo ""
        echo "🔍 Service Details:"
        launchctl list | grep "com.jarvis.vscode.server" || echo "   Not currently running"
    else
        echo "❌ Service not installed"
        echo ""
        echo "To install, run: bash setup-autostart.sh install"
    fi
    echo ""

elif [ "$1" = "start" ]; then
    echo "▶️  Starting JARVIS server..."
    launchctl start "com.jarvis.vscode.server"
    sleep 2
    echo "✅ Server started"
    echo ""

elif [ "$1" = "stop" ]; then
    echo "⏹️  Stopping JARVIS server..."
    launchctl stop "com.jarvis.vscode.server" 2>/dev/null || true
    echo "✅ Server stopped"
    echo ""

elif [ "$1" = "restart" ]; then
    echo "🔄 Restarting JARVIS server..."
    launchctl stop "com.jarvis.vscode.server" 2>/dev/null || true
    sleep 1
    launchctl start "com.jarvis.vscode.server"
    sleep 2
    echo "✅ Server restarted"
    echo ""

else
    echo "📋 Usage:"
    echo ""
    echo "  bash setup-autostart.sh install     - Install auto-start service"
    echo "  bash setup-autostart.sh uninstall   - Remove auto-start service"
    echo "  bash setup-autostart.sh status      - Check service status"
    echo "  bash setup-autostart.sh start       - Start JARVIS server"
    echo "  bash setup-autostart.sh stop        - Stop JARVIS server"
    echo "  bash setup-autostart.sh restart     - Restart JARVIS server"
    echo ""
    echo "🎯 Quick Setup:"
    echo "  1. bash setup-autostart.sh install"
    echo "  2. Log out and back in (or restart)"
    echo "  3. JARVIS will auto-start!"
    echo ""
fi
