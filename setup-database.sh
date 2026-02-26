#!/bin/bash
# Jarvis Database Setup Script for macOS
# Sets up PostgreSQL, creates database, and initializes schema

set -e  # Exit on error

echo "======================================"
echo "JARVIS DATABASE SETUP"
echo "======================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if PostgreSQL is installed
echo "Checking PostgreSQL installation..."
if ! command -v psql &> /dev/null; then
    echo -e "${RED}❌ PostgreSQL not found${NC}"
    echo ""
    echo "Installing PostgreSQL via Homebrew..."
    if ! command -v brew &> /dev/null; then
        echo -e "${RED}Homebrew not found. Please install from https://brew.sh${NC}"
        exit 1
    fi
    
    brew install postgresql@15
    brew services start postgresql@15
    
    # Add PostgreSQL to PATH for current session
    export PATH="/usr/local/opt/postgresql@15/bin:$PATH"
    
    echo -e "${GREEN}✅ PostgreSQL installed and started${NC}"
else
    echo -e "${GREEN}✅ PostgreSQL found$(psql --version)${NC}"
fi

echo ""
echo "Starting PostgreSQL service..."
# Try to start the service (won't error if already running)
brew services start postgresql@15 2>/dev/null || true

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to be ready..."
for i in {1..30}; do
    if pg_isready -h localhost -U postgres >/dev/null 2>&1; then
        echo -e "${GREEN}✅ PostgreSQL is ready${NC}"
        break
    fi
    if [ $i -eq 30 ]; then
        echo -e "${RED}❌ PostgreSQL is not responding${NC}"
        exit 1
    fi
    sleep 1
done

echo ""
echo "Installing Python dependencies..."
pip install -r requirements.txt

echo ""
echo "Running database initialization..."
python3 database/init_db.py

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✅ DATABASE SETUP COMPLETE${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Copy .env.example to .env and update DATABASE_URL if needed"
    echo "2. Start the backend: python3 backend/app.py"
    echo "3. Access the dashboard: http://localhost:3000"
    echo ""
else
    echo -e "${RED}❌ Database initialization failed${NC}"
    exit 1
fi
