"""
Jarvis Brain - Unified Launcher
Choose your AI backend: Ollama, GitHub Copilot, or Local Patterns
"""

import subprocess
import sys
from pathlib import Path


class JarvisLauncher:
    """Unified launcher for all Jarvis Brain features"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
    
    def display_main_menu(self):
        """Display main menu"""
        print("""
╔════════════════════════════════════════════════════════════════════════╗
║                                                                        ║
║                    🤖 JARVIS BRAIN LAUNCHER                            ║
║                                                                        ║
║              Choose your AI backend & start analyzing                  ║
║                                                                        ║
╚════════════════════════════════════════════════════════════════════════╝
""")
        print("What would you like to do?\n")
        print("🚀 AUTO-EVOLUTION OPTIONS:")
        print("  1. Ollama (Recommended - Free, Local, Private)")
        print("  2. GitHub Copilot (Cloud AI via VS Code)")
        print("  3. Local Patterns (No AI, Works Now!)")
        print()
        print("💬 OTHER OPTIONS:")
        print("  4. Interactive Chatbot")
        print("  5. Run Tests")
        print("  6. Setup & Configuration")
        print()
        print("📊 UTILITIES:")
        print("  7. Show System Status")
        print("  8. View Improvement History")
        print()
        print("  0. Exit")
        print()
    
    def check_ollama_status(self) -> bool:
        """Check if Ollama is installed and running"""
        try:
            result = subprocess.run(
                ["curl", "-s", "http://localhost:11434/api/tags"],
                capture_output=True,
                timeout=2
            )
            return result.returncode == 0
        except:
            return False
    
    def check_github_copilot(self) -> bool:
        """Check if GitHub Copilot is available"""
        try:
            # Check if VS Code Copilot extension is installed
            vscode_extensions = Path.home() / ".vscode" / "extensions"
            if vscode_extensions.exists():
                copilot_installed = any(
                    "GitHub.Copilot" in ext.name 
                    for ext in vscode_extensions.iterdir()
                    if ext.is_dir()
                )
                return copilot_installed
        except:
            pass
        return False
    
    def show_ai_status(self):
        """Show status of AI backends"""
        print("\n📡 AI BACKEND STATUS:")
        print("─" * 60)
        
        ollama_running = self.check_ollama_status()
        copilot_available = self.check_github_copilot()
        
        status = "✅ Running" if ollama_running else "⏸️  Not running"
        print(f"  Ollama:          {status}")
        
        status = "✅ Available" if copilot_available else "❌ Not installed"
        print(f"  GitHub Copilot:  {status}")
        
        print(f"  Local Patterns:  ✅ Ready (Always)")
        print()
    
    def option_ollama(self):
        """Run with Ollama"""
        print("\n🌐 Ollama Setup")
        print("─" * 60)
        
        if not self.check_ollama_status():
            print("⚠️  Ollama is not running!")
            print("\n📝 Setup steps:")
            print("  1. Install: brew install ollama")
            print("  2. Start: ollama serve")
            print("  3. Download model: ollama pull mistral")
            print("\n💬 Once running, come back and select this option again.")
            input("\nPress Enter to continue...")
            return
        
        print("✅ Ollama is running!")
        print("\n🔍 Analyzing your code with Ollama...\n")
        
        subprocess.run([
            sys.executable,
            "-m",
            "core.auto_evolution",
            "--ai",
            "ollama"
        ], cwd=self.project_root)
    
    def option_copilot(self):
        """Run with GitHub Copilot"""
        print("\n🔐 GitHub Copilot Setup")
        print("─" * 60)
        
        if not self.check_github_copilot():
            print("⚠️  GitHub Copilot is not installed!")
            print("\n📝 Setup steps:")
            print("  1. Open VS Code Command Palette: Cmd+Shift+P")
            print("  2. Search: Extensions: Install Extensions")
            print("  3. Search: GitHub Copilot")
            print("  4. Click Install")
            print("  5. Sign in with your GitHub account")
            print("\n💬 Once installed, come back and select this option again.")
            input("\nPress Enter to continue...")
            return
        
        print("✅ GitHub Copilot is installed!")
        print("\n🔍 Analyzing your code with GitHub Copilot...\n")
        
        subprocess.run([
            sys.executable,
            "-m",
            "core.auto_evolution",
            "--ai",
            "copilot"
        ], cwd=self.project_root)
    
    def option_patterns(self):
        """Run with local patterns"""
        print("\n🎯 Local Pattern Analysis")
        print("─" * 60)
        print("Running local pattern-based analysis (no AI needed)...\n")
        
        subprocess.run([
            sys.executable,
            "-m",
            "core.auto_evolution",
            "--ai",
            "patterns"
        ], cwd=self.project_root)
    
    def option_chatbot(self):
        """Launch interactive chatbot"""
        print("\n💬 Starting Interactive Chatbot...\n")
        
        subprocess.run([
            sys.executable,
            "-m",
            "core.chatbot"
        ], cwd=self.project_root)
    
    def option_tests(self):
        """Run tests"""
        print("\n🧪 Running Tests...\n")
        
        subprocess.run([
            sys.executable,
            "-m",
            "pytest",
            "tests/",
            "-v"
        ], cwd=self.project_root)
    
    def option_setup(self):
        """Setup configuration"""
        print("\n⚙️  Setup & Configuration")
        print("─" * 60)
        print("\nAvailable setup options:")
        print("  1. Install Ollama")
        print("  2. Check GitHub Copilot")
        print("  3. View Configuration")
        print("  4. Reset to Defaults")
        print("  0. Back to Main Menu")
        
        choice = input("\nChoose option: ").strip()
        
        if choice == "1":
            print("\n📦 Installing Ollama...")
            print("Running: brew install ollama")
            subprocess.run(["brew", "install", "ollama"])
        elif choice == "2":
            print("\n🔍 GitHub Copilot Checker")
            if self.check_github_copilot():
                print("✅ GitHub Copilot is installed!")
            else:
                print("❌ GitHub Copilot not found")
                print("\nInstall via VS Code: Cmd+Shift+P → Extensions: Install Extensions → GitHub Copilot")
        elif choice == "3":
            self.show_config()
        elif choice == "4":
            print("\n🔄 Resetting to defaults...")
            self.reset_config()
    
    def show_config(self):
        """Show configuration"""
        config_file = self.project_root / ".evolution_config.json"
        
        print("\n📋 Configuration File")
        print("─" * 60)
        print(f"Location: {config_file}\n")
        
        if config_file.exists():
            import json
            with open(config_file) as f:
                config = json.load(f)
            print(json.dumps(config, indent=2))
        else:
            print("No configuration file found (using defaults)")
    
    def reset_config(self):
        """Reset configuration to defaults"""
        config_file = self.project_root / ".evolution_config.json"
        
        default_config = {
            "auto_evolution": {
                "enabled": True,
                "ai_backend": "patterns",  # patterns, ollama, copilot
                "scan_interval_seconds": 3600,
                "auto_apply_security_fixes": False,
                "auto_apply_performance": True,
                "notify_on_improvements": True
            }
        }
        
        import json
        with open(config_file, 'w') as f:
            json.dump(default_config, f, indent=2)
        
        print("✅ Configuration reset to defaults")
    
    def show_status(self):
        """Show system status"""
        print("\n📊 SYSTEM STATUS")
        print("─" * 60)
        
        # Project structure
        print("\n📁 Project Structure:")
        dirs = [
            "core/", "agents/", "modules/", "tests/", "data/"
        ]
        for dir_name in dirs:
            dir_path = self.project_root / dir_name
            if dir_path.exists():
                file_count = len(list(dir_path.glob("**/*.py")))
                print(f"  ✅ {dir_name:<15} ({file_count} Python files)")
            else:
                print(f"  ❌ {dir_name:<15} (missing)")
        
        # AI Status
        self.show_ai_status()
        
        # Evolution history
        history_file = self.project_root / ".evolution_log.json"
        if history_file.exists():
            import json
            try:
                with open(history_file) as f:
                    history = json.load(f)
                improvements = history.get("improvements", [])
                if improvements:
                    latest = improvements[-1]
                    print("📈 Latest Analysis:")
                    print(f"  • Last run: {latest.get('timestamp', 'Unknown')}")
                    print(f"  • Files scanned: {latest.get('scanned_files', 0)}")
                    print(f"  • Improvements found: {latest.get('improvements', 0)}")
            except:
                pass
    
    def show_history(self):
        """Show improvement history"""
        history_file = self.project_root / ".evolution_log.json"
        
        print("\n📊 IMPROVEMENT HISTORY")
        print("─" * 60)
        
        if not history_file.exists():
            print("\nNo history found yet. Run an analysis to get started!")
            return
        
        import json
        try:
            with open(history_file) as f:
                history = json.load(f)
            
            improvements = history.get("improvements", [])
            if not improvements:
                print("\nNo improvement records found.")
                return
            
            print(f"\n📈 Analysis History ({len(improvements)} runs):\n")
            
            for i, record in enumerate(improvements[-10:], 1):
                timestamp = record.get("timestamp", "Unknown")
                scanned = record.get("scanned_files", 0)
                found = record.get("improvements", 0)
                
                print(f"{i}. {timestamp}")
                print(f"   • Scanned: {scanned} files")
                print(f"   • Found: {found} improvements")
                
                by_type = record.get("by_type", {})
                if by_type:
                    for imp_type, count in by_type.items():
                        print(f"     - {imp_type}: {count}")
                print()
        
        except Exception as e:
            print(f"\n❌ Error reading history: {e}")
    
    def run(self):
        """Run the launcher"""
        while True:
            self.display_main_menu()
            choice = input("Choose option (0-8): ").strip()
            
            print()
            
            if choice == "0":
                print("👋 Goodbye!\n")
                break
            elif choice == "1":
                self.option_ollama()
            elif choice == "2":
                self.option_copilot()
            elif choice == "3":
                self.option_patterns()
            elif choice == "4":
                self.option_chatbot()
            elif choice == "5":
                self.option_tests()
            elif choice == "6":
                self.option_setup()
            elif choice == "7":
                self.show_status()
            elif choice == "8":
                self.show_history()
            else:
                print("❌ Invalid option. Please try again.\n")
                continue
            
            if choice in ["1", "2", "3", "4", "5"]:
                input("\n\nPress Enter to continue...")


def main():
    """Main entry point"""
    launcher = JarvisLauncher()
    launcher.run()


if __name__ == "__main__":
    main()
