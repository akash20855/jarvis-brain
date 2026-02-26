## Claude Haiku 4.5 - Quick Reference Card

### 🚀 Setup (2 minutes)

```bash
# 1. Get API key
# https://console.anthropic.com

# 2. Set environment variable
export ANTHROPIC_API_KEY="sk-ant-..."

# 3. Start backend
FLASK_PORT=8001 python backend/app.py
```

---

### 💻 API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/claude/status` | GET | Check if Claude is available |
| `/api/claude/generate` | POST | Generate code from description |
| `/api/claude/analyze` | POST | Analyze code & get suggestions |
| `/api/claude/test` | POST | Generate unit tests |
| `/api/claude/refactor` | POST | Improve code quality |
| `/api/claude/explain` | POST | Explain code clearly |

---

### 📝 Code Examples

#### Generate
```json
{
  "request": "REST API for todo app",
  "language": "python"
}
```

#### Analyze
```json
{
  "code": "def foo(): pass",
  "filename": "script.py"
}
```

#### Test
```json
{
  "code": "def get_name(): return 'John'",
  "language": "python"
}
```

#### Refactor
```json
{
  "code": "x = [i for i in range(10) if i%2]",
  "language": "python",
  "style": "readable"
}
```
**Styles:** `clean`, `performance`, `readable`, `pythonic`

#### Explain
```json
{
  "code": "result = [x*2 for x in nums if x > 0]"
}
```

---

### 🐍 Python Usage

```python
from core.claude_code_generator import get_claude_generator

claude = get_claude_generator()

# Generate
result = claude.generate_code("calculator app")
print(result['code'])

# Analyze
result = claude.analyze_code("complex code", "main.py")

# Test
result = claude.generate_test("def add(a,b): return a+b", "python")

# Refactor
result = claude.refactor_code(code, "python", "pythonic")

# Explain
result = claude.explain_code(complex_code)
```

---

### 🔧 Environment Variables

```bash
# Required
export ANTHROPIC_API_KEY="sk-ant-..."

# Optional (backend)
export FLASK_PORT=8001
export FLASK_ENV=production
```

---

### 📊 Response Format

```json
{
  "success": true,
  "code": "generated_code_here",
  "filename": "script.py",
  "filepath": "/path/to/script.py",
  "language": "python",
  "created_at": "2026-02-26T21:45:00.123456"
}
```

Error response:
```json
{
  "success": false,
  "error": "error message"
}
```

---

### 🎯 Common Tasks

#### Generate FastAPI Server
```bash
curl -X POST http://localhost:8001/api/claude/generate \
  -H "Content-Type: application/json" \
  -d '{"request":"FastAPI REST API with JWT auth","language":"python"}'
```

#### Analyze Security
```bash
curl -X POST http://localhost:8001/api/claude/analyze \
  -H "Content-Type: application/json" \
  -d '{"code":"db.execute(f\"SELECT * FROM users WHERE id={user_id}\")"}'
```

#### Generate Tests for Function
```bash
curl -X POST http://localhost:8001/api/claude/test \
  -H "Content-Type: application/json" \
  -d '{"code":"def validate_email(e): return \"@\" in e","language":"python"}'
```

#### Make Code More Pythonic
```bash
curl -X POST http://localhost:8001/api/claude/refactor \
  -H "Content-Type: application/json" \
  -d '{"code":"nums = []\nfor i in range(10):\n  nums.append(i*2)","style":"pythonic"}'
```

---

### ✅ Troubleshooting

| Error | Solution |
|-------|----------|
| `API key not set` | `export ANTHROPIC_API_KEY="sk-ant-..."` |
| `anthropic not installed` | `pip install anthropic` |
| `Connection refused` | Start backend: `FLASK_PORT=8001 python backend/app.py` |
| `Rate limited` | Free tier has limits - wait or upgrade |

---

### 💰 Pricing Quick Fact

- **Haiku**: $0.80 per million input tokens
- **Sonnet**: 4x more expensive
- **Opus**: 10x more expensive

💡 Haiku is perfect for production code generation!

---

### 📚 Documentation

- Full Guide: `CLAUDE_HAIKU_GUIDE.md`
- Integration Summary: `CLAUDE_INTEGRATION_SUMMARY.md`
- Test Script: `python test_claude.py`

---

### 🚀 Quick Start Checklist

- [ ] Get API key from anthropic.com
- [ ] Export ANTHROPIC_API_KEY
- [ ] Run `python test_claude.py`
- [ ] Start backend with `FLASK_PORT=8001 python backend/app.py`
- [ ] Test with first curl command
- [ ] Read CLAUDE_HAIKU_GUIDE.md for advanced usage

---

**You have Claude Haiku 4.5 built-in to Jarvis! 🧠**
