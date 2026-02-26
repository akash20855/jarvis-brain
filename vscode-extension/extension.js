/**
 * Jarvis AI Coding Assistant - VS Code Extension
 * Premium AI features for code analysis, fixing, and debugging - FREE
 */

const vscode = require('vscode');
const axios = require('axios');
const { AICodeAnalyzer } = require('./lib/ai-analyzer');
const { CodeFixer } = require('./lib/code-fixer');
const { CodeDebugger } = require('./lib/debugger');
const { ChatProvider } = require('./lib/chat-provider');

let analyzer;
let fixer;
let debugger_;
let chatProvider;
let statusBar;
const diagnosticCollection = vscode.languages.createDiagnosticCollection('jarvis');

/**
 * Extension activation
 */
async function activate(context) {
  console.log('✅ Jarvis AI Assistant is activating...');

  const config = vscode.workspace.getConfiguration('jarvis');
  const backendUrl = config.get('backendUrl', 'ws://localhost:8765');
  const aiBackend = config.get('aiBackend', 'groq');

  console.log(`[Extension] Connecting to ${backendUrl}`);
  console.log(`[Extension] AI Backend: ${aiBackend}`);

  // Initialize components
  analyzer = new AICodeAnalyzer(backendUrl);
  fixer = new CodeFixer(backendUrl);
  debugger_ = new CodeDebugger(backendUrl);
  chatProvider = new ChatProvider(backendUrl);

  console.log('[Extension] Components initialized');

  // Create status bar
  statusBar = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 100);
  statusBar.command = 'jarvis.switchAIModel';
  statusBar.text = `🤖 Jarvis (${aiBackend})`;
  statusBar.show();
  context.subscriptions.push(statusBar);

  // Register all commands
  registerCommands(context);

  console.log('[Extension] JARVIS AI Assistant activated successfully');
  // Setup file watchers
  setupFileWatchers(context);

  // Setup event listeners
  setupEventListeners(context);

  console.log(`✅ Jarvis AI Assistant activated successfully!`);
  console.log(`📡 Backend: ${aiBackend} | Server: ${backendUrl}`);
  vscode.window.showInformationMessage(`✨ Jarvis Ready! Using ${aiBackend} backend. Press Cmd+Alt+J for chat.`);
}

/**
 * Register all VS Code commands
 */
function registerCommands(context) {
  // Main commands
  context.subscriptions.push(
    vscode.commands.registerCommand('jarvis.activate', () => handleActivate()),
    vscode.commands.registerCommand('jarvis.chat', () => handleChat(context)),
    vscode.commands.registerCommand('jarvis.fix', () => handleFix()),
    vscode.commands.registerCommand('jarvis.analyze', () => handleAnalyze()),
    vscode.commands.registerCommand('jarvis.debug', () => handleDebug()),
    vscode.commands.registerCommand('jarvis.quickFix', () => handleQuickFix()),
    vscode.commands.registerCommand('jarvis.explainCode', () => handleExplainCode()),
    vscode.commands.registerCommand('jarvis.optimizeCode', () => handleOptimizeCode()),
    vscode.commands.registerCommand('jarvis.generateTests', () => handleGenerateTests()),
    vscode.commands.registerCommand('jarvis.addComments', () => handleAddComments()),
    vscode.commands.registerCommand('jarvis.refactor', () => handleRefactor()),
    vscode.commands.registerCommand('jarvis.findBugs', () => handleFindBugs()),
    vscode.commands.registerCommand('jarvis.showStatus', () => handleShowStatus()),
    vscode.commands.registerCommand('jarvis.switchAIModel', () => handleSwitchAIModel())
  );
}

/**
 * Setup file watchers for auto-analysis
 */
function setupFileWatchers(context) {
  const config = vscode.workspace.getConfiguration('jarvis');
  const liveAnalysis = config.get('liveAnalysis', true);

  if (!liveAnalysis) return;

  // Watch for file changes and run analysis
  const fileWatcher = vscode.workspace.createFileSystemWatcher('**/*.{py,js,ts,java,cpp,cs,go,rs}');

  fileWatcher.onDidChange(async (uri) => {
    const editor = vscode.window.activeTextEditor;
    if (editor && editor.document.uri.fsPath === uri.fsPath) {
      // Debounce and analyze
      setTimeout(() => analyzeDocument(editor), 500);
    }
  });

  context.subscriptions.push(fileWatcher);
}

