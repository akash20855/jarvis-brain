# 🚀 Jarvis Brain Full-Stack - Getting Started Guide

Everything you need to know to get Jarvis Brain up and running!

## ⚡ 5-Minute Quick Start

### Docker (Easiest)
```bash
# Clone and navigate
cd /Volumes/Akash\ SSD/repos/jarvis-brain

# Start everything
chmod +x start-fullstack.sh
./start-fullstack.sh

# Open in browser
open http://localhost:3000
```

### Local (Manual)
```bash
# Terminal 1: Backend
cd backend
pip install -r requirements.txt
python3 app.py

# Terminal 2: Frontend
cd frontend
npm install
npm start

# Terminal 3: AI Services
ollama serve
ollama pull mistral
ollama pull neural-chat
```

## 🎯 What You Get

### 💻 Frontend (React)
- Beautiful chat interface
- Real-time code analysis
- Project dashboard
- Improvement history
- Dark theme UI

### 🔌 Backend API (Flask)
- 27 REST endpoints
- Real-time processing
- Auto-scaling support
- Error handling
- CORS enabled

### 🤖 AI Services (Ollama, 3 instances)
- **Code Analysis** - Detects issues (Port 11434)
- **Chat AI** - Answers questions (Port 11435)
- **Suggestions** - Generates improvements (Port 11436)

### 💾 Data Storage
- JSON files for history
- Redis for caching
- PostgreSQL for scale

## 📚 Quick Reference

### Commands to Try

**In the Chat Interface:**
```
> analyze               # Scan entire project
> file core/main.py    # Analyze specific file
> suggestions          # Show top improvements
> How can I optimize?  # Ask questions
> help                 # Show all commands
```

### API Endpoints

```bash
# Health check
curl http://localhost:5000/api/health

# Check AI status
curl http://localhost:5000/api/ai/status

# Analyze project
curl -X POST http://localhost:5000/api/evolve/analyze

# Send chat message
curl -X POST http://localhost:5000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{"message":"analyze"}'
```

### Docker Commands

```bash
# View logs
docker-compose logs -f jarvis-backend
docker-compose logs -f ollama-analysis

# Stop services
docker-compose down

# Rebuild
docker-compose build

# Check status
docker-compose ps
```

## 🏗️ File Structure

```
jarvis-brain/
├── frontend/              # React UI
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── Dockerfile
├── backend/               # Flask API
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
├── core/                  # Python core
│   ├── auto_evolution.py
│   ├── chatbot.py
│   ├── ai_services.py
│   └── launcher.py
├── docker-compose.yml     # Services definition
├── start-fullstack.sh     # Startup script
├── FULLSTACK.md          # Detailed guide
├── ARCHITECTURE.md       # Tech design
└── README.md             # Main readme
```

## 🔧 Configuration

### Environment Variables (.env)

```env
# Frontend
REACT_APP_API_URL=http://localhost:5000/api

# Backend
FLASK_ENV=development
API_PORT=5000

# AI Services
OLLAMA_ANALYSIS_URL=http://localhost:11434
OLLAMA_CHAT_URL=http://localhost:11435
OLLAMA_SUGGESTIONS_URL=http://localhost:11436

# Database
DATABASE_URL=postgresql://jarvis:password@localhost/jarvis_brain
```

### Project Configuration (.evolution_config.json)

```json
{
  "auto_evolution": {
    "enabled": true,
    "ai_backend": "patterns",
    "scan_interval_seconds": 3600,
    "auto_apply_security_fixes": false,
    "auto_apply_performance": true
  }
}
```

## 🎓 Learning Resources

### Beginner Level
- Start with: FULLSTACK.md
- Try Docker setup first
- Use quick commands
- Explore the UI

### Intermediate Level
- Read: ARCHITECTURE.md
- Understand API endpoints
- Learn about AI services
- Setup PostgreSQL

### Advanced Level
- Explore source code
- Modify AI prompts
- Add custom patterns
- Scale horizontally

## 🚨 Troubleshooting

### "Cannot connect to frontend"
```bash
# Check if service is running
curl http://localhost:3000

# Check Docker
docker-compose logs jarvis-frontend

# Rebuild
docker-compose build jarvis-frontend
docker-compose up -d jarvis-frontend
```

### "API not responding"
```bash
# Check if backend is running
curl http://localhost:5000/api/health

# View logs
docker-compose logs jarvis-backend

# Rebuild
docker-compose build jarvis-backend
docker-compose up -d jarvis-backend
```

### "Ollama not found"
```bash
# Install
brew install ollama

# Start in new terminal
ollama serve

# Download models
ollama pull mistral
ollama pull neural-chat
```

### "Database connection error"
```bash
# Check PostgreSQL
docker-compose logs postgres

# Reset database
docker-compose down -v
docker-compose up -d postgres

# Wait for startup
sleep 10
docker-compose up -d
```

