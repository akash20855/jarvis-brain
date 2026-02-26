## 🚀 Claude Haiku - Quick Automation Reference

**Everything is automated! Pick your style:**

---

## 1️⃣ Quickest Start (Copy & Paste)

```bash
# Terminal 1
cd /Volumes/Akash\ SSD/repos/jarvis-brain
make claude-start

# Terminal 2
./claude generate "fibonacci function" python
./claude status
```

**Time to first code: 30 seconds** ⚡

---

## 2️⃣ Most Convenient (Shell Aliases)

Setup once:
```bash
source /Volumes/Akash\ SSD/repos/jarvis-brain/claude-shell-setup.sh
```

Add to `~/.zshrc`:
```bash
echo 'source /Volumes/Akash\ SSD/repos/jarvis-brain/claude-shell-setup.sh' >> ~/.zshrc
```

Use anywhere:
```bash
claude-start
cg "hello world" python
claude-stop
```

---

## 3️⃣ Always-Running (Auto-Start on Login)

Setup:
```bash
bash /Volumes/Akash\ SSD/repos/jarvis-brain/setup-autostart-macos.sh
```

Edit the plist file:
```bash
nano ~/Library/LaunchAgents/com.jarvis.claude.haiku.plist
```

Replace `sk-ant-your-key-here` with your actual key, then:
```bash
launchctl load ~/Library/LaunchAgents/com.jarvis.claude.haiku.plist
```

Claude will **automatically start on login!**

---

## 📋 All Automation Methods

### Makefile (Zero Setup)
```bash
cd /Volumes/Akash\ SSD/repos/jarvis-brain
make claude-start        # Start
make claude-stop         # Stop
make claude-status       # Check status
make claude-test-api     # Test endpoints
```

### Shell Script (One Command)
```bash
bash /Volumes/Akash\ SSD/repos/jarvis-brain/start-claude.sh
```

### CLI Wrapper (Direct Control)
```bash
/Volumes/Akash\ SSD/repos/jarvis-brain/claude generate "request" python
/Volumes/Akash\ SSD/repos/jarvis-brain/claude analyze "code"
/Volumes/Akash\ SSD/repos/jarvis-brain/claude test "code" python
/Volumes/Akash\ SSD/repos/jarvis-brain/claude refactor "code" python clean
/Volumes/Akash\ SSD/repos/jarvis-brain/claude explain "code"
```

### Aliases (After Setup)
```bash
claude-start
cg "request" python
ca "code"
ct "code" python
cr "code" python clean
ce "code"
```

### Auto-Start (LaunchAgent)
```bash
bash /Volumes/Akash\ SSD/repos/jarvis-brain/setup-autostart-macos.sh
# Edit plist with API key
launchctl load ~/Library/LaunchAgents/com.jarvis.claude.haiku.plist
```

---

## ⚡ One-Liner Commands

Start Claude:
```bash
cd /Volumes/Akash\ SSD/repos/jarvis-brain && make claude-start
```

Stop Claude:
```bash
cd /Volumes/Akash\ SSD/repos/jarvis-brain && make claude-stop
```

Check status:
```bash
cd /Volumes/Akash\ SSD/repos/jarvis-brain && make claude-status
```

Generate code:
```bash
cd /Volumes/Akash\ SSD/repos/jarvis-brain && ./claude generate "hello world" python
```

---

## 🎯 Recommended Setup (5 minutes)

```bash
# 1. Go to project
cd /Volumes/Akash\ SSD/repos/jarvis-brain

# 2. Source aliases
source claude-shell-setup.sh

# 3. Add to shell profile (permanent)
echo 'source /Volumes/Akash\ SSD/repos/jarvis-brain/claude-shell-setup.sh' >> ~/.zshrc

# 4. Test it
claude-start
sleep 3
./claude status

# 5. Start using!
cg "fibonacci function" python
```

---

## 🔥 Pro Tips

### Use with Aliases
```bash
# After: source claude-shell-setup.sh
claude-start
cg "REST API" python             # Generate
ca "my code here"                # Analyze
ct "def add(a,b): return a+b"   # Test
cr "x=[i for i in range(10)]"   # Refactor
ce "complex code"                # Explain
claude-status
claude-stop
```

### Batch Operations
```bash
# Generate multiple files
cg "fibonacci" python > fib.py
cg "quicksort" python > sort.py
cg "binary search" python > search.py

# Analyze all
cd generated_code
for file in *.py; do
    echo "=== $file ==="
    ca "$(cat $file)"
done
```

### Watch Mode
```bash
# Start in one terminal
make claude-start

# Watch logs in another
tail -f backend.log

# Use in third terminal
./claude generate "your request" python
```

---

## 🛑 Stopping Claude

### Normal Stop
```bash
make claude-stop
```

### Force Stop
```bash
pkill -f "python backend/app.py"
```

### Remove Auto-Start
```bash
launchctl unload ~/Library/LaunchAgents/com.jarvis.claude.haiku.plist
```

---

## ✅ Verify Setup

Check if running:
```bash
curl http://localhost:8001/api/claude/status
```

List processes:
```bash
ps aux | grep "python backend"
```

Check port:
```bash
lsof -i :8001
```

---

## 🚀 Start Here

**Fastest path to using Claude:**

```bash
# Terminal 1
cd /Volumes/Akash\ SSD/repos/jarvis-brain && bash start-claude.sh

# Terminal 2 (wait 3 seconds)
./claude generate "hello world function" python
```

**Go from zero to code generation in < 1 minute!** ⚡

---

**Choose your automation style above and start building! 🧠🚀**
