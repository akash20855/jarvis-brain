#!/bin/bash
# JARVIS Quick Start Reference
# Run this file to print quick commands

cat << 'EOF'

╔══════════════════════════════════════════════════════════════════════════════╗
║                     🚀 JARVIS QUICK START REFERENCE 🚀                       ║
╚══════════════════════════════════════════════════════════════════════════════╝

📍 WORKSPACE: /Volumes/Akash SSD/repos/jarvis-brain

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🌟 SETUP (First Time Only)

  1️⃣  Configure API Key:
      cp .env.template .env
      nano .env  # Add: ANTHROPIC_API_KEY=sk-proj-your-key

  2️⃣  Install Auto-Start:
      bash setup-autostart.sh install

  3️⃣  Log out/in or restart Mac
      
  ✅ Done! JARVIS auto-starts from now on

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚡ DAILY USE (After Setup)

  Open VS Code:
      code .

  Use JARVIS:
      Cmd+Shift+P → type "JARVIS" → select command

  That's it! Server runs automatically in background.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔧 SERVICE MANAGEMENT

  Check Status:
      bash setup-autostart.sh status

  Restart Server:
      bash setup-autostart.sh restart

  Stop Server:
      bash setup-autostart.sh stop

  Remove Auto-Start:
      bash setup-autostart.sh uninstall

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔍 MONITORING & DEBUG

  View Logs (Real-Time):
      tail -f .jarvis_logs/server.log

  Check if Running:
      ps aux | grep vscode_server.py

  Check Port:
      lsof -i :8765

  Manual Start:
      source jarvis_env/bin/activate
      python3 core/vscode_server.py

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💻 AVAILABLE JARVIS COMMANDS (Cmd+Shift+P → JARVIS: ...)

  ✓ JARVIS: Generate Code
  ✓ JARVIS: Analyze Code
  ✓ JARVIS: Debug Project
  ✓ JARVIS: Improve Code
  ✓ JARVIS: Generate Tests
  ✓ JARVIS: Refactor Code
  ✓ JARVIS: Explain Code
  ✓ JARVIS: Build Project
  ✓ JARVIS: Status

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚨 TROUBLESHOOTING

  Server won't start?
      • Check .env has ANTHROPIC_API_KEY
      • Kill existing: pkill -f vscode_server.py
      • Check port: lsof -i :8765

  Service won't install?
      • mkdir -p ~/Library/LaunchAgents
      • Run install again

  Still stuck?
      Check logs: tail -f .jarvis_logs/server.log

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📚 DOCUMENTATION

  Complete Setup Guide:
      AUTO_START_SETUP.md

  VS Code Integration:
      VSCODE_COMPLETE_GUIDE.md

  Architecture Overview:
      ARCHITECTURE.md

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✨ YOU'RE ALL SET!

  JARVIS is fully automated and ready to use.
  Just open VS Code and start coding with AI assistance!

  Questions? Check AUTO_START_SETUP.md for detailed guide.

╔══════════════════════════════════════════════════════════════════════════════╗
║                    Happy coding with JARVIS! 🎉                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

EOF
