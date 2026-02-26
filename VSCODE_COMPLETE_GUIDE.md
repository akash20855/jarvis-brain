# JARVIS Pro: Complete VS Code Integration Guide

## Overview

JARVIS Pro provides **complete integration with VS Code**, enabling you to access all JARVIS capabilities directly within your editor without leaving VS Code.

## 🎯 What You Get

### Direct Access to:
- 🤖 Claude Haiku AI code generation
- 🔍 Code analysis and documentation
- 🐛 Autonomous project debugging  
- ✨ Code improvement and optimization
- 🧪 Automatic test generation
- 🔧 Code refactoring
- 📚 In-line code explanation
- 🏗️ Advanced 7-phase builds with debugging

### Integration Points:
- ✅ Command Palette (Cmd+Shift+P)
- ✅ Context Menu (right-click)
- ✅ Status Bar indicator
- ✅ WebSocket API for real-time communication
- ✅ Custom tasks and debug configurations
- ✅ EditorConfig support

---

## ⚡ Quick Start (30 seconds)

### Method 1: Easiest (No Installation)

```bash
# 1. Start JARVIS server
python3 core/vscode_server.py &

# 2. Open VS Code in the project folder
code .

# 3. Press Cmd+Shift+P and type "JARVIS"
# Commands are available immediately!
```

### Method 2: Install as Extension

```bash
# 1. Install the extension
make vscode-install

# 2. Install the packaged VSIX
code --install-extension .vscode-extension/jarvis-pro.vsix

# 3. Restart VS Code

# Server will auto-start on VS Code launch
```

### Method 3: Development Mode

```bash
# 1. Install dependencies
npm install -g @vscode/vsce

# 2. Launch in debug mode
make vscode-dev

# 3. Press F5 in VS Code Extension Development Host
```

---

## 📖 Complete Feature List

### 🤖 Code Generation

**Command**: `JARVIS: Generate Code`

Generate any code from natural language:

```
Prompt: "REST API with FastAPI that has GET and POST endpoints"
Language: Python
Result: Fully functional REST API code inserted
```

**Supports**:
- Python, JavaScript/TypeScript, Java, C++, Go, Rust, C#
- Web APIs, CLIs, libraries, scripts, anything

### 🔍 Code Analysis

**Command**: `JARVIS: Analyze Code`

Analyze selected code for issues:

```python
def my_function(x, y):
    result = x + y
    return result
```

**Results**:
- Issues found
- Performance concerns
- Best practice violations
- Suggested improvements

### 🐛 Project Debugging

**Command**: `JARVIS: Debug Project`

Scan entire project for bugs:

```
Issues Found: 5
├─ File: core/main.py (2 issues)
├─ File: core/utils.py (1 issue)
├─ File: agents/ai.py (2 issues)
```

Follow-up: Use `JARVIS: Improve Code` to auto-fix

### ✨ Code Improvement

**Command**: `JARVIS: Improve Code`

Auto-improve multiple files:

```bash
Input: "How many files to improve?" → 10
Result:
  ✅ Improved 10 files
  ├─ Performance optimized
  ├─ Readability enhanced
  ├─ Best practices applied
  └─ Tests generated
```

### 🧪 Test Generation

**Command**: `JARVIS: Generate Tests`

Generate unit tests for selected code:

```python
# INPUT
def add(a, b):
    return a + b

# OUTPUT (generated)
import unittest

class TestAdd(unittest.TestCase):
    def test_positive_numbers(self):
        self.assertEqual(add(2, 3), 5)
    
    def test_negative_numbers(self):
        self.assertEqual(add(-2, -3), -5)
    
    def test_zero(self):
        self.assertEqual(add(0, 0), 0)
```

### 🔧 Code Refactoring

**Command**: `JARVIS: Refactor Code`

Intelligent refactoring:

```python
# BEFORE
def process(items):
    r = []
    for i in items:
        if i > 0:
            r.append(i * 2)
    return r

# AFTER (generated)
def process(items: List[int]) -> List[int]:
    """Process items by doubling positive values."""
    return [item * 2 for item in items if item > 0]
```

