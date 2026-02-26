#!/bin/bash

# ════════════════════════════════════════════════════════════════════════
# JARVIS BRAIN - System Status Script
# ════════════════════════════════════════════════════════════════════════

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/." && pwd)"
cd "$PROJECT_ROOT/.."

log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

echo ""
echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     JARVIS BRAIN - SYSTEM STATUS                          ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

log_info "Environment Status:"
echo ""

# Python
if command -v python3 &> /dev/null; then
    PYTHON_VER=$(python3 --version 2>&1 | awk '{print $2}')
    log_success "Python: $PYTHON_VER"
else
    log_warning "Python not found"
fi

# Virtual Environment
if [ -d "jarvis_env" ]; then
    log_success "Virtual Environment: Active"
else
    log_warning "Virtual Environment: Not created"
fi

# Docker
if command -v docker &> /dev/null; then
    DOCKER_VER=$(docker --version | awk '{print $3}')
    log_success "Docker: $DOCKER_VER"
else
    log_warning "Docker not installed"
fi

echo ""
log_info "Project Structure:"
echo ""

echo -e "${YELLOW}Core modules:${NC}"
ls -1 core/*.py 2>/dev/null | wc -l | xargs echo "  Files:"

echo -e "${YELLOW}Agents:${NC}"
ls -1 agents/*.py 2>/dev/null | wc -l | xargs echo "  Files:"

echo -e "${YELLOW}Modules:${NC}"
ls -1 modules/*.py 2>/dev/null | wc -l | xargs echo "  Files:"

echo -e "${YELLOW}Tests:${NC}"
ls -1 tests/*.py 2>/dev/null | wc -l | xargs echo "  Files:"

echo ""
log_info "Build Artifacts:"
echo ""

if [ -d "build" ]; then
    echo -e "${YELLOW}build/${NC} ($(find build -type f | wc -l) files)"
fi

if [ -d "dist" ]; then
    echo -e "${YELLOW}dist/${NC} ($(find dist -type f | wc -l) files)"
fi

if [ -d "htmlcov" ]; then
    echo -e "${YELLOW}htmlcov/${NC} (coverage report)"
fi

if [ -f "build_summary.txt" ]; then
    echo -e "${YELLOW}build_summary.txt${NC}"
fi

echo ""
log_info "Docker Services:"
echo ""

if command -v docker-compose &> /dev/null; then
    docker-compose ps 2>/dev/null || log_warning "No Docker services running"
else
    log_warning "docker-compose not available"
fi

echo ""
log_info "Last Build:"
echo ""

if [ -f "build_summary.txt" ]; then
    head -5 build_summary.txt
else
    log_warning "No build summary found"
fi

echo ""
log_success "Status check complete"
echo ""
