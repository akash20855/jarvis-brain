import * as vscode from 'vscode';
import axios from 'axios';

const BACKEND_URL = 'http://localhost:8001/api/jarvis';

export function activate(context: vscode.ExtensionContext) {
    console.log('🤖 Jarvis AI Assistant activated!');
    console.log('⚙️ Auto-Pilot: ENABLED (automatic mode)');
    
    const statusBar = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 100);
    statusBar.text = '🤖 Auto-Pilot ON';
    statusBar.command = 'jarvis.status';
    statusBar.show();
    
    // Register commands
    context.subscriptions.push(
        vscode.commands.registerCommand('jarvis.analyzeFile', analyzeFile),
        vscode.commands.registerCommand('jarvis.autoFix', autoFix),
        vscode.commands.registerCommand('jarvis.autoDebug', autoDebug),
        vscode.commands.registerCommand('jarvis.generateTests', generateTests),
        vscode.commands.registerCommand('jarvis.refactor', refactor),
        vscode.commands.registerCommand('jarvis.optimizePerformance', optimizePerformance),
        vscode.commands.registerCommand('jarvis.addComments', addComments),
        vscode.commands.registerCommand('jarvis.findSecurityIssues', findSecurityIssues),
        vscode.commands.registerCommand('jarvis.startAutoPilot', startAutoPilot),
        vscode.commands.registerCommand('jarvis.stopAutoPilot', stopAutoPilot),
        vscode.commands.registerCommand('jarvis.status', showStatus)
    );
    
    // Get configuration
    const config = vscode.workspace.getConfiguration('jarvis');
    const autoPilotEnabled = config.get('autoPilot', true);
    
    // Auto-Pilot mode - continuous analysis (default: ON)
    if (autoPilotEnabled) {
        console.log('✅ Starting Auto-Pilot continuous analysis...');
        startAutoPilot();
        vscode.window.showInformationMessage('✨ Jarvis Auto-Pilot activated - monitoring code automatically');
    }
    
    context.subscriptions.push(statusBar);
}

async function analyzeFile() {
    const editor = vscode.window.activeTextEditor;
    if (!editor) return;
    
    vscode.window.showInformationMessage('🔍 Analyzing code...');
    
    try {
        const response = await axios.post(`${BACKEND_URL}/command/execute`, {
            command: 'code.analyze',
            args: { code: editor.document.getText() }
        });
        
        if (response.data.success) {
            vscode.window.showInformationMessage('✅ Analysis complete!');
        }
    } catch (error) {
        vscode.window.showErrorMessage('❌ Analysis failed');
    }
}

async function autoFix() {
    const editor = vscode.window.activeTextEditor;
    if (!editor) return;
    
    vscode.window.showInformationMessage('🔧 Auto-fixing code...');
    
    try {
        const response = await axios.post(`${BACKEND_URL}/command/execute`, {
            command: 'code.format',
            args: { code: editor.document.getText() }
        });
        
        if (response.data.success && response.data.result) {
            await editor.edit(editBuilder => {
                const fullRange = new vscode.Range(
                    editor.document.positionAt(0),
                    editor.document.positionAt(editor.document.getText().length)
                );
                editBuilder.replace(fullRange, response.data.result);
            });
            vscode.window.showInformationMessage('✅ Code fixed!');
        }
    } catch (error) {
        vscode.window.showErrorMessage('❌ Fix failed');
    }
}

async function autoDebug() {
    vscode.window.showInformationMessage('🐛 Debugging code...');
    
    try {
        const editor = vscode.window.activeTextEditor;
        if (!editor) return;
        
        const response = await axios.post(`${BACKEND_URL}/command/execute`, {
            command: 'ai.debug',
            args: { code: editor.document.getText() }
        });
        
        if (response.data.success) {
            vscode.window.showInformationMessage('✅ Debug analysis complete!');
        }
    } catch (error) {
        vscode.window.showErrorMessage('❌ Debug failed');
    }
}

async function generateTests() {
    vscode.window.showInformationMessage('🧪 Generating tests...');
    
    try {
        const editor = vscode.window.activeTextEditor;
        if (!editor) return;
        
        const response = await axios.post(`${BACKEND_URL}/command/execute`, {
            command: 'ai.test',
            args: { code: editor.document.getText() }
        });
        
        if (response.data.success) {
            vscode.window.showInformationMessage('✅ Tests generated!');
        }
    } catch (error) {
        vscode.window.showErrorMessage('❌ Test generation failed');
    }
}

async function refactor() {
    vscode.window.showInformationMessage('♻️ Refactoring code...');
    
    try {
        const editor = vscode.window.activeTextEditor;
        if (!editor) return;
        
        const response = await axios.post(`${BACKEND_URL}/command/execute`, {
            command: 'code.refactor',
            args: { code: editor.document.getText() }
        });
        
        if (response.data.success) {
            vscode.window.showInformationMessage('✅ Refactoring complete!');
        }
    } catch (error) {
        vscode.window.showErrorMessage('❌ Refactoring failed');
    }
}

async function optimizePerformance() {
    vscode.window.showInformationMessage('⚡ Optimizing performance...');
    
    try {
        const editor = vscode.window.activeTextEditor;
        if (!editor) return;
        
        const response = await axios.post(`${BACKEND_URL}/command/execute`, {
            command: 'code.optimize',
            args: { code: editor.document.getText() }
        });
        
        if (response.data.success) {
            vscode.window.showInformationMessage('✅ Optimization suggestions provided!');
        }
    } catch (error) {
        vscode.window.showErrorMessage('❌ Optimization failed');
    }
}

async function addComments() {
    vscode.window.showInformationMessage('📝 Adding comments...');
    
    try {
        const editor = vscode.window.activeTextEditor;
        if (!editor) return;
        
        const response = await axios.post(`${BACKEND_URL}/command/execute`, {
            command: 'ai.comment',
            args: { code: editor.document.getText() }
        });
        
        if (response.data.success && response.data.result) {
            await editor.edit(editBuilder => {
                const fullRange = new vscode.Range(
                    editor.document.positionAt(0),
                    editor.document.positionAt(editor.document.getText().length)
                );
                editBuilder.replace(fullRange, response.data.result);
            });
            vscode.window.showInformationMessage('✅ Comments added!');
        }
    } catch (error) {
        vscode.window.showErrorMessage('❌ Comment addition failed');
    }
}

async function findSecurityIssues() {
    vscode.window.showInformationMessage('🔒 Scanning for security issues...');
    
    try {
        const editor = vscode.window.activeTextEditor;
        if (!editor) return;
        
        const response = await axios.post(`${BACKEND_URL}/command/execute`, {
            command: 'code.security',
            args: { code: editor.document.getText() }
        });
        
        if (response.data.success) {
            vscode.window.showInformationMessage('✅ Security scan complete!');
        }
    } catch (error) {
        vscode.window.showErrorMessage('❌ Security scan failed');
    }
}

function startAutoPilot() {
    vscode.window.showInformationMessage('✅ Auto-Pilot enabled');
    
    // Continuous analysis every 2 seconds
    setInterval(() => {
        const editor = vscode.window.activeTextEditor;
        if (editor) {
            analyzeFile();
        }
    }, 2000);
}

function stopAutoPilot() {
    vscode.window.showInformationMessage('⏹️ Auto-Pilot disabled');
}

function showStatus() {
    vscode.window.showInformationMessage('🤖 Jarvis AI Assistant - Status: ACTIVE (v2.0.0)');
}

export function deactivate() {}
