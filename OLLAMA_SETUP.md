# 🦙 JARVIS with Ollama - Complete Setup Guide

## What is Ollama?

**Ollama** is a free, open-source tool that lets you run AI models locally on your Mac:
- ✅ **100% Free** - No API keys, no costs ever
- ✅ **Private** - Data stays on your computer
- ✅ **Fast** - Instant startup and inference
- ✅ **Offline** - Works without internet

JARVIS now supports both Claude (cloud) and Ollama (local)!

---

## 🚀 Quick Start (5 minutes)

### Step 1: Download Ollama
Visit: https://ollama.ai

Click "Download" → Install on Mac → Done

### Step 2: Start Ollama Server
Open Terminal and run:
```bash
ollama serve
```

You'll see:
```
listening on 127.0.0.1:11434
```

Leave this running!

### Step 3: Download a Model (in new Terminal)
```bash
# Download Llama 2 (recommended for code)
ollama pull llama2

# Or try these alternatives:
# ollama pull mistral        # (faster, good quality)
# ollama pull neural-chat    # (optimized for chat)
```

This downloads the model (~4-7 GB depending on model).

### Step 4: Configure JARVIS
Edit your `.env`:
```bash
nano .env
```

Change:
```ini
AI_BACKEND=ollama
OLLAMA_HOST=localhost
OLLAMA_PORT=11434
OLLAMA_MODEL=llama2
```

### Step 5: Restart JARVIS Server
```bash
# Kill old server
pkill -f vscode_server.py

# Start new server
python3 core/vscode_server.py
```

Watch for:
```
Using Ollama AI backend
✓ Ollama server is running at http://localhost:11434
```

### Step 6: Use in VS Code
```bash
code .
# Cmd+Shift+P → JARVIS: Generate Code
```

**Done!** Now using free local AI! 🎉

---

## 🛠️ Installation Details

### Option A: Homebrew (Easiest on Mac)
```bash
brew install ollama
ollama serve     # Start server
```

### Option B: Direct Download
https://ollama.ai → Download → Install → Run

### Model Selection

| Model | Size | Speed | Quality | Best For |
|-------|------|-------|---------|----------|
| **Llama 2** | 4 GB | Medium | Great | Code generation |
| **Mistral** | 4 GB | Fast | Good | Speed + quality |
| **Neural-Chat** | 4 GB | Fast | Good | Conversations |
| **Code-Llama** | 7 GB | Slow | Best | Code (specialized) |

**My Recommendation**: Start with **Llama 2** (balanced)

---

## 🔧 Configuration

### In `.env` file:

```bash
# Which AI to use
AI_BACKEND=ollama              # Switch to 'claude' to go back

# Ollama server location
OLLAMA_HOST=localhost          # Where Ollama is running
OLLAMA_PORT=11434             # Default Ollama port

# Which model to use
OLLAMA_MODEL=llama2           # Switch to: mistral, neural-chat, etc.
```

### Switching Models

**To use a different model:**

```bash
# 1. Download new model (if not already downloaded)
ollama pull mistral

# 2. Update .env
nano .env
# Change: OLLAMA_MODEL=mistral

# 3. Restart JARVIS server
pkill -f vscode_server.py
python3 core/vscode_server.py
```

Multiple models can be installed. You only use storage when running.

---

## 🚦 Typical Workflow

### Setup (First Time)
```bash
# Terminal 1: Start Ollama
ollama serve

# Terminal 2: Initialize JARVIS
cd /path/to/jarvis-brain
nano .env          # Set AI_BACKEND=ollama
python3 core/vscode_server.py
```

### Daily Use
```bash
# Morning: Open Ollama (stays running)
ollama serve

# Use JARVIS normally in VS Code
code .
```

---

## 📊 Claude vs Ollama

| Feature | Claude | Ollama |
|---------|--------|--------|
| **Cost** | $5 free, then paid | 100% free |
| **Speed** | Fast (cloud) | Slower (local Mac) |
| **Quality** | Excellent | Good |
| **Privacy** | Data to Anthropic | Stays local |
| **Internet** | Required | Not needed |
| **Setup** | Just add API key | Download + run |
| **Models** | Claude only | Many options |

