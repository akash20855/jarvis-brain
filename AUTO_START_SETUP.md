# JARVIS Auto-Start Complete Setup Guide

## 📋 What You Have

Three automation methods to run JARVIS:

1. **Manual Script** (`auto-init.sh`) - Run anytime
2. **System Daemon** (`setup-autostart.sh`) - Auto-start on boot
3. **Direct Command** - For development/debugging

---

## 🚀 OPTION 1: Quick System Auto-Start (Recommended)

### Step 1: Setup Environment
```bash
cd /Volumes/Akash SSD/repos/jarvis-brain

# Copy environment template
cp .env.template .env

# Edit .env and add your Claude API key
nano .env
# Or use VS Code
code .env
```

**In `.env`, add:**
```
ANTHROPIC_API_KEY=sk-proj-your-actual-key-here
```

### Step 2: Install Auto-Start Service
```bash
bash setup-autostart.sh install
```

Expected output:
```
✅ Plist copied to: /Users/yourname/Library/LaunchAgents/com.jarvis.vscode.server.plist
✅ JARVIS auto-start service installed!
✅ Server will auto-start on next login or system restart
```

### Step 3: Verify Installation
```bash
bash setup-autostart.sh status
```

### Step 4: Log Out and Back In
OR restart your Mac. JARVIS will auto-start automatically!

### Now Use JARVIS
```bash
# Open VS Code (server already running in background)
code .

# Press Cmd+Shift+P → type "JARVIS" → select any command
```

---

## ⚙️ OPTION 2: Manual Startup Script

Use this if you don't want system-level auto-start yet.

### Step 1: Make Script Executable
```bash
chmod +x auto-init.sh
```

### Step 2: Run Anytime
```bash
./auto-init.sh
```

The script will:
- ✅ Activate virtual environment
- ✅ Load API key from .env
- ✅ Kill any old processes
- ✅ Start JARVIS server
- ✅ Verify it's running
- ✅ Log everything

### Step 3: Use JARVIS
```bash
code .  # Open VS Code (server already running)
```

---

## 🔧 OPTION 3: Manual Development Start

For development or debugging:

```bash
# Navigate to workspace
cd /Volumes/Akash SSD/repos/jarvis-brain

# Activate virtual environment
source jarvis_env/bin/activate

# Load environment variables
export $(cat .env | xargs)

# Run server directly (shows all output)
python3 core/vscode_server.py
```

Server output will show:
```
[INFO] WebSocket server starting on ws://localhost:8765
[INFO] Command 'generateCode' registered
[INFO] Command 'analyzeCode' registered
...
[INFO] Server ready! 9 commands available
```

Press `Ctrl+C` to stop.

---

## 📊 Service Management Commands

### Check Status
```bash
bash setup-autostart.sh status
```

### Start Service
```bash
bash setup-autostart.sh start
```

### Stop Service
```bash
bash setup-autostart.sh stop
```

### Restart Service
```bash
bash setup-autostart.sh restart
```

### Remove Auto-Start
```bash
bash setup-autostart.sh uninstall
```

---

## 🔍 Monitoring & Troubleshooting

### View Server Logs
```bash
# Real-time logs
tail -f .jarvis_logs/server.log

# Or see launchd logs (if using system daemon)
tail -f .jarvis_logs/launchd.log

# Or view complete log
cat .jarvis_logs/server.log
```

### Check if Server is Running
```bash
# Check WebSocket connection
ps aux | grep "vscode_server.py"

# Or
lsof -i :8765
```

### Server PID File
```bash
# See the process ID
cat .jarvis_server.pid
```

### Kill Server Manually (if needed)
```bash
pkill -f "core/vscode_server.py"

# Or use PID file
kill $(cat .jarvis_server.pid)
```

---

## 🎯 Typical Workflow

### Day 1: Initial Setup
```bash
# 1. Configure environment
cp .env.template .env
nano .env  # Add your API key

# 2. Install auto-start
bash setup-autostart.sh install

# 3. Log out/in or restart
# Done! - JARVIS now starts automatically
```

### Every Day After
```bash
# JARVIS is already running in background!
code .

# Press Cmd+Shift+P → type "JARVIS" → use features
# Done!
```

### If Server Stops
```bash
# Manually restart anytime
bash setup-autostart.sh restart

# Or let launchd auto-restart it (5 minute check)
```

---

## 🚨 Troubleshooting

### Server won't start?

1. **Check API Key**
   ```bash
   cat .env | grep ANTHROPIC_API_KEY
   ```

2. **Check Port in Use**
   ```bash
   lsof -i :8765
   # If something is using it, kill it
   pkill -f "vscode_server.py"
   ```

3. **Manual Test**
   ```bash
   source jarvis_env/bin/activate
   python3 core/vscode_server.py
   ```

### Service won't install?

1. **Check plist file exists**
   ```bash
   ls -la com.jarvis.vscode.server.plist
   ```

2. **Verify LaunchAgents directory**
   ```bash
   mkdir -p ~/Library/LaunchAgents
   ```

3. **Try manual load**
   ```bash
   launchctl load ~/Library/LaunchAgents/com.jarvis.vscode.server.plist
   ```

### Service installed but not starting?

1. **Check logs**
   ```bash
   tail -f .jarvis_logs/launchd.log
   ```

2. **Unload and reload**
   ```bash
   bash setup-autostart.sh uninstall
   bash setup-autostart.sh install
   ```

3. **Log out and back in** (required for launchd)

---

## 📚 Available JARVIS Commands in VS Code

Once running, access via `Cmd+Shift+P`:

- **JARVIS: Generate Code** - Create new code from description
- **JARVIS: Analyze Code** - Analyze selected code
- **JARVIS: Debug Project** - Auto-debug issues
- **JARVIS: Improve Code** - Suggest improvements
- **JARVIS: Generate Tests** - Create test files
- **JARVIS: Refactor Code** - Refactor selected code
- **JARVIS: Explain Code** - Get code explanation
- **JARVIS: Build Project** - Run build system
- **JARVIS: Status** - Check server status

---

## 🎨 File Locations Reference

```
/Volumes/Akash SSD/repos/jarvis-brain/
├── .env                                    # Configuration (add API key here)
├── .env.template                           # Template for .env
├── auto-init.sh                            # Manual startup script
├── setup-autostart.sh                      # Service management
├── com.jarvis.vscode.server.plist          # macOS launchd config
├── .jarvis_logs/                           # Log directory
│   ├── server.log                          # Server logs
│   └── launchd.log                         # launchd daemon logs
├── .jarvis_server.pid                      # Server process ID
├── core/
│   ├── vscode_server.py                    # Main WebSocket server
│   ├── claude_code_generator.py            # Claude AI integration
│   └── ...
└── .vscode/
    ├── extensions.json                     # VS Code extension config
    └── ...
```

---

## ✨ Next Steps

1. **Copy `.env.template` to `.env`** and add your API key
2. **Run `bash setup-autostart.sh install`**
3. **Log out and back in** (or restart)
4. **Open VS Code** - JARVIS is already running!
5. **Press `Cmd+Shift+P` and type "JARVIS"** to use commands

---

## 📞 Getting Help

- Check logs: `tail -f .jarvis_logs/server.log`
- Check service: `bash setup-autostart.sh status`
- Manual start: `./auto-init.sh`
- Direct run: `python3 core/vscode_server.py`

---

## 🎉 You're All Set!

JARVIS is now ready for **fully automatic operation**. Just use it!

For questions, check logs or run status command. Everything is self-contained and works on macOS 10.15+.

**Happy coding with JARVIS! 🚀**
