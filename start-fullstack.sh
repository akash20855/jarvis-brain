#!/bin/bash

# Jarvis Brain - Full Stack Launcher
# Complete setup and run script for the full-stack application

set -e

echo "
╔════════════════════════════════════════════════════════════════════════╗
║                                                                        ║
║           🤖 JARVIS BRAIN - FULL STACK LAUNCHER                        ║
║                                                                        ║
║              Backend • Frontend • 3x Ollama AI Instances                ║
║                                                                        ║
╚════════════════════════════════════════════════════════════════════════╝
"

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo ""
echo "📋 Checking prerequisites..."

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    exit 1
fi
echo "✅ Python 3 found"

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "⚠️  Node.js is not installed (only needed for frontend development)"
else
    echo "✅ Node.js found"
fi

echo ""
echo "🏗️  Setting up directories..."

# Create necessary directories
mkdir -p data logs configs
echo "✅ Directories created"

echo ""
echo "🔧 Building Docker images..."

# Build backend
echo "  Building backend..."
docker-compose build jarvis-backend

# Build frontend
echo "  Building frontend..."
docker-compose build jarvis-frontend

echo "✅ Docker images built"

echo ""
echo "🚀 Starting services..."

# Start all services
docker-compose up -d

echo "✅ All services started"

echo ""
echo "⏳ Waiting for services to be ready..."

# Wait for backend to be ready
echo "  Waiting for Backend API..."
for i in {1..30}; do
    if curl -s http://localhost:5000/api/health > /dev/null; then
        echo "  ✅ Backend API is ready"
        break
    fi
    echo "  ⏳ Attempt $i/30..."
    sleep 2
done

# Wait for frontend to be ready
echo "  Waiting for Frontend..."
for i in {1..30}; do
    if curl -s http://localhost:3000 > /dev/null; then
        echo "  ✅ Frontend is ready"
        break
    fi
    echo "  ⏳ Attempt $i/30..."
    sleep 2
done

echo ""
echo "🎉 Jarvis Brain Full Stack is Running!"
echo ""
echo "📱 Access Points:"
echo "  • Frontend:        http://localhost:3000"
echo "  • Backend API:     http://localhost:5000/api"
echo "  • API Health:      http://localhost:5000/api/health"
echo ""
echo "🤖 AI Services:"
echo "  • Code Analysis:   http://localhost:11434"
echo "  • Chat AI:         http://localhost:11435"
echo "  • Suggestions AI:  http://localhost:11436"
echo ""
echo "📊 Utilities:"
echo "  • Redis:           http://localhost:6379"
echo "  • PostgreSQL:      localhost:5432"
echo ""
echo "📋 Available Commands:"
echo "  • View logs:       docker-compose logs -f jarvis-backend"
echo "  • Stop services:   docker-compose down"
echo "  • Restart:         docker-compose restart"
echo "  • Check status:    docker-compose ps"
echo ""
echo "💡 Next Steps:"
echo "  1. Open http://localhost:3000 in your browser"
echo "  2. Start chatting with Jarvis!"
echo "  3. Run 'analyze' to scan your project"
echo "  4. Check improvements in the Analysis tab"
echo ""
echo "📖 Documentation:"
echo "  • Backend API:     ./backend/README.md"
echo "  • Frontend:        ./frontend/README.md"
echo "  • AI Services:     ./core/ai_services.py"
echo ""