## 📊 System Requirements

### Minimum
- 4GB RAM
- 2 CPU cores
- 10GB storage
- Docker & Docker Compose

### Recommended
- 8GB+ RAM
- 4+ CPU cores
- 50GB+ storage
- Solid-state drive
- Gigabit internet

## 🚀 Deployment

### Local Development
```bash
./start-fullstack.sh
```

### Production (Docker)
```bash
# Set environment
export FLASK_ENV=production
export REACT_APP_API_URL=https://api.yoursite.com

# Deploy
docker-compose -f docker-compose.yml up -d
```

### Cloud Platforms
- **AWS**: ECS, ECR, RDS
- **Google Cloud**: Cloud Run, Artifact Registry
- **Azure**: Container Instances, App Service
- **Heroku**: Buildpacks
- **DigitalOcean**: App Platform

## 💡 Tips & Tricks

### Faster Analysis
```
> Use 'patterns' AI backend (fastest)
> Single file analysis is faster than full project
> Results are cached
```

### Better Suggestions
```
> Use 'ollama' backend for AI (slower but better)
> Install additional Ollama models
> Provide more context in questions
```

### Performance Tuning
```bash
# Increase Flask workers
WORKERS=8 gunicorn -w 8 app:app

# Enable caching
CACHE_ENABLED=true

# Batch processing
BATCH_SIZE=50
```

## 🔐 Security Best Practices

1. **Change Default Credentials**
   ```env
   POSTGRES_PASSWORD=your_secure_password
   JWT_SECRET=your_jwt_secret
   ```

2. **Enable HTTPS in Production**
   - Use nginx/Apache reverse proxy
   - Install SSL certificate
   - Configure CORS properly

3. **Protect Sensitive Data**
   - Use .env file (never commit)
   - Enable database encryption
   - Rotate API keys regularly

4. **Update Dependencies**
   ```bash
   pip install --upgrade -r requirements.txt
   npm update
   ```

## 📞 Support & Help

### Documentation
- FULLSTACK.md - Complete guide
- ARCHITECTURE.md - Technical design
- backend/README.md - API docs
- frontend/README.md - UI guide

### Getting Help
1. Check the relevant documentation
2. Search GitHub issues
3. Review troubleshooting section
4. Create detailed issue report

### Issue Reporting Template
```
Title: [Component] Short description

Description:
What were you trying to do?

Steps to Reproduce:
1. ...
2. ...

Expected: ...
Actual: ...

Environment:
- OS: macOS/Windows/Linux
- Docker version: ...
- Python: ...
```

## 🎯 Next Steps

1. **Start Services**
   ```bash
   ./start-fullstack.sh
   ```

2. **Open Frontend**
   - Go to http://localhost:3000

3. **Analyze Your Code**
   - Type "analyze" in chat
   - Or: "file core/main.py"

4. **Explore Features**
   - Try different commands
   - Check Analysis tab
   - View History

5. **Configure for Your Needs**
   - Edit .evolution_config.json
   - Customize AI prompts
   - Set up database

6. **Read Documentation**
   - Study ARCHITECTURE.md
   - Learn API endpoints
   - Understand AI services

## 🏆 Common Workflows

### Workflow 1: Quick Code Review
```
1. > analyze
2. > suggestions
3. Review improvements
4. Take notes
```

### Workflow 2: Detailed Analysis
```
1. > file src/core.py
2. Read suggestions
3. > file src/utils.py
4. Ask questions
5. Apply improvements
```

### Workflow 3: Performance Optimization
```
1. > analyze
2. Look for "performance" issues
3. > How can I optimize loops?
4. Implement suggestions
5. > analyze (verify)
```

### Workflow 4: Security Audit
```
1. > analyze
2. Look for "security" issues
3. > Any vulnerable patterns?
4. Fix issues
5. > analyze (confirm)
```

## 📊 Monitoring

### Check Service Health
```bash
# Frontend
curl http://localhost:3000

# Backend
curl http://localhost:5000/api/health

# AI Services
curl http://localhost:11434/api/tags

# Database
docker-compose logs postgres
```

### View Error Logs
```bash
# Docker logs
docker-compose logs -f --tail 100

# Specific service
docker-compose logs -f jarvis-backend
```

## 🎊 You're Ready!

Congratulations! You now have:
- ✅ Full-stack application running
- ✅ AI-powered code analysis
- ✅ Interactive chatbot
- ✅ Beautiful web interface
- ✅ Scalable architecture

**Now go analyze some code and watch Jarvis work its magic!** 🤖✨

---

**Need help?** Check the documentation or create an issue!

**Want to contribute?** We'd love to have help improving Jarvis Brain!

**Questions?** Open an issue on GitHub!

---

Happy coding! 🚀
