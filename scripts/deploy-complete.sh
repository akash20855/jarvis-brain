#!/bin/bash
# Deploy Jarvis Brain to Production
# Supports Docker, Heroku, and AWS EC2

set -e

echo "🚀 JARVIS BRAIN - DEPLOYMENT SCRIPT"
echo "===================================="

# Color output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Get deployment target
DEPLOY_TARGET=${1:-docker}

echo -e "${BLUE}📦 Deployment Target: $DEPLOY_TARGET${NC}"

# Deploy with Docker
deploy_docker() {
    echo -e "${BLUE}📦 Building Docker images...${NC}"
    docker-compose build
    
    echo -e "${BLUE}🚀 Starting containers...${NC}"
    docker-compose up -d
    
    echo -e "${GREEN}✅ Docker deployment complete!${NC}"
    echo "Backend: http://localhost:8000"
    echo "Frontend: http://localhost:3000"
}

# Deploy to Heroku
deploy_heroku() {
    APP_NAME=${2:-jarvis-brain}
    
    echo -e "${BLUE}🌍 Deploying to Heroku ($APP_NAME)...${NC}"
    
    # Check if Heroku CLI is installed
    if ! command -v heroku &> /dev/null; then
        echo -e "${RED}❌ Heroku CLI not found. Install it first:${NC}"
        echo "brew install heroku/brew/heroku"
        exit 1
    fi
    
    # Login
    heroku login
    
    # Create or get app
    heroku apps:info --app $APP_NAME || heroku create $APP_NAME
    
    # Add buildpacks
    heroku buildpacks:set heroku/python --app $APP_NAME
    heroku buildpacks:add heroku/nodejs --app $APP_NAME
    
    # Deploy
    git push heroku main --force
    
    # Set environment variables
    heroku config:set AI_TYPE=openai --app $APP_NAME
    heroku config:set FLASK_ENV=production --app $APP_NAME
    
    echo -e "${GREEN}✅ Heroku deployment complete!${NC}"
    echo "App URL: https://$APP_NAME.herokuapp.com"
    echo "View logs: heroku logs --tail --app $APP_NAME"
}

# Deploy to AWS EC2
deploy_aws() {
    INSTANCE_IP=${2:-}
    KEY_FILE=${3:-}
    
    if [ -z "$INSTANCE_IP" ] || [ -z "$KEY_FILE" ]; then
        echo -e "${RED}❌ Usage: $0 aws <instance-ip> <key-file.pem>${NC}"
        exit 1
    fi
    
    echo -e "${BLUE}🌍 Deploying to AWS EC2 ($INSTANCE_IP)...${NC}"
    
    # SSH and deploy
    ssh -i "$KEY_FILE" ubuntu@"$INSTANCE_IP" << 'EOF'
    set -e
    
    # Update system
    sudo apt update && sudo apt upgrade -y
    
    # Install dependencies
    sudo apt install -y curl git python3-pip nodejs npm
    
    # Clone repo
    cd /home/ubuntu
    git clone https://github.com/your-repo/jarvis-brain.git || cd jarvis-brain && git pull
    cd jarvis-brain
    
    # Install Python dependencies
    pip3 install -r requirements.txt
    
    # Install Node dependencies
    cd frontend && npm install && cd ..
    
    # Build React
    cd frontend && npm run build && cd ..
    
    # Start services with systemd
    sudo tee /etc/systemd/system/jarvis.service > /dev/null <<UNIT
[Unit]
Description=Jarvis Brain Backend
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/jarvis-brain
ExecStart=/usr/bin/python3 backend/app.py
Restart=always

[Install]
WantedBy=multi-user.target
UNIT
    
    sudo systemctl daemon-reload
    sudo systemctl enable jarvis
    sudo systemctl start jarvis
    
    echo "Deployment complete!"
EOF
    
    echo -e "${GREEN}✅ AWS EC2 deployment complete!${NC}"
    echo "Access at: http://$INSTANCE_IP:8000"
}

# Deploy to Vercel (Frontend only)
deploy_vercel() {
    echo -e "${BLUE}🌍 Deploying frontend to Vercel...${NC}"
    
    if ! command -v vercel &> /dev/null; then
        echo "Installing Vercel CLI..."
        npm install -g vercel
    fi
    
    cd frontend
    vercel --prod
    
    echo -e "${GREEN}✅ Vercel deployment complete!${NC}"
}

# Main deployment logic
case $DEPLOY_TARGET in
    docker)
        deploy_docker
        ;;
    heroku)
        deploy_heroku "$2" "$3"
        ;;
    aws)
        deploy_aws "$2" "$3"
        ;;
    vercel)
        deploy_vercel
        ;;
    *)
        echo -e "${RED}❌ Unknown deployment target: $DEPLOY_TARGET${NC}"
        echo "Usage: $0 [docker|heroku|aws|vercel]"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}==================================="${NC}
echo -e "${GREEN}🎉 Deployment Successful!${NC}"
echo -e "${GREEN}==================================="${NC}
