#!/bin/bash

# ════════════════════════════════════════════════════════════════════════
# JARVIS BRAIN - Cleanup Script
# ════════════════════════════════════════════════════════════════════════

set -e

# Colors
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

echo ""
echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     JARVIS BRAIN - CLEANUP                                ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

read -p "$(echo -e ${YELLOW}Clean build artifacts? [y/N]: ${NC})"
if [[ $REPLY =~ ^[Yy]$ ]]; then
    log_info "Removing build artifacts..."
    rm -rf build/ dist/ .eggs/ *.egg-info/
    log_success "Build artifacts removed"
fi

echo ""
read -p "$(echo -e ${YELLOW}Clean Python cache? [y/N]: ${NC})"
if [[ $REPLY =~ ^[Yy]$ ]]; then
    log_info "Removing Python cache..."
    find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
    find . -type f -name "*.pyc" -delete
    log_success "Python cache cleaned"
fi

echo ""
read -p "$(echo -e ${YELLOW}Remove virtual environment? [y/N]: ${NC})"
if [[ $REPLY =~ ^[Yy]$ ]]; then
    log_info "Removing virtual environment..."
    rm -rf jarvis_env/
    log_success "Virtual environment removed"
fi

echo ""
log_success "Cleanup complete"
