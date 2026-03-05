# 🚀 JARVIS BRAIN - Complete Build System

**Status:** ✅ Production Ready | **Build Date:** 2026-02-26 | **Python:** 3.8+

---

## 📋 Build System Overview

The Jarvis Brain build system provides complete automation for:
- Virtual environment setup
- Dependency installation
- Unit & integration testing
- Distribution building
- Docker containerization
- Cloud deployment

---

## 🛠️ Quick Start

### Option 1: Automated Build (Recommended)
```bash
# Run complete build in one command
bash scripts/build.sh
```

### Option 2: Using Makefile
```bash
# Complete setup
make all

# Or individual steps
make setup       # venv + install + test
make run         # Start Jarvis
make docker-up   # Deploy with Docker
```

### Option 3: Manual Steps
```bash
# Create virtual environment
python3 -m venv jarvis_env
source jarvis_env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run tests
export PYTHONPATH=/Volumes/Akash\ SSD/repos/jarvis-brain
python3 -m pytest tests/ -v

# Start Jarvis
python3 core/main.py
```

---

## 📦 Build Commands

### Virtual Environment & Setup
```bash
make venv              # Create Python virtual environment
make install           # Install all dependencies
make setup             # Complete setup (venv + install + test)
```

### Testing & Quality
```bash
make test              # Run all unit tests
make test-fast         # Quick test run
make test-coverage     # Run with coverage report
make lint              # Code quality check (pylint)
make ci               # Full CI/CD pipeline
```

### Building & Deployment
```bash
make build             # Build distribution packages
make run               # Start Jarvis interactive REPL
make demo              # Run workflow demonstration
make integration-test  # Run integration tests
```

### Android
```bash
make android           # Run Android agent tests and show status
make android-test      # Run Android agent unit tests
make android-status    # Show Android agent status
```

### Docker Operations
```bash
make docker-build      # Build Docker image
make docker-up         # Start Docker services
make docker-down       # Stop Docker services
make docker-logs       # View Docker logs
```

### Cloud & Maintenance
```bash
make deploy            # Deploy to AWS S3
make docs              # Generate documentation
make clean             # Remove build artifacts
make clean-all         # Full cleanup including venv
```

---

## 📂 Project Structure After Build

```
jarvis-brain/
├── jarvis_env/                 # Virtual environment
├── build/                      # Build artifacts
├── dist/                       # Distribution packages
│   ├── jarvis-brain-*.tar.gz  # Source distribution
│   └── jarvis-brain-*.whl     # Wheel distribution
├── htmlcov/                    # Coverage report
├── docs/                       # Documentation
├── scripts/                    # Build automation scripts
│   ├── build.sh               # Full build automation
│   ├── test.sh                # Test runner
│   ├── deploy.sh              # Cloud deployment
│   ├── docker-build.sh        # Docker builder
│   ├── status.sh              # System status
│   └── clean.sh               # Cleanup script
└── core, agents, modules, tests/  # Source code
```

---

## 🔧 Build Scripts Reference

### `scripts/build.sh`
Complete automated build:
- Creates virtual environment
- Installs all dependencies
- Runs unit tests
- Builds distribution packages
- Generates documentation

**Usage:**
```bash
bash scripts/build.sh
```

### `scripts/test.sh`
Runs complete test suite:
- Unit tests
- Integration tests
- Test output formatting

**Usage:**
```bash
bash scripts/test.sh
```

### `scripts/deploy.sh`
Cloud deployment to AWS S3:
- Builds distribution
- Uploads to S3 bucket
- Generates deployment report

**Usage:**
```bash
AWS_BUCKET=my-bucket bash scripts/deploy.sh
```

### `scripts/docker-build.sh`
Docker container operations:
- Builds Docker image
- Starts services
- Shows access endpoints

**Usage:**
```bash
bash scripts/docker-build.sh
```

### `scripts/status.sh`
System status and diagnostics:
- Environment check
- Project structure
- Build artifacts
- Service status

**Usage:**
```bash
bash scripts/status.sh
```

### `scripts/clean.sh`
Interactive cleanup:
- Remove build artifacts
- Clear Python cache
- Remove virtual environment

**Usage:**
```bash
bash scripts/clean.sh
```

---

## 📊 Makefile Targets

### Help & Information
```bash
make help              # Show all available commands
```

### Complete Workflows
```bash
make all               # Full build: venv → install → test → build
make ci               # CI/CD: test → lint → coverage
```

---

## 🐳 Docker Deployment

### Quick Start
```bash
# Build and start everything
make docker-build
make docker-up

# View services
docker-compose ps

# Access points:
# - Jarvis HQ: http://localhost:5000
# - Prometheus: http://localhost:9090
# - Grafana: http://localhost:3000
# - Redis: localhost:6379
# - PostgreSQL: localhost:5432
```

