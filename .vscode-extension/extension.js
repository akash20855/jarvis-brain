const vscode = require('vscode');
const WebSocket = require('ws');
const { spawn } = require('child_process');
const path = require('path');

let jarvisClient = null;
let statusBar = null;
let serverProcess = null;
let extensionContext = null;

class JarvisClient {
    constructor(host = 'localhost', port = 8765) {
        this.host = host;
        this.port = port;
        this.ws = null;
        this.connected = false;
        this.messageHandlers = {};
    }

    connect() {
        return new Promise((resolve, reject) => {
            try {
                const url = `ws://${this.host}:${this.port}`;
                this.ws = new WebSocket(url);

                this.ws.onopen = () => {
                    this.connected = true;
                    console.log('Connected to JARVIS');
                    updateStatusBar('JARVIS: Online');
                    resolve();
                };

                this.ws.onmessage = (event) => {
                    try {
                        const message = JSON.parse(event.data);
                        this.handleMessage(message);
                    } catch (e) {
                        console.error('Error parsing message:', e);
                    }
                };

                this.ws.onerror = (error) => {
                    console.error('WebSocket error:', error);
                    this.connected = false;
                    updateStatusBar('JARVIS: Offline');
                    reject(error);
                };

                this.ws.onclose = () => {
                    this.connected = false;
                    console.log('Disconnected from JARVIS');
                    updateStatusBar('JARVIS: Offline');
                };
            } catch (error) {
                reject(error);
            }
        });
    }

    disconnect() {
        if (this.ws) {
            this.ws.close();
            this.connected = false;
        }
    }

    sendCommand(command, args = [], kwargs = {}) {
        return new Promise((resolve, reject) => {
            if (!this.connected) {
                reject(new Error('Not connected to JARVIS'));
                return;
            }

            const messageId = Date.now();
            this.messageHandlers[messageId] = { resolve, reject };

            try {
                const message = JSON.stringify({
                    id: messageId,
                    command,
                    args,
                    kwargs
                });
                this.ws.send(message);

                // Timeout after 30 seconds
                setTimeout(() => {
                    if (this.messageHandlers[messageId]) {
                        delete this.messageHandlers[messageId];
                        reject(new Error(`Command timeout: ${command}`));
                    }
                }, 30000);
            } catch (error) {
                reject(error);
            }
        });
    }

    handleMessage(message) {
        if (message.id && this.messageHandlers[message.id]) {
            const { resolve, reject } = this.messageHandlers[message.id];
            delete this.messageHandlers[message.id];

            if (message.success) {
                resolve(message.result);
            } else {
                reject(new Error(message.error || 'Unknown error'));
            }
        }
    }
}

async function updateStatusBar(text) {
    if (!statusBar) {
        statusBar = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 100);
        statusBar.command = 'jarvis.status';
    }
    statusBar.text = text;
    statusBar.show();
}

async function startJarvisServer() {
    return new Promise((resolve, reject) => {
        try {
            const workspaceFolder = vscode.workspace.workspaceFolders?.[0]?.uri?.fsPath;
            if (!workspaceFolder) {
                reject(new Error('No workspace folder open'));
                return;
            }

            console.log('Starting JARVIS server...');
            serverProcess = spawn('python3', ['core/vscode_server.py'], {
                cwd: workspaceFolder,
                detached: false,
                stdio: ['ignore', 'pipe', 'pipe']
            });

            serverProcess.stdout.on('data', (data) => {
                console.log(`JARVIS Server: ${data}`);
            });

            serverProcess.stderr.on('data', (data) => {
                console.error(`JARVIS Server Error: ${data}`);
            });

            // Wait a moment for server to start
            setTimeout(() => resolve(), 2000);
        } catch (error) {
            reject(error);
        }
    });
}

function stopJarvisServer() {
    if (serverProcess) {
        serverProcess.kill();
        serverProcess = null;
    }
}

async function initializeJarvis() {
    try {
        const config = vscode.workspace.getConfiguration('jarvis');
        const host = config.get('serverHost', 'localhost');
        const port = config.get('serverPort', 8765);

        jarvisClient = new JarvisClient(host, port);

        try {
            await jarvisClient.connect();
            vscode.window.showInformationMessage('✅ Connected to JARVIS Pro');
        } catch (error) {
            console.log('Connection failed, starting server...');
            await startJarvisServer();
            await new Promise(resolve => setTimeout(resolve, 2000));
            await jarvisClient.connect();
            vscode.window.showInformationMessage('✅ JARVIS Pro server started');
        }
    } catch (error) {
        console.error('Failed to initialize JARVIS:', error);
        vscode.window.showErrorMessage(`Failed to initialize JARVIS: ${error.message}`);
    }
}

