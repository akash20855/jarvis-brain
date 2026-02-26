# 🔨 Jarvis Brain Code Generation Guide

## Overview

Jarvis Brain now includes **AI-powered code generation** capabilities! When you ask Jarvis to create or generate code through the chat interface, it will:

1. **Generate** production-ready code using Mistral 7B AI
2. **Save** the code to your workspace directory
3. **Open** the code in VS Code automatically
4. **Execute** the code to validate it works

## Quick Start Examples

### Example 1: Generate a Calculator

```bash
User: "make a calculator"

Jarvis will:
✅ Generate calculator.py with add, subtract, multiply, divide functions
✅ Save to /workspace/generated_code/calculator.py
✅ Open in VS Code
```

### Example 2: Generate a Fibonacci Function

```bash
User: "create a fibonacci function"

Jarvis will:
✅ Generate fibonacci.py with optimized implementation
✅ Save to /workspace/generated_code/fibonacci.py
✅ Open in VS Code
```

### Example 3: Generate a Todo App

```bash
User: "generate a todo app"

Jarvis will:
✅ Generate todo.py with add, list, delete functionality
✅ Save to /workspace/generated_code/todo.py
✅ Open in VS Code
```

## Supported Languages

The code generator supports:
- **Python** (default) - Most versatile, works with all frameworks
- **JavaScript** - Web and Node.js scripts
- **HTML** - Web pages and components
- **Bash** - Shell scripts

### Requesting Specific Languages

```bash
User: "make a simple web server in javascript"
User: "create an html page with a form"
User: "write a bash script to backup files"
```

## Available Endpoints

### 1. Generate Code
```bash
POST /api/generate/code

Request:
{
  "request": "make a calculator",
  "language": "python"  # optional, defaults to python
}

Response:
{
  "success": true,
  "code": "def add(x, y):\n    return x + y\n...",
  "language": "python",
  "request": "make a calculator"
}
```

### 2. Save Code
```bash
POST /api/code/save

Request:
{
  "code": "print('hello')",
  "filename": "script.py",
  "language": "python"
}

Response:
{
  "success": true,
  "message": "Code saved successfully",
  "filepath": "/workspace/generated_code/script.py"
}
```

### 3. Execute Code
```bash
POST /api/code/execute

Request:
{
  "filepath": "/workspace/generated_code/calculator.py"
}

Response:
{
  "success": true,
  "output": {
    "stdout": "Output from the script",
    "stderr": "Any errors",
    "return_code": 0
  }
}
```

### 4. Generate, Save & Open in VS Code (Full Workflow)
```bash
POST /api/code/create-and-open

Request:
{
  "request": "make a calculator",
  "filename": "calculator.py",
  "language": "python"
}

Response:
{
  "success": true,
  "message": "Code generated, saved, and opened in VS Code",
  "code": "def add(x, y):\n    return x + y\n...",
  "filepath": "/workspace/generated_code/calculator.py",
  "language": "python"
}
```

### 5. List Generated Files
```bash
GET /api/code/list

Response:
{
  "success": true,
  "files": [
    {
      "name": "calculator.py",
      "path": "/workspace/generated_code/calculator.py",
      "created": "2026-02-26T13:03:00"
    },
    {
      "name": "fibonacci.py",
      "path": "/workspace/generated_code/fibonacci.py",
      "created": "2026-02-26T13:04:00"
    }
  ],
  "total": 2
}
```

## System Architecture

### File Structure
```
jarvis-brain/
├── backend/
│   ├── app.py                    # Flask routes including code generation endpoints
│   └── Dockerfile
├── core/
│   ├── code_generator.py         # CodeGenerator class
│   ├── chatbot.py                # Enhanced with code generation detection
│   └── ai_services.py
├── frontend/
│   ├── src/
│   │   ├── App.jsx              # Updated with code generation UI
│   │   └── App.css
│   └── Dockerfile
└── generated_code/              # Generated Python/JS/HTML files
    ├── calculator.py
    ├── fibonacci.py
    ├── hello.py
    └── ...
```

### Data Flow

```
User Chat Input
    ↓
/api/chat/message (Flask Route)
    ↓
Chatbot.chat() - Detects if request is for code generation
    ↓
If Code Generation:
    ├→ CodeGenerator.generate_code() - Call Mistral AI
    ├→ CodeGenerator.save_code() - Write to file system
    ├→ CodeGenerator.open_in_vscode() - Launch VS Code
    └→ Return JSON response with code
    ↓
Frontend displays:
    ├→ Generated code (syntax highlighted)
    ├→ File location
    ├→ Execution status
    └→ VS Code open confirmation
```

## Code Generation Process

### Phase 1: Detection
The chatbot detects code generation requests using keywords:
- "make", "create", "generate", "write", "build"
- Combined with "a code", "a script", "a function", etc.

Example matches:
- ✅ "make a calculator"
- ✅ "create a todo app"
- ✅ "generate a fibonacci function"
- ✅ "write a hello world script"
- ✅ "build a web server"

