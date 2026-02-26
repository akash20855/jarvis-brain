#!/bin/bash
# Production startup script for Jarvis Brain

set -e

echo "🚀 JARVIS BRAIN - PRODUCTION STARTUP"
echo "===================================="

# Get the directory this script is in
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

# Color output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if .env exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠️  .env file not found. Creating from .env.example...${NC}"
    cp .env.example .env
    echo -e "${YELLOW}⚠️  Please edit .env with your configuration${NC}"
fi

# Load environment variables
set -a
source .env
set +a

# Ensure virtual environment exists
if [ ! -d "jarvis_env" ]; then
    echo -e "${BLUE}📦 Creating virtual environment...${NC}"
    python3 -m venv jarvis_env
fi

# Activate virtual environment
echo -e "${BLUE}🔧 Activating virtual environment...${NC}"
source jarvis_env/bin/activate

# Install/update dependencies
echo -e "${BLUE}📦 Installing dependencies...${NC}"
pip install --upgrade pip
pip install -r requirements.txt

# Install frontend dependencies if needed
if [ ! -d "frontend/node_modules" ]; then
    echo -e "${BLUE}📦 Installing frontend dependencies...${NC}"
    cd frontend
    npm install
    npm run build
    cd ..
fi

# Database setup (if needed)
if [ -n "$DATABASE_URL" ]; then
    echo -e "${BLUE}📊 Setting up database...${NC}"
    # Add your database initialization here
fi

# Start services
echo ""
echo -e "${GREEN}===================================${NC}"
echo -e "${GREEN}✅ All dependencies installed!${NC}"
echo -e "${GREEN}===================================${NC}"
echo ""

# Ask what to start
echo "What would you like to start?"
echo "1. Backend only (Flask API)"
echo "2. Frontend only (React dev server)"
echo "3. Both (Backend + Frontend)"
echo "4. Both (production mode)"
echo ""
read -p "Enter choice (1-4): " choice

case $choice in
    1)
        echo -e "${BLUE}Starting Backend...${NC}"
        cd backend
        python3 app.py
        ;;
    2)
        echo -e "${BLUE}Starting Frontend...${NC}"
        cd frontend
        npm run dev
        ;;
    3)
        echo -e "${BLUE}Starting Both (Development)...${NC}"
        
        # Start backend in background
        cd backend
        python3 app.py &
        BACKEND_PID=$!
        echo -e "${GREEN}Backend PID: $BACKEND_PID${NC}"
        cd ..
        
        # Start frontend
        cd frontend
        npm run dev
        
        # Clean up on exit
        kill $BACKEND_PID
        ;;
    4)
        echo -e "${BLUE}Starting Both (Production)...${NC}"
        
        # Build frontend for production
        echo -e "${BLUE}Building frontend...${NC}"
        cd frontend
        npm run build
        cd ..
        
        # Start backend with production settings
        echo -e "${BLUE}Starting backend (production)...${NC}"
        export FLASK_ENV=production
        export FLASK_DEBUG=False
        cd backend
        python3 app.py
        ;;
    *)
        echo -e "${YELLOW}Invalid choice${NC}"
        exit 1
        ;;
esac