async function getSelectedCode() {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
        throw new Error('No active editor');
    }

    let code;
    if (editor.selection.isEmpty) {
        code = editor.document.getText();
    } else {
        code = editor.document.getText(editor.selection);
    }

    const language = editor.document.languageId;
    return { code, language };
}

async function showProgressDialog(title, fn) {
    return vscode.window.withProgress(
        {
            location: vscode.ProgressLocation.Notification,
            title,
            cancellable: false
        },
        async (progress) => {
            return fn(progress);
        }
    );
}

// Command: Generate Code
async function cmdGenerateCode() {
    try {
        const input = await vscode.window.showInputBox({
            prompt: 'Describe the code you want to generate',
            placeHolder: 'e.g., REST API endpoint in Python'
        });

        if (!input) return;

        const language = await vscode.window.showQuickPick(
            ['python', 'javascript', 'typescript', 'java', 'cpp', 'csharp', 'go', 'rust'],
            { placeHolder: 'Select language' }
        ) || 'python';

        const result = await showProgressDialog(
            'Generating code with JARVIS...',
            async () => {
                return jarvisClient.sendCommand('jarvis.generateCode', [input, language]);
            }
        );

        const editor = vscode.window.activeTextEditor;
        if (editor) {
            editor.edit(editBuilder => {
                editBuilder.insert(editor.selection.active, result.code);
            });
        }

        vscode.window.showInformationMessage('✅ Code generated and inserted');
    } catch (error) {
        vscode.window.showErrorMessage(`Error: ${error.message}`);
    }
}

// Command: Analyze Code
async function cmdAnalyzeCode() {
    try {
        const { code, language } = await getSelectedCode();

        const result = await showProgressDialog(
            'Analyzing code with JARVIS...',
            async () => {
                return jarvisClient.sendCommand('jarvis.analyzeCode', [code, language]);
            }
        );

        const message = `Analysis Results:\n\n${result.analysis}`;
        vscode.window.showInformationMessage(message);
    } catch (error) {
        vscode.window.showErrorMessage(`Error: ${error.message}`);
    }
}

// Command: Debug Project
async function cmdDebugProject() {
    try {
        const result = await showProgressDialog(
            'Debugging project with JARVIS...',
            async () => {
                return jarvisClient.sendCommand('jarvis.debugProject', []);
            }
        );

        const message = `🐛 Issues Found: ${result.issues_found}\n\n${JSON.stringify(result.issues, null, 2)}`;
        vscode.window.showInformationMessage(message);
    } catch (error) {
        vscode.window.showErrorMessage(`Error: ${error.message}`);
    }
}

// Command: Improve Code
async function cmdImproveCode() {
    try {
        const fileCount = await vscode.window.showInputBox({
            prompt: 'Number of files to improve',
            placeHolder: '5',
            validate: (value) => /^\d+$/.test(value) ? null : 'Must be a number'
        });

        if (!fileCount) return;

        const result = await showProgressDialog(
            `Improving ${fileCount} files with JARVIS...`,
            async () => {
                return jarvisClient.sendCommand('jarvis.improveCode', [parseInt(fileCount)]);
            }
        );

        vscode.window.showInformationMessage(
            `✅ Improved ${result.count} files: ${result.files_improved.join(', ')}`
        );
    } catch (error) {
        vscode.window.showErrorMessage(`Error: ${error.message}`);
    }
}

// Command: Generate Tests
async function cmdGenerateTests() {
    try {
        const { code, language } = await getSelectedCode();

        const result = await showProgressDialog(
            'Generating tests with JARVIS...',
            async () => {
                return jarvisClient.sendCommand('jarvis.generateTests', [code, language]);
            }
        );

        const doc = await vscode.workspace.openTextDocument({
            content: result.tests,
            language: language === 'python' ? 'python' : 'javascript'
        });

        await vscode.window.showTextDocument(doc);
    } catch (error) {
        vscode.window.showErrorMessage(`Error: ${error.message}`);
    }
}

// Command: Refactor Code
async function cmdRefactorCode() {
    try {
        const { code, language } = await getSelectedCode();

        const result = await showProgressDialog(
            'Refactoring code with JARVIS...',
            async () => {
                return jarvisClient.sendCommand('jarvis.refactorCode', [code, language]);
            }
        );

        const editor = vscode.window.activeTextEditor;
        if (editor && !editor.selection.isEmpty) {
            editor.edit(editBuilder => {
                editBuilder.replace(editor.selection, result.refactored);
            });
        }

        vscode.window.showInformationMessage('✅ Code refactored');
    } catch (error) {
        vscode.window.showErrorMessage(`Error: ${error.message}`);
    }
}

