# 🏗️ Jarvis Brain Full-Stack Architecture

Complete technical design and system overview.

## System Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                          │
│                        USER (Browser / Terminal)                        │
│                                                                          │
└────────────────────────────┬────────────────────────────────────────────┘
                             │
             ┌───────────────┼───────────────┐
             │               │               │
             ▼               ▼               ▼
        ┌────────┐      ┌────────┐      ┌─────────┐
        │Frontend│      │Backend │      │Terminal │
        │ (React)│      │ (Flask)│      │ Launcher│
        └────┬───┘      └───┬────┘      └────┬────┘
             │              │               │
             └──────────────┼───────────────┘
                           │
                    HTTP/REST API
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
    ┌─────────┐      ┌──────────┐      ┌──────────┐
    │  Ollama │      │Ollama    │      │ Ollama   │
    │Analysis │      │  Chat    │      │Suggestions
    │Port 11434       │Port11435       │Port 11436
    └────┬────┘      └────┬─────┘      └────┬─────┘
         │                │                  │
         │                │                  │
    [Mistral]        [Neural-Chat]       [Mistral]
         │                │                  │
         └────────────────┼──────────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
     Python           SQLite         Local Files
    Patterns         Redis/PG        Cache
```

## 📊 Component Architecture

### 1. Frontend Layer

**Technology**: React 18 + Axios

**Components**:
- `App.jsx` - Main component with tab routing
- Chat Interface - Message display & input
- Analysis Dashboard - Project statistics
- History Viewer - Improvement tracking
- Settings Panel - Configuration display

**Features**:
- Real-time chat with Jarvis
- Interactive analysis commands
- Dark theme with gradient UI
- Responsive mobile design
- WebSocket-ready for real-time updates

**State Management**:
- React Hooks (useState, useEffect)
- Axios for API calls
- Local component state

### 2. Backend API Layer

**Technology**: Flask 3.0 + Flask-CORS

**Endpoints** (27 total):

**Health & Status**:
- `GET /api/health` - Service health
- `GET /api/project/status` - Project info
- `GET /api/ai/status` - AI service status

**Analysis**:
- `POST /api/evolve/analyze` - Full project scan
- `POST /api/evolve/file` - File-specific analysis
- `GET /api/evolve/suggestions` - Top suggestions

**Chat**:
- `POST /api/chat/message` - User message
- `GET /api/chat/commands` - Available commands

**Data**:
- `GET /api/history/improvements` - Past runs
- `GET /api/config/get` - Current config
- `POST /api/config/set` - Update config

**Error Handling**:
- Global exception handlers
- JSON error responses
- HTTP status codes
- Logging for debugging

### 3. AI Service Layer

**Technology**: Ollama + Local Patterns

**Three Independent Services**:

**Service 1: Code Analysis AI**
- Port: 11434
- Model: Mistral 7B
- Task: Analyzes code patterns
- Detects: Performance issues, bugs, complexity
- Response Time: 5-15 seconds

**Service 2: Chat AI**
- Port: 11435
- Model: Neural-Chat 13B
- Task: User conversations
- Purpose: Answer questions contextually
- Response Time: 3-10 seconds

**Service 3: Suggestion Generator**
- Port: 11436
- Model: Mistral 7B
- Task: Generates improvement suggestions
- Focus: Actionable, ranked suggestions
- Response Time: 5-15 seconds

**Local Patterns Fallback**:
- No API calls needed
- Instant response
- Rule-based analysis
- Pattern matching
- Works offline

### 4. Core Engine Layer

**Auto-Evolution Engine** (`core/auto_evolution.py`):
- Scans Python files
- Extracts code content
- Gets AI suggestions
- Records history
- Tracks metrics

**Chatbot** (`core/chatbot.py`):
- Interactive CLI interface
- Command parsing
- Question understanding
- Response routing
- Conversation history

**AI Service Manager** (`core/ai_services.py`):
- Manages 3 Ollama instances
- Health checks
- Fallback logic
- Error recovery
- Task delegation

**Launcher** (`core/launcher.py`):
- CLI menu system
- Service orchestration
- Configuration management
- Status reporting

### 5. Data Layer

**Storage Options**:

**Option 1: JSON (Default)**
- `.evolution_log.json` - History
- `.evolution_config.json` - Configuration
- Lightweight, portable
- Good for small projects

**Option 2: Redis (In-Memory)**
- Session caching
- Job queue
- Real-time stats
- Fast read/write

**Option 3: PostgreSQL (Relational)**
- Scalable storage
- Complex queries
- Multi-user support
- Transaction support

## 🔄 Data Flow

### User runs "analyze" command:

```
1. User types: "analyze"
   ↓
2. Frontend sends: POST /api/chat/message {"message": "analyze"}
   ↓
3. Backend recognizes command
   ↓
4. Backend calls: AutoEvolutionEngine.scan_project()
   ↓
5. Engine finds all Python files
   ↓
6. For each file:
   - Read source code
   - Get AI suggestions
   - Record results
   ↓
7. AI Service Manager tries:
   - Option 1: Ollama (if running)
   - Option 2: GitHub Copilot (via VS Code)
   - Option 3: Local patterns (always works)
   ↓
8. Results saved to .evolution_log.json
   ↓
9. Response sent to frontend:
   {
     "scanned_files": 42,
     "improvements_found": 15,
     "by_type": {
       "performance": 5,
       "security": 3,
       "quality": 7
     }
   }
   ↓
10. Frontend displays results in chat
    and "Analysis" tab
