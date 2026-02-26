## Claude Haiku 4.5 - Automatic Mode

Everything is now automated! Here's how to use it.

---

## ⚡ Quick Start (One Command)

```bash
bash start-claude.sh
```

This automatically:
1. Activates Python environment ✅
2. Checks/installs dependencies ✅
3. Clears port 8001 ✅
4. Starts Flask backend ✅
5. Verifies Claude is online ✅

---

## 🎯 Setup Instructions

### 1. Get API Key (One-Time)
1. Visit: https://console.anthropic.com
2. Sign up (free tier available)
3. Generate API key
4. Copy key: `sk-ant-...`

### 2. Set Environment Variable

**Option A: Temporary (per session)**
```bash
export ANTHROPIC_API_KEY="sk-ant-your-key"
bash start-claude.sh
```

**Option B: Permanent (add to ~/.zshrc or ~/.bash_profile)**
```bash
echo 'export ANTHROPIC_API_KEY="sk-ant-your-key"' >> ~/.zshrc
source ~/.zshrc
bash start-claude.sh
```

**Option C: Interactive**
```bash
bash start-claude.sh
# Script will prompt you to paste key if not set
```

### 3. That's It!
Backend will start automatically and Claude Haiku will be ready to use.

---

## 💻 Using Claude CLI

Once the backend is running (in another terminal):

### Generate Code
```bash
./claude generate "fibonacci function" python
./claude generate "REST API with auth" python
./claude generate "web scraper for news" javascript
```

### Analyze Code
```bash
./claude analyze "def foo(): pass" script.py
./claude analyze "import os; os.system('rm -rf /')" dangerous.py
```

### Generate Tests
```bash
./claude test "def add(a,b): return a+b" python
./claude test "function greet(name) { return 'Hi ' + name }" javascript
```

### Refactor Code
```bash
./claude refactor "x = [i for i in range(10)]" python pythonic
./claude refactor "if x > 0: return x*2; else: return 0" python clean
./claude refactor "for item in items: if item: result.append(item)" python readable
```

### Explain Code
```bash
./claude explain "result = [x*2 for x in nums if x > 0]"
./claude explain "async def fetch(): return await requests.get(url)"
```

### Check Status
```bash
./claude status
```

---

## 🔄 Automated Workflow

### Complete Development Cycle

```bash
# Terminal 1: Start Claude
bash start-claude.sh

# Terminal 2: Use Claude for development
./claude generate "calculator with add/subtract/multiply" python
./claude test "def add(a,b): return a+b" python
./claude refactor "x=[i*2 for i in range(10) if i%2==0]" python pythonic
./claude analyze "my_code_here" myfile.py
```

### Batch Processing

Create `batch.sh`:
```bash
#!/bin/bash

# Generate multiple functions
./claude generate "fibonacci function" python > fibonacci.py
./claude generate "quick sort algorithm" python > quicksort.py
./claude generate "binary search" python > binsearch.py

# Analyze them all
./claude analyze "$(cat fibonacci.py)" fibonacci.py
./claude analyze "$(cat quicksort.py)" quicksort.py
./claude analyze "$(cat binsearch.py)" binsearch.py

# Generate tests
./claude test "$(cat fibonacci.py)" python
./claude test "$(cat quicksort.py)" python
./claude test "$(cat binsearch.py)" python
```

Then run:
```bash
bash batch.sh
```

---

## 🛠️ System Commands

### View Logs
```bash
tail -f backend.log
```

### Stop Backend
```bash
pkill -f "python backend/app.py"
```

### Check If Running
```bash
curl http://localhost:8001/api/claude/status
```

### Restart Backend
```bash
pkill -f "python backend/app.py"
sleep 2
bash start-claude.sh
```

---

## 🔗 Add to Shell

Make `claude` and `start-claude` commands available globally:

### For macOS (zsh)
```bash
# Add to ~/.zshrc
export PATH="/Volumes/Akash SSD/repos/jarvis-brain:$PATH"
source ~/.zshrc
```

Then you can run from anywhere:
```bash
start-claude.sh
claude generate "hello world" python
```

### Create Alias
```bash
alias claude="/Volumes/Akash SSD/repos/jarvis-brain/claude"
alias start-claude="bash /Volumes/Akash SSD/repos/jarvis-brain/start-claude.sh"
```

---

## 📊 What Gets Automated

| Task | Before | After |
|------|--------|-------|
| Activate venv | Manual | Automatic ✅ |
| Install deps | Manual | Automatic ✅ |
| Set API key | Manual | Prompted ✅ |
| Start backend | Manual | Automatic ✅ |
| Generate code | curl command | `claude generate` ✅ |
| Analyze code | curl command | `claude analyze` ✅ |
| Generate tests | curl command | `claude test` ✅ |
| Refactor | curl command | `claude refactor` ✅ |
| Check status | curl command | `claude status` ✅ |

---

## 🚀 One-Liner Start

```bash
export ANTHROPIC_API_KEY="sk-ant-your-key" && bash start-claude.sh
```

And in another terminal:
```bash
./claude generate "your request" python
```

---

## 🎯 Common Workflows

### Workflow 1: Learn Programming
```bash
./claude generate "fibonacci function with explanation" python
./claude explain "$(output from above)"
./claude test "$(function from above)" python
```

### Workflow 2: Code Review
```bash
# Analyze code for issues
./claude analyze "$(cat mycode.py)"

# Get refactored version
./claude refactor "$(cat mycode.py)" python clean

# Generate tests
./claude test "$(cat mycode.py)" python
```

### Workflow 3: Rapid Prototyping
```bash
# Generate feature
./claude generate "user authentication system" python

# Test it
./claude test "$(output)" python

# Refactor for performance
./claude refactor "$(output)" python performance

# Deploy
# (save generated code and deploy)
```

---

## 📁 Automation Files

- **start-claude.sh** - Automatic startup script
- **claude** - CLI wrapper for easy commands
- **docker-compose.yml** - Docker automation (optional)
- **Makefile** - Make commands (optional)

---

## ✅ Verification

Test that everything is automated:

```bash
# Terminal 1
bash start-claude.sh

# Terminal 2 (after backend starts)
./claude status
./claude generate "hello world function" python
```

You should see Claude working without any manual setup!

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| "Port already in use" | `start-claude.sh` handles this ✅ |
| "API key missing" | `start-claude.sh` will prompt you ✅ |
| "Backend not responding" | Wait 3-5 seconds, backend is starting |
| "curl: command not found" | macOS should have curl pre-installed |
| "Python not found" | Make sure venv is activated |

---

**🎉 Everything is now automated! Just run `bash start-claude.sh` and start generating code!**
