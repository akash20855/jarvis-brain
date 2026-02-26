## Claude Haiku 4.5 - Complete Automation Guide

Everything is now automated! Here are all the ways to run Claude:

---

## ⚡ Option 1: Simple Makefile Commands (RECOMMENDED)

```bash
# Start
make claude-start

# Stop
make claude-stop

# Restart
make claude-restart

# Check status
make claude-status

# View logs
make claude-logs

# Test API
make claude-test-api
```

**Most convenient - type from project directory!**

---

## 🚀 Option 2: Shell Aliases (Quick Commands)

Setup once:
```bash
source claude-shell-setup.sh
```

Then use anywhere:
```bash
# Start/Stop
claude-start
claude-stop
claude-restart
claude-status

# Quick CLIs
cg "fibonacci function" python     # Generate
ca "def bad(): eval(input())"      # Analyze
ct "def add(a,b): return a+b"     # Test
cr "code here" python clean        # Refactor
ce "complex code"                  # Explain
```

---

## 🔄 Option 3: Auto-Start on Login (macOS)

Setup:
```bash
bash setup-autostart-macos.sh
```

This creates a LaunchAgent that:
- Auto-starts Claude when you log in
- Keeps it running (auto-restart if it crashes)
- Logs to files you can monitor

**Once configured, Claude is always running in the background!**

---

## 📜 Option 4: Cron Job (Scheduled Start)

Add to crontab:
```bash
crontab -e
```

Then add:
```cron
# Start Claude every morning at 8 AM
0 8 * * * cd /Volumes/Akash\ SSD/repos/jarvis-brain && bash start-claude.sh >> claude-cron.log 2>&1

# Check if running and restart if needed (every 30 mins)
*/30 * * * * curl http://localhost:8001/api/claude/status || (pkill -f "python backend" && cd /Volumes/Akash\ SSD/repos/jarvis-brain && bash start-claude.sh)
```

---

## 🎯 Option 5: Custom Bash Function

Add to `~/.zshrc`:
```bash
function claude {
    if [ "$1" = "start" ]; then
        cd /Volumes/Akash\ SSD/repos/jarvis-brain && make claude-start
    elif [ "$1" = "stop" ]; then
        cd /Volumes/Akash\ SSD/repos/jarvis-brain && make claude-stop
    elif [ "$1" = "status" ]; then
        curl http://localhost:8001/api/claude/status 2>/dev/null | python3 -m json.tool
    elif [ "$1" = "gen" ]; then
        /Volumes/Akash\ SSD/repos/jarvis-brain/claude generate "$2" "${3:-python}"
    else
        echo "Usage: claude {start|stop|status|gen 'request' language}"
    fi
}
```

Then use:
```bash
claude start
claude status
claude gen "fibonacci" python
claude stop
```

---

## 🐳 Option 6: Docker (Complete Isolation)

Build image:
```bash
make docker-build
```

Run:
```bash
docker run -d \
  -e ANTHROPIC_API_KEY="sk-ant-your-key" \
  -p 8001:8001 \
  jarvis-brain:latest
```

---

## 🔗 Recommended Workflow

**Terminal 1 - Start Claude:**
```bash
make claude-start
```

**Terminal 2 - Use Claude:**
```bash
# Check status
./claude status

# Generate code
./claude generate "fibonacci function" python

# Analyze code
./claude analyze "def foo(): pass"

# Test code
./claude test "def add(a,b): return a+b" python

# Refactor code
./claude refactor "x=[i for i in range(10)]" python pythonic

# Explain code
./claude explain "result = [x*2 for x in nums if x > 0]"
```

---

## 📊 Comparison Table

| Method | Setup Time | Ease of Use | Auto-Start | Background |
|--------|-----------|-----------|-----------|-----------|
| Makefile | 0 minutes | ⭐⭐⭐ | ❌ | Manual |
| Shell Aliases | 1 minute | ⭐⭐⭐⭐ | ❌ | Manual |
| LaunchAgent | 5 minutes | ⭐⭐⭐ | ✅ | Always on |
| Cron Job | 3 minutes | ⭐⭐ | ✅ | Scheduled |
| Bash Function | 2 minutes | ⭐⭐⭐⭐ | ❌ | Manual |
| Docker | 10 minutes | ⭐⭐⭐ | ✅ | Container |

---

## 🚀 Quick Start Guide

### Fastest Way (Right Now)

```bash
# Terminal 1
make claude-start

# Terminal 2
./claude generate "hello world" python
```

### Best Long-Term Solution

1. Setup shell aliases:
   ```bash
   source claude-shell-setup.sh
   ```

2. Add to your `~/.zshrc`:
   ```bash
   source /Volumes/Akash\ SSD/repos/jarvis-brain/claude-shell-setup.sh
   ```

3. Reload shell:
   ```bash
   source ~/.zshrc
   ```

4. Now use from anywhere:
   ```bash
   claude-start
   cg "fibonacci function" python
   ```

### Always-Running Solution (Auto-Start)

```bash
# One-time setup
bash setup-autostart-macos.sh

# Edit with your API key
nano ~/Library/LaunchAgents/com.jarvis.claude.haiku.plist

# Load it
launchctl load ~/Library/LaunchAgents/com.jarvis.claude.haiku.plist

# Claude will now auto-start on login!
```

---

## ✅ Available Commands

### With Makefile (`make`)
```
make claude-start       Start Claude
make claude-stop        Stop Claude
make claude-restart     Restart Claude
make claude-status      Check status
make claude-logs        View logs
make claude-test-api    Test API endpoints
```

### With CLI (`./claude`)
```
./claude generate "request" [language]     Generate code
./claude analyze "code" [filename]         Analyze code
./claude test "code" [language]            Generate tests
./claude refactor "code" [lang] [style]    Refactor code
./claude explain "code"                    Explain code
./claude status                            Check status
```

### With Aliases (after sourcing setup)
```
claude-start            Start Claude
claude-stop             Stop Claude
claude-status           Check status
cg "request" python     Generate code
ca "code"              Analyze code
ct "code" python       Generate tests
cr "code" python clean Refactor code
ce "code"              Explain code
```

---

## 🛠️ Troubleshooting

| Problem | Solution |
|---------|----------|
| "Port in use" | `make claude-stop` then `make claude-start` |
| "API key missing" | `export ANTHROPIC_API_KEY="sk-ant-your-key"` |
| "Command not found" | Make sure you're in the project directory or sourced aliases |
| "Backend not responding" | Check logs with `make claude-logs` |
| "LaunchAgent not loading" | Check syntax with `plutil` or check error logs |

---

## 📚 Files for Automation

| File | Purpose |
|------|---------|
| `Makefile` | Make commands for easy control |
| `start-claude.sh` | Automatic startup script |
| `claude` | CLI wrapper for requests |
| `claude-shell-setup.sh` | Shell aliases and functions |
| `setup-autostart-macos.sh` | Auto-start on login |
| `docker-compose.yml` | Docker automation |

---

## 🎯 Summary

You now have **6 different ways** to automate Claude Haiku:

1. **Makefile** - Easiest for quick testing
2. **Shell Aliases** - Best for daily use
3. **LaunchAgent** - Best for always-on
4. **Cron Jobs** - Best for scheduled use
5. **Bash Functions** - Best for flexibility
6. **Docker** - Best for isolation

**Start with: `make claude-start` or `bash start-claude.sh`**

Once comfortable, upgrade to **shell aliases** for maximum convenience!

---

**🧠 Claude Haiku 4.5 is fully automated and ready for any workflow! Pick your favorite automation method above. 🚀**