```

### Real-time Chat Flow:

```
1. User types: "How can I optimize loops?"
   ↓
2. Frontend: POST /api/chat/message
   ↓
3. Backend: chatbot.chat(message)
   ↓
4. Chatbot recognizes performance question
   ↓
5. AI Service Manager.chat_response()
   ↓
6. Tries Ollama connection
   If success:
   - Sends prompt to Chat AI (Port 11435)
   - Gets response
   - Returns to user
   If failed:
   - Uses fallback response
   - Sends general guidance
   ↓
7. Response to frontend
   ↓
8. Frontend displays in chat
```

## 🎯 AI Backend Strategy

### Tier 1: Ollama (Preferred)
**Pros**:
- Free and open-source
- Runs locally (private)
- Full control
- No API key needed
- Customizable models

**Setup**:
```bash
brew install ollama
ollama serve
ollama pull mistral
ollama pull neural-chat
```

### Tier 2: GitHub Copilot (Enterprise)
**Pros**:
- Premium models (Claude, GPT-4)
- Higher accuracy
- Context-aware
- VS Code integration

**Setup**:
- Install GitHub.Copilot extension
- Sign in with GitHub

### Tier 3: Local Patterns (Always Available)
**Pros**:
- Instant response
- No dependencies
- Works offline
- Fallback safety

**Uses**:
- Loop + append → list comp
- eval/exec → security issue
- Long functions → refactor
- TODO comments → cleanup

## 🔐 Security Design

### API Security
- CORS configured for frontend only
- Input validation on all endpoints
- Error messages sanitized
- No sensitive data in responses

### AI Service Security
- Local Ollama (no internet traffic)
- No API keys stored in code
- Environment variables for config
- Service isolation with network

### Data Security
- No credentials in source code
- .env file for secrets
- PostgreSQL password protected
- Redis in isolated network

## 📈 Scalability

### Current Limits
- Single-machine deployment
- ~1000 files analyzed per scan
- ~100 concurrent connections
- ~10MB max file size

### Scaling Options

**Horizontal Scaling**:
- Multiple backend instances
- Load balancer (HAProxy/Nginx)
- Shared database (PostgreSQL)
- Distributed cache (Redis Cluster)

**Vertical Scaling**:
- Larger Docker container
- More CPU cores
- More RAM
- Faster storage

**AI Scaling**:
- Add more Ollama instances
- Use GPU acceleration
- Batch processing
- Async queues (Celery)

## 🧪 Testing Architecture

### Unit Tests
- Backend: `tests/test_api.py`
- Frontend: `src/__tests__/`
- Core: `core/tests/`

### Integration Tests
- API + Database
- Frontend + Backend
- AI + Core Engine

### E2E Tests
- Full user workflows
- Docker container tests
- Multi-service tests

## 📊 Monitoring & Logging

### Logging Levels
```
DEBUG   - Detailed debugging info
INFO    - General information
WARNING - Warning messages
ERROR   - Error details
CRITICAL - System failures
```

### Metrics Tracked
- API response times
- AI service latency
- Files scanned per run
- Improvements found
- User sessions
- Error rates

### Health Checks
- `/api/health` - Service health
- `/api/ai/status` - AI backend status
- Docker health checks
- Database connectivity

## 🚀 Deployment Options

### Development
```bash
npm start (frontend)
python3 app.py (backend)
ollama serve (AI)
```

### Docker Compose (Recommended)
```bash
docker-compose up -d
```

### Kubernetes
```bash
kubectl apply -f k8s/
```

### Cloud Platforms
- AWS ECS
- Google Cloud Run
- Azure Container Instances
- Heroku

## 📚 Technology Stack

```
FRONTEND:
├── React 18.2.0
├── Axios 1.6.0
├── React Icons 4.12.0
├── React Router 6.20.0
└── Tailwind CSS 3.3.0

BACKEND:
├── Flask 3.0.0
├── Flask-CORS 4.0.0
├── Flask-RESTful 0.3.10
├── Python 3.11
└── Gunicorn 21.2.0

AI:
├── Ollama (3 instances)
├── Mistral 7B (analysis)
├── Neural-Chat 13B (chat)
└── Local patterns (fallback)

DATA:
├── PostgreSQL 15
├── Redis 7
├── SQLite (fallback)
└── JSON files

INFRASTRUCTURE:
├── Docker 24.0
├── Docker Compose 2.0
├── GitHub Actions (CI/CD)
└── Nginx (proxy)
```

## 🔄 Continuous Deployment

### GitHub Actions Workflow
1. Commit to main branch
2. Run tests
3. Build Docker images
4. Push to container registry
5. Deploy to production
6. Run smoke tests

## 📝 Configuration Management

### Environment Variables
- API URLs
- AI models
- Database connections
- Log levels
- Feature flags

### Configuration Files
- `.evolution_config.json` - Evolution settings
- `docker-compose.yml` - Services
- `.env` - Environment
- `app.py` - Flask config

## 🎯 Future Architecture

### Planned Enhancements
- Microservices for each AI service
- Event-driven architecture
- Message queue (Kafka/RabbitMQ)
- GraphQL API
- Real-time WebSocket
- Machine learning models
- Advanced analytics

### Phase 2 (Q2 2026)
- User authentication
- Team collaboration
- Git integration
- IDE plugins

### Phase 3 (Q3 2026)
- Custom model training
- Advanced refactoring
- Performance profiling
- Security scanning

---

**Architecture designed for scalability, reliability, and ease of maintenance.**

Last Updated: February 26, 2026
