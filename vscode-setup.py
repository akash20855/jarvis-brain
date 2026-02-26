#!/usr/bin/env python3
"""
JARVIS VS Code Integration Setup Helper
Helps setup and verify VS Code integration
"""

import subprocess
import sys
import json
from pathlib import Path
from datetime import datetime

class VSCodeSetupHelper:
    def __init__(self):
        self.workspace = Path("/Volumes/Akash SSD/repos/jarvis-brain")
        self.ext_dir = self.workspace / ".vscode-extension"
    
    def check_setup(self):
        """Check if VS Code setup is complete"""
        print("\n" + "="*70)
        print("🔍 JARVIS VS Code Integration - Setup Check")
        print("="*70 + "\n")
        
        checks = {
            "Python Environment": self.check_python(),
            "WebSocket Server": self.check_websocket_server(),
            "VS Code Extension Files": self.check_extension_files(),
            "Configuration": self.check_configuration(),
            "Dependencies": self.check_dependencies(),
        }
        
        print("\n📊 SETUP STATUS:")
        print("-" * 70)
        
        all_good = True
        for check, status in checks.items():
            if isinstance(status, tuple):
                result, msg = status
                icon = "✅" if result else "❌"
                print(f"{icon} {check:30} {msg}")
                all_good = all_good and result
            else:
                icon = "✅" if status else "❌"
                print(f"{icon} {check}")
                all_good = all_good and status
        
        print("-" * 70)
        
        if all_good:
            print("\n✅ ALL CHECKS PASSED - VS Code integration is ready!\n")
            self.show_quick_start()
        else:
            print("\n❌ SOME CHECKS FAILED - Run setup instructions above\n")
        
        return all_good
    
    def check_python(self):
        """Check Python installation"""
        try:
            result = subprocess.run(
                ["python3", "--version"],
                capture_output=True,
                text=True
            )
            version = result.stdout.strip()
            return (True, f"({version})")
        except:
            return (False, "Python 3 not found")
    
    def check_websocket_server(self):
        """Check websocket-server installation"""
        try:
            import websocket_server
            return (True, "installed")
        except ImportError:
            return (False, "install with: pip install websocket-server")
    
    def check_extension_files(self):
        """Check if extension files exist"""
        files = [
            self.ext_dir / "package.json",
            self.ext_dir / "extension.js",
            self.ext_dir / "README.md"
        ]
        
        missing = [f.name for f in files if not f.exists()]
        
        if missing:
            return (False, f"missing: {', '.join(missing)}")
        
        return (True, f"all {len(files)} files present")
    
    def check_configuration(self):
        """Check VS Code configuration"""
        vscode_dir = self.workspace / ".vscode"
        
        files_exist = {
            "tasks.json": (vscode_dir / "tasks.json").exists(),
            "launch.json": (vscode_dir / "launch.json").exists(),
            "settings.json": (vscode_dir / "settings.json").exists(),
        }
        
        existing = sum(1 for v in files_exist.values() if v)
        total = len(files_exist)
        
        return (existing > 0, f"{existing}/{total} files configured")
    
    def check_dependencies(self):
        """Check all dependencies"""
        deps = {
            "anthropic": False,
            "websocket_server": False,
            "requests": False,
        }
        
        for dep in deps:
            try:
                __import__(dep.replace("-", "_"))
                deps[dep] = True
            except ImportError:
                pass
        
        installed = sum(1 for v in deps.values() if v)
        total = len(deps)
        
        if installed == total:
            return (True, f"all {total} packages installed")
        else:
            missing = [k for k, v in deps.items() if not v]
            return (False, f"missing: {', '.join(missing)}")
    
    def show_quick_start(self):
        print("🚀 QUICK START:")
        print("-" * 70)
        print("\n1️⃣  Start JARVIS Server:")
        print("   python3 core/vscode_server.py &")
        print("\n2️⃣  Open VS Code:")
        print("   code .")
        print("\n3️⃣  Use JARVIS:")
        print("   • Press Cmd+Shift+P")
        print("   • Type 'JARVIS'")
        print("   • Select any command")
        print("\n4️⃣  Available Commands:")
        print("   • JARVIS: Generate Code")
        print("   • JARVIS: Analyze Code")
        print("   • JARVIS: Refactor Code")
        print("   • JARVIS: Generate Tests")
        print("   • JARVIS: Improve Code")
        print("   • JARVIS: Build with Debug")
        print("   • JARVIS: Debug Project")
        print("   • JARVIS: Explain Code")
        print("   • JARVIS: Show Status")
    
    def install_missing_dependencies(self):
        """Install missing dependencies"""
        print("\n" + "="*70)
        print("📦 Installing Missing Dependencies")
        print("="*70 + "\n")
        
        packages = [
            "websocket-server",
            "anthropic",
            "requests"
        ]
        
        for package in packages:
            try:
                __import__(package.replace("-", "_"))
                print(f"✅ {package} already installed")
            except ImportError:
                print(f"📦 Installing {package}...")
                subprocess.run(
                    [sys.executable, "-m", "pip", "install", "-q", package],
                    check=True
                )
                print(f"✅ {package} installed")
        
        print("\n✅ All dependencies installed!")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="JARVIS VS Code Integration Setup",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 vscode-setup.py check              # Check setup status
  python3 vscode-setup.py install            # Install missing dependencies
  python3 vscode-setup.py full               # Full setup and check
        """
    )
    
    parser.add_argument(
        "command",
        nargs="?",
        choices=["check", "install", "full"],
        default="check",
        help="Command to execute"
    )
    
    args = parser.parse_args()
    helper = VSCodeSetupHelper()
    
    if args.command == "check":
        helper.check_setup()
    elif args.command == "install":
        helper.install_missing_dependencies()
        print("\nRunning full check...")
        helper.check_setup()
    elif args.command == "full":
        helper.install_missing_dependencies()
        print("\nRunning full check...")
        helper.check_setup()


if __name__ == "__main__":
    main()
