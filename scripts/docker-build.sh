#!/bin/bash

# ════════════════════════════════════════════════════════════════════════
# JARVIS BRAIN - Docker Build & Deployment Script
# ════════════════════════════════════════════════════════════════════════

set -e

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

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

echo ""
echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     JARVIS BRAIN - DOCKER DEPLOYMENT                      ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check Docker
if ! command -v docker &> /dev/null; then
    log_error "Docker not installed. Install from https://www.docker.com/"
    exit 1
fi
log_success "Docker found"
echo ""

# Check docker-compose
if ! command -v docker-compose &> /dev/null; then
    log_warning "docker-compose not found, trying 'docker compose'"
    DOCKER_COMPOSE="docker compose"
else
    DOCKER_COMPOSE="docker-compose"
fi
log_success "Docker compose found: $DOCKER_COMPOSE"
echo ""

# Build image
log_info "Building Docker image..."
docker build -t jarvis-brain:latest --no-cache . 2>&1 | tail -20
log_success "Docker image built"
echo ""

# Show image info
log_info "Image information:"
docker images | grep jarvis-brain
echo ""

# Start services
log_info "Starting Docker services..."
$DOCKER_COMPOSE up -d
log_success "Docker services started"
echo ""

# Show running services
log_info "Running services:"
$DOCKER_COMPOSE ps
echo ""

log_info "Access points:"
echo -e "${YELLOW}  • Jarvis HQ: http://localhost:5000${NC}"
echo -e "${YELLOW}  • Prometheus: http://localhost:9090${NC}"
echo -e "${YELLOW}  • Grafana: http://localhost:3000${NC}"
echo -e "${YELLOW}  • Redis: localhost:6379${NC}"
echo -e "${YELLOW}  • PostgreSQL: localhost:5432${NC}"
echo ""

log_success "Docker deployment complete!"
echo ""
