# Jarvis Brain - Deployment Guide

## Quick Start - Deploy Online

### Step 1: Environment Setup
```bash
# Copy environment template
cp .env.example .env

# Update .env with your values:
# - FLASK_PORT=8000
# - REACT_PORT=3000
# - OPENAI_API_KEY (if using OpenAI)
# - ANTHROPIC_API_KEY (if using Anthropic)
# - DATABASE_URL (if using external DB)
```

### Step 2: Install Dependencies
```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd ../frontend
npm install
```

### Step 3: Run Locally (Pre-deployment Test)
```bash
# Terminal 1: Start Backend
cd backend
python3 app.py

# Terminal 2: Start Frontend
cd frontend
npm run dev
```

### Step 4: Deploy to Cloud

#### Option A: Deploy to Heroku
```bash
# Install Heroku CLI
brew install heroku/brew/heroku

# Login
heroku login

# Create app
heroku create your-jarvis-brain

# Deploy
git push heroku main

# View logs
heroku logs --tail
```

#### Option B: Deploy to AWS EC2
```bash
# 1. Launch EC2 instance (Ubuntu 22.04)
# 2. SSH into instance
ssh -i your-key.pem ubuntu@your-instance-ip

# 3. Clone repo
git clone https://github.com/your-repo/jarvis-brain.git
cd jarvis-brain

# 4. Run deployment script
bash scripts/deploy.sh
```

#### Option C: Deploy with Docker
```bash
# Build images
docker-compose build

# Run containers
docker-compose up -d

# Access at http://localhost:8000
```

### Step 5: Configure HTTPS
```bash
# Using Let's Encrypt + Nginx
sudo certbot certonly --standalone -d yourdomain.com

# Update nginx config with SSL
sudo systemctl reload nginx
```

## API Endpoints

### Health Check
```
GET /health
```

### Chat API
```
POST /api/chat
Body: { "message": "your question" }
```

### Code Evolution
```
POST /api/evolve
Body: { "code": "your code" }
```

### Scan Project
```
GET /api/scan
```

## Monitoring

### Check Status
```bash
curl http://your-domain/health
```

### View Logs
```bash
# Docker
docker-compose logs -f app

# Systemd
sudo journalctl -u jarvis -f
```

## Troubleshooting

### Port Already in Use
```bash
# macOS
lsof -i :8000
kill -9 <PID>
```

### CORS Issues
- Update `ALLOWED_ORIGINS` in backend/app.py
- Ensure frontend URL is whitelisted

### AI Service Connection
- Verify Ollama/OpenAI credentials in ai_config.yaml
- Check network connectivity: `curl http://ai-service-url`

## Security Checklist

- [ ] Set strong API keys in .env
- [ ] Enable HTTPS/SSL
- [ ] Configure firewall rules
- [ ] Enable CORS only for trusted domains
- [ ] Set up API rate limiting
- [ ] Enable authentication/JWT tokens
- [ ] Regular backups of evolution_log.json

## Performance Optimization

1. Enable Caching
   - Redis for API responses
   - Browser caching for frontend assets

2. Database Optimization
   - Index frequently queried fields
   - Archive old evolution logs

3. Code Analysis Optimization
   - Batch file processing
   - Use async/await for I/O operations

## Next Steps

1. Set up CI/CD pipeline (GitHub Actions)
2. Configure monitoring & alerts (CloudWatch/DataDog)
3. Set up auto-scaling
4. Enable database replication
5. Configure CDN for static assets
