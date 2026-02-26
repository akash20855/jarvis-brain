#!/bin/bash
# Claude Haiku 4.5 - Shell Configuration
# Add this to your ~/.zshrc or ~/.bash_profile for convenient commands

# Project directory
export CLAUDE_PROJECT_DIR="/Volumes/Akash SSD/repos/jarvis-brain"

# Convenient aliases
alias claude-start="cd $CLAUDE_PROJECT_DIR && make claude-start"
alias claude-stop="cd $CLAUDE_PROJECT_DIR && make claude-stop"
alias claude-restart="cd $CLAUDE_PROJECT_DIR && make claude-restart"
alias claude-status="cd $CLAUDE_PROJECT_DIR && make claude-status"
alias claude-logs="cd $CLAUDE_PROJECT_DIR && tail -f backend.log"
alias claude-test="cd $CLAUDE_PROJECT_DIR && make claude-test-api"

# Claude CLI commands (shorter names)
alias cg="$CLAUDE_PROJECT_DIR/claude generate"
alias ca="$CLAUDE_PROJECT_DIR/claude analyze"
alias ct="$CLAUDE_PROJECT_DIR/claude test"
alias cr="$CLAUDE_PROJECT_DIR/claude refactor"
alias ce="$CLAUDE_PROJECT_DIR/claude explain"

# Quick functions for common tasks
function claude-quick() {
    echo "🧠 Starting Claude..."
    cd "$CLAUDE_PROJECT_DIR"
    make claude-start
}

function claude-dev() {
    echo "👨‍💻 Starting Claude in development mode..."
    cd "$CLAUDE_PROJECT_DIR"
    source jarvis_env/bin/activate
    make claude-start
}

# Add project directory to PATH for easy access
export PATH="$CLAUDE_PROJECT_DIR:$PATH"

echo "✅ Claude Haiku 4.5 shell aliases loaded!"
echo ""
echo "Quick Commands:"
echo "  claude-start  - Start Claude"
echo "  claude-stop   - Stop Claude"
echo "  claude-status - Check status"
echo "  cg            - Generate code (cg 'request' python)"
echo "  ca            - Analyze code (ca 'code')"
echo "  ct            - Generate tests (ct 'code' python)"
echo "  cr            - Refactor code (cr 'code' python clean)"
echo "  ce            - Explain code (ce 'code')"
