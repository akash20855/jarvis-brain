## Claude Haiku 4.5 - Setup Checklist

Complete this checklist to get Claude Haiku 4.5 working with Jarvis Brain.

---

## Step 1️⃣: Get API Key

- [ ] Go to https://console.anthropic.com
- [ ] Create an account (or log in)
- [ ] Generate a new API key
- [ ] Copy the key (format: `sk-ant-...`)
- [ ] Keep it safe ⚠️ (Don't share or commit to git)

**Estimated time: 2 minutes**

---

## Step 2️⃣: Set Environment Variable

Choose one method below:

### Option A: Terminal Session (Temporary)
```bash
export ANTHROPIC_API_KEY="sk-ant-your-actual-key-here"
```

### Option B: Shell Profile (Permanent)
```bash
# Add to ~/.zshrc (or ~/.bash_profile for bash)
echo 'export ANTHROPIC_API_KEY="sk-ant-..."' >> ~/.zshrc
source ~/.zshrc
```

### Option C: .env File
Create `.env` in project root:
```
ANTHROPIC_API_KEY=sk-ant-...
```

Then load it:
```bash
source .env
```

**Verify it worked:**
```bash
echo $ANTHROPIC_API_KEY
# Should show: sk-ant-xxxxx
```

**Estimated time: 3 minutes**

---

## Step 3️⃣: Verify Installation

### Check Virtual Environment
```bash
cd /Volumes/Akash\ SSD/repos/jarvis-brain
source jarvis_env/bin/activate
```

### Check Python Version
```bash
python --version
# Should be 3.14.x
```

### Check Anthropic Package
```bash
python -c "import anthropic; print(anthropic.__version__)"
# Should print: 0.84.0 or similar
```

### Run Test Script
```bash
python test_claude.py
```

Expected output:
```
🧠 Testing Claude Haiku 4.5 Integration

============================================================

1️⃣  Checking ANTHROPIC_API_KEY...
   ✅ API Key found: sk-ant-...

2️⃣  Checking anthropic package...
   ✅ anthropic installed: 0.84.0

3️⃣  Checking Claude module...
   ✅ ClaudeCodeGenerator imported successfully

4️⃣  Initializing Claude...
   ✅ Claude initialized with model: claude-3-5-haiku-20241022

5️⃣  Checking model info...
   ✅ Claude Haiku 4.5 Ready

6️⃣  Available Claude API Endpoints:
   ✅ All endpoints registered

✅ All Claude Haiku 4.5 tests passed!
```

**Estimated time: 2 minutes**

---

## Step 4️⃣: Start Backend Server

```bash
cd /Volumes/Akash\ SSD/repos/jarvis-brain
source jarvis_env/bin/activate
FLASK_PORT=8001 python backend/app.py
```

Expected output:
```
🚀 Starting Jarvis Brain Backend API...
Environment: development
Debug Mode: False
📡 Listening on http://0.0.0.0:8001
```

Keep this terminal open (it's your API server)

**Estimated time: 1 minute**

---

## Step 5️⃣: Test Claude Status (New Terminal)

Open a NEW terminal window while backend is running:

```bash
curl http://localhost:8001/api/claude/status
```

Expected response:
```json
{
  "success": true,
  "status": "✅ Claude Haiku 4.5 Ready",
  "model": {
    "model": "claude-3-5-haiku-20241022",
    "provider": "anthropic",
    "type": "claude",
    "usage": "code generation, analysis, testing, refactoring"
  },
  "api_available": true
}
```

**Estimated time: 1 minute**

---

## Step 6️⃣: Generate Your First Code

```bash
curl -X POST http://localhost:8001/api/claude/generate \
  -H "Content-Type: application/json" \
  -d '{
    "request": "create a simple hello world function",
    "language": "python"
  }'
```

Expected response:
```json
{
  "success": true,
  "code": "def hello_world():\n    \"\"\"Print hello world.\"\"\"\n    print(\"Hello, World!\")\n\nif __name__ == \"__main__\":\n    hello_world()",
  "filename": "hello_world.py",
  "filepath": "/Volumes/Akash SSD/repos/jarvis-brain/generated_code/hello_world.py",
  "language": "python",
  "created_at": "2026-02-26T21:45:00.123456"
}
```

🎉 **You just generated code with Claude!**

**Estimated time: 2 minutes**

---

## Step 7️⃣: Explore Other Features

Try these commands:

### Analyze Code
```bash
curl -X POST http://localhost:8001/api/claude/analyze \
  -H "Content-Type: application/json" \
  -d '{"code": "def bad(): eval(input())"}'
```

### Generate Tests
```bash
curl -X POST http://localhost:8001/api/claude/test \
  -H "Content-Type: application/json" \
  -d '{"code": "def add(a, b): return a + b", "language": "python"}'
```

### Refactor Code
```bash
curl -X POST http://localhost:8001/api/claude/refactor \
  -H "Content-Type: application/json" \
  -d '{"code": "x = [i for i in range(10)]", "language": "python", "style": "pythonic"}'
```

See `CLAUDE_QUICK_REFERENCE.md` for more examples.

**Estimated time: 5 minutes**

---

## 🎯 Summary

| Step | Task | Status |
|------|------|--------|
| 1 | Get API Key | ⬜ |
| 2 | Set Environment Variable | ⬜ |
| 3 | Verify Installation | ⬜ |
| 4 | Start Backend | ⬜ |
| 5 | Test Claude Status | ⬜ |
| 6 | Generate First Code | ⬜ |
| 7 | Explore Features | ⬜ |

---

## ⏱️ Total Setup Time: ~15 minutes

- Getting API key: 2 min
- Environment setup: 3 min
- Verification: 2 min
- Backend startup: 1 min
- Testing: 1 min
- First code generation: 2 min
- Exploration: 5 min

---

## 🚀 What's Next?

After setup, you can:

1. **Use Python API**: `from core.claude_code_generator import get_claude_generator`
2. **Automate Code Generation**: Generate code in bulk for your projects
3. **Integrate with Dashboard**: Use Claude features from the web UI
4. **Scale Up**: Add Claude to your CI/CD pipeline
5. **Customize**: Modify prompts and add your own Claude code generation functions

---

## ❓ Troubleshooting

### Problem: "API Key not recognized"
**Solution:** 
- Verify key starts with `sk-ant-`
- Check no extra spaces: `echo "$ANTHROPIC_API_KEY" | wc -c`
- Log into console.anthropic.com to verify key is active

### Problem: "Connection refused"
**Solution:**
- Make sure backend is running in another terminal
- Check Flask is listening on 8001: `lsof -i :8001`
- Verify FLASK_PORT is set: `echo $FLASK_PORT`

### Problem: "anthropic not installed"
**Solution:**
```bash
source jarvis_env/bin/activate
pip install anthropic
```

### Problem: "Module not found"
**Solution:**
```bash
# Verify you're in the right directory
cd /Volumes/Akash\ SSD/repos/jarvis-brain

# Verify venv is activated
source jarvis_env/bin/activate

# Check Python path
python -c "import sys; print(sys.path)"
```

---

## 📚 Documentation

- **Full Guide**: [CLAUDE_HAIKU_GUIDE.md](CLAUDE_HAIKU_GUIDE.md)
- **Quick Reference**: [CLAUDE_QUICK_REFERENCE.md](CLAUDE_QUICK_REFERENCE.md)
- **Integration Summary**: [CLAUDE_INTEGRATION_SUMMARY.md](CLAUDE_INTEGRATION_SUMMARY.md)
- **Official Docs**: https://docs.anthropic.com

---

## 💡 Pro Tips

1. **Batch Processing**: Generate multiple code snippets and save to a list
2. **Cost Optimization**: Haiku is 10x cheaper than Opus for same quality on code
3. **CI/CD Integration**: Add Claude code generation to your build pipeline
4. **Custom Prompts**: Modify `CLAUDE_HAIKU_GUIDE.md` examples for your needs
5. **Rate Limiting**: Cache results to avoid repeated API calls

---

## ✅ Verification Commands

Keep these handy for testing:

```bash
# Check API key is set
echo $ANTHROPIC_API_KEY

# Verify venv
which python

# Check anthropic installed
python -m pip list | grep anthropic

# Test backend
curl http://localhost:8001/api/health

# Test Claude specifically
curl http://localhost:8001/api/claude/status

# Generate code
curl -X POST http://localhost:8001/api/claude/generate \
  -H "Content-Type: application/json" \
  -d '{"request":"hello world","language":"python"}'
```

---

**🎉 You're all set! Enjoy using Claude Haiku 4.5 with Jarvis! 🧠**

Questions? See [CLAUDE_HAIKU_GUIDE.md](CLAUDE_HAIKU_GUIDE.md) for detailed documentation.
