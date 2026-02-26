#!/bin/bash

# ════════════════════════════════════════════════════════════════════════
# JARVIS BRAIN - AI Auto-Evolution Setup
# Configures free AI for continuous code evolution
# ════════════════════════════════════════════════════════════════════════

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

echo ""
echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     JARVIS BRAIN - AI AUTO-EVOLUTION SETUP                ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

PROJECT_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." && pwd )"
cd "$PROJECT_ROOT"

# Activate venv
if [ -d "jarvis_env" ]; then
    source jarvis_env/bin/activate
    log_success "Virtual environment activated"
else
    log_error "Virtual environment not found"
    exit 1
fi

echo ""
log_info "Setting up AI Auto-Evolution..."
echo ""

# Option 1: Check for Ollama (free, local)
echo "1️⃣  Checking for Ollama (free local AI)..."
if command -v ollama &> /dev/null; then
    log_success "Ollama found! Running locally"
    echo ""
    echo "Make sure Ollama is running:"
    echo "  $ ollama serve"
    echo ""
    echo "Download a model (first time):"
    echo "  $ ollama pull mistral  # ~4GB, fast inference"
    echo "  $ ollama pull neural-chat  # ~4GB, good quality"
else
    log_warning "Ollama not installed (optional, for local free AI)"
    echo "Install from: https://ollama.ai"
    echo ""
fi

# Option 2: GitHub Copilot (free with GitHub account)
echo "2️⃣  GitHub Copilot setup..."
log_info "VS Code extension can use Copilot (free tier available)"
echo "  Install: GitHub.Copilot extension"
echo "  Uses: Free tier + Claude AI"
echo ""

# Option 3: Local pattern-based improvements
log_success "Local pattern-based improvements (works without AI)"
echo "  • Detects performance issues"
echo "  • Security vulnerability checks"
echo "  • Code quality analysis"
echo ""

# Setup VS Code integration
log_info "Setting up VS Code integration..."
python3 -c "
from core.vscode_integration import VSCodeIntegration
integration = VSCodeIntegration('.')
integration.setup_all()
"

log_success "VS Code integration complete"
echo ""

# Create evolution config
log_info "Creating evolution configuration..."

cat > .evolution_config.json << 'EOF'
{
  "auto_evolution": {
    "enabled": true,
    "free_ai_options": [
      {
        "name": "Ollama (Local)",
        "provider": "ollama",
        "models": ["mistral", "neural-chat", "dolphin-mixtral"],
        "cost": "FREE - runs locally",
        "setup": "ollama.ai",
        "speed": "Fast",
        "privacy": "100% local"
      },
      {
        "name": "GitHub Copilot",
        "provider": "github_copilot",
        "cost": "FREE tier available",
        "setup": "GitHub.Copilot VS Code extension",
        "speed": "Instant",
        "quality": "High"
      },
      {
        "name": "Hugging Face (Free)",
        "provider": "hugging_face",
        "models": ["mistral-7b", "neural-chat"],
        "cost": "FREE - rate limited",
        "api": "https://huggingface.co/inference-api",
        "setup": "Get free API key"
      },
      {
        "name": "Claude API (Free tier)",
        "provider": "anthropic",
        "cost": "$5 free credit monthly",
        "setup": "API key from console.anthropic.com",
        "quality": "Excellent",
        "rate_limit": "5 requests/minute"
      }
    ],
    "recommended": "Ollama (completely free, runs locally, no rate limits)",
    "scan_interval_seconds": 3600,
    "auto_apply_security_fixes": false,
    "auto_apply_performance": true,
    "notify_on_improvements": true
  }
}
EOF

log_success "Evolution config created: .evolution_config.json"
echo ""

# Show usage
echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
echo "🚀 READY TO USE AUTO-EVOLUTION!"
echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
echo ""

echo "Option A: Use Ollama (Recommended - Free, Local)"
echo "  1. Install: brew install ollama"
echo "  2. Start: ollama serve"
echo "  3. Download: ollama pull mistral"
echo "  4. Run analysis: python3 -m core.auto_evolution"
echo ""

echo "Option B: Use via VS Code (GitHub Copilot)"
echo "  1. Install extension: GitHub.Copilot"
echo "  2. Press Cmd+Shift+P"
echo "  3. Run: Tasks: Run Task → Jarvis: Auto-Evolve Code"
echo ""

echo "Option C: Local Pattern-Based (Works Now!)"
echo "  • No AI needed"
echo "  • Detects issues automatically"
echo "  • Run: python3 -m core.auto_evolution"
echo ""

echo "📚 Learn More:"
echo "  • .evolution_config.json - Configuration"
echo "  • core/auto_evolution.py - Main engine"
echo "  • core/vscode_integration.py - VS Code setup"
echo ""

log_success "Setup complete!"
echo ""
