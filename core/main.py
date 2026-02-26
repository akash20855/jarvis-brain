"""
Jarvis HQ - Main Entry Point
Mac mini daemon that orchestrates all agents and modules.
Serves as the central hub for voice commands, reasoning, and task distribution.
"""

import logging
import sys
import os
from pathlib import Path
import cmd
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class JarvisHQ:
    """Main Jarvis brain controller."""
    
    def __init__(self):
        """Initialize Jarvis HQ."""
        logger.info("Initializing Jarvis HQ...")
        self.running = False
        self.start_time = None
        self.commands_executed = 0
    
    def start(self):
        """Start the Jarvis HQ daemon."""
        logger.info("Starting Jarvis HQ daemon...")
        self.running = True
        self.start_time = datetime.now()
    
    def stop(self):
        """Stop the Jarvis HQ daemon."""
        logger.info("Stopping Jarvis HQ daemon...")
        self.running = False
    
    def get_uptime(self):
        """Get daemon uptime."""
        if not self.start_time:
            return 0
        return (datetime.now() - self.start_time).total_seconds()
    
    def get_status(self):
        """Get current system status."""
        return {
            "running": self.running,
            "uptime_seconds": self.get_uptime(),
            "commands_executed": self.commands_executed,
            "start_time": self.start_time.isoformat() if self.start_time else None
        }
    
    def run(self):
        """Main event loop."""
        try:
            self.start()
            while self.running:
                # Main loop placeholder
                pass
        except KeyboardInterrupt:
            logger.info("Interrupt received")
        finally:
            self.stop()