// Command: Explain Code
async function cmdExplainCode() {
    try {
        const { code, language } = await getSelectedCode();

        const result = await showProgressDialog(
            'Getting explanation from JARVIS...',
            async () => {
                return jarvisClient.sendCommand('jarvis.explainCode', [code, language]);
            }
        );

        const panel = vscode.window.createWebviewPanel(
            'jarvisExplanation',
            'JARVIS Code Explanation',
            vscode.ViewColumn.Beside,
            {}
        );

        panel.webview.html = `
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; line-height: 1.6; }
        h1 { color: #333; }
        p { color: #666; white-space: pre-wrap; }
    </style>
</head>
<body>
    <h1>Code Explanation</h1>
    <p>${result.explanation.replace(/</g, '&lt;').replace(/>/g, '&gt;')}</p>
</body>
</html>
        `;
    } catch (error) {
        vscode.window.showErrorMessage(`Error: ${error.message}`);
    }
}

// Command: Build Project
async function cmdBuildProject() {
    try {
        const result = await showProgressDialog(
            'Building project with JARVIS...',
            async () => {
                return jarvisClient.sendCommand('jarvis.buildProject', []);
            }
        );

        vscode.window.showInformationMessage(
            `✅ Build successful\nTime: ${result.total_time.toFixed(2)}s\nPhases: ${result.phases_completed}`
        );
    } catch (error) {
        vscode.window.showErrorMessage(`Error: ${error.message}`);
    }
}

// Command: Status
async function cmdStatus() {
    try {
        const status = await jarvisClient.sendCommand('jarvis.status', []);

        const message = `
JARVIS Pro Status
═══════════════════
Status: ${status.status.toUpperCase()}
Version: ${status.version}
Connected Clients: ${status.connected_clients}
Available Commands: ${status.available_commands}

Components:
${Object.entries(status.components).map(([k, v]) => `  • ${k}: ${v}`).join('\n')}
        `;

        vscode.window.showInformationMessage(message);
    } catch (error) {
        vscode.window.showErrorMessage(`Error: ${error.message}`);
    }
}

// Command: Start Server
async function cmdStartServer() {
    try {
        if (jarvisClient?.connected) {
            vscode.window.showInformationMessage('JARVIS server is already running');
            return;
        }

        await showProgressDialog(
            'Starting JARVIS server...',
            async () => {
                await startJarvisServer();
                await new Promise(resolve => setTimeout(resolve, 2000));
                await jarvisClient.connect();
            }
        );

        vscode.window.showInformationMessage('✅ JARVIS server started');
    } catch (error) {
        vscode.window.showErrorMessage(`Error: ${error.message}`);
    }
}

// Command: Stop Server
async function cmdStopServer() {
    try {
        jarvisClient.disconnect();
        stopJarvisServer();
        vscode.window.showInformationMessage('✅ JARVIS server stopped');
    } catch (error) {
        vscode.window.showErrorMessage(`Error: ${error.message}`);
    }
}

function activate(context) {
    extensionContext = context;
    console.log('🚀 JARVIS Pro extension activated');

    // Initialize JARVIS on startup
    initializeJarvis().catch(console.error);

    // Register commands
    const commands = [
        ['jarvis.generateCode', cmdGenerateCode],
        ['jarvis.analyzeCode', cmdAnalyzeCode],
        ['jarvis.debugProject', cmdDebugProject],
        ['jarvis.improveCode', cmdImproveCode],
        ['jarvis.generateTests', cmdGenerateTests],
        ['jarvis.refactorCode', cmdRefactorCode],
        ['jarvis.explainCode', cmdExplainCode],
        ['jarvis.buildProject', cmdBuildProject],
        ['jarvis.status', cmdStatus],
        ['jarvis.startServer', cmdStartServer],
        ['jarvis.stopServer', cmdStopServer]
    ];

    commands.forEach(([command, handler]) => {
        const disposable = vscode.commands.registerCommand(command, handler);
        context.subscriptions.push(disposable);
    });

    updateStatusBar('JARVIS: Initializing...');
}

function deactivate() {
    console.log('🛑 JARVIS Pro extension deactivated');
    if (jarvisClient) {
        jarvisClient.disconnect();
    }
    stopJarvisServer();
}

module.exports = {
    activate,
    deactivate
};
