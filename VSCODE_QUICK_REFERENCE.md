# 🤖 JARVIS AI Quick Reference Card

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Cmd+Alt+J` | 💬 Open Chat |
| `Cmd+Alt+F` | 🔧 Auto-Fix |
| `Cmd+Alt+A` | 📊 Analyze |
| `Cmd+Alt+D` | 🐛 Debug |
| `Cmd+Shift+P` | 🎯 Command Palette |

## 🚀 Quick Commands

```
Cmd+Shift+P then type:

jarvis: Chat                    💬 Ask anything
jarvis: Generate Tests          🧪 Create tests
jarvis: Analyze Code            📊 Code review
jarvis: Auto-Fix                🔧 Fix bugs
jarvis: Debug                   🐛 Find issues
jarvis: Explain Code            ❓ Get explanation
jarvis: Refactor Code           ♻️ Improve code
jarvis: Optimize Code           ⚙️ Performance
jarvis: Switch AI Model         🤖 Change backend
```

## 🤖 AI Models

**Click 🤖 in status bar to switch:**

| Model | Speed | Cost | Setup |
|-------|-------|------|-------|
| 🚀 **Groq** | Fast | Free | ✅ Ready |
| 🔐 **Claude** | Slow | $ | 🔑 Add key |
| 💻 **Ollama** | Medium | Free | 💻 Local |

## 📝 Usage Examples

### Generate Tests
```
1. Select function
2. Cmd+Shift+P → Generate Tests
3. Tests created in new file
```

### Fix Code
```
1. Open file with errors
2. Cmd+Alt+F
3. Issues fixed automatically
```

### Chat
```
1. Cmd+Alt+J
2. Type your question
3. Get AI response
```

### Analyze
```
1. Open any code file
2. Cmd+Alt+A
3. See issues & suggestions
```

## 🔑 API Keys

**Groq:** Already set up ✅  
**Claude:** https://console.anthropic.com/account/keys  
**Ollama:** Install from https://ollama.ai

## ⚙️ Server Commands

```bash
# Start server
bash start-jarvis.sh

# Stop server
pkill -f vscode_server

# Check status
ps aux | grep vscode_server

# View logs
tail -f .jarvis_logs/startup.log

# Full setup
bash setup-vscode-ai.sh
```

## 📱 VS Code Tips

- **Context Menu:** Right-click code for quick fixes
- **CodeLens:** Suggestions appear above functions
- **Status Bar:** Click 🤖 to change AI model
- **Output Panel:** See detailed analysis results

## 🔗 Important Links

```
JARVIS Server:       ws://localhost:8765
Groq Console:        https://console.groq.com
Claude Console:      https://console.anthropic.com
Ollama Download:     https://ollama.ai
```

## ❓ FAQ

**Q: Server won't start?**
A: `pkill -f vscode_server` then `bash start-jarvis.sh`

**Q: Want to switch to Claude?**
A: Click 🤖 → Configure API Keys → Add Claude key

**Q: How do I use local AI?**
A: Install Ollama, run `ollama serve`, click 🤖 → Select Ollama

**Q: Is Groq really free?**
A: Yes! 100% free with rate limits. Perfect for learning.

## 🎯 Common Tasks

| Task | Command |
|------|---------|
| Create function | Chat: "Create function that..." |
| Write tests | Select code → Generate Tests |
| Fix errors | Auto-Fix or right-click → Quick Fix |
| Understand code | Select → Explain Code |
| Improve performance | Select → Optimize Code |
| Better code style | Select → Refactor Code |

## 🚀 Get Started

1. **Start Server:** `bash start-jarvis.sh`
2. **Open VS Code:** `code .`
3. **Start Chatting:** `Cmd+Alt+J`
4. **Have Fun!** 🎉

---

**Print this card for quick reference!**  
*Last Updated: Feb 26, 2026*