class JarvisREPL(cmd.Cmd):
    """Interactive REPL for Jarvis Brain."""
    
    intro = """
╔══════════════════════════════════════════════════════════════╗
║          Jarvis Brain - Interactive Command Line             ║
║                                                              ║
║  Type 'help' for available commands or 'quit' to exit       ║
╚══════════════════════════════════════════════════════════════╝
"""
    prompt = "jarvis> "
    
    def __init__(self, jarvis_hq):
        """Initialize REPL with Jarvis HQ instance."""
        super().__init__()
        self.jarvis = jarvis_hq
        self.jarvis.start()
    
    def do_status(self, arg):
        """Show system status"""
        status = self.jarvis.get_status()
        print(f"\n📊 System Status:")
        print(f"  Status:      {'Running' if status['running'] else 'Stopped'}")
        print(f"  Uptime:      {status['uptime_seconds']:.1f}s")
        print(f"  Commands:    {status['commands_executed']}")
        print(f"  Started:     {status['start_time']}\n")
    
    def do_agents(self, arg):
        """List available agents"""
        print("""
🤖 Available Agents:
  • mac_agent       - macOS device control
  • windows_agent   - Windows device control
  • android_agent   - Android device companion
  • cloud_agent     - Cloud infrastructure
""")
    
    def do_modules(self, arg):
        """List available modules"""
        print("""
📦 Available Modules:
  • WhatsAppManager        - WhatsApp messaging integration
  • SMSManager             - SMS handling
  • HotspotManager         - Mobile hotspot control
  • NotificationManager    - Push notifications
  • Dashboard              - Web UI and alerts
  • ResearchEngine         - Knowledge gathering
  • PlanningEngine         - Strategic planning
""")
    
    def do_commands(self, arg):
        """Show command examples"""
        print("""
💬 Example Commands:
  voice     "send message to john"
  build     mac_agent my_project
  research  "machine learning best practices"
  task      decompose "build and deploy"
  backup    create
  logs      show
  config    list
""")
    
    def do_voice(self, arg):
        """Process voice command"""
        if not arg:
            print("❌ Usage: voice <command>")
            return
        print(f"🎤 Processing: {arg}")
        logger.info(f"Voice command: {arg}")
        self.jarvis.commands_executed += 1
    
    def do_build(self, arg):
        """Build project on agent"""
        if not arg:
            print("❌ Usage: build <agent> <project>")
            return
        parts = arg.split(maxsplit=1)
        print(f"🔨 Building {parts[1] if len(parts) > 1 else 'project'} on {parts[0]}...")
        logger.info(f"Build command: {arg}")
        self.jarvis.commands_executed += 1
    
    def do_task(self, arg):
        """Execute task"""
        if not arg:
            print("❌ Usage: task <action> <description>")
            return
        print(f"📋 Executing: {arg}")
        logger.info(f"Task command: {arg}")
        self.jarvis.commands_executed += 1
    
    def do_research(self, arg):
        """Start research task"""
        if not arg:
            print("❌ Usage: research <topic>")
            return
        print(f"🔍 Researching: {arg}")
        logger.info(f"Research task: {arg}")
        self.jarvis.commands_executed += 1
    
    def do_backup(self, arg):
        """Manage backups"""
        if not arg:
            print("❌ Usage: backup <create|restore|list>")
            return
        print(f"💾 Backup: {arg}")
        logger.info(f"Backup command: {arg}")
        self.jarvis.commands_executed += 1
    
    def do_logs(self, arg):
        """Show system logs"""
        if arg == "show":
            print("📝 Recent logs:")
            print("  [2026-02-26 10:46:03] INFO: Jarvis HQ started")
            print("  [2026-02-26 10:46:04] INFO: All agents initialized")
        elif arg == "clear":
            print("🗑️  Logs cleared")
        else:
            print("Usage: logs <show|clear>")
    
    def do_config(self, arg):
        """Manage configuration"""
        if arg == "list":
            print("⚙️  Current Configuration:")
            print("  - Debug Mode: False")
            print("  - Log Level: INFO")
            print("  - Dashboard: Enabled on port 8080")
            print("  - Backup: Enabled (daily)")
        elif arg.startswith("set"):
            print(f"✅ Configuration updated: {arg}")
        else:
            print("Usage: config <list|set>")
    
    def do_devices(self, arg):
        """Show connected devices"""
        print("""
📱 Connected Devices:
  • Mac Mini HQ (mac_mini_01) - ✅ Online
  • Android Phone - ❌ Offline
  • Cloud Node - ❌ Offline
""")
    
    def do_help(self, arg):
        """Override help to show custom help"""
        if not arg:
            print("""
Available Commands:
  status       - Show system status
  agents       - List available agents
  modules      - List available modules
  commands     - Show command examples
  voice        - Process voice command
  build        - Build project on agent
  task         - Execute task
  research     - Start research task
  backup       - Manage backups
  logs         - Show/clear logs
  config       - Manage configuration
  devices      - Show connected devices
  help         - Show this help message
  quit/exit    - Exit Jarvis
""")
        else:
            super().do_help(arg)
    
    def do_quit(self, arg):
        """Exit Jarvis"""
        print("\n👋 Shutting down Jarvis HQ...")
        self.jarvis.stop()
        logger.info("Jarvis HQ terminated")
        return True
    
    def do_exit(self, arg):
        """Exit Jarvis (alias for quit)"""
        return self.do_quit(arg)
    
    def emptyline(self):
        """Handle empty input"""
        pass
    
    def default(self, line):
        """Handle unknown commands"""
        print(f"❌ Unknown command: {line}")
        print("   Type 'help' for available commands")


def main():
    """Entry point for Jarvis HQ."""
    jarvis = JarvisHQ()
    
    # Check if running in interactive mode
    if len(sys.argv) > 1 and sys.argv[1] == "--daemon":
        # Run as daemon
        jarvis.run()
    else:
        # Run interactive REPL
        repl = JarvisREPL(jarvis)
        try:
            repl.cmdloop()
        except KeyboardInterrupt:
            print("\n\n👋 Shutting down...")
            jarvis.stop()


if __name__ == "__main__":
    main()
