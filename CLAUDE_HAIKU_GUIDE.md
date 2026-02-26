## Claude Haiku 4.5 - Built-In AI for Jarvis Coding

### 🚀 Quick Start

Claude Haiku 4.5 is now integrated as Jarvis's built-in AI provider for all coding tasks. It provides **fast, affordable, high-quality code generation, analysis, and refactoring**.

**Features:**
- ⚡ Code generation from natural language
- 🔍 Code analysis with improvement suggestions
- 🧪 Automatic test generation
- ♻️ Code refactoring (multiple styles)
- 📚 Code explanation and documentation
- 💰 10x cheaper than Opus (perfect for scale)

---

## Setup

### 1️⃣ Get Anthropic API Key

1. Go to https://console.anthropic.com
2. Create an account (free trial available)
3. Generate API key in the dashboard
4. Copy your key: `sk-ant-...`

### 2️⃣ Install Dependencies

```bash
cd /Volumes/Akash\ SSD/repos/jarvis-brain
pip install anthropic
```

Or run the requirements installer:
```bash
pip install -r requirements.txt
```

### 3️⃣ Set Environment Variable

```bash
# Add to your shell profile (.zshrc, .bash_profile, etc.)
export ANTHROPIC_API_KEY="sk-ant-your-actual-key-here"

# Or export before running Jarvis
export ANTHROPIC_API_KEY="sk-ant-..."
python backend/app.py
```

### 4️⃣ Verify Setup

Check if Claude is available:
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

---

## API Endpoints

All Claude endpoints are available at `http://localhost:8001/api/claude/`

### 1. Generate Code
**POST `/api/claude/generate`**

Generate code from natural language description.

```bash
curl -X POST http://localhost:8001/api/claude/generate \
  -H "Content-Type: application/json" \
  -d '{
    "request": "create a fibonacci function that returns the first 10 numbers",
    "language": "python"
  }'
```

**Response:**
```json
{
  "success": true,
  "code": "def fibonacci(n=10):\n    fib = [0, 1]\n    while len(fib) < n:\n        fib.append(fib[-1] + fib[-2])\n    return fib[:n]\n\nprint(fibonacci())",
  "filename": "fibonacci.py",
  "filepath": "/Volumes/Akash SSD/repos/jarvis-brain/generated_code/fibonacci.py",
  "language": "python",
  "created_at": "2026-02-26T21:45:00.123456"
}
```

**Supported Languages:**
- python, javascript, typescript, java, cpp, csharp, go, rust, ruby, php, html, css, sql, bash

### 2. Analyze Code
**POST `/api/claude/analyze`**

Get detailed analysis and improvement suggestions.

```bash
curl -X POST http://localhost:8001/api/claude/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def bad_code(x): return eval(x)",
    "filename": "script.py"
  }'
```

**Response includes:**
- Issues and security concerns
- Performance optimizations
- Refactoring suggestions
- Comments on code quality

### 3. Generate Tests
**POST `/api/claude/test`**

Auto-generate comprehensive unit tests.

```bash
curl -X POST http://localhost:8001/api/claude/test \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def add(a, b):\n    return a + b",
    "language": "python"
  }'
```

**Response:**
```json
{
  "success": true,
  "tests": "import pytest\n\ndef test_add_positive(): assert add(2, 3) == 5\ndef test_add_negative(): assert add(-1, -1) == -2\n...",
  "filename": "test_add.py",
  "filepath": "/Volumes/Akash SSD/repos/jarvis-brain/generated_code/test_add.py"
}
```

### 4. Refactor Code
**POST `/api/claude/refactor`**

Refactor code with different styles.

```bash
curl -X POST http://localhost:8001/api/claude/refactor \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def foo(x):\n    if x > 0:\n        return x * 2\n    else:\n        return 0",
    "language": "python",
    "style": "clean"
  }'
```

**Available Styles:**
- `clean` - Readability and maintainability (default)
- `performance` - Speed and efficiency
- `readable` - Maximum clarity with comments
- `pythonic` - Python idioms and best practices

### 5. Explain Code
**POST `/api/claude/explain`**

Get a clear explanation of what code does.

```bash
curl -X POST http://localhost:8001/api/claude/explain \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def factorial(n): return 1 if n <= 1 else n * factorial(n-1)"
  }'
```

**Response includes:**
- Overall purpose
- Key steps broken down
- Important concepts
- Potential edge cases

### 6. Check Status
**GET `/api/claude/status`**

Check if Claude is available and configured.

```bash
curl http://localhost:8001/api/claude/status
```

---

## Python Usage

Use Claude directly in your Python code:

```python
from core.claude_code_generator import get_claude_generator

# Get the generator
claude = get_claude_generator()

# Generate code
result = claude.generate_code("make a web scraper for hacker news")
print(result['code'])
print(result['filepath'])

# Analyze code
analysis = claude.analyze_code("def bad(): eval('dangerous')")
print(analysis['analysis'])

# Generate tests
tests = claude.generate_test("def add(a, b): return a + b")
print(tests['tests'])

# Refactor
refactored = claude.refactor_code(old_code, style="pythonic")
print(refactored['refactored_code'])

# Explain
explanation = claude.explain_code("for i in range(10): print(i)")
print(explanation['explanation'])
```

---

## Configuration

### Using ai_config.yaml

Edit `/Volumes/Akash SSD/repos/jarvis-brain/ai_config.yaml` to use Claude for specific tasks:

```yaml
ai:
  code_analysis:
    enabled: true
    type: "anthropic"
    api_key: "${ANTHROPIC_API_KEY}"
    model: "claude-3-5-haiku-20241022"
    timeout: 30
    description: "Claude Haiku for code analysis"
  
  chat:
    enabled: true
    type: "anthropic"
    api_key: "${ANTHROPIC_API_KEY}"
    model: "claude-3-5-haiku-20241022"
    timeout: 30
    description: "Claude Haiku for coding chat"
```

### Available Claude Models

| Model | Best For | Cost | Speed |
|-------|----------|------|-------|
| `claude-3-5-haiku-20241022` | Code tasks, chat | 💰 Cheapest | ⚡ Fastest |
| `claude-3-sonnet-20240229` | Balanced tasks | 💰💰 Medium | ⏱️ Medium |
| `claude-3-opus-20240229` | Complex reasoning | 💰💰💰 Expensive | ⏳ Slower |

---

## Troubleshooting

### Error: "ANTHROPIC_API_KEY not set"

**Solution:** Set the environment variable:
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

### Error: "anthropic package not installed"

**Solution:** Install the package:
```bash
pip install anthropic
```

### Claude requests are slow

**Solution:** This is normal for the first request (API cold start). Subsequent requests should be faster.

### Rate limiting errors

**Solution:** 
1. Check your API usage at https://console.anthropic.com/account/billing/overview
2. Free tier has limits - consider upgrading
3. Add delays between requests if making many calls

### API Key not recognized

**Solution:**
1. Verify key format starts with `sk-ant-`
2. Check key hasn't expired or been revoked
3. Generate a new key from the Anthropic console
4. Make sure no extra spaces in the key

---

## Examples

### Example 1: Generate a FastAPI App

```bash
curl -X POST http://localhost:8001/api/claude/generate \
  -H "Content-Type: application/json" \
  -d '{
    "request": "create a FastAPI REST API with authentication, database models, and a get/post endpoint for todos",
    "language": "python"
  }'
```

### Example 2: Analyze Security Issue

```bash
curl -X POST http://localhost:8001/api/claude/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "code": "from flask import Flask\napp = Flask(__name__)\n\n@app.route(''/api/data'', methods=[''GET''])\ndef get_data():\n    user_id = request.args.get(''id'')\n    query = f\"SELECT * FROM users WHERE id = {user_id}\"\n    return db.execute(query)"
  }'
```

(Claude will identify SQL injection vulnerability!)

### Example 3: Auto-Generate Tests

```bash
curl -X POST http://localhost:8001/api/claude/test \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def validate_email(email):\n    return '@' in email and '.' in email",
    "language": "python"
  }'
```

### Example 4: Refactor for Performance

```bash
curl -X POST http://localhost:8001/api/claude/refactor \
  -H "Content-Type: application/json" \
  -d '{
    "code": "numbers = [1,2,3,4,5]\nresult = []\nfor n in numbers:\n    if n % 2 == 0:\n        result.append(n*2)",
    "style": "performance"
  }'
```

---

## Integration with Dashboard

Claude is automatically available in the Jarvis Dashboard. Coming soon:
- Claude code generation panel in dashboard
- Real-time code analysis
- Test generation UI
- Refactoring recommendations

---

## Pricing

Claude Haiku is the cheapest option:
- **Input:** $0.80 per million tokens
- **Output:** $4.00 per million tokens

Example costs:
- Generate 1000 code snippets: ~$1-2
- Analyze 100 files: ~$0.50
- Generate 1000 tests: ~$2-3

[View current pricing](https://www.anthropic.com/pricing)

---

## What's Next?

1. **Dashboard Integration** - Add Claude UI panels to dashboard
2. **WebSocket Support** - Real-time streaming responses
3. **Batch Processing** - Analyze multiple files at once
4. **Custom Models** - Support for fine-tuned Claude models
5. **Local Caching** - Cache analysis results

---

## Support

- **API Docs:** https://docs.anthropic.com
- **Console:** https://console.anthropic.com
- **Status:** https://status.anthropic.com

---

**🎉 You now have Claude Haiku 4.5 built-in to Jarvis for all your coding needs!**
