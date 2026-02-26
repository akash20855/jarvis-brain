#!/bin/bash
# macOS LaunchAgent for Auto-Starting Claude Haiku
# This file enables Claude to auto-start on login

# Create LaunchAgent directory if it doesn't exist
mkdir -p ~/Library/LaunchAgents

# Create the plist file
cat > ~/Library/LaunchAgents/com.jarvis.claude.haiku.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.jarvis.claude.haiku</string>
    
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>/Volumes/Akash SSD/repos/jarvis-brain/start-claude.sh</string>
    </array>
    
    <key>RunAtLoad</key>
    <true/>
    
    <key>KeepAlive</key>
    <true/>
    
    <key>StandardOutPath</key>
    <string>/Volumes/Akash SSD/repos/jarvis-brain/claude-launchd.log</string>
    
    <key>StandardErrorPath</key>
    <string>/Volumes/Akash SSD/repos/jarvis-brain/claude-launchd-error.log</string>
    
    <key>EnvironmentVariables</key>
    <dict>
        <key>ANTHROPIC_API_KEY</key>
        <string>sk-ant-your-key-here</string>
    </dict>
</dict>
</plist>
EOF

echo "✅ LaunchAgent created!"
echo ""
echo "⚠️  IMPORTANT: Edit the plist file to add your API key:"
echo "   nano ~/Library/LaunchAgents/com.jarvis.claude.haiku.plist"
echo "   Change: sk-ant-your-key-here → your actual key"
echo ""
echo "Load the LaunchAgent:"
echo "   launchctl load ~/Library/LaunchAgents/com.jarvis.claude.haiku.plist"
echo ""
echo "Check status:"
echo "   launchctl list | grep claude"
echo ""
echo "View logs:"
echo "   tail -f /Volumes/Akash\ SSD/repos/jarvis-brain/claude-launchd.log"
echo ""
echo "Unload (stop auto-start):"
echo "   launchctl unload ~/Library/LaunchAgents/com.jarvis.claude.haiku.plist"
