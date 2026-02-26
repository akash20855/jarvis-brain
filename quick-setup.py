#!/usr/bin/env python3
"""
Jarvis Brain - Quick Start Setup
Automated setup for full-stack deployment
"""

import subprocess
import sys
import os
from pathlib import Path


class JarvisSetup:
    """Setup assistant for Jarvis Brain"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.os_type = sys.platform
    
    def print_welcome(self):
        """Print welcome message"""
        print("""
╔════════════════════════════════════════════════════════════════════════╗
║                                                                        ║
║           🤖 JARVIS BRAIN - FULL STACK SETUP WIZARD                    ║
║                                                                        ║
║              Complete AI-Powered Code Evolution System                 ║
║                                                                        ║
╚════════════════════════════════════════════════════════════════════════╝

Welcome! This wizard will help you set up Jarvis Brain.

Options:
  1. 🐳 Docker Setup (Recommended - All-in-one)
  2. 🚀 Local Setup (Manual - Requires more config)
  3. ☁️ Cloud Deploy (AWS/GCP/Azure)
  4. 📚 View Documentation
  5. ❓ Help & Support
  6. ❌ Exit
""")
    
    def option_docker(self):
        """Docker setup"""
        print("""
╔════════════════════════════════════════════════════════════════════════╗
║                    🐳 DOCKER SETUP (RECOMMENDED)                       ║
╚════════════════════════════════════════════════════════════════════════╝

This will start all services in Docker containers:
  ✅ Frontend (React) - Port 3000
  ✅ Backend API (Flask) - Port 5000
  ✅ Ollama Analysis AI - Port 11434
  ✅ Ollama Chat AI - Port 11435
  ✅ Ollama Suggestions AI - Port 11436
  ✅ Redis Cache - Port 6379
  ✅ PostgreSQL Database - Port 5432

