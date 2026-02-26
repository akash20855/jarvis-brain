# 🦙 JARVIS + Ollama Quick Reference

## Two AI Options Now Available

```
Claude (Premium)          Ollama (Free)
├─ Cost: $5 trial        ├─ Cost: $0 forever
├─ Quality: Excellent    ├─ Quality: Good  
├─ Speed: Fast           ├─ Speed: Medium
└─ Internet: Required    └─ Internet: No
```

---

## Quick Setup

**For Claude (Existing Setup):**
```bash
# Just add your API key to .env - already configured!
nano .env
```

**For Ollama (New Free Option):**
```bash
# 1. Download
# https://ollama.ai → Install

# 2. Start (open new terminal)
ollama serve

# 3. Get Model (another terminal)
ollama pull llama2

# 4. Configure JARVIS
nano .env
# Change: AI_BACKEND=ollama

# 5. Restart JARVIS
pkill -f vscode_server.py
python3 core/vscode_server.py
```

---

## Switch Between Them

```bash
# Use Ollama (free local)
bash switch-ai.sh ollama

# Use Claude (cloud, quality)
bash switch-ai.sh claude

# Check current
bash switch-ai.sh status
```

---

## Configuration

Edit `.env`:

```ini
# Which AI to use
AI_BACKEND=ollama          # or 'claude'

# For Ollama
OLLAMA_HOST=localhost
OLLAMA_PORT=11434
OLLAMA_MODEL=llama2        # or mistral, neural-chat

# For Claude
ANTHROPIC_API_KEY=sk-proj-...
```

---

## Popular Ollama Models

| Model | Size | Speed | Best For |
|-------|------|-------|----------|
| Llama 2 | 4 GB | Medium | All-purpose coding |
| Mistral | 4 GB | Fast | Speed + quality |
| Neural-Chat | 4 GB | Fast | Conversations |
| Code-Llama | 7 GB | Slow | Code (specialized) |

```bash
# Download models
ollama pull llama2
ollama pull mistral
ollama pull neural-chat

# See what you have
ollama list

# Use different model
nano .env
# Change: OLLAMA_MODEL=mistral
```

---

## Commands

**Ollama Server:**
```bash
ollama serve              # Start server
ollama pull llama2        # Download model
ollama list              # See models
ollama rm llama2         # Remove model
```

**JARVIS with Ollama:**
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Start JARVIS
python3 core/vscode_server.py

# View logs
tail -f .jarvis_logs/server.log
```

**Switching:**
```bash
bash switch-ai.sh ollama      # Start using Ollama
bash switch-ai.sh claude      # Go back to Claude
bash switch-ai.sh status      # Check current setup
```

---

## Troubleshooting

**"Ollama not running"**
```bash
# Start in new terminal
ollama serve
```

**"Model not found"**
```bash
# Download it
ollama pull llama2
```

**"Want to go back to Claude"**
```bash
bash switch-ai.sh claude
```

**"Server slow"**
```bash
# Try faster model
ollama pull mistral
# Update .env: OLLAMA_MODEL=mistral
```

---

## All 9 JARVIS Commands Work With Both

- Generate Code
- Analyze Code
- Debug Project
- Improve Code
- Generate Tests
- Refactor Code
- Explain Code
- Build Project
- Status

Same commands, different AI engine!

---

## My Recommendations

**Best Quality** → Use Claude
```bash
bash switch-ai.sh claude
```

**Free Forever** → Use Ollama
```bash
bash switch-ai.sh ollama
```

**Try Both** → Keep both, switch easily
```bash
bash switch-ai.sh [claude|ollama]
```

---

## Files Related to AI

- `core/claude_code_generator.py` - Claude integration
- `core/ollama_code_generator.py` - Ollama integration
- `core/vscode_server.py` - Both supported, switches via .env
- `.env.template` - Configuration template
- `switch-ai.sh` - Easy switching script
- `OLLAMA_SETUP.md` - Detailed Ollama guide

---

## Reading Order

1. This file (quick reference) - 5 min
2. `OLLAMA_SETUP.md` (full guide) - 15 min
3. `AUTO_START_SETUP.md` (overall automation) - 10 min

---

**You now have choice: Premium Claude OR Free Ollama!** 🎉

