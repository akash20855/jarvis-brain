#!/bin/bash

# ════════════════════════════════════════════════════════════════════════
# JARVIS BRAIN - QUICK REFERENCE GUIDE
# All commands you need to know to build, test, and deploy
# ════════════════════════════════════════════════════════════════════════

cat << 'EOF'

╔════════════════════════════════════════════════════════════════════════╗
║        🚀 JARVIS BRAIN - COMPLETE BUILD SYSTEM (QUICK REFERENCE)      ║
╚════════════════════════════════════════════════════════════════════════╝

📋 TABLE OF CONTENTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  1. Getting Started (First Time)
  2. Common Workflows
  3. Testing & Quality
  4. Docker Deployment
  5. Cloud Deployment
  6. Troubleshooting
  7. Build Scripts Reference


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1️⃣  GETTING STARTED (First Time)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Option A: One-Command Complete Build
  $ make all
  → Creates venv, installs deps, runs tests, builds distribution

Option B: Automated Script
  $ bash scripts/build.sh
  → Complete setup with detailed progress

Option C: Manual Step-by-Step
  $ python3 -m venv jarvis_env
  $ source jarvis_env/bin/activate
  $ pip install -r requirements.txt
  $ export PYTHONPATH=/Volumes/Akash\ SSD/repos/jarvis-brain
  $ python3 -m pytest tests/ -v


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
2️⃣  COMMON WORKFLOWS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 Start Jarvis
  $ make run
  → Launches interactive REPL
  → Commands: status, agents, modules, voice, build, task, research, backup, logs

🎬 See Live Demo
  $ make demo
  → Shows all 6 workflows in action
  → No interaction needed, just watch

🔧 Virtual Environment
  $ make venv              # Create environment
  $ make install           # Install dependencies
  $ make setup             # Both + test

📦 Build Distribution
  $ make build
  → Creates dist/jarvis-brain-*.tar.gz and .whl


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
3️⃣  TESTING & QUALITY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Run All Tests
  $ make test              # Full test suite (all 16 tests)
  $ make test-fast         # Quick run
  $ make test-coverage     # With coverage report (opens htmlcov/)

🔍 Code Quality
  $ make lint              # Check code with pylint

🔄 CI/CD Pipeline
  $ make ci               # test → lint → coverage (full pipeline)


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
4️⃣  DOCKER DEPLOYMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🐳 Local Docker Deployment
  $ bash scripts/docker-build.sh
  → Builds image and starts all services

Manual Steps:
  $ docker build -t jarvis-brain:latest .
  $ docker-compose up -d
  $ docker-compose ps                  # Check services
  $ docker-compose logs -f              # View logs
  $ docker-compose down                 # Stop services

📍 Access Points (After docker-compose up):
  • Jarvis HQ:    http://localhost:5000
  • Prometheus:   http://localhost:9090
  • Grafana:      http://localhost:3000
  • Redis:        localhost:6379
  • PostgreSQL:   localhost:5432


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
5️⃣  CLOUD DEPLOYMENT (AWS S3)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

☁️  Deploy to AWS S3
  $ export AWS_BUCKET=my-jarvis-brain
  $ bash scripts/deploy.sh
  
OR:
  $ make deploy AWS_BUCKET=my-jarvis-brain

Prerequisites:
  ✓ AWS CLI installed: brew install awscli
  ✓ AWS credentials configured: aws configure
  ✓ S3 bucket created

After Deployment:
  → Access files: https://my-jarvis-brain.s3.amazonaws.com/jarvis-brain/


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
6️⃣  TROUBLESHOOTING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔍 Check System Status
  $ bash scripts/status.sh
  → Shows Python version, Docker status, build artifacts

🧹 Clean & Rebuild
  $ make clean             # Remove build artifacts
  $ make clean-all         # Remove everything including venv
  $ bash scripts/clean.sh  # Interactive cleanup

📋 View Documentation
  $ cat BUILD.md           # Complete build guide
  $ cat README.md          # Project documentation

❌ Python3 Not Found
  → macOS: brew install python3
  → Ubuntu: apt install python3

❌ Permission Denied
  $ chmod +x scripts/*.sh

❌ Virtual Env Issues
  $ rm -rf jarvis_env && make venv

❌ Dependencies Won't Install
  $ pip install --upgrade pip
  $ pip install -r requirements.txt


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
7️⃣  BUILD SCRIPTS REFERENCE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📄 scripts/build.sh
  → Automated complete build
  → Creates venv, installs deps, runs tests, builds dist
  $ bash scripts/build.sh

📄 scripts/test.sh
  → Runs unit tests and integration tests
  $ bash scripts/test.sh

📄 scripts/deploy.sh
  → Deploys to AWS S3
  $ AWS_BUCKET=bucket bash scripts/deploy.sh

📄 scripts/docker-build.sh
  → Builds Docker image and starts services
  $ bash scripts/docker-build.sh

📄 scripts/status.sh
  → Shows system diagnostics
  $ bash scripts/status.sh

📄 scripts/clean.sh
  → Interactive cleanup
  $ bash scripts/clean.sh


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 COMPLETE MAKEFILE COMMAND LIST
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SETUP & ENVIRONMENT:
  make help              Show all commands
  make setup             Complete setup (venv + install + test)
  make venv              Create Python virtual environment
  make install           Install all dependencies

TESTING:
  make test              Run all unit tests
  make test-fast         Quick test run
  make test-coverage     Run with coverage report
  make lint              Code quality check

BUILDING:
  make build             Build distribution packages
  make run               Start Jarvis interactive REPL
  make demo              Run workflow demonstration
  make integration-test  Run integration tests

DOCKER:
  make docker-build      Build Docker image
  make docker-up         Start Docker services
  make docker-down       Stop Docker services
  make docker-logs       View Docker logs

CLOUD & MAINTENANCE:
  make deploy            Deploy to AWS S3
  make docs              Generate documentation
  make clean             Remove build artifacts
  make clean-all         Full cleanup (including venv)

CI/CD:
  make ci               Full CI/CD pipeline
  make all              Complete build (everything)


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 TYPICAL WORKFLOW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

First Time:
  1. $ make all              # Everything in one command
  2. $ bash scripts/status.sh # Verify installation
  3. $ make demo             # See it in action

Daily Development:
  1. $ make run              # Start Jarvis
  2. $ make test-fast        # Quick test
  3. $ make docker-up        # Deploy

Before Release:
  1. $ make ci               # Full validation
  2. $ make clean            # Clean artifacts
  3. $ make build            # Build distributions
  4. $ make deploy           # Deploy to cloud


═══════════════════════════════════════════════════════════════════════════
✅ JARVIS BRAIN IS READY! Start with: make all
═══════════════════════════════════════════════════════════════════════════

EOF
