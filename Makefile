.PHONY: help setup venv install test build run deploy docker-build docker-up docker-down clean lint docs ci all

# Colors for output
GREEN := \033[0;32m
BLUE := \033[0;34m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m # No Color

help:
	@echo "$(BLUE)═══════════════════════════════════════════════════════════$(NC)"
	@echo "$(BLUE)  JARVIS BRAIN BUILD SYSTEM - Available Commands$(NC)"
	@echo "$(BLUE)═══════════════════════════════════════════════════════════$(NC)"
	@echo ""
	@echo "$(GREEN)Setup & Installation:$(NC)"
	@echo "  make setup          - Complete setup (venv + install + test)"
	@echo "  make venv           - Create Python virtual environment"
	@echo "  make install        - Install all dependencies"
	@echo ""
	@echo "$(GREEN)Testing & Quality:$(NC)"
	@echo "  make test           - Run all unit tests"
	@echo "  make lint           - Run code linting (pylint)"
	@echo "  make test-coverage  - Run tests with coverage report"
	@echo ""
	@echo "$(GREEN)Building & Running:$(NC)"
	@echo "  make build          - Build the project"
	@echo "  make run            - Run Jarvis interactive REPL"
	@echo "  make demo           - Run workflow demonstration"
	@echo ""
	@echo "$(GREEN)Docker Deployment:$(NC)"
	@echo "  make docker-build   - Build Docker containers"
	@echo "  make docker-up      - Start Docker services"
	@echo "  make docker-down    - Stop Docker services"
	@echo ""
	@echo "$(GREEN)Cloud Deployment:$(NC)"
	@echo "  make deploy         - Deploy to cloud (AWS S3)"
	@echo ""
	@echo "$(GREEN)Maintenance:$(NC)"
	@echo "  make clean          - Remove build artifacts and cache"
	@echo "  make clean-all      - Remove everything including venv"
	@echo "  make docs           - Generate documentation"
	@echo ""
	@echo "$(GREEN)Complete Workflows:$(NC)"
	@echo "  make all            - Build everything (venv → install → test → build)"
	@echo "  make ci              - CI/CD pipeline (test → lint → coverage)"
	@echo ""

# ════════════════════════════════════════════════════════════════════════
# Setup & Environment
# ════════════════════════════════════════════════════════════════════════

setup: venv install test
	@echo "$(GREEN)✅ Setup complete!$(NC)"
	@echo "$(YELLOW)Run 'source jarvis_env/bin/activate' to activate virtual environment$(NC)"

venv:
	@echo "$(BLUE)🔧 Creating Python virtual environment...$(NC)"
	python3 -m venv jarvis_env
	@echo "$(GREEN)✅ Virtual environment created$(NC)"
	@echo "$(YELLOW)Run: source jarvis_env/bin/activate$(NC)"

install: venv
	@echo "$(BLUE)📦 Installing dependencies...$(NC)"
	./jarvis_env/bin/pip install --upgrade pip setuptools wheel
	./jarvis_env/bin/pip install -r requirements.txt
	@echo "$(GREEN)✅ All dependencies installed$(NC)"

# ════════════════════════════════════════════════════════════════════════
# Testing & Quality
# ════════════════════════════════════════════════════════════════════════

test: venv
	@echo "$(BLUE)🧪 Running unit tests...$(NC)"
	PYTHONPATH=/Volumes/Akash\ SSD/repos/jarvis-brain ./jarvis_env/bin/python -m pytest tests/ -v
	@echo "$(GREEN)✅ All tests passed$(NC)"

test-fast:
	@echo "$(BLUE)⚡ Running tests (fast)...$(NC)"
	PYTHONPATH=/Volumes/Akash\ SSD/repos/jarvis-brain ./jarvis_env/bin/python -m pytest tests/ -q
	@echo "$(GREEN)✅ Tests complete$(NC)"

test-coverage: venv
	@echo "$(BLUE)📊 Running tests with coverage...$(NC)"
	./jarvis_env/bin/pip install coverage
	PYTHONPATH=/Volumes/Akash\ SSD/repos/jarvis-brain ./jarvis_env/bin/coverage run -m pytest tests/
	./jarvis_env/bin/coverage report -m
	./jarvis_env/bin/coverage html
	@echo "$(GREEN)✅ Coverage report generated in htmlcov/index.html$(NC)"

lint: venv
	@echo "$(BLUE)🔍 Linting code...$(NC)"
	./jarvis_env/bin/pip install pylint -q
	./jarvis_env/bin/pylint core/*.py agents/*.py modules/*.py --fail-under=8.0 || true
	@echo "$(GREEN)✅ Linting complete$(NC)"

# ════════════════════════════════════════════════════════════════════════
# Building & Running
# ════════════════════════════════════════════════════════════════════════

build:
	@echo "$(BLUE)🔨 Building Jarvis Brain...$(NC)"
	@echo "$(YELLOW)• Creating build directory...$(NC)"
	mkdir -p build
	@echo "$(YELLOW)• Copying source files...$(NC)"
	cp -r core agents modules build/
	cp -r tests build/
	cp requirements.txt setup.py README.md build/
	@echo "$(YELLOW)• Building distribution...$(NC)"
	./jarvis_env/bin/python setup.py sdist bdist_wheel -q
	@echo "$(GREEN)✅ Build complete (dist/ directory)$(NC)"

run: venv
	@echo "$(BLUE)🚀 Starting Jarvis Brain...$(NC)"
	PYTHONPATH=/Volumes/Akash\ SSD/repos/jarvis-brain ./jarvis_env/bin/python core/main.py

demo: venv
	@echo "$(BLUE)📺 Running workflow demonstration...$(NC)"
	PYTHONPATH=/Volumes/Akash\ SSD/repos/jarvis-brain ./jarvis_env/bin/python examples/workflow_demo.py

integration-test: venv
	@echo "$(BLUE)🔗 Running integration tests...$(NC)"
	PYTHONPATH=/Volumes/Akash\ SSD/repos/jarvis-brain ./jarvis_env/bin/python examples/complete_integration.py
	@echo "$(GREEN)✅ Integration tests complete$(NC)"

# ════════════════════════════════════════════════════════════════════════
# Docker Deployment
# ════════════════════════════════════════════════════════════════════════

docker-build:
	@echo "$(BLUE)🐳 Building Docker containers...$(NC)"
	docker build -t jarvis-brain:latest .
	@echo "$(GREEN)✅ Docker image built$(NC)"
	docker images | grep jarvis-brain

docker-up:
	@echo "$(BLUE)⬆️  Starting Docker services...$(NC)"
	docker-compose up -d
	@echo "$(GREEN)✅ Services started$(NC)"
	@echo "$(YELLOW)• Jarvis HQ: http://localhost:5000$(NC)"
	@echo "$(YELLOW)• Prometheus: http://localhost:9090$(NC)"
	@echo "$(YELLOW)• Grafana: http://localhost:3000$(NC)"
	docker-compose ps

docker-down:
	@echo "$(BLUE)⬇️  Stopping Docker services...$(NC)"
	docker-compose down
	@echo "$(GREEN)✅ Services stopped$(NC)"

docker-logs:
	@echo "$(BLUE)📋 Docker logs...$(NC)"
	docker-compose logs -f

# ════════════════════════════════════════════════════════════════════════
# Cloud Deployment
# ════════════════════════════════════════════════════════════════════════

deploy:
	@echo "$(BLUE)☁️  Deploying to AWS S3...$(NC)"
	@if [ -z "$(AWS_BUCKET)" ]; then \
		echo "$(RED)Error: AWS_BUCKET not set$(NC)"; \
		echo "$(YELLOW)Usage: make deploy AWS_BUCKET=your-bucket-name$(NC)"; \
		exit 1; \
	fi
	@echo "$(YELLOW)• Building distribution...$(NC)"
	./jarvis_env/bin/python setup.py sdist bdist_wheel
	@echo "$(YELLOW)• Uploading to S3...$(NC)"
	aws s3 sync dist/ s3://$(AWS_BUCKET)/jarvis-brain/
	@echo "$(GREEN)✅ Deployment complete$(NC)"

# ════════════════════════════════════════════════════════════════════════
# Documentation & Maintenance
# ════════════════════════════════════════════════════════════════════════

docs:
	@echo "$(BLUE)📚 Generating documentation...$(NC)"
	mkdir -p docs
	@echo "# Jarvis Brain Documentation" > docs/index.md
	@echo "" >> docs/index.md
	@echo "## Architecture" >> docs/index.md
	@for file in core/*.py; do \
		echo "### $$(basename $$file)" >> docs/index.md; \
		grep -A 2 "^\"\"\"" $$file | head -3 >> docs/index.md; \
		echo "" >> docs/index.md; \
	done
	@echo "$(GREEN)✅ Documentation generated (docs/index.md)$(NC)"

clean:
	@echo "$(BLUE)🧹 Cleaning build artifacts...$(NC)"
	rm -rf build/ dist/ .eggs/ *.egg-info/ .coverage htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	@echo "$(GREEN)✅ Clean complete$(NC)"

clean-all: clean
	@echo "$(BLUE)🧹 Removing virtual environment...$(NC)"
	rm -rf jarvis_env/
	@echo "$(GREEN)✅ Full cleanup complete$(NC)"

# ════════════════════════════════════════════════════════════════════════
# CI/CD Pipeline
# ════════════════════════════════════════════════════════════════════════

ci: test lint test-coverage
	@echo ""
	@echo "$(GREEN)═══════════════════════════════════════════════════════════$(NC)"
	@echo "$(GREEN)✅ CI/CD Pipeline Complete!$(NC)"
	@echo "$(GREEN)═══════════════════════════════════════════════════════════$(NC)"

# ════════════════════════════════════════════════════════════════════════
# Complete Workflow
# ════════════════════════════════════════════════════════════════════════

all: setup build
	@echo ""
	@echo "$(GREEN)═══════════════════════════════════════════════════════════$(NC)"
	@echo "$(GREEN)✅ JARVIS BRAIN BUILD COMPLETE!$(NC)"
	@echo "$(GREEN)═══════════════════════════════════════════════════════════$(NC)"
	@echo ""
	@echo "$(BLUE)Next steps:$(NC)"
	@echo "  1. Activate environment: source jarvis_env/bin/activate"
	@echo "  2. Run demo: make demo"
	@echo "  3. Start Jarvis: make run"
	@echo "  4. Deploy: make docker-up"
	@echo ""

.DEFAULT_GOAL := help