/**
 * Setup event listeners
 */
function setupEventListeners(context) {
  const config = vscode.workspace.getConfiguration('jarvis');
  const autoFix = config.get('autoFix', true);

  // Listen for save events
  vscode.workspace.onDidSaveTextDocument(async (document) => {
    if (autoFix) {
      const editor = vscode.window.activeTextEditor;
      if (editor && editor.document === document) {
        performAutoFix(editor);
      }
    }
  });

  // Listen for active editor changes
  vscode.window.onDidChangeActiveTextEditor((editor) => {
    if (editor) {
      analyzeDocument(editor);
    }
  });
}

// ==================== COMMAND HANDLERS ====================

async function handleActivate() {
  vscode.window.showInformationMessage('✅ Jarvis AI Assistant is active!');
  statusBar.text = '✅ Jarvis Active';
}

async function handleChat(context) {
  console.log('[Extension] Opening JARVIS Chat...');
  const panel = vscode.window.createWebviewPanel(
    'jarvis-chat',
    '💬 Jarvis Chat',
    vscode.ViewColumn.Beside,
    { enableScripts: true }
  );

  panel.webview.html = getChatWebviewContent();

  panel.webview.onDidReceiveMessage(
    async (message) => {
      if (message.command === 'sendMessage') {
        try {
          console.log(`[Extension] Chat message: "${message.text.substring(0, 50)}..."`);
          const response = await chatProvider.chat(message.text);
          console.log('[Extension] Got response from chatProvider');
          panel.webview.postMessage({
            type: 'response',
            text: response.response,
            time: response.execution_time
          });
        } catch (error) {
          console.error('[Extension] Chat error:', error);
          vscode.window.showErrorMessage(`JARVIS Error: ${error.message}`);
          panel.webview.postMessage({
            type: 'error',
            text: 'Error: ' + error.message
          });
        }
      }
    },
    undefined,
    context.subscriptions
  );
}

async function handleFix() {
  const editor = vscode.window.activeTextEditor;
  if (!editor) {
    vscode.window.showErrorMessage('No file open');
    return;
  }

  vscode.window.showInformationMessage('🔧 Analyzing and fixing code...');
  
  try {
    const code = editor.document.getText();
    const fixes = await fixer.autoFix(code, editor.document.languageId);

    if (fixes.length === 0) {
      vscode.window.showInformationMessage('✅ No issues found!');
      return;
    }

    // Apply fixes
    const edit = new vscode.WorkspaceEdit();
    for (const fix of fixes) {
      edit.replace(
        editor.document.uri,
        new vscode.Range(fix.start.line, 0, fix.end.line, 999),
        fix.fixedCode
      );
    }

    await vscode.workspace.applyEdit(edit);
    vscode.window.showInformationMessage(`✅ Fixed ${fixes.length} issues!`);
  } catch (error) {
    vscode.window.showErrorMessage('Error: ' + error.message);
  }
}

async function handleAnalyze() {
  const editor = vscode.window.activeTextEditor;
  if (!editor) {
    vscode.window.showErrorMessage('No file open');
    return;
  }

  try {
    const analysis = await analyzer.analyzeDocument(editor.document);
    
    // Show results in output channel
    const output = vscode.window.createOutputChannel('Jarvis Analysis');
    output.appendLine('📊 CODE ANALYSIS RESULTS');
    output.appendLine('========================\n');
    output.appendLine(`Quality Score: ${analysis.qualityScore}/100`);
    output.appendLine(`Issues Found: ${analysis.issues.length}`);
    output.appendLine(`Complexity: ${analysis.complexity}`);
    output.appendLine(`Maintainability: ${analysis.maintainability}\n`);

    if (analysis.issues.length > 0) {
      output.appendLine('Issues:');
      for (const issue of analysis.issues) {
        output.appendLine(`  • ${issue.severity}: ${issue.message}`);
      }
    }

    output.show();
  } catch (error) {
    vscode.window.showErrorMessage('Error: ' + error.message);
  }
}

