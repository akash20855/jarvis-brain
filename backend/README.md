# 🚀 Jarvis Brain Backend API

Flask-based REST API for AI-powered code evolution.

## 📋 Requirements

- Python 3.11+
- Flask 3.0.0+
- Ollama (optional, for AI features)

## 🔧 Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
python3 app.py

# Server will start on http://localhost:5000
```

## 📡 API Endpoints

### Health & Status
```
GET /api/health
Response: {"status": "online", "version": "1.0.0", "timestamp": "2026-02-26T..."}

GET /api/project/status
Response: {"project_root": "...", "status": "ready", "features": [...]}

GET /api/ai/status
Response: {"ollama": {...}, "local_patterns": {...}}
```

### Code Analysis
```
POST /api/evolve/analyze
Body: {"ai_backend": "patterns"}
Response: {"success": true, "data": {"scanned_files": 42, ...}}

POST /api/evolve/file
Body: {"filepath": "core/main.py"}
Response: {"success": true, "file": "core/main.py", "suggestions": [...]}

GET /api/evolve/suggestions?limit=10
Response: {"success": true, "suggestions": [...], "total": 42}
```

### Chatbot
```
POST /api/chat/message
Body: {"message": "analyze"}
Response: {"success": true, "message": "...", "timestamp": "..."}

GET /api/chat/commands
Response: {"success": true, "commands": {"analyze": "...", ...}}
```

### History & Configuration
```
GET /api/history/improvements?limit=20
Response: {"success": true, "improvements": [...], "total": 15}

GET /api/config/get
Response: {"success": true, "config": {...}}

POST /api/config/set
Body: {"auto_evolution": {"enabled": true}}
Response: {"success": true, "message": "Configuration updated"}
```

## 🔌 Environment Variables

```env
FLASK_ENV=development
FLASK_DEBUG=1
API_HOST=0.0.0.0
API_PORT=5000

# Ollama
OLLAMA_ANALYSIS_URL=http://localhost:11434
OLLAMA_CHAT_URL=http://localhost:11435
OLLAMA_SUGGESTIONS_URL=http://localhost:11436

# Project
PROJECT_ROOT=/path/to/jarvis-brain
```

## 🏗️ Architecture

```
app.py (Flask application)
├── Routes
│   ├── /api/health
│   ├── /api/project/status
│   ├── /api/ai/status
│   ├── /api/evolve/*
│   ├── /api/chat/*
│   ├── /api/history/*
│   └── /api/config/*
└── Engines
    ├── AutoEvolutionEngine (from core/)
    ├── JarvisChatbot (from core/)
    └── AIServiceManager (from core/)
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_api.py

# Run with coverage
pytest --cov=.
```

## 📦 Deployment

### Docker
```bash
docker build -t jarvis-backend .
docker run -p 5000:5000 jarvis-backend
```

### Gunicorn (Production)
```bash
gunicorn --bind 0.0.0.0:5000 --workers 4 app:app
```

### Kubernetes
```bash
kubectl apply -f k8s/deployment.yaml
```

## 🔒 Security

- CORS enabled for frontend
- Input validation on all endpoints
- Error messages sanitized
- Environment variables for sensitive data
- Rate limiting ready (implement in production)

## 💡 Examples

### Analyze a Project
```bash
curl -X POST http://localhost:5000/api/evolve/analyze \
  -H "Content-Type: application/json" \
  -d '{"ai_backend": "patterns"}'
```

### Chat with Jarvis
```bash
curl -X POST http://localhost:5000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{"message": "How can I improve performance?"}'
```

### Get Suggestions
```bash
curl http://localhost:5000/api/evolve/suggestions?limit=5
```

## 📊 Response Format

All responses follow this format:

```json
{
  "success": true,
  "data": {},
  "timestamp": "2026-02-26T11:20:00"
}
```

Error responses:
```json
{
  "success": false,
  "error": "Error message"
}
```

## 🚨 Error Handling

- 400: Bad Request (invalid input)
- 404: Not Found (file/endpoint not found)
- 500: Internal Server Error
- All errors return JSON with `success: false`

## 📈 Performance

- Caching for repeated analyses
- Async support for long operations
- Connection pooling for Ollama
- Request timeouts configured
- Memory optimization for large files

## 🔄 Integration with Frontend

Frontend connects via:
- WebSocket (for real-time updates)
- REST API (for data operations)
- Environment variable `REACT_APP_API_URL`

## 📚 Code Structure

```
backend/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── Dockerfile         # Docker configuration
├── tests/
│   ├── test_api.py
│   └── test_endpoints.py
└── config/
    └── settings.py    # Configuration management
```

## 🤝 Contributing

1. Create a feature branch
2. Make changes
3. Run tests
4. Submit pull request

## 📄 License

MIT License
