# 🚀 JARVIS BRAIN - QUICK START TO PRODUCTION

## What Has Been Fixed

✅ **Fixed Issues:**
1. ✅ Hardcoded localhost URLs changed to environment variables
2. ✅ Added `.env` file support with `python-dotenv`
3. ✅ Added `/health` endpoint for monitoring
4. ✅ Production-ready server configuration
5. ✅ Proper error handling and logging
6. ✅ Environment-based configuration (development vs production)

## Step 1: Local Setup (Development)

```bash
# Activate virtual environment
source jarvis_env/bin/activate

# Create .env file
cp .env.example .env

# Edit .env with your AI service configuration:
# - AI_TYPE: ollama, openai, or anthropic
# - Appropriate API keys or URLs
```

## Step 2: Run Locally

**Option A: Development (Both) - One Command**
```bash
bash start-prod.sh
# Then select option 3
```

**Option B: Terminal Approach**
```bash
# Terminal 1 - Backend
source jarvis_env/bin/activate
cd backend
python3 app.py
# Runs at http://localhost:8000

# Terminal 2 - Frontend  
cd frontend
npm install  # First time only
npm run dev
# Runs at http://localhost:5173
```

## Step 3: Test Endpoints

```bash
# Health check
curl http://localhost:8000/health

# API status
curl http://localhost:8000/api/ai-status

# Chat endpoint
curl -X POST http://localhost:8000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello Jarvis"}'

# Code analysis
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"code": "def hello(): print(\"world\")"}'

# Get suggestions
curl http://localhost:8000/api/suggestions
```

## Step 4: Deploy Online

### Deploy with Docker (Recommended)
```bash
# Make sure Docker is running
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f app
```

Access at: `http://localhost:8000`

### Deploy to Heroku
```bash
bash scripts/deploy-complete.sh heroku your-app-name

# View live app
heroku open --app your-app-name
```

Access at: `https://your-app-name.herokuapp.com`

### Deploy to AWS
```bash
# Launch EC2 instance, then:
bash scripts/deploy-complete.sh aws your-instance-ip /path/to/key.pem
```

### Deploy to Vercel (Frontend Only)
```bash
bash scripts/deploy-complete.sh vercel
```

## Step 5: Continuous Improvement

Run auto-evolution:
```bash
python3 -m core.auto_evolution
```

Scan for improvements:
```bash
python3 -c "from core.auto_evolution import AutoEvolutionEngine; e = AutoEvolutionEngine(); print(e.scan_project())"
```

## Configuration Guide

### Using Ollama (Local AI - Free)
```yaml
# In .env:
AI_TYPE=ollama
OLLAMA_URL=http://localhost:11434

# Or with Docker:
AI_TYPE=ollama
OLLAMA_URL=http://host.docker.internal:11434  # Docker host
```

### Using OpenAI
```yaml
AI_TYPE=openai
OPENAI_API_KEY=sk-your-key-here
```

### Using Anthropic  
```yaml
AI_TYPE=anthropic
ANTHROPIC_API_KEY=your-api-key-here
```

## Monitoring

### Health Check
```bash
curl http://your-domain/health
```

Response:
```json
{
  "status": "healthy",
  "timestamp": "2026-02-26T18:57:38.669588",
  "service": "Jarvis Brain API"
}
```

### View Logs
```bash
# Docker
docker-compose logs -f app

# Local (with systemd)
sudo journalctl -u jarvis -f

# Heroku
heroku logs --tail --app your-app-name
```

## Performance Optimization

1. **Redis Caching** (Optional)
   - Speeds up API responses
   - Reduces AI service calls

2. **Database Indexing**
   - SQLite by default
   - Use PostgreSQL for production scale

3. **Frontend Build Optimization**
   - `npm run build` creates optimized bundle
   - ~50KB gzipped

## Security Checklist

- [ ] Change `SECRET_KEY` in .env
- [ ] Enable HTTPS (Let's Encrypt free)
- [ ] Configure firewall rules
- [ ] Set strong API keys
- [ ] Enable API rate limiting
- [ ] Use CORS whitelist
- [ ] Regular backups of evolution_log.json

## Troubleshooting

### Error: Host docker.internal not found
**Solution:** Change OLLAMA_URL in .env
```bash
OLLAMA_URL=http://localhost:11434
```

### Error: Port 8000 already in use
```bash
# Find process using port
lsof -i :8000

# Kill it
kill -9 <PID>
```

### Error: Module not found
```bash
# Verify virtual environment
source jarvis_env/bin/activate
pip install -r requirements.txt
```

## Environment Variables Reference

| Variable | Default | Description |
|----------|---------|-------------|
| FLASK_ENV | development | development or production |
| FLASK_PORT | 8000 | Backend server port |
| FLASK_DEBUG | False | Enable debug mode |
| AI_TYPE | ollama | ollama, openai, or anthropic |
| OLLAMA_URL | localhost:11434 | Ollama server URL |
| OPENAI_API_KEY | (none) | OpenAI API key |
| ANTHROPIC_API_KEY | (none) | Anthropic API key |
| DATABASE_URL | sqlite:///jarvis.db | Database connection URL |
| LOG_LEVEL | INFO | Logging level |
| ALLOWED_ORIGINS | localhost:3000,localhost:8000 | CORS allowed origins |

## Next Steps

1. ✅ **Local Testing** - Run `start-prod.sh` and test thoroughly
2. ✅ **Dashboard** - Visit http://localhost:3000
3. ✅ **API Docs** - View http://localhost:8000/api
4. 🚀 **Deploy** - Use `deploy-complete.sh` script
5. 📊 **Monitor** - Check health endpoint regularly
6. 🔄 **Evolve** - Run auto-evolution periodically

## Support & Documentation

- 📖 [Deployment Guide](DEPLOYMENT.md)
- 🏗️ [Architecture](ARCHITECTURE.md)
- 🔧 [Configuration Guide](AI_CONFIG_GUIDE.md)
- 📝 [Auto-Evolution](AUTO_EVOLUTION.md)

---

**🎉 Your Jarvis Brain is ready for production!**

Questions? Check the docs or run: `python3 core/main.py`
