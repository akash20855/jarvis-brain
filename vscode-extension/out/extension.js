"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.activate = activate;
exports.deactivate = deactivate;
const vscode = __importStar(require("vscode"));
const axios_1 = __importDefault(require("axios"));
const BACKEND_URL = 'http://localhost:8001/api/jarvis';
function activate(context) {
    console.log('🤖 Jarvis AI Assistant activated!');
    console.log('⚙️ Auto-Pilot: ENABLED (automatic mode)');
    const statusBar = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 100);
    statusBar.text = '🤖 Auto-Pilot ON';
    statusBar.command = 'jarvis.status';
    statusBar.show();
    // Register commands
    context.subscriptions.push(vscode.commands.registerCommand('jarvis.analyzeFile', analyzeFile), vscode.commands.registerCommand('jarvis.autoFix', autoFix), vscode.commands.registerCommand('jarvis.autoDebug', autoDebug), vscode.commands.registerCommand('jarvis.generateTests', generateTests), vscode.commands.registerCommand('jarvis.refactor', refactor), vscode.commands.registerCommand('jarvis.optimizePerformance', optimizePerformance), vscode.commands.registerCommand('jarvis.addComments', addComments), vscode.commands.registerCommand('jarvis.findSecurityIssues', findSecurityIssues), vscode.commands.registerCommand('jarvis.startAutoPilot', startAutoPilot), vscode.commands.registerCommand('jarvis.stopAutoPilot', stopAutoPilot), vscode.commands.registerCommand('jarvis.status', showStatus));
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
    if (!editor)
        return;
    vscode.window.showInformationMessage('🔍 Analyzing code...');
    try {
        const response = await axios_1.default.post(`${BACKEND_URL}/command/execute`, {
            command: 'code.analyze',
            args: { code: editor.document.getText() }
        });
        if (response.data.success) {
            vscode.window.showInformationMessage('✅ Analysis complete!');
        }
    }
    catch (error) {
        vscode.window.showErrorMessage('❌ Analysis failed');
    }
}
async function autoFix() {
    const editor = vscode.window.activeTextEditor;
    if (!editor)
        return;
    vscode.window.showInformationMessage('🔧 Auto-fixing code...');
    try {
        const response = await axios_1.default.post(`${BACKEND_URL}/command/execute`, {
            command: 'code.format',
            args: { code: editor.document.getText() }
        });
        if (response.data.success && response.data.result) {
            await editor.edit(editBuilder => {
                const fullRange = new vscode.Range(editor.document.positionAt(0), editor.document.positionAt(editor.document.getText().length));
                editBuilder.replace(fullRange, response.data.result);
            });
            vscode.window.showInformationMessage('✅ Code fixed!');
        }
    }
    catch (error) {
        vscode.window.showErrorMessage('❌ Fix failed');
    }
}
async function autoDebug() {
    vscode.window.showInformationMessage('🐛 Debugging code...');
    try {
        const editor = vscode.window.activeTextEditor;
        if (!editor)
            return;
        const response = await axios_1.default.post(`${BACKEND_URL}/command/execute`, {
            command: 'ai.debug',
            args: { code: editor.document.getText() }
        });
        if (response.data.success) {
            vscode.window.showInformationMessage('✅ Debug analysis complete!');
        }
    }
    catch (error) {
        vscode.window.showErrorMessage('❌ Debug failed');
    }
}
async function generateTests() {
    vscode.window.showInformationMessage('🧪 Generating tests...');
    try {
        const editor = vscode.window.activeTextEditor;
        if (!editor)
            return;
        const response = await axios_1.default.post(`${BACKEND_URL}/command/execute`, {
            command: 'ai.test',
            args: { code: editor.document.getText() }
        });
        if (response.data.success) {
            vscode.window.showInformationMessage('✅ Tests generated!');
        }
    }
    catch (error) {
        vscode.window.showErrorMessage('❌ Test generation failed');
    }
}
async function refactor() {
    vscode.window.showInformationMessage('♻️ Refactoring code...');
    try {
        const editor = vscode.window.activeTextEditor;
        if (!editor)
            return;
        const response = await axios_1.default.post(`${BACKEND_URL}/command/execute`, {
            command: 'code.refactor',
            args: { code: editor.document.getText() }
        });
        if (response.data.success) {
            vscode.window.showInformationMessage('✅ Refactoring complete!');
        }
    }
    catch (error) {
        vscode.window.showErrorMessage('❌ Refactoring failed');
    }
}
async function optimizePerformance() {
    vscode.window.showInformationMessage('⚡ Optimizing performance...');
    try {
        const editor = vscode.window.activeTextEditor;
        if (!editor)
            return;
        const response = await axios_1.default.post(`${BACKEND_URL}/command/execute`, {
            command: 'code.optimize',
            args: { code: editor.document.getText() }
        });
        if (response.data.success) {
            vscode.window.showInformationMessage('✅ Optimization suggestions provided!');
        }
    }
    catch (error) {
        vscode.window.showErrorMessage('❌ Optimization failed');
    }
}
async function addComments() {
    vscode.window.showInformationMessage('📝 Adding comments...');
    try {
        const editor = vscode.window.activeTextEditor;
        if (!editor)
            return;
        const response = await axios_1.default.post(`${BACKEND_URL}/command/execute`, {
            command: 'ai.comment',
            args: { code: editor.document.getText() }
        });
        if (response.data.success && response.data.result) {
            await editor.edit(editBuilder => {
                const fullRange = new vscode.Range(editor.document.positionAt(0), editor.document.positionAt(editor.document.getText().length));
                editBuilder.replace(fullRange, response.data.result);
            });
            vscode.window.showInformationMessage('✅ Comments added!');
        }
    }
    catch (error) {
        vscode.window.showErrorMessage('❌ Comment addition failed');
    }
}
async function findSecurityIssues() {
    vscode.window.showInformationMessage('🔒 Scanning for security issues...');
    try {
        const editor = vscode.window.activeTextEditor;
        if (!editor)
            return;
        const response = await axios_1.default.post(`${BACKEND_URL}/command/execute`, {
            command: 'code.security',
            args: { code: editor.document.getText() }
        });
        if (response.data.success) {
            vscode.window.showInformationMessage('✅ Security scan complete!');
        }
    }
    catch (error) {
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
function deactivate() { }