### 📚 Code Explanation

**Command**: `JARVIS: Explain Code`

Get detailed explanation in a webview:

```
CODE EXPLANATION
═════════════════

This function implements a binary search algorithm...
[Full detailed explanation with examples]
```

### 🏗️ Build with Debug

**Command**: `JARVIS: Build with Debug`

Executes 7-phase build:
1. ✅ Syntax Check
2. ✅ Linting
3. ✅ Testing
4. ✅ Debug Info Generation
5. ✅ Code Optimization
6. ✅ Documentation
7. ✅ Packaging

Results displayed with timing and any errors.

### 📊 Status Monitoring

**Status Bar**: Shows connection status
- 🟢 JARVIS: Online
- 🔴 JARVIS: Offline
- 🟡 JARVIS: Initializing

Click to see detailed status.

---

## 🎯 Real-World Examples

### Example 1: Develop a New Feature

```
1. Press Cmd+Shift+P → "JARVIS: Generate Code"
2. Input: "Database migration function using SQLAlchemy"
3. Code generated and inserted
4. Right-click → "JARVIS: Generate Tests"
5. Tests generated in new document
6. Cmd+Shift+P → "JARVIS: Build with Debug"
7. Full build and test execution
✅ Feature complete!
```

### Example 2: Debug & Improve Existing Code

```
1. Cmd+Shift+P → "JARVIS: Debug Project"
2. Review found issues
3. Cmd+Shift+P → "JARVIS: Improve Code" (count: 10)
4. Auto-fixes applied to 10 files
5. Cmd+Shift+P → "JARVIS: Build with Debug"
6. Verify improvements
✅ Code quality improved!
```

### Example 3: Refactor Legacy Code

```
1. Select function in editor
2. Right-click → "JARVIS: Refactor Code"
3. Modern, clean code appears
4. Right-click → "JARVIS: Explain Code"
5. Understand the refactored code
6. Right-click → "JARVIS: Generate Tests"
7. Tests for refactored code generated
✅ Legacy code modernized!
```

### Example 4: Quick Code Review

```
1. Select code block
2. Right-click → "JARVIS: Analyze Code"
3. Issues and suggestions displayed
4. Right-click → "JARVIS: Explain Code"
5. Understand the code and fixes
✅ Code review complete!
```

---

## 🔧 Configuration

### VS Code Settings

Open Settings (Cmd+, / Ctrl+,) and configure:

```json
{
  "jarvis.serverHost": "localhost",
  "jarvis.serverPort": 8765,
  "jarvis.autoStart": true,
  "jarvis.defaultLanguage": "python"
}
```

### Keyboard Shortcuts

You can add custom shortcuts. Edit `.vscode/keybindings.json`:

```json
[
  {
    "key": "cmd+shift+g",
    "command": "jarvis.generateCode"
  },
  {
    "key": "cmd+shift+a",
    "command": "jarvis.analyzeCode"
  },
  {
    "key": "cmd+shift+r",
    "command": "jarvis.refactorCode"
  }
]
```

### Environment Variables

```bash
# VS Code environment
export ANTHROPIC_API_KEY="sk-..."
export JARVIS_PORT=8765
export JARVIS_DEBUG=true
export JARVIS_HOST=localhost
```

---

## 🏗️ Architecture

### System Diagram

```
┌─────────────────────────────────────────┐
│       VS Code Editor                    │
│  (User Types Commands)                  │
└────────────────┬────────────────────────┘
                 │ Command Palette /
                 │ Context Menu / API
                 ▼
┌─────────────────────────────────────────┐
│   JARVIS VS Code Extension              │
│  (JavaScript / TypeScript)              │
│  • Command handlers                     │
│  • UI Components                        │
│  • WebSocket client                     │
└────────────────┬────────────────────────┘
                 │ WebSocket (ws://:8765)
                 ▼
┌─────────────────────────────────────────┐
│   JARVIS Integration Server             │
│   (Python / Flask)                      │
│  • Command routing                      │
│  • WebSocket server                     │
│  • API endpoints                        │
└─────────┬──────────┬──────────┬─────────┘
          │          │          │
    ┌─────▼───┐ ┌────▼────┐ ┌──▼──────┐
    │ Claude  │ │ DebugEngine  │ │ Builder │
    │ Generator│ │ Improver  │ │ System  │
    └─────────┘ └──────────┘ └─────────┘
```