---

## ⚡ Performance Tips

### Speed Options

**Fastest (but lower quality):**
```bash
AI_BACKEND=ollama
OLLAMA_MODEL=mistral       # Faster than Llama
```

**Balanced:**
```bash
OLLAMA_MODEL=llama2        # Good speed + quality
```

**Best Quality (but slow):**
```bash
OLLAMA_MODEL=code-llama    # Specialized for code
```

### Memory Management

Check your Mac's resources:
```bash
# View Ollama processes
ps aux | grep ollama

# View memory usage
top -p $(pgrep -f ollama)
```

If slow, reduce what else is running.

---

## 🐛 Troubleshooting

### "Connection refused" or "Ollama not running"

**Problem:** Ollama server isn't running
```bash
# Solution: Start Ollama in terminal
ollama serve

# Should show: listening on 127.0.0.1:11434
```

### "Model not found"

**Problem:** Requested model isn't downloaded
```bash
# Solution: Download it
ollama pull llama2

# See what you have
ollama list
```

### "Server running but slow"

**Problem:** Model is slow or your Mac is busy
```bash
# Try faster model
ollama pull mistral
# Update .env: OLLAMA_MODEL=mistral

# Or free up RAM
# Close other apps
```

### "Want to switch back to Claude"

**Easy!** Just change `.env`:
```bash
nano .env
# Change: AI_BACKEND=claude
# Change: ANTHROPIC_API_KEY=sk-proj-your-key

# Restart server
pkill -f vscode_server.py
python3 core/vscode_server.py
```

---

## 📝 Command Reference

### Managing Ollama

```bash
# Start the server
ollama serve

# Download a model
ollama pull llama2

# See installed models
ollama list

# Remove a model
ollama rm llama2

# Test a model
ollama run llama2 "Hello, world!"
```

### Managing JARVIS with Ollama

```bash
# Start server (terminal 1 starts: ollama serve)
python3 core/vscode_server.py

# Check if Ollama is responding
curl http://localhost:11434/api/tags

# View JARVIS logs
tail -f .jarvis_logs/server.log

# Stop JARVIS
pkill -f vscode_server.py
```

---

## 🎯 Switching Between Claude and Ollama

### To Use Claude (Paid but Better)
```bash
nano .env
# Set: AI_BACKEND=claude
# Set: ANTHROPIC_API_KEY=sk-proj-your-key

# Restart
pkill -f vscode_server.py
python3 core/vscode_server.py
```

### To Use Ollama (Free but Slower)
```bash
# 1. Start Ollama
ollama serve

# 2. Configure JARVIS
nano .env
# Set: AI_BACKEND=ollama
# Set: OLLAMA_MODEL=llama2

# 3. Restart JARVIS
pkill -f vscode_server.py
python3 core/vscode_server.py
```

---

## 🔐 Privacy Notes

### Claude (Cloud)
- Your code/prompts sent to Anthropic's servers
- Subject to their privacy policy
- Can cache requests

### Ollama (Local)
- Everything runs on your Mac
- No data leaves your computer
- True offline privacy

Pick what matters to you!

---

## 📚 Resources

- **Ollama**: https://ollama.ai
- **Models Available**: https://ollama.ai/library
- **Llama 2**: https://llama.meta.com
- **Mistral**: https://mistral.ai

---

## 💡 My Recommendation

**For Most Users:**
- Start with **Claude** ($5 free trial)
- Better quality, faster
- Less setup

**If You Want Free:**
- Use **Ollama** with Llama 2
- Runs locally, no costs
- Good quality, slightly slower

**If You Want Both:**
- Keep both installed
- Switch in `.env` anytime
- Easy to test both!

---

## ✨ Summary

You can now:

✅ **Use Claude** (cloud AI)
✅ **Use Ollama** (free local AI)
✅ **Switch between them** (one line in `.env`)
✅ **Run multiple models** (download as many as you want)

Everything integrated with JARVIS!

---

**Enjoy coding with free or premium AI! 🚀**

