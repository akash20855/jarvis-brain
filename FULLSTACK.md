# 🤖 Jarvis Brain - Full Stack AI Code Evolution

Transform your code with **AI-powered automatic improvements** using a complete full-stack application with **separate AI instances**.

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (React)                          │
│              http://localhost:3000                          │
│  • Chat Interface  • Analysis Dashboard  • History Viewer    │
└───────────────────┬─────────────────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────────────────┐
│              BACKEND API (Flask)                            │
│              http://localhost:5000/api                      │
│  • REST Endpoints  • File Analysis  • Configuration         │
└───────────────────┬──────────────────┬──────────────────────┘
                    │                  │
        ┌───────────┴──────┐    ┌──────┴─────────────┐
        │                  │    │                    │
        ▼                  ▼    ▼                    ▼
    ┌────────────┐  ┌────────────┐  ┌────────────┐
    │  Ollama 1  │  │  Ollama 2  │  │  Ollama 3  │
    │  Analysis  │  │    Chat    │  │ Suggestions│
    │ Port 11434 │  │ Port 11435 │  │ Port 11436 │
    └────────────┘  └────────────┘  └────────────┘
```

## ✨ Features

- **Frontend UI**: Beautiful React dashboard with real-time chat
- **Backend API**: Flask REST API with CORS support
- **Separate AI Instances**: 3 independent Ollama services
  - Code Analysis (Mistral)
  - Chat Responses (Neural-Chat)  
  - Suggestion Generation (Mistral)
- **Fallback Modes**: Works offline with pattern-based analysis
- **Docker Support**: Complete containerization with docker-compose
- **Database Support**: PostgreSQL + Redis for data persistence

## 🚀 Quick Start

### Option 1: Docker (Recommended)

```bash
# Make the startup script executable
chmod +x start-fullstack.sh

# Start everything with one command
./start-fullstack.sh

# Open http://localhost:3000 in your browser
```

### Option 2: Manual Setup

**Backend:**
```bash
cd backend
pip install -r requirements.txt
python3 app.py
# Runs on http://localhost:5000
```

**Frontend:**
```bash
cd frontend
npm install
npm start
# Runs on http://localhost:3000
```

**AI Services (requires Ollama):**
```bash
# Terminal 1: Analysis AI
ollama serve
# Then in another terminal: ollama pull mistral

# Terminal 2: Chat AI (on port 11435)
OLLAMA_HOST=127.0.0.1:11435 ollama serve

# Terminal 3: Suggestions AI (on port 11436)  
OLLAMA_HOST=127.0.0.1:11436 ollama serve
```

## 📡 API Endpoints

### Health & Status
- `GET /api/health` - Health check
- `GET /api/project/status` - Project status
- `GET /api/ai/status` - AI services status

### Code Analysis
- `POST /api/evolve/analyze` - Analyze entire project
- `POST /api/evolve/file` - Analyze specific file
- `GET /api/evolve/suggestions` - Get suggestions

### Chatbot
- `POST /api/chat/message` - Send chat message
- `GET /api/chat/commands` - Get available commands

### History & Configuration
- `GET /api/history/improvements` - Get improvement history
- `GET /api/config/get` - Get configuration
- `POST /api/config/set` - Update configuration

## 🎯 Usage Examples

### Chat Commands

```
> analyze              # Scan entire project
> file core/main.py   # Analyze specific file
> suggestions         # Show top suggestions
> help               # Show all commands
```

### Chat Questions

```
> How can I improve performance?
> Any security issues?
> How do I refactor this?
> Best practices for X?
```

## 🛠️ Configuration

Create `.env` file (example provided):

```env
# AI Services
OLLAMA_ANALYSIS_URL=http://localhost:11434
OLLAMA_CHAT_URL=http://localhost:11435
OLLAMA_SUGGESTIONS_URL=http://localhost:11436

# Database
DATABASE_URL=postgresql://jarvis:password@localhost/jarvis_brain
REDIS_URL=redis://localhost:6379

