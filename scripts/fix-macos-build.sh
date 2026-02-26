#!/bin/bash

# ════════════════════════════════════════════════════════════════════════
# JARVIS BRAIN - macOS Build Fix Script
# Handles common build issues on macOS
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
echo -e "${BLUE}║     JARVIS BRAIN - macOS BUILD FIX UTILITY                ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

PROJECT_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." && pwd )"
cd "$PROJECT_ROOT"

# Check OS
if [[ "$OSTYPE" != "darwin"* ]]; then
    log_error "This script is for macOS only"
    exit 1
fi

# Menu
echo "Choose an option:"
echo ""
echo "1. Install Xcode Command Line Tools (Recommended)"
echo "2. Upgrade pip/setuptools/wheel"
echo "3. Clean and rebuild (remove venv)"
echo "4. Install with binary-only packages"
echo "5. Show build error details"
echo ""

read -p "Enter option (1-5): " option

case $option in
    1)
        log_info "Installing Xcode Command Line Tools..."
        log_warning "This may take 10-20 minutes. Please complete the system dialog."
        xcode-select --install
        log_success "Xcode tools installed. Run 'make all' again."
        ;;
    
    2)
        log_info "Upgrading pip, setuptools, wheel..."
        if [ -d "jarvis_env" ]; then
            source jarvis_env/bin/activate
            pip install --upgrade pip setuptools wheel
            log_success "Upgraded successfully"
        else
            log_error "Virtual environment not found. Run 'make venv' first."
        fi
        ;;
    
    3)
        log_warning "This will delete your virtual environment."
        read -p "Continue? (y/n): " confirm
        if [[ $confirm == "y" ]]; then
            log_info "Removing virtual environment..."
            rm -rf jarvis_env
            log_info "Creating new environment..."
            python3 -m venv jarvis_env
            source jarvis_env/bin/activate
            pip install --upgrade pip setuptools wheel
            log_success "Clean environment ready. Run 'make install' to proceed."
        fi
        ;;
    
    4)
        log_info "Installing with binary-only packages (--only-binary :all:)..."
        if [ -d "jarvis_env" ]; then
            source jarvis_env/bin/activate
            pip install --upgrade pip setuptools wheel
            pip install --only-binary :all: -r requirements.txt 2>&1 | head -20 || true
            log_warning "Some packages may not have binary wheels. Trying with --prefer-binary..."
            pip install --prefer-binary -r requirements.txt
            log_success "Installation complete"
        else
            log_error "Virtual environment not found. Run 'make venv' first."
        fi
        ;;
    
    5)
        log_info "Build system information:"
        echo ""
        echo "Python Version:"
        python3 --version
        echo ""
        echo "pip Configuration:"
        pip show pip | grep Version
        echo ""
        echo "System Information:"
        uname -a
        echo ""
        echo "Xcode Status:"
        if xcode-select -p &> /dev/null; then
            log_success "Xcode command line tools: INSTALLED"
        else
            log_warning "Xcode command line tools: NOT INSTALLED"
            echo "Install with: xcode-select --install"
        fi
        ;;
    
    *)
        log_error "Invalid option"
        ;;
esac

echo ""
