# JARVIS Pro VS Code Extension

Intelligent code generation, debugging, and improvement directly in VS Code using Claude AI.

## 🎯 Features

- ✨ **Code Generation** - Generate code from natural language descriptions
- 🔍 **Code Analysis** - Analyze code for improvements and issues
- 🐛 **Project Debugging** - Automatic bug detection and fixing
- 📈 **Code Improvement** - Auto-improve code quality and performance
- 🧪 **Test Generation** - Generate unit tests automatically
- 🔧 **Code Refactoring** - Intelligent code refactoring
- 📚 **Code Explanation** - Get detailed explanations of code
- 🏗️ **Build with Debug** - Full 7-phase build with debugging support
- 📊 **Real-time Status** - Monitor JARVIS in status bar

## 🚀 Installation

### Option 1: From VS Code Marketplace
1. Open VS Code Extension Marketplace
2. Search for "JARVIS Pro"
3. Click Install

### Option 2: From Source
```bash
cd .vscode-extension
npm install
vsce package
code --install-extension jarvis-pro-*.vsix
```

## ⚙️ Setup

### 1. Install Dependencies
```bash
pip install websocket-server anthropic
npm install -g @vscode/vsce
```

### 2. Configure JARVIS Server
Open Settings (Cmd+, or Ctrl+,) and configure:

```json
{
  "jarvis.serverHost": "localhost",
  "jarvis.serverPort": 8765,
  "jarvis.autoStart": true,
  "jarvis.defaultLanguage": "python"
}
```

### 3. Start JARVIS Server
Run command palette (Cmd+Shift+P) and select:
```
JARVIS: Start Integration Server
```

Or let it auto-start on VS Code launch (default).

## 💻 Usage

### Command Palette (Cmd+Shift+P)

All JARVIS commands are available in command palette:

#### Code Generation
- **JARVIS: Generate Code** - Create new code from description
- **JARVIS: Generate Tests** - Generate unit tests for selected code

#### Code Analysis
- **JARVIS: Analyze Code** - Analyze selected code for improvements
- **JARVIS: Explain Code** - Get detailed explanation of code
- **JARVIS: Refactor Code** - Refactor selected code intelligently
- **JARVIS: Debug Project** - Scan entire project for bugs
- **JARVIS: Improve Code** - Auto-improve multiple files

#### Building & Status
- **JARVIS: Build with Debug** - Full 7-phase build with debugging
- **JARVIS: Show Status** - Display JARVIS status
- **JARVIS: Start Integration Server** - Start JARVIS server
- **JARVIS: Stop Integration Server** - Stop JARVIS server

### Context Menu (Right-click in Editor)

Right-click on selected code for quick access to:
- Analyze Code
- Refactor Code
- Explain Code
- Generate Tests

### Status Bar

The JARVIS status appears in the bottom left status bar:
- 🟢 **JARVIS: Online** - Server is running
- 🔴 **JARVIS: Offline** - Server is not running
- 🟡 **JARVIS: Initializing** - Server is starting

Click status bar to see detailed status.

## 📝 Examples

### Example 1: Generate a REST API

1. Open Command Palette (Cmd+Shift+P)
2. Type: `JARVIS: Generate Code`
3. Input: `Flask REST API with GET and POST endpoints`
4. Select language: `python`
5. Code is generated and inserted

### Example 2: Analyze & Refactor Code

1. Select code in editor
2. Right-click → `JARVIS: Analyze Code`
3. Review findings
4. Right-click again → `JARVIS: Refactor Code`
5. Code is refactored in place

### Example 3: Generate Tests

1. Select function code
2. Right-click → `JARVIS: Generate Tests`
3. Tests open in new document
4. Copy/paste into test file

### Example 4: Debug Project

1. Command Palette → `JARVIS: Debug Project`
2. JARVIS scans project for bugs
3. Issues are displayed
4. Auto-fix with `JARVIS: Improve Code`

### Example 5: Build with Debugging

1. Command Palette → `JARVIS: Build with Debug`
2. Full 7-phase build executes:
   - Syntax Check
   - Linting
   - Testing
   - Debug Info Generation
   - Code Optimization
   - Documentation
   - Packaging
3. Results displayed

## 🔧 Configuration

### Settings

```json
{
  // JARVIS server hostname
  "jarvis.serverHost": "localhost",

  // JARVIS server port
  "jarvis.serverPort": 8765,

  // Auto-start server on VS Code launch
  "jarvis.autoStart": true,

  // Default programming language for operations
  "jarvis.defaultLanguage": "python"
}
```

### Environment Variables

```bash
# Set JARVIS API key
export ANTHROPIC_API_KEY="your-key-here"

# Set server port
export JARVIS_PORT=8765

# Enable debug logging
export JARVIS_DEBUG=true
```

## 🧠 How It Works

### Architecture

```
VS Code Extension
    ↓
WebSocket Connection (port 8765)
    ↓
JARVIS Integration Server
    ↓
    ├→ Claude Code Generator
    ├→ Auto Debug Engine
    ├→ Performance Optimizer
    └→ JARVIS Pro Model
```

### Workflow

1. **User Input**: Type command in VS Code
2. **Send to Server**: Extension sends command via WebSocket
3. **Process**: JARVIS server executes Claude operation
4. **Return Result**: Server sends result back to extension
5. **Display**: Extension shows result in VS Code

### Supported Languages

- Python 🐍
- JavaScript/TypeScript 📘
- Java ☕
- C++ 🔧
- C# 🎮
- Go 🐹
- Rust 🦀
- HTML/CSS 🎨

## 🐛 Troubleshooting

### Server Connection Failed

```bash
# Check if server is running
lsof -i :8765

# Start server manually
python3 core/vscode_server.py

# Check logs
tail -f .vscode_server.log
```

### Commands Not Working

1. Check server status: `JARVIS: Show Status`
2. Restart server: `JARVIS: Stop Server` → `JARVIS: Start Server`
3. Check Python environment has dependencies:
   ```bash
   pip install anthropic websocket-server
   ```

### Slow Response

1. Reduce file count in `JARVIS: Improve Code`
2. Use `JARVIS: Build with Debug --fast` for quick builds
3. Check Claude API rate limits

## 📚 Related Documentation

- [JARVIS Pro Model](../JARVIS_PRO_MODEL.md)
- [Build & Debug Integration](../BUILD_DEBUG_INTEGRATION.md)
- [VS Code Integration Guide](../PRO_INTEGRATION_GUIDE.md)
- [In-Code Debug System](../core/in_code_debug.py)

## 🤝 Support

For issues and feature requests:
1. Check [troubleshooting](#troubleshooting) section
2. Review JARVIS logs: `.vscode_server.log`, `.debug.log`
3. Check VS Code extension output panel

## 📄 License

MIT License - See LICENSE file

## 🎉 Quick Start

```bash
# 1. Install dependencies
pip install websocket-server anthropic

# 2. Start JARVIS server (if auto-start disabled)
python3 core/vscode_server.py &

# 3. Open VS Code
code .

# 4. Press Cmd+Shift+P and type "JARVIS"
# 5. Select any command and follow prompts

# That's it! Start using JARVIS for AI-powered coding 🚀
```

---

**Made with ❤️ by JARVIS Brain**

**Version**: 2.0.0  
**Requires**: VS Code 1.75+, Python 3.8+, Node.js 14+
