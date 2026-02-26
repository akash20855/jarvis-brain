# 🤖 JARVIS AI Integration with VS Code

Complete guide to use JARVIS as your AI coding assistant in Visual Studio Code.

## Quick Start (2 minutes)

### 1️⃣ Start JARVIS Server
```bash
cd /Volumes/Akash\ SSD/repos/jarvis-brain
bash start-jarvis.sh
```

You should see:
```
✓ Server started with PID: XXXXX
✓ WebSocket listening on 8765
✓ Using Groq AI backend (free & fast)
```

### 2️⃣ Open VS Code and Install Extension
```bash
# Open VS Code to the JARVIS project
code /Volumes/Akash\ SSD/repos/jarvis-brain

# The JARVIS AI Assistant extension will auto-activate
# You should see "✨ Jarvis Ready!" notification
```

### 3️⃣ Start Using JARVIS

**Open Command Palette:** `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows/Linux)

Type any of these commands:

- **`jarvis: Chat`** → Open JARVIS chat
  - Shortcut: `Cmd+Alt+J` (Mac) or `Ctrl+Alt+J` (Windows)
- **`jarvis: Generate Tests`** → Create unit tests for selected code
- **`jarvis: Analyze Code`** → Get detailed code analysis
  - Shortcut: `Cmd+Alt+A`
- **`jarvis: Auto-Fix`** → Fix code automatically
  - Shortcut: `Cmd+Alt+F`
- **`jarvis: Debug`** → Find bugs
  - Shortcut: `Cmd+Alt+D`
- **`jarvis: Explain Code`** → Get code explanations
- **`jarvis: Refactor Code`** → Refactor selected code
- **`jarvis: Optimize Code`** → Performance optimization

---

## 🤖 Switch AI Models

Click the **`🤖 Jarvis (groq)`** button in the bottom status bar, or run:

```
Cmd+Shift+P → "Jarvis: Switch AI Model"
```

### Available Models

#### 🚀 **Groq (Recommended - Default)**
- ✅ Completely **FREE**
- ✅ **FAST** responses (2-5 seconds)
- ✅ No installation needed
- ✅ Model: Llama 3.3 70B
- 📍 Status: **✅ Running**

**Setup:**
- Get free API key: https://console.groq.com/keys
- Already configured in `.env` with your key

#### 🔐 **Claude (Premium - Optional)**
- Requires API key
- More advanced reasoning
- Costs money after free trial
- Model: Claude 3.5 Haiku

**Setup:**
```
1. Get API key: https://console.anthropic.com/account/keys
2. Command Palette → "Jarvis: Switch AI Model"
3. Select "⚙️ Configure API Keys"
4. Paste your Claude API key
5. Reload VS Code
```

#### 💻 **Ollama (Local & Free)**
- **Completely local** - No API calls!
- Requires ~8GB RAM
- Fast responses (after model loads)
- Models: Llama, Mistral, Neural Chat

**Setup:**
```
1. Install: https://ollama.ai
2. Download model: ollama pull mistral
3. Start: ollama serve
4. In VS Code → "Jarvis: Switch AI Model"
5. Select "💻 Ollama"
6. Reload VS Code
```

---

## 📋 Right-Click Context Menu

Select code and right-click for quick JARVIS actions:
- ⚡ **Quick Fix** - Auto-fix issues
- **Explain Code** - Get explanation
- **Optimize Code** - Performance tips

---

## ⌨️ Keyboard Shortcuts

| Command | Mac | Windows/Linux |
|---------|-----|---------------|
| Chat | `Cmd+Alt+J` | `Ctrl+Alt+J` |
| Fix Code | `Cmd+Alt+F` | `Ctrl+Alt+F` |
| Analyze | `Cmd+Alt+A` | `Ctrl+Alt+A` |
| Debug | `Cmd+Alt+D` | `Ctrl+Alt+D` |

---

## ⚙️ Configuration

Edit VS Code settings (`Cmd+,`):

```json
{
  "jarvis.enabled": true,
  "jarvis.aiBackend": "groq",           // groq | claude | ollama
  "jarvis.backendUrl": "ws://localhost:8765",
  "jarvis.autoFix": true,               // Auto-fix on save
  "jarvis.liveAnalysis": true,          // Real-time analysis
  "jarvis.showSuggestions": true,       // Show CodeLens
  "jarvis.analysisLevel": "standard"    // basic | standard | advanced
}
```

---

## 🔧 Troubleshooting

### "Jarvis not found" or "Connection refused"

1. Check if server is running:
   ```bash
   ps aux | grep "vscode_server"
   ```

2. Restart the server:
   ```bash
   pkill -f "vscode_server" || true
   bash start-jarvis.sh
   ```

3. Verify WebSocket is listening:
   ```bash
   lsof -i :8765
   ```

### API Key Issues

If you get "API key not set" error:

1. **For Groq:**
   - Get key from: https://console.groq.com/keys
   - Update `.env`: `GROQ_API_KEY=your_key_here`
   - Restart server: `bash start-jarvis.sh`

2. **For Claude:**
   - Get key from: https://console.anthropic.com/account/keys
   - In VS Code Settings → Configure API Key
   - Switch to Claude model

### Slow Responses

- **Groq is slow?** → Usually means API is busy. Try later.
- **Claude slow?** → Normal, it's doing heavy computation
- **Ollama slow?** → First run takes longer. Model stays in memory.

### Not seeing suggestions?

1. Reload VS Code: `Cmd+Shift+P` → "Reload Window"
2. Check `jarvis.showSuggestions` is enabled
3. Check `jarvis.liveAnalysis` is enabled

---

## 📊 Usage Examples

### Generate Tests
```
Select a function → Cmd+Shift+P → "Jarvis: Generate Tests"
```
Creates unittest, pytest, or Jest tests depending on language.

### Analyze Code
```
Open a file → Cmd+Shift+P → "Jarvis: Analyze Code"
```
Shows:
- Code quality score
- Issues found
- Complexity analysis
- Maintainability suggestions

### Chat with JARVIS
```
Cmd+Alt+J → Open chat panel
```
Ask anything:
- "Create a Python function that..."
- "Explain this error message"
- "How to optimize this code?"
- "What's wrong with this code?"

---

## 🚀 Behind the Scenes

**How it works:**
1. VS Code extension → WebSocket message
2. JARVIS server processes → Forwards to AI backend
3. AI backend (Groq/Claude/Ollama) → Generates response
4. Server → Returns to VS Code
5. VS Code → Shows results to you

**Server Details:**
- **Runs on:** `ws://localhost:8765`
- **Language:** Python
- **Main file:** `core/vscode_server.py`
- **Log file:** `.jarvis_logs/startup.log`

---

## 📚 Full Feature List

✅ Code generation
✅ Code analysis & linting
✅ Bug detection
✅ Auto-fix issues
✅ Code refactoring
✅ Performance optimization
✅ Unit test generation
✅ Code explanation
✅ Comment generation
✅ Debug assistance
✅ Chat with AI
✅ Multi-language support (Python, JS, TS, Java, C++, Go, Rust, C#)

---

## 🎯 Next Steps

1. ✅ Start the server: `bash start-jarvis.sh`
2. ✅ Open VS Code
3. ✅ Click the Jarvis icon in the activity bar
4. ✅ Start coding with AI assistance!

**Need help?** Check the main README.md or STATUS.md

---

## 💡 Tips & Tricks

- **Live Analysis:** Code is analyzed in real-time as you type
- **Auto-Fix:** Errors are fixed automatically when you save (toggle in settings)
- **Quick Suggestions:** Right-click for context menu suggestions
- **Chat Shortcuts:** Use predefined prompts in chat for common tasks
- **Model Comparison:** Try different AI backends to compare quality and speed

---

**Version:** 1.0.0  
**Status:** ✅ Production Ready  
**Last Updated:** Feb 26, 2026