### Phase 2: AI Generation
When detected, the request is sent to Mistral 7B AI with a prompt:
```
User requested: "make a calculator"

Generate complete, working python code that fulfills this request.
Include error handling and comments.
Make the code production-ready.
```

### Phase 3: Code Extraction
The AI response is processed to extract clean code:
1. If wrapped in markdown code blocks (```python...```), extract the code
2. If explanations precede the code, find the first line of code
3. Return clean, executable code

### Phase 4: File Save & Execution
The generated code is:
1. Saved to `/workspace/generated_code/`
2. File extension determined by language (`.py`, `.js`, `.html`, `.sh`)
3. Opened in VS Code automatically
4. Can be executed via `/api/code/execute`

## Testing Code Generation

### Test in Terminal
```bash
# Generate code
curl -X POST http://localhost:8000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{"message": "make a calculator"}'

# List generated files
curl http://localhost:8000/api/code/list

# Execute a file
curl -X POST http://localhost:8000/api/code/execute \
  -H "Content-Type: application/json" \
  -d '{"filepath": "/workspace/generated_code/calculator.py"}'
```

### Test in Frontend
1. Open http://localhost:3000 in your browser
2. Click on the "Chat" tab
3. Type: "make a calculator"
4. See the generated code displayed
5. Check VS Code - file should open automatically

## Configuration

### Workspace Directory
Generated code is saved to:
```
/workspace/generated_code/  (inside Docker)
/Volumes/Akash SSD/repos/jarvis-brain/generated_code/  (on host)
```

### AI Model
Default model: **Mistral 7B**
Located at: `http://host.docker.internal:11434`

### Language Support
Each language maps to a file extension:
- Python → `.py`
- JavaScript → `.js`
- HTML → `.html`
- Bash → `.sh`

## Best Practices

### 1. Clear Requests
✅ "make a calculator with add, subtract, multiply, divide"
❌ "code"

### 2. Specify Language When Needed
✅ "create a web server in javascript"
✅ "write a bash script to backup files"
❌ "make a server" (defaults to Python)

### 3. Test Generated Code
Generated code is production-ready, but always review:
1. Generated code displays in the UI
2. File is saved and can be opened in VS Code
3. Use `/api/code/execute` to run and test

### 4. File Management
All generated files are saved to `generated_code/` directory:
- Easy to find and manage
- Can be backed up or version controlled
- Persists across sessions (Docker volume mounted)

## Troubleshooting

### Code Not Generated
- Check the message contains a code-generation keyword: make, create, generate, write, build
- Verify Ollama/Mistral AI is running: `curl http://localhost:11434/api/tags`
- Check backend logs: `docker logs jarvis-backend`

### File Not Created
- Verify the directory exists: `ls /workspace/generated_code/`
- Check file permissions: `ls -la /workspace/generated_code/`
- Review backend logs for errors

### Code Has Syntax Errors
- The AI extraction may have issues with complex code
- Check the generated file directly
- Edit and save changes manually
- Use `/api/code/execute` to test

### VS Code Not Opening
- Ensure `code` command is in PATH: `which code`
- On macOS: Install VS Code command line tools
- Manual workaround: Open files from VS Code directly from `generated_code/` folder

## Examples

### Example: Calculator
```python
def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y == 0:
        raise ValueError("Cannot divide by zero")
    return x / y
```

### Example: Fibonacci
```python
def fibonacci(n: int) -> int:
    """Return the nth Fibonacci number."""
    if n <= 0:
        raise ValueError("n must be positive")
    if n == 1 or n == 2:
        return 1
    
    a, b = 1, 1
    for _ in range(2, n):
        a, b = b, a + b
    return b
```

### Example: Todo App
```python
class TodoList:
    def __init__(self):
        self.tasks = {}
    
    def add_task(self, task_id, description):
        self.tasks[task_id] = description
    
    def list_tasks(self):
        for id, desc in self.tasks.items():
            print(f"{id}: {desc}")
```

## API Integration

### Using Generated Code in Your Own Project

```python
import requests

# Generate code
response = requests.post(
    'http://localhost:8000/api/generate/code',
    json={
        'request': 'make a calculator',
        'language': 'python'
    }
)

generated_code = response.json()['code']

# Save to file
with open('calculator.py', 'w') as f:
    f.write(generated_code)

# Execute
exec_response = requests.post(
    'http://localhost:8000/api/code/execute',
    json={'filepath': '/path/to/calculator.py'}
)

print(exec_response.json()['output'])
```

## Future Enhancements

Planned features:
- [ ] Code formatting and linting
- [ ] Syntax highlighting in UI
- [ ] Code review and suggestions
- [ ] Version control integration
- [ ] Collaborative code generation
- [ ] Custom AI models support
- [ ] Code templates and snippets

---

**Last Updated:** February 26, 2026  
**Version:** 1.0.0  
**Status:** Production Ready