### Data Flow

```
User Input
    ↓
VS Code Extension (extension.js)
    ↓
Validate Input
    ↓
Send WebSocket Message
    ↓
JARVIS Server (vscode_server.py)
    ↓
Route to Handler
    ↓
Execute Command (Claude / Debugger / Builder)
    ↓
Send Result Back
    ↓
VS Code Extension
    ↓
Display to User
```

---

## 🚀 Advanced Usage

### Custom Commands

You can add custom commands by editing `core/vscode_server.py`:

```python
def register_custom_command(self):
    self.register_command(
        "jarvis.customOperation",
        "My custom operation",
        self.cmd_custom_operation
    )

def cmd_custom_operation(self, param1, param2):
    # Your logic here
    return {"result": "value"}
```

### Batch Operations

Chain multiple commands:

```bash
# Debug, improve, and build in sequence
make vscode-start &
JARVIS_PID=$!

# Then in VS Code:
# 1. JARVIS: Debug Project
# 2. JARVIS: Improve Code (count: 20)
# 3. JARVIS: Build with Debug

kill $JARVIS_PID
```

### Integration with Other Tools

VS Code extension works with:
- ✅ Pytest for testing
- ✅ Black for formatting
- ✅ Pylint for linting
- ✅ Git for version control
- ✅ Terminal for shell commands

---

## 📋 Makefile Commands

```bash
# Installation
make vscode-install        # Complete setup
make vscode-setup          # Configure VS Code
make vscode-package        # Build VSIX file

# Development
make vscode-dev            # Debug mode
make vscode-start          # Start server

# Building
make build-advanced        # Build with debug
make build-clean           # Clean artifacts

# Testing
make debug-full            # Full debug suite
```

---

## 🐛 Troubleshooting

### Server Not Connecting

```bash
# Check if server is running
lsof -i :8765

# Start server manually
python3 core/vscode_server.py

# Check Python packages
pip list | grep anthropic
pip list | grep websocket
```

### Commands Not Available

1. Check Status Bar - should show connection
2. Open Output panel: View → Output → "JARVIS"
3. Check `code --status` in terminal
4. Reload VS Code window: Cmd+Shift+P → "Developer: Reload Window"

### Slow Response

- Reduce file count in batch operations
- Use `--fast` build option
- Check Claude API rate limits
- Monitor system resources

### Extension Not Loading

```bash
# Check extension logs
code --status

# Reinstall extension
code --uninstall-extension jarvis.jarvis-pro
make vscode-install

# Clear cache
rm -rf ~/.vscode/extensions/jarvis.*
```

---

## 📚 Related Documentation

- [JARVIS Pro Model Guide](JARVIS_PRO_MODEL.md)
- [Build & Debug Integration](BUILD_DEBUG_INTEGRATION.md)
- [In-Code Debugging](core/in_code_debug.py)
- [VS Code Extension README](.vscode-extension/README.md)

---

## 🎉 Summary

JARVIS Pro in VS Code gives you:

| Feature | Before | With JARVIS |
|---------|--------|-------------|
| Generate code | Manual | Cmd+Shift+P |
| Debug code | Debug tools | JARVIS scan |
| Write tests | Manual | Auto-generate |
| Refactor | Manual | One-click |
| Improve code | Manual analysis | Auto-improve |
| Build | Terminal | Cmd+Shift+P |

**Result**: 10x faster development! 🚀

---

**Ready to use?** Start with the [Quick Start](#-quick-start-30-seconds) section!