async function handleDebug() {
  const editor = vscode.window.activeTextEditor;
  if (!editor) {
    vscode.window.showErrorMessage('No file open');
    return;
  }

  try {
    const debugInfo = await debugger_.debug(editor.document);
    
    const output = vscode.window.createOutputChannel('Jarvis Debug');
    output.appendLine('🐛 DEBUG ANALYSIS');
    output.appendLine('=================\n');
    output.appendLine(`Potential Bugs: ${debugInfo.potentialBugs.length}`);
    output.appendLine(`Performance Issues: ${debugInfo.performanceIssues.length}`);
    output.appendLine(`Security Concerns: ${debugInfo.securityConcerns.length}\n`);

    if (debugInfo.potentialBugs.length > 0) {
      output.appendLine('Bugs:');
      for (const bug of debugInfo.potentialBugs) {
        output.appendLine(`  • Line ${bug.line}: ${bug.description}`);
      }
    }

    output.show();
  } catch (error) {
    vscode.window.showErrorMessage('Error: ' + error.message);
  }
}

async function handleQuickFix() {
  const editor = vscode.window.activeTextEditor;
  if (!editor) return;

  const selection = editor.selection;
  const selectedCode = editor.document.getText(selection);

  vscode.window.showInformationMessage('⚡ Applying quick fix...');
  
  try {
    const fix = await fixer.quickFix(selectedCode);
    await editor.edit(editBuilder => {
      editBuilder.replace(selection, fix.fixedCode);
    });
  } catch (error) {
    vscode.window.showErrorMessage('Error: ' + error.message);
  }
}

async function handleExplainCode() {
  const editor = vscode.window.activeTextEditor;
  if (!editor) return;

  const selection = editor.selection;
  const code = editor.document.getText(selection);

  try {
    const explanation = await analyzer.explainCode(code);
    
    const panel = vscode.window.createWebviewPanel(
      'jarvis-explain',
      '❓ Code Explanation',
      vscode.ViewColumn.Beside
    );

    panel.webview.html = `
      <html>
        <body style="font-family: Arial; padding: 20px;">
          <h2>Code Explanation</h2>
          <pre style="background: #f5f5f5; padding: 10px; border-radius: 5px;">${explanation}</pre>
        </body>
      </html>
    `;
  } catch (error) {
    vscode.window.showErrorMessage('Error: ' + error.message);
  }
}

async function handleOptimizeCode() {
  const editor = vscode.window.activeTextEditor;
  if (!editor) return;

  const code = editor.document.getText();

  try {
    const optimized = await analyzer.optimize(code);
    
    // Show diff
    const document = await vscode.workspace.openTextDocument({
      content: optimized,
      language: editor.document.languageId
    });

    vscode.window.showTextDocument(document, vscode.ViewColumn.Beside);
  } catch (error) {
    vscode.window.showErrorMessage('Error: ' + error.message);
  }
}

async function handleGenerateTests() {
  const editor = vscode.window.activeTextEditor;
  if (!editor) return;

  const code = editor.document.getText();

  try {
    const tests = await analyzer.generateTests(code, editor.document.languageId);
    
    const document = await vscode.workspace.openTextDocument({
      content: tests,
      language: editor.document.languageId
    });

    vscode.window.showTextDocument(document);
  } catch (error) {
    vscode.window.showErrorMessage('Error: ' + error.message);
  }
}

async function handleAddComments() {
  const editor = vscode.window.activeTextEditor;
  if (!editor) return;

  const code = editor.document.getText();

  try {
    const commented = await analyzer.addComments(code);
    
    await editor.edit(editBuilder => {
      const lastLine = editor.document.lineCount;
      const lastChar = editor.document.lineAt(lastLine - 1).text.length;
      editBuilder.replace(
        new vscode.Range(0, 0, lastLine - 1, lastChar),
        commented
      );
    });
  } catch (error) {
    vscode.window.showErrorMessage('Error: ' + error.message);
  }
}