# AI Backend (patterns, ollama, copilot)
AI_BACKEND=patterns
```

## 📊 Project Structure

```
jarvis-brain/
├── frontend/              # React UI
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── index.jsx
│   ├── package.json
│   └── Dockerfile
├── backend/               # Flask API
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
├── core/                  # Python core
│   ├── auto_evolution.py
│   ├── chatbot.py
│   ├── launcher.py
│   └── ai_services.py
├── docker-compose.yml     # Full stack compose
├── start-fullstack.sh     # Startup script
└── README.md             # This file
```

## 🔧 Architecture Details

### AI Service Manager

The `core/ai_services.py` module manages separate AI instances:

```python
# Three dedicated AI services
1. Code Analysis AI (Port 11434)
   - Analyzes code for improvements
   - Detects performance issues
   
2. Chat AI (Port 11435)
   - Handles user conversations
   - Provides contextual responses
   
3. Suggestions AI (Port 11436)
   - Generates improvement suggestions
   - Prioritizes by severity
```

### Fallback Strategy

If AI services are offline:
- Uses pattern-based analysis
- Works completely offline
- Smaller but functional suggestions
- Automatic fallback, no configuration needed

## 🧪 Testing

```bash
# Run backend tests
cd backend
pytest

# Run frontend tests
cd frontend
npm test

# Check AI services
python3 -m core.ai_services
```

## 📈 Monitoring

### Docker Status
```bash
docker-compose ps
docker-compose logs -f jarvis-backend
docker-compose logs -f ollama-analysis
```

### API Health
```bash
curl http://localhost:5000/api/health
curl http://localhost:5000/api/ai/status
```

### Frontend
Open http://localhost:3000 and check the Settings tab

## 🔒 Security

- Flask CORS configured for frontend
- API authentication ready (extend in `app.py`)
- Environment variables for sensitive data
- Docker isolation between services
- No credentials in source code

## 📝 Example Workflow

1. **Start Application**
   ```bash
   ./start-fullstack.sh
   ```

2. **Open Frontend**
   - Go to http://localhost:3000

3. **Chat with Jarvis**
   - "analyze" - Scan your project
   - "suggestions" - See top improvements
   - "How can I optimize X?" - Ask questions

4. **View Results**
   - Improvement suggestions appear in chat
   - Click "Analysis" tab for detailed breakdown
   - Check "History" tab for past improvements

5. **Take Action**
   - Read suggestions
   - Apply improvements manually
   - Re-run analysis to verify

## 🐳 Docker Commands

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild images
docker-compose build

# Check service health
docker-compose ps

# Scale AI services (if needed)
docker-compose up -d --scale ollama-analysis=2
```

## 🚨 Troubleshooting

### Frontend can't connect to API
```bash
# Check if backend is running
curl http://localhost:5000/api/health

# Check CORS settings in backend/app.py
# Make sure http://localhost:3000 is in CORS_ORIGINS
```

### AI services not responding
```bash
# Check if Ollama containers are running
docker-compose logs ollama-analysis

# Download models if needed
docker exec ollama-analysis ollama pull mistral
docker exec ollama-chat ollama pull neural-chat
docker exec ollama-suggestions ollama pull mistral
```

### Database connection errors
```bash
# Check PostgreSQL is running
docker-compose logs postgres

# Reset database
docker-compose down -v
docker-compose up -d postgres
```

## 📚 Additional Resources

- [Backend README](./backend/README.md)
- [Frontend README](./frontend/README.md)
- [AI Services Documentation](./core/ai_services.py)
- [Auto-Evolution Engine](./core/auto_evolution.py)
- [Chatbot Documentation](./core/chatbot.py)

## 🤝 Contributing

Contributions welcome! Areas to enhance:
- Add more AI backends (GPT, LLaMA, etc.)
- Improve frontend UI/UX
- Add unit tests
- Performance optimizations
- Documentation improvements

## 📄 License

MIT License - feel free to use for personal or commercial projects

## 🎉 Features Roadmap

- [ ] Multi-user support with authentication
- [ ] Real-time code synchronization
- [ ] Git integration for auto-commits
- [ ] Chrome extension for inline code reviews
- [ ] Mobile app support
- [ ] Team analytics dashboard
- [ ] Custom AI model training
- [ ] Advanced refactoring engine

---

**🚀 Built with React, Flask, Ollama, and ❤️**

Made by the Jarvis Brain Team • 2026
