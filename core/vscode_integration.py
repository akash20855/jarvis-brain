"""
VS Code Integration for Auto-Evolution
Enables AI-powered code improvement directly in the editor
"""

import json
from pathlib import Path
from core.auto_evolution import AutoEvolutionEngine


class VSCodeIntegration:
    """VS Code integration for auto-evolution"""
    
    def __init__(self, workspace_root: str = "."):
        self.workspace_root = Path(workspace_root)
        self.engine = AutoEvolutionEngine(workspace_root)
        self.config_file = self.workspace_root / ".vscode" / "evolution-settings.json"
    
    def create_settings(self):
        """Create VS Code settings for auto-evolution"""
        vs_code_dir = self.workspace_root / ".vscode"
        vs_code_dir.mkdir(exist_ok=True)
        
        settings = {
            "python.analysis.extraPaths": ["core", "agents", "modules"],
            "python.linting.enabled": True,
            "python.linting.pylintEnabled": True,
            "[python]": {
                "editor.defaultFormatter": "ms-python.python",
                "editor.formatOnSave": True,
                "editor.codeActionsOnSave": {
                    "source.organizeImports": True
                }
            },
            "jarvis.autoEvolution": {
                "enabled": True,
                "scanOnSave": True,
                "suggestImprovements": True,
                "autoApplyMinor": False
            }
        }
        
        settings_file = vs_code_dir / "settings.json"
        with open(settings_file, 'w') as f:
            json.dump(settings, f, indent=2)
        
        print(f"✅ VS Code settings created: {settings_file}")
    
    def create_tasks(self):
        """Create VS Code tasks for auto-evolution"""
        vs_code_dir = self.workspace_root / ".vscode"
        vs_code_dir.mkdir(exist_ok=True)
        
        tasks = {
            "version": "2.0.0",
            "tasks": [
                {
                    "label": "Jarvis: Auto-Evolve Code",
                    "type": "shell",
                    "command": "python3",
                    "args": [
                        "-m", "core.auto_evolution"
                    ],
                    "group": {
                        "kind": "build",
                        "isDefault": False
                    },
                    "presentation": {
                        "reveal": "always",
                        "panel": "new"
                    }
                },
                {
                    "label": "Jarvis: Scan for Improvements",
                    "type": "shell",
                    "command": "python3",
                    "args": [
                        "-c",
                        "from core.auto_evolution import AutoEvolutionEngine; e = AutoEvolutionEngine(); print(e.scan_project())"
                    ]
                },
                {
                    "label": "Jarvis: Run Tests + Evolve",
                    "type": "shell",
                    "command": "bash",
                    "args": [
                        "-c",
                        "python3 -m pytest tests/ && python3 -m core.auto_evolution"
                    ]
                }
            ]
        }
        
        tasks_file = vs_code_dir / "tasks.json"
        with open(tasks_file, 'w') as f:
            json.dump(tasks, f, indent=2)
        
        print(f"✅ VS Code tasks created: {tasks_file}")
    
    def create_launch_config(self):
        """Create VS Code debug configuration"""
        vs_code_dir = self.workspace_root / ".vscode"
        vs_code_dir.mkdir(exist_ok=True)
        
        launch = {
            "version": "0.2.0",
            "configurations": [
                {
                    "name": "Python: Jarvis Main",
                    "type": "python",
                    "request": "launch",
                    "program": "${workspaceFolder}/core/main.py",
                    "console": "integratedTerminal"
                },
                {
                    "name": "Python: Auto-Evolution",
                    "type": "python",
                    "request": "launch",
                    "program": "${workspaceFolder}/core/auto_evolution.py",
                    "console": "integratedTerminal"
                },
                {
                    "name": "Python: Tests",
                    "type": "python",
                    "request": "launch",
                    "module": "pytest",
                    "args": ["tests/", "-v"],
                    "console": "integratedTerminal"
                }
            ]
        }
        
        launch_file = vs_code_dir / "launch.json"
        with open(launch_file, 'w') as f:
            json.dump(launch, f, indent=2)
        
        print(f"✅ VS Code launch config created: {launch_file}")
    
    def create_extensions_file(self):
        """Create recommended VS Code extensions list"""
        vs_code_dir = self.workspace_root / ".vscode"
        vs_code_dir.mkdir(exist_ok=True)
        
        extensions = {
            "recommendations": [
                "ms-python.python",
                "ms-python.vscode-pylance",
                "ms-python.debugpy",
                "GitHub.Copilot",
                "charliermarsh.ruff",
                "ms-vscode.makefile-tools",
                "ms-vscode-remote.remote-docker"
            ]
        }
        
        ext_file = vs_code_dir / "extensions.json"
        with open(ext_file, 'w') as f:
            json.dump(extensions, f, indent=2)
        
        print(f"✅ VS Code extensions file created: {ext_file}")
    
    def setup_all(self):
        """Setup complete VS Code integration"""
        print("""
╔════════════════════════════════════════════════════════════════════════╗
║       🔧 SETTING UP VS CODE INTEGRATION FOR AUTO-EVOLUTION             ║
╚════════════════════════════════════════════════════════════════════════╝
""")
        self.create_settings()
        self.create_tasks()
        self.create_launch_config()
        self.create_extensions_file()
        
        print("""
✅ VS Code Setup Complete!

Available in VS Code:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Commands (Cmd+Shift+P):
  • Tasks: Run Task → Jarvis: Auto-Evolve Code
  • Tasks: Run Task → Jarvis: Scan for Improvements
  • Tasks: Run Task → Jarvis: Run Tests + Evolve

Debug Configurations (F5):
  • Python: Jarvis Main
  • Python: Auto-Evolution
  • Python: Tests

To use:
  1. Open folder in VS Code
  2. Install recommended extensions
  3. Run tasks with Cmd+Shift+P → Tasks: Run Task
""")


def setup_vscode():
    """Setup VS Code integration"""
    integration = VSCodeIntegration("/Volumes/Akash SSD/repos/jarvis-brain")
    integration.setup_all()


if __name__ == "__main__":
    setup_vscode()