### Stop Services
```bash
make docker-down
```

### View Logs
```bash
make docker-logs
```

---

## ☁️ Cloud Deployment

### Deploy to AWS S3
```bash
# Set bucket name
export AWS_BUCKET=my-jarvis-bucket

# Deploy
make deploy
```

**Required:**
- AWS CLI installed
- AWS credentials configured
- S3 bucket created

---

## 🧪 Testing

### Run All Tests
```bash
make test
```

### With Coverage
```bash
make test-coverage
# View report: open htmlcov/index.html
```

### Quick Test
```bash
make test-fast
```

### Integration Tests
```bash
make integration-test
```

---

## 🔍 Verification

### Check Build Status
```bash
bash scripts/status.sh
```

### View Build Summary
```bash
cat build_summary.txt
```

### Check Artifacts
```bash
ls -lh dist/
```

---

## 📋 Build Configuration

### `requirements.txt`
All Python dependencies:
- Flask (web dashboard)
- NLTK (NLP processing)
- SpeechRecognition (voice input)
- pytest (testing)
- Docker (containerization)
- And 40+ more packages

### `setup.py`
Package configuration:
- Project metadata
- Dependencies
- Entry points
- Package discovery

### `.env.example`
Environment template:
```bash
cp .env.example .env
# Edit .env with your credentials
```

---

## 🚀 Running Jarvis

### Interactive REPL
```bash
make run
```

**Commands:**
- `status` - System status
- `agents` - List available agents
- `modules` - List modules
- `voice your_command` - Process voice command
- `build` - Build project
- `task description` - Create task
- `research topic` - Research
- `backup` - Backup system
- `logs` - View audit logs

### Workflow Demo
```bash
make demo
```

Shows all 6 workflows:
1. Voice → AI Decision → Execution
2. 24/7 Listening with device switching
3. Autonomous integration setup
4. Cloud failover when offline
5. Watchdog auto-recovery
6. Android control hub

---

## 🔧 Customization

### Modify Dependencies
Edit `requirements.txt` then:
```bash
make install
```

### Update Configuration
Edit `config.yaml`:
```yaml
logging:
  level: INFO
  handlers: [console, file]

agents:
  mac:
    enabled: true
    devices: 10
  
  android:
    enabled: true
    control_hub: true
```

### Environment Variables
Create `.env`:
```bash
AWS_BUCKET=my-bucket
WHATSAPP_API_KEY=key
TWILIO_API_KEY=key
GITHUB_TOKEN=token
```

---

## 📚 Build Artifacts

### Distribution Packages
- `dist/jarvis-brain-*.tar.gz` - Source distribution
- `dist/jarvis-brain-*.whl` - Wheel distribution

### Documentation
- `docs/BUILD_INFO.md` - Build information
- `docs/index.md` - API documentation
- `htmlcov/` - Test coverage report
- `build_summary.txt` - Last build summary

---

## ⚠️ Troubleshooting

### Python3 Not Found
```bash
# Install Python 3.8+
brew install python3  # macOS
apt install python3   # Ubuntu/Debian
```

### Permission Denied on Scripts
```bash
chmod +x scripts/*.sh
```

### Virtual Environment Issues
```bash
# Remove and recreate
rm -rf jarvis_env
make venv
```

### Dependency Installation Fails
```bash
# Upgrade pip and try again
pip install --upgrade pip
pip install -r requirements.txt
```

### Docker Not Running
```bash
# Install or start Docker
brew install docker-desktop  # macOS
docker-compose up           # Start services
```

---

## 🎯 Next Steps

1. **Run Build**
   ```bash
   make all
   ```

2. **Verify Installation**
   ```bash
   bash scripts/status.sh
   ```

3. **Run Demo**
   ```bash
   make demo
   ```

4. **Start Jarvis**
   ```bash
   make run
   ```

5. **Deploy** (optional)
   ```bash
   # Local Docker
   make docker-up
   
   # Or Cloud
   make deploy AWS_BUCKET=your-bucket
   ```

---

## 📞 Support

Check logs for issues:
```bash
# View audit logs in Jarvis
> logs

# View recent build summary
cat build_summary.txt

# Check Docker logs
docker-compose logs -f
```

---

## ✅ Production Checklist

- [ ] Run `make all` successfully
- [ ] All 16 tests passing
- [ ] Demo runs without errors
- [ ] Virtual environment created
- [ ] Distribution packages built
- [ ] Documentation generated
- [ ] `.env` file configured
- [ ] Docker installed (for deployment)
- [ ] AWS CLI configured (for cloud deployment)

---

**🚀 Jarvis Brain is ready for deployment!**

*Build System Version: 1.0 | Last Updated: 2026-02-26*
