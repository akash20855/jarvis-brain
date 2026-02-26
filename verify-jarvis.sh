#!/bin/bash
# JARVIS Verification & Health Check Script
# Run this to verify everything is working correctly

set -e

WORKSPACE="/Volumes/Akash SSD/repos/jarvis-brain"
LOG_DIR="$WORKSPACE/.jarvis_logs"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║        ✓ JARVIS System Health Check                             ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Counter for checks
PASSED=0
FAILED=0
WARNINGS=0

# Function to print check result
check_result() {
    local name=$1
    local result=$2
    local details=$3
    
    if [ "$result" = "PASS" ]; then
        echo -e "${GREEN}✓${NC} $name"
        ((PASSED++))
    elif [ "$result" = "FAIL" ]; then
        echo -e "${RED}✗${NC} $name"
        [ -n "$details" ] && echo "  $details"
        ((FAILED++))
    elif [ "$result" = "WARN" ]; then
        echo -e "${YELLOW}⚠${NC} $name"
        [ -n "$details" ] && echo "  $details"
        ((WARNINGS++))
    fi
}

echo "1️⃣  Environment Checks"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check workspace
if [ -d "$WORKSPACE" ]; then
    check_result "Workspace exists" "PASS"
else
    check_result "Workspace exists" "FAIL" "Directory not found: $WORKSPACE"
fi

# Check .env file
if [ -f "$WORKSPACE/.env" ]; then
    check_result "Configuration file (.env)" "PASS"
    
    # Check API key is set
    if grep -q "ANTHROPIC_API_KEY=" "$WORKSPACE/.env"; then
        if grep -q "ANTHROPIC_API_KEY=sk-proj" "$WORKSPACE/.env" || grep -q "ANTHROPIC_API_KEY=your" "$WORKSPACE/.env"; then
            if grep "ANTHROPIC_API_KEY=your" "$WORKSPACE/.env" > /dev/null; then
                check_result "API Key configured" "FAIL" "API key not set (still has placeholder: 'your_api_key_here')"
            else
                check_result "API Key configured" "PASS"
            fi
        else
            check_result "API Key configured" "FAIL" "API key value appears invalid"
        fi
    else
        check_result "API Key configured" "FAIL" "ANTHROPIC_API_KEY not found in .env"
    fi
else
    check_result "Configuration file (.env)" "WARN" "Not found. Run: cp .env.template .env"
fi

echo ""
echo "2️⃣  Virtual Environment Checks"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check venv
if [ -d "$WORKSPACE/jarvis_env" ]; then
    check_result "Virtual environment exists" "PASS"
else
    check_result "Virtual environment exists" "FAIL" "venv not found. Run: python3 -m venv jarvis_env"
fi

# Check Python
if [ -f "$WORKSPACE/jarvis_env/bin/python3" ]; then
    PYTHON_VERSION=$("$WORKSPACE/jarvis_env/bin/python3" --version 2>&1 | awk '{print $2}')
    check_result "Python available ($PYTHON_VERSION)" "PASS"
else
    check_result "Python available" "FAIL" "Python binary not found in venv"
fi

echo ""
echo "3️⃣  Dependencies Check"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

check_dep() {
    local pkg=$1
    local import=$2
    
    if "$WORKSPACE/jarvis_env/bin/python3" -c "import $import" 2>/dev/null; then
        check_result "$pkg installed" "PASS"
    else
        check_result "$pkg installed" "FAIL" "Missing: pip install $pkg"
    fi
}

check_dep "websocket-server" "websocket_server"
check_dep "anthropic" "anthropic"
check_dep "requests" "requests"

echo ""
echo "4️⃣  Core Files Check"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

check_file() {
    local file=$1
    local name=$2
    
    if [ -f "$WORKSPACE/$file" ]; then
        check_result "$name exists" "PASS"
    else
        check_result "$name exists" "FAIL" "File not found: $file"
    fi
}

check_file "core/vscode_server.py" "WebSocket server"
check_file "core/claude_code_generator.py" "Claude integration"
check_file "core/auto_debug.py" "Auto-debug engine"
check_file "setup-autostart.sh" "Auto-start script"
check_file "auto-init.sh" "Init script"

echo ""
echo "5️⃣  Service Status Check"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check if server is running
if ps aux | grep -q "[p]ython3.*vscode_server.py"; then
    PID=$(pgrep -f "vscode_server.py")
    check_result "Server running (PID: $PID)" "PASS"
else
    check_result "Server running" "WARN" "Not currently running (you can start it with ./auto-init.sh)"
fi

# Check port
if lsof -i :8765 >/dev/null 2>&1; then
    check_result "Port 8765 available" "PASS"
else
    check_result "Port 8765 available" "WARN" "Server not listening (not running yet)"
fi

# Check launchd service
if [ -f "$HOME/Library/LaunchAgents/com.jarvis.vscode.server.plist" ]; then
    check_result "Auto-start service installed" "PASS"
    
    if launchctl list | grep -q "com.jarvis.vscode.server"; then
        check_result "Auto-start service loaded" "PASS"
    else
        check_result "Auto-start service loaded" "FAIL" "Service installed but not loaded. Run: launchctl load ~/Library/LaunchAgents/com.jarvis.vscode.server.plist"
    fi
else
    check_result "Auto-start service installed" "WARN" "Not installed. Run: bash setup-autostart.sh install"
fi

echo ""
echo "6️⃣  Logging Setup Check"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ -d "$LOG_DIR" ]; then
    check_result "Log directory exists" "PASS"
    
    # Check for log files
    if [ -f "$LOG_DIR/server.log" ]; then
        LOG_SIZE=$(stat -f%z "$LOG_DIR/server.log" 2>/dev/null | numfmt --to=iec-i 2>/dev/null || du -h "$LOG_DIR/server.log" | awk '{print $1}')
        check_result "Server logs exist" "PASS" "Size: $LOG_SIZE"
    else
        check_result "Server logs exist" "WARN" "Not created yet (logs generate when server runs)"
    fi
else
    check_result "Log directory exists" "WARN" "Will be created when server starts"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${BLUE}Summary:${NC}"
echo -e "  ${GREEN}Passed:${NC} $PASSED"
[ $WARNINGS -gt 0 ] && echo -e "  ${YELLOW}Warnings:${NC} $WARNINGS"
[ $FAILED -gt 0 ] && echo -e "  ${RED}Failed:${NC} $FAILED"

echo ""

if [ $FAILED -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo -e "${GREEN}✓ All checks passed! JARVIS is ready to use.${NC}"
    echo ""
    echo "Next steps:"
    echo "  1. Make sure server is running:"
    echo "     bash setup-autostart.sh start"
    echo "  2. Open VS Code:"
    echo "     code ."
    echo "  3. Use JARVIS:"
    echo "     Cmd+Shift+P → type 'JARVIS' → select command"
    exit 0
elif [ $FAILED -eq 0 ]; then
    echo -e "${YELLOW}! Some warnings found, but JARVIS should work.${NC}"
    echo ""
    echo "To fix warnings, see recommendations above."
    exit 0
else
    echo -e "${RED}✗ Some checks failed. See above for details.${NC}"
    echo ""
    echo "Common fixes:"
    echo "  • Missing .env: cp .env.template .env && nano .env"
    echo "  • Missing deps: pip install websocket-server anthropic requests"
    echo "  • Missing venv: python3 -m venv jarvis_env && source jarvis_env/bin/activate"
    exit 1
fi
