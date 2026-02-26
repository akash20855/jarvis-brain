#!/bin/bash

# ════════════════════════════════════════════════════════════════════════
# JARVIS BRAIN - Test Suite Runner
# ════════════════════════════════════════════════════════════════════════

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/." && pwd)"
cd "$PROJECT_ROOT/.."

log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

echo ""
echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     JARVIS BRAIN - TEST SUITE                             ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Activate venv if exists
if [ -d "jarvis_env" ]; then
    source jarvis_env/bin/activate
fi

export PYTHONPATH="$PROJECT_ROOT/.."

log_info "Running unit tests..."
echo ""
python3 -m pytest tests/ -v --tb=short
echo ""
log_success "Unit tests complete"
echo ""

log_info "Running integration tests..."
echo ""
python3 examples/complete_integration.py || log_error "Integration tests had issues (expected if dependencies missing)"
echo ""
log_success "Test suite complete"
