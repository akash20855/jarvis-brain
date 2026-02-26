#!/bin/bash
# Jarvis Phase 1 Quick Start Guide
# This script demonstrates how everything is connected

echo "======================================"
echo "JARVIS PHASE 1 - QUICK START"
echo "======================================"
echo ""

# Check if running on macOS
if [[ "$OSTYPE" == "darwin"* ]]; then
  echo "🍎 Detected: macOS"
else
  echo "🐧 Detected: Linux"
fi

echo ""
echo "📋 PHASE 1 COMPONENTS:"
echo "  ✅ PostgreSQL Database (data persistence)"
echo "  ✅ Flask Backend API (8001)"
echo "  ✅ React Dashboard (3000)"
echo "  ✅ Complete ORM Models"
echo "  ✅ 15+ REST Endpoints"
echo ""

echo "🚀 STARTUP OPTIONS:"
echo ""
echo "1️⃣  DOCKER (RECOMMENDED - One command):"
echo "   $ docker-compose up -d"
echo ""
echo "2️⃣  AUTOMATED SETUP (macOS):"
echo "   $ chmod +x setup-database.sh"
echo "   $ ./setup-database.sh"
echo ""
echo "3️⃣  MANUAL SETUP:"
echo "   $ pip install -r requirements.txt"
echo "   $ python3 database/init_db.py"
echo "   $ python3 backend/app.py"
echo "   $ cd dashboard && npm install && npm run dev"
echo ""

echo "📱 ACCESS POINTS AFTER STARTUP:"
echo "  🌐 Dashboard:  http://localhost:3000"
echo "  🔌 Backend:    http://localhost:8001"
echo "  📊 pgAdmin:    http://localhost:5050"
echo "  💾 Database:   localhost:5432"
echo ""

echo "🧪 QUICK TEST (after startup):"
echo "  curl http://localhost:8001/api/persistence/health"
echo ""
echo "💾 FILES TO CONFIGURE:"
echo "  $ cp .env.example .env"
echo "  $ # Edit .env with your settings"
echo ""

echo "📚 DOCUMENTATION:"
echo "  - PHASE_1_DATABASE.md (Full documentation)"
echo "  - PHASE_1_COMPLETE.md (Implementation summary)"
echo "  - backend/routes_persistence.py (API reference)"
echo "  - dashboard/README.md (Frontend guide)"
echo ""

echo "✅ SUCCESS CHECKLIST:"
echo "  [ ] PostgreSQL running"
echo "  [ ] Backend connected to database"
echo "  [ ] Dashboard loading at localhost:3000"
echo "  [ ] Chat persistence working"
echo "  [ ] Command logging working"
echo ""

echo "Need help? Check the documentation files or GitHub issues."
echo ""