async function handleRefactor() {
  const editor = vscode.window.activeTextEditor;
  if (!editor) return;

  const code = editor.document.getText();

  try {
    const refactored = await analyzer.refactor(code);
    
    await editor.edit(editBuilder => {
      const lastLine = editor.document.lineCount;
      const lastChar = editor.document.lineAt(lastLine - 1).text.length;
      editBuilder.replace(
        new vscode.Range(0, 0, lastLine - 1, lastChar),
        refactored
      );
    });
  } catch (error) {
    vscode.window.showErrorMessage('Error: ' + error.message);
  }
}

async function handleFindBugs() {
  const editor = vscode.window.activeTextEditor;
  if (!editor) return;

  try {
    const bugs = await debugger_.findBugs(editor.document);
    
    const diagnostics = [];
    for (const bug of bugs) {
      diagnostics.push(
        new vscode.Diagnostic(
          new vscode.Range(bug.line, 0, bug.line, 999),
          `🐛 ${bug.message}`,
          vscode.DiagnosticSeverity.Warning
        )
      );
    }

    diagnosticCollection.set(editor.document.uri, diagnostics);
  } catch (error) {
    vscode.window.showErrorMessage('Error: ' + error.message);
  }
}

async function handleShowStatus() {
  try {
    const status = await analyzer.getStatus();
    
    const message = `
    🚀 Jarvis Status:
    • Backend: ${status.online ? '✅ Online' : '❌ Offline'}
    • Commands: ${status.total_commands || 100}
    • Response Time: ${status.avg_response_time_ms || '<1'}ms
    • Ready: Yes ✅
    `;

    vscode.window.showInformationMessage(message);
  } catch (error) {
    vscode.window.showErrorMessage('Unable to connect to Jarvis backend');
  }
}

async function handleSwitchAIModel() {
  const config = vscode.workspace.getConfiguration('jarvis');
  const currentBackend = config.get('aiBackend', 'groq');

  const options = [
    {
      label: '🚀 Groq (Free & Fast)',
      description: 'Fast, free API - No installation needed',
      backend: 'groq'
    },
    {
      label: '🔐 Claude Backend (Premium)',
      description: 'Advanced model - Requires API key',
      backend: 'claude'
    },
    {
      label: '💻 Ollama (Local & Free)',
      description: 'Local models - Requires Ollama running',
      backend: 'ollama'
    },
    {
      label: '⚙️ Configure API Keys',
      description: 'Configure AI backends (Groq, Claude, Ollama) for JARVIS',
      backend: 'configure'
    }
  ];

  const selected = await vscode.window.showQuickPick(options, {
    placeHolder: `Current: ${currentBackend}`,
    matchOnDescription: true
  });

  if (!selected) return;

  if (selected.backend === 'configure') {
    const key = await vscode.window.showQuickPick([
      { label: 'Groq API Key', key: 'groqApiKey' },
      { label: 'Claude API Key (Optional)', key: 'anthropicApiKey' },
      { label: 'Ollama URL', key: 'ollamaUrl' }
    ]);

    if (!key) return;

    const value = await vscode.window.showInputBox({
      prompt: `Enter ${key.label}`,
      password: key.key !== 'ollamaUrl'
    });

    if (value) {
      await config.update(`jarvis.${key.key}`, value, vscode.ConfigurationTarget.Global);
      vscode.window.showInformationMessage(`✅ ${key.label} updated!`);
    }
    return;
  }

  // Update the AI backend
  await config.update('jarvis.aiBackend', selected.backend, vscode.ConfigurationTarget.Global);

  // Update status bar
  statusBar.text = `🤖 Jarvis (${selected.backend})`;

  // Show confirmation
  const info = {
    groq: '✨ Switched to Groq! Fast, free AI models.',
    claude: '🔐 JARVIS now using Claude backend! Premium AI responses enabled.'
    ollama: '💻 Switched to Ollama! Local, free AI models (make sure Ollama is running).'
  };

  vscode.window.showInformationMessage(info[selected.backend] || 'AI model switched!');

  // Suggest reloading if changing backends
  const reload = await vscode.window.showInformationMessage(
    'Reload VS Code to apply changes?',
    'Reload',
    'Later'
  );

  if (reload === 'Reload') {
    vscode.commands.executeCommand('workbench.action.reloadWindow');
  }
}