Prerequisites:
  ✓ Docker (https://docker.com)
  ✓ Docker Compose
  ✓ 8GB+ RAM recommended
  ✓ 50GB+ storage for AI models

""")
        
        # Check Docker
        print("Checking Docker installation...")
        result = subprocess.run(
            ["docker", "--version"],
            capture_output=True
        )
        
        if result.returncode != 0:
            print("❌ Docker not found!")
            print("   Install from: https://docker.com")
            return
        
        print(f"✅ {result.stdout.decode().strip()}")
        
        # Check Docker Compose
        print("Checking Docker Compose...")
        result = subprocess.run(
            ["docker-compose", "--version"],
            capture_output=True
        )
        
        if result.returncode != 0:
            print("❌ Docker Compose not found!")
            print("   Install from: https://docs.docker.com/compose")
            return
        
        print(f"✅ {result.stdout.decode().strip()}")
        
        # Start services
        print("\n🚀 Starting services...")
        print("   This may take a few minutes on first run...\n")
        
        result = subprocess.run(
            ["docker-compose", "up", "-d"],
            cwd=self.project_root
        )
        
        if result.returncode == 0:
            print("\n✅ All services started successfully!")
            print("\n📱 Access Points:")
            print("   • Frontend:        http://localhost:3000")
            print("   • Backend API:     http://localhost:5000/api")
            print("   • AI Services:     http://localhost:11434+ (local)")
            print("\n💡 Next Steps:")
            print("   1. Open http://localhost:3000 in your browser")
            print("   2. Start chatting with Jarvis!")
            print("   3. Type 'analyze' to scan your project")
        else:
            print("\n❌ Error starting services")
    
    def option_local(self):
        """Local setup"""
        print("""
╔════════════════════════════════════════════════════════════════════════╗
║                    🚀 LOCAL SETUP (MANUAL)                            ║
╚════════════════════════════════════════════════════════════════════════╝

This will guide you through setting up each component locally.

Prerequisites:
  ✓ Python 3.11+
  ✓ Node.js 18+
  ✓ Ollama (for AI features)

Step 1: Install Python Dependencies
""")
        
        print("  Installing backend requirements...")
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r",
             "backend/requirements.txt"],
            cwd=self.project_root
        )
        
        if result.returncode == 0:
            print("  ✅ Backend dependencies installed")
        else:
            print("  ❌ Error installing backend")
            return
        
        print("\nStep 2: Install Frontend Dependencies")
        print("  Installing Node.js packages...")
        result = subprocess.run(
            ["npm", "install"],
            cwd=self.project_root / "frontend"
        )
        
        if result.returncode == 0:
            print("  ✅ Frontend dependencies installed")
        else:
            print("  ❌ Error installing frontend")
        
        print("""
Step 3: Start Services

Terminal 1 - Backend API:
  cd backend
  python3 app.py
  # Runs on http://localhost:5000

Terminal 2 - Frontend:
  cd frontend
  npm start
  # Runs on http://localhost:3000

Terminal 3 - Ollama (if using AI):
  ollama serve
  ollama pull mistral
  ollama pull neural-chat

✅ Setup complete!
""")
    
    def option_cloud(self):
        """Cloud deployment"""
        print("""
╔════════════════════════════════════════════════════════════════════════╗
║                    ☁️ CLOUD DEPLOYMENT                                 ║
╚════════════════════════════════════════════════════════════════════════╝

Deployment Options:

1. AWS Deployment
   - Use ECS, ECR, and RDS
   - Follow: ./docs/aws-deployment.md
   - Command: aws deploy --service=jarvis-brain

2. Google Cloud Deploy
   - Use Cloud Run, Artifact Registry
   - Follow: ./docs/gcp-deployment.md
   - Command: gcloud run deploy jarvis-brain

3. Azure Deploy
   - Use Container Instances, App Service
   - Follow: ./docs/azure-deployment.md
   - Command: az container create --name jarvis-brain

4. Heroku Deploy
   - Use buildpacks and dynos
   - Follow: ./docs/heroku-deployment.md
   - Command: git push heroku main

5. DigitalOcean Deploy
   - Use App Platform
   - Follow: ./docs/digitalocean-deployment.md

📚 See deployment documentation for details
""")
    
    def option_docs(self):
        """View documentation"""
        print("""
╔════════════════════════════════════════════════════════════════════════╗
║                    📚 DOCUMENTATION                                    ║
╚════════════════════════════════════════════════════════════════════════╝

Available Documentation:

1. 📖 FULLSTACK.md
   Complete guide to the full-stack setup
   Covers: Architecture, deployment, usage

2. 🏗️ ARCHITECTURE.md
   Technical architecture and design
   Covers: Components, data flow, scalability

3. 🔌 backend/README.md
   Backend API documentation
   Covers: Endpoints, configuration, deployment

4. 💻 frontend/README.md
   Frontend application documentation
   Covers: Features, installation, development

5. 🤖 core/chatbot.py
   Chatbot implementation details
   Covers: Commands, conversation flow

6. ⚙️ core/auto_evolution.py
   Auto-evolution engine documentation
   Covers: Analysis, AI integration

7. 🎯 core/ai_services.py
   AI service manager documentation
   Covers: Multi-instance management, fallback

8. 🚀 core/launcher.py
   CLI launcher documentation
   Covers: Menu system, navigation

💡 Open a documentation file:
   - In VS Code: File > Open
   - In Terminal: cat FULLSTACK.md
   - In Browser: Open .md file with GitHub/Markdown viewer
""")
    
    def option_help(self):
        """Help and support"""
        print("""
╔════════════════════════════════════════════════════════════════════════╗
║                    ❓ HELP & SUPPORT                                    ║
╚════════════════════════════════════════════════════════════════════════╝

Need help? Here are some resources:

🐛 Common Issues:

1. "Docker command not found"
   Solution: Install Docker from https://docker.com

2. "Cannot connect to API"
   - Check: curl http://localhost:5000/api/health
   - Verify backend is running
   - Check firewall/network

3. "Frontend not loading"
   - Clear browser cache (Ctrl+Shift+Delete)
   - Check: http://localhost:3000
   - Check browser console for errors

4. "AI not responding"
   - Check: curl http://localhost:11434/api/tags
   - Verify Ollama is running
   - Download models: ollama pull mistral

5. "Database connection error"
   - Check PostgreSQL is running
   - Verify credentials in .env
   - Check: psql -U jarvis -d jarvis_brain

📞 Get Help:

- Documentation: See option 4
- GitHub Issues: Create an issue report
- Discord Community: Join our server
- Email: support@jarvis-brain.dev

🤝 Contributing:

Contributions welcome! Areas:
- Bug fixes
- Feature requests
- Documentation
- Performance improvements
- Additional AI backends

📋 Before Reporting Issues:

1. Check existing documentation
2. Review the architecture
3. Check the FAQ section
4. Review similar issues

✅ Issue Template:

Title: [Backend/Frontend/AI] Brief description

Description:
- What were you doing?
- What happened?
- What did you expect?

Steps to Reproduce:
1. ...
2. ...

Environment:
- OS: macOS/Windows/Linux
- Docker version: ...
- Python version: ...

Logs:
[Paste relevant logs]

Let's build Jarvis Brain together! 🚀
""")
    
    def run(self):
        """Run the setup wizard"""
        while True:
            self.print_welcome()
            choice = input("Choose an option (1-6): ").strip()
            
            if choice == "1":
                self.option_docker()
            elif choice == "2":
                self.option_local()
            elif choice == "3":
                self.option_cloud()
            elif choice == "4":
                self.option_docs()
            elif choice == "5":
                self.option_help()
            elif choice == "6":
                print("\n👋 Goodbye! Happy coding with Jarvis Brain! 🤖\n")
                break
            else:
                print("❌ Invalid option. Please try again.\n")
            
            input("\nPress Enter to continue...")
            print("\n" * 2)


if __name__ == "__main__":
    setup = JarvisSetup()
    setup.run()