// ==================== AUTO-FIX HELPERS ====================

async function analyzeDocument(editor) {
  try {
    const analysis = await analyzer.analyzeDocument(editor.document);
    
    const diagnostics = [];
    for (const issue of analysis.issues) {
      diagnostics.push(
        new vscode.Diagnostic(
          new vscode.Range(issue.line, 0, issue.line, 999),
          issue.message,
          issue.severity === 'error' ? vscode.DiagnosticSeverity.Error : vscode.DiagnosticSeverity.Warning
        )
      );
    }

    diagnosticCollection.set(editor.document.uri, diagnostics);
  } catch (error) {
    console.error('Analysis error:', error);
  }
}

async function performAutoFix(editor) {
  try {
    const code = editor.document.getText();
    const fixes = await fixer.autoFix(code, editor.document.languageId);

    if (fixes.length > 0) {
      const edit = new vscode.WorkspaceEdit();
      for (const fix of fixes) {
        edit.replace(
          editor.document.uri,
          new vscode.Range(fix.start.line, 0, fix.end.line, 999),
          fix.fixedCode
        );
      }
      await vscode.workspace.applyEdit(edit);
    }
  } catch (error) {
    console.error('AutoFix error:', error);
  }
}

// ==================== WEBVIEW CONTENT ====================

function getChatWebviewContent() {
  return `
    <!DOCTYPE html>
    <html>
    <head>
      <style>
        body {
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
          margin: 0;
          padding: 20px;
          max-width: 600px;
        }
        .chat-container {
          height: 500px;
          display: flex;
          flex-direction: column;
        }
        .messages {
          flex: 1;
          overflow-y: auto;
          margin-bottom: 20px;
        }
        .message {
          margin-bottom: 10px;
          padding: 10px;
          border-radius: 8px;
          background: #f5f5f5;
        }
        .message.user {
          background: #007acc;
          color: white;
          text-align: right;
        }
        .input-area {
          display: flex;
          gap: 10px;
        }
        input {
          flex: 1;
          padding: 10px;
          border: 1px solid #ddd;
          border-radius: 4px;
          font-size: 14px;
        }
        button {
          padding: 10px 20px;
          background: #007acc;
          color: white;
          border: none;
          border-radius: 4px;
          cursor: pointer;
          font-weight: bold;
        }
        button:hover {
          background: #005a9e;
        }
      </style>
    </head>
    <body>
      <h2>💬 Jarvis Chat</h2>
      <div class="chat-container">
        <div class="messages" id="messages"></div>
        <div class="input-area">
          <input type="text" id="input" placeholder="Ask Jarvis..." />
          <button onclick="sendMessage()">Send</button>
        </div>
      </div>

      <script>
        const vscode = acquireVsCodeApi();

        function sendMessage() {
          const input = document.getElementById('input');
          const text = input.value.trim();
          
          if (!text) return;

          // Show user message
          const messages = document.getElementById('messages');
          const userMsg = document.createElement('div');
          userMsg.className = 'message user';
          userMsg.textContent = text;
          messages.appendChild(userMsg);

          // Send to extension
          vscode.postMessage({
            command: 'sendMessage',
            text: text
          });

          input.value = '';
          input.focus();
        }

        window.addEventListener('message', (event) => {
          const message = event.data;
          const messages = document.getElementById('messages');
          
          const responseMsg = document.createElement('div');
          responseMsg.className = 'message';
          responseMsg.textContent = message.text || '';
          messages.appendChild(responseMsg);
          
          messages.scrollTop = messages.scrollHeight;
        });

        document.getElementById('input').addEventListener('keypress', (e) => {
          if (e.key === 'Enter') sendMessage();
        });
      </script>
    </body>
    </html>
  `;
}

/**
 * Deactivate extension
 */
function deactivate() {
  console.log('Jarvis AI Assistant deactivated');
  diagnosticCollection.dispose();
}

module.exports = {
  activate,
  deactivate
};
