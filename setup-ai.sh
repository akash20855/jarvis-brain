#!/bin/bash

# ═══════════════════════════════════════════════════════════════════════════
# JARVIS LOCAL LLM SETUP FOR MAC M4 WITH APPLE SILICON
# ═══════════════════════════════════════════════════════════════════════════
# Install and configure local LLMs (Llama 3, Mistral, etc.) 
# OR connect to cloud AI (OpenAI, Claude, etc.)
# ═══════════════════════════════════════════════════════════════════════════

set -e

clear

cat << 'EOF'

╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║          🚀 JARVIS AI SETUP - LOCAL & CLOUD AI CONFIGURATION            ║
║                                                                           ║
║              Choose: Local LLMs (Mac M4) OR Cloud AI Services            ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝

EOF

sleep 1

# Check if Ollama is installed
check_ollama() {
    if command -v ollama &> /dev/null; then
        echo "✅ Ollama already installed"
        return 0
    else
        return 1
    fi
}

# Install Ollama on Mac
install_ollama_mac() {
    echo ""
    echo "📦 Installing Ollama for Mac M4..."
    echo ""
    
    # Download Ollama for macOS
    # Check if we can install via Homebrew
    if command -v brew &> /dev/null; then
        echo "Using Homebrew to install Ollama..."
        brew install ollama
    else
        echo "⚠️  Homebrew not found. Installing Ollama manually..."
        echo ""
        echo "Option 1: Download from https://ollama.ai/download/mac"
        echo "Option 2: Use this command:"
        echo ""
        echo "curl -fsSL https://ollama.ai/install.sh | sh"
        echo ""
        read -p "Press Enter after Ollama is installed, or Ctrl+C to cancel..."
    fi
    
    echo "✅ Ollama installation complete"
}

# Start Ollama service
start_ollama() {
    echo ""
    echo "🚀 Starting Ollama service..."
    echo ""
    
    # Start Ollama in background
    if pgrep -f "ollama serve" > /dev/null; then
        echo "✅ Ollama service already running"
    else
        echo "Starting ollama serve..."
        nohup ollama serve > /tmp/ollama.log 2>&1 &
        sleep 3
        
        if pgrep -f "ollama serve" > /dev/null; then
            echo "✅ Ollama service started successfully"
        else
            echo "❌ Failed to start Ollama. Check: cat /tmp/ollama.log"
            return 1
        fi
    fi
}

# Pull LLM models
pull_llm_models() {
    echo ""
    echo "📥 Downloading LLM models for your Mac M4..."
    echo ""
    echo "Available models for Apple Silicon:"
    echo "  1. llama2 (7B) - Fast, good for coding"
    echo "  2. llama2:13b - More capable"
    echo "  3. mistral (7B) - Recommended for M4"
    echo "  4. neural-chat - Chat optimized"
    echo "  5. codellama - Code-specific"
    echo ""
    
    read -p "Enter model number (1-5) or model name [default: mistral]: " model_input
    
    case "${model_input:-3}" in
        1) MODEL="llama2" ;;
        2) MODEL="llama2:13b" ;;
        3) MODEL="mistral" ;;
        4) MODEL="neural-chat" ;;
        5) MODEL="codellama" ;;
        *) MODEL="${model_input:-mistral}" ;;
    esac
    
    echo ""
    echo "📥 Pulling $MODEL model (this takes 2-5 minutes on M4)..."
    echo ""
    
    ollama pull "$MODEL"
    
    echo ""
    echo "✅ Model $MODEL downloaded successfully"
    
    return 0
}

# Setup local LLM configuration
setup_local_llm() {
    echo ""
    echo "⚙️  Setting up Local LLM configuration..."
    echo ""
    
    # Create .env file for local LLM
    JARVIS_DIR="/Volumes/Akash SSD/repos/jarvis-brain"
    
    cat > "$JARVIS_DIR/.env.local" << 'LOCALENV'
# ═══════════════════════════════════════════════════════════════════════════
# LOCAL LLM CONFIGURATION (Run on Mac M4)
# ═══════════════════════════════════════════════════════════════════════════

# AI Provider: local, openai, anthropic
AI_TYPE=local

# Local Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral
OLLAMA_CODE_MODEL=codellama
OLLAMA_CHAT_MODEL=neural-chat

# Model parameters (optimize for M4)
OLLAMA_NUM_THREAD=8
OLLAMA_NUM_GPU=0
OLLAMA_CONTEXT_SIZE=2048

# Flask Port
FLASK_PORT=8001

# Logging
LOG_LEVEL=INFO
LOCALENV
    
    echo "✅ Created $JARVIS_DIR/.env.local"
    echo ""
    echo "Configuration:"
    cat "$JARVIS_DIR/.env.local"
}

# Setup cloud AI configuration
setup_cloud_ai() {
    echo ""
    echo "☁️  Setting up Cloud AI configuration..."
    echo ""
    
    JARVIS_DIR="/Volumes/Akash SSD/repos/jarvis-brain"
    
    cat > "$JARVIS_DIR/.env.cloud" << 'CLOUDENV'
# ═══════════════════════════════════════════════════════════════════════════
# CLOUD AI CONFIGURATION (OpenAI, Claude, etc.)
# ═══════════════════════════════════════════════════════════════════════════

# AI Provider: openai, anthropic, cohere, huggingface
AI_TYPE=openai

# OpenAI Configuration
# Get API key from: https://platform.openai.com/api-keys
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4-turbo-preview
OPENAI_VISION_MODEL=gpt-4-vision-preview

# Anthropic (Claude) Configuration
# Get API key from: https://console.anthropic.com
ANTHROPIC_API_KEY=your_claude_api_key_here
ANTHROPIC_MODEL=claude-3-opus-20240229

# Cohere Configuration
COHERE_API_KEY=your_cohere_api_key_here

# HuggingFace Configuration
HUGGINGFACE_API_KEY=your_huggingface_api_key_here

# Flask Port
FLASK_PORT=8001

# Logging
LOG_LEVEL=INFO
CLOUDENV
    
    echo "✅ Created $JARVIS_DIR/.env.cloud"
    echo ""
    echo "⚠️  IMPORTANT: Add your API keys to .env.cloud"
    echo ""
    cat "$JARVIS_DIR/.env.cloud" | head -20
}

# Create switching script
create_switching_script() {
    echo ""
    echo "🔄 Creating AI provider switching script..."
    echo ""
    
    JARVIS_DIR="/Volumes/Akash SSD/repos/jarvis-brain"
    
    cat > "$JARVIS_DIR/switch-ai.sh" << 'SWITCHSCRIPT'
#!/bin/bash

# Switch between Local LLM and Cloud AI providers

JARVIS_DIR="/Volumes/Akash SSD/repos/jarvis-brain"

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║          SWITCH AI PROVIDER - LOCAL vs CLOUD                  ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""
echo "Choose your AI provider:"
echo "  1. Local LLM (Llama 3 / Mistral on Mac M4)"
echo "  2. OpenAI (GPT-4, advanced reasoning)"
echo "  3. Anthropic Claude (long context, analysis)"
echo "  4. Cohere (fast, reliable)"
echo "  5. HuggingFace (open source models)"
echo ""

read -p "Enter option (1-5): " option

case $option in
    1)
        echo "🚀 Switching to LOCAL LLM..."
        cp "$JARVIS_DIR/.env.local" "$JARVIS_DIR/.env"
        echo "✅ Now using: Local LLM (Ollama)"
        echo "   Models: Mistral, Llama 3, CodeLlama"
        echo "   Status: Check with: lsof -i :11434"
        ;;
    2)
        echo "☁️  Switching to OPENAI..."
        cp "$JARVIS_DIR/.env.cloud" "$JARVIS_DIR/.env"
        echo "✅ Now using: OpenAI (GPT-4)"
        echo "   Update API key in .env file"
        echo "   Get key: https://platform.openai.com/api-keys"
        ;;
    3)
        echo "🧠 Switching to ANTHROPIC CLAUDE..."
        cp "$JARVIS_DIR/.env.cloud" "$JARVIS_DIR/.env"
        sed -i '' 's/openai/anthropic/g' "$JARVIS_DIR/.env"
        echo "✅ Now using: Anthropic Claude"
        echo "   Update API key in .env file"
        echo "   Get key: https://console.anthropic.com"
        ;;
    4)
        echo "⚡ Switching to COHERE..."
        cp "$JARVIS_DIR/.env.cloud" "$JARVIS_DIR/.env"
        sed -i '' 's/openai/cohere/g' "$JARVIS_DIR/.env"
        echo "✅ Now using: Cohere"
        echo "   Update API key in .env file"
        ;;
    5)
        echo "🤗 Switching to HUGGINGFACE..."
        cp "$JARVIS_DIR/.env.cloud" "$JARVIS_DIR/.env"
        sed -i '' 's/openai/huggingface/g' "$JARVIS_DIR/.env"
        echo "✅ Now using: HuggingFace"
        echo "   Update API key in .env file"
        ;;
    *)
        echo "❌ Invalid option"
        exit 1
        ;;
esac

echo ""
echo "⚠️  Restart backend to apply changes:"
echo "   bash $JARVIS_DIR/start-auto.sh"

SWITCHSCRIPT
    
    chmod +x "$JARVIS_DIR/switch-ai.sh"
    echo "✅ Created $JARVIS_DIR/switch-ai.sh"
}

# Main menu
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "SETUP OPTIONS:"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "1️⃣  Setup LOCAL LLM (Llama 3/Mistral on Mac M4)"
echo "2️⃣  Setup CLOUD AI (OpenAI, Claude, etc.)"
echo "3️⃣  Setup BOTH (Local primary, Cloud backup)"
echo "4️⃣  View Documentation"
echo "5️⃣  Exit"
echo ""

read -p "Choose option (1-5): " choice

case $choice in
    1)
        echo ""
        echo "🏠 LOCAL LLM SETUP"
        echo "─────────────────────────────────────────────────────────"
        
        if ! check_ollama; then
            install_ollama_mac
        fi
        
        start_ollama
        pull_llm_models
        setup_local_llm
        create_switching_script
        
        echo ""
        echo "✅ LOCAL LLM SETUP COMPLETE!"
        echo ""
        echo "Next steps:"
        echo "  1. Verify Ollama is running: lsof -i :11434"
        echo "  2. Test local model: ollama run mistral 'Hello'"
        echo "  3. Start Jarvis: bash /Volumes/Akash\ SSD/repos/jarvis-brain/start-auto.sh"
        echo ""
        ;;
    2)
        echo ""
        echo "☁️  CLOUD AI SETUP"
        echo "─────────────────────────────────────────────────────────"
        
        setup_cloud_ai
        create_switching_script
        
        echo ""
        echo "✅ CLOUD AI SETUP COMPLETE!"
        echo ""
        echo "Next steps:"
        echo "  1. Add your API key to .env"
        echo "  2. Switch provider: bash /Volumes/Akash\ SSD/repos/jarvis-brain/switch-ai.sh"
        echo "  3. Restart Jarvis: bash /Volumes/Akash\ SSD/repos/jarvis-brain/start-auto.sh"
        echo ""
        ;;
    3)
        echo ""
        echo "⚖️  BOTH LOCAL AND CLOUD SETUP"
        echo "─────────────────────────────────────────────────────────"
        
        if ! check_ollama; then
            install_ollama_mac
        fi
        
        start_ollama
        pull_llm_models
        setup_local_llm
        setup_cloud_ai
        create_switching_script
        
        echo ""
        echo "✅ BOTH LOCAL & CLOUD SETUP COMPLETE!"
        echo ""
        echo "Next steps:"
        echo "  1. Setup Ollama: lsof -i :11434"
        echo "  2. Add cloud API keys to .env"
        echo "  3. Switch providers:"
        echo "     bash /Volumes/Akash\ SSD/repos/jarvis-brain/switch-ai.sh"
        echo "  4. Start Jarvis: bash /Volumes/Akash\ SSD/repos/jarvis-brain/start-auto.sh"
        echo ""
        ;;
    4)
        cat << 'DOCS'

═══════════════════════════════════════════════════════════════════════════
📚 LOCAL LLM vs CLOUD AI - COMPLETE GUIDE
═══════════════════════════════════════════════════════════════════════════

🏠 LOCAL LLMS (On Your Mac M4)
─────────────────────────────────────────────────────────────────────────

Advantages:
  ✅ No API costs (run completely free)
  ✅ Privacy - data never leaves your Mac
  ✅ Fast - no network latency
  ✅ Works offline
  ✅ Unlimited usage
  ✅ Customize models locally

Disadvantages:
  ❌ Requires compute resources (but M4 is powerful!)
  ❌ Smaller models = less capable
  ❌ Training/fine-tuning limited
  ❌ Can't access latest models instantly

Models Available:
  🦙 Llama 3 (8B, 70B) - Excellent coding
  🎯 Mistral (7B) - Fast, balanced
  💻 CodeLlama (7B, 13B, 34B) - Code specialized
  🤖 Neural-Chat - Chat optimized
  📚 Phi (3B, 7B, 14B) - Compact, fast

Setup:
  1. brew install ollama
  2. ollama pull mistral (or llama2, codellama)
  3. ollama serve (starts on port 11434)
  4. Use in Jarvis via local API

Commands:
  ollama run mistral "your prompt"
  ollama list (show installed models)
  ollama rm Model_name (delete model)


☁️  CLOUD AI SERVICES
─────────────────────────────────────────────────────────────────────────

1️⃣  OPENAI (GPT-4, GPT-4 Vision)
    Advantages:
      ✅ Most capable models
      ✅ GPT-4 for complex reasoning
      ✅ Vision/image understanding
      ✅ Large context window
      ✅ Continuous improvements
    
    Pricing: $0.03-0.06 per 1K tokens
    Website: https://platform.openai.com
    Get API Key: https://platform.openai.com/api-keys

2️⃣  ANTHROPIC CLAUDE (Claude 3 family)
    Advantages:
      ✅ Long context (200K tokens)
      ✅ Great for analysis
      ✅ Strong reasoning
      ✅ Constitutional AI
      ✅ Good documentation
    
    Pricing: $0.003-0.024 per 1K tokens
    Website: https://www.anthropic.com
    Get API Key: https://console.anthropic.com

3️⃣  COHERE
    Advantages:
      ✅ Fast completion
      ✅ Fine-tuning available
      ✅ Multilingual
      ✅ Cost-effective
    
    Pricing: $0.50-15 per million tokens
    Website: https://cohere.io
    Get API Key: https://dashboard.cohere.ai

4️⃣  HUGGINGFACE
    Advantages:
      ✅ Open source models
      ✅ Many options
      ✅ Community driven
      ✅ Fine-tuning support
    
    Website: https://huggingface.co
    Get API Key: https://huggingface.co/settings/tokens


⚖️  COMPARISON TABLE
─────────────────────────────────────────────────────────────────────────

                Local LLM   OpenAI    Claude    Cohere
Cost            Free        $$        $$        $$
Speed           Fast        Fast      Medium    Fast
Privacy         100%        Low       Medium    Low
Capability      Good        Excellent Great     Good
Offline         Yes         No        No        No
Context Size    2-4K        128K      200K      4-100K
Setup Time      5 min       1 min     1 min     1 min
Customization   High        Low       Low       Medium


🎯 RECOMMENDED SETUP
─────────────────────────────────────────────────────────────────────────

For Mac M4 (Best of Both Worlds):
  Primary: Local Mistral (free, fast, private)
  Secondary: OpenAI GPT-4 (advanced tasks)
  Fallback: Claude (long analysis)

This gives you:
  ✅ Fast local responses
  ✅ Cloud power when needed
  ✅ Cost control
  ✅ Privacy for sensitive code
  ✅ Best of both worlds


🔧 HOW TO SWITCH BETWEEN PROVIDERS
─────────────────────────────────────────────────────────────────────────

1. Run: bash /Volumes/Akash\ SSD/repos/jarvis-brain/switch-ai.sh
2. Choose provider (1-5)
3. Restart Jarvis: bash start-auto.sh
4. Done!

Or manually:
  cp /Volumes/Akash\ SSD/repos/jarvis-brain/.env.local /Volumes/Akash\ SSD/repos/jarvis-brain/.env
  bash /Volumes/Akash\ SSD/repos/jarvis-brain/start-auto.sh


📊 PERFORMANCE ON MAC M4
─────────────────────────────────────────────────────────────────────────

Local Mistral:
  Token generation: 50-100 tokens/sec
  Response time: 1-3 seconds for coding tasks
  Memory: 4-6GB RAM
  No GPU needed (uses CPU efficiently)

For reference:
  OpenAI GPT-4: Response time 2-5 seconds (network dependent)
  Claude: Response time 1-4 seconds (network dependent)


🚀 JARVIS INTEGRATION
─────────────────────────────────────────────────────────────────────────

Jarvis automatically detects and uses:

1. Local LLM (if Ollama is running)
   - Fast, offline, free
   - ~100ms response time

2. Cloud AI (if configured)
   - Powerful, feature-rich
   - 1-5 second response time

3. Pattern-based fallback
   - Always works offline
   - Basic analysis capability


❓ FAQ
─────────────────────────────────────────────────────────────────────────

Q: Can I run multiple models locally?
A: Yes! Ollama can run multiple models on M4
   Just pull different models and use different ports

Q: Will local LLMs work offline?
A: Yes! Completely offline operation supported

Q: Can I switch providers on the fly?
A: Yes! Use switch-ai.sh script

Q: How much does local LLM cost?
A: Nothing! It's free (just electricity)

Q: Which is faster, local or cloud?
A: Local is faster (no network latency)

Q: Which is more capable?
A: Cloud (OpenAI, Claude) are more advanced

Q: Can I use both?
A: Yes! Jarvis supports hybrid mode


📝 GETTING STARTED
─────────────────────────────────────────────────────────────────────────

1. Choose setup: Local, Cloud, or Both
   bash /Volumes/Akash\ SSD/repos/jarvis-brain/setup-ai.sh

2. Switch between providers:
   bash /Volumes/Akash\ SSD/repos/jarvis-brain/switch-ai.sh

3. Start Jarvis:
   bash /Volumes/Akash\ SSD/repos/jarvis-brain/start-auto.sh

4. Enjoy your AI-powered development!

DOCS
        echo ""
        read -p "Press Enter to continue..."
        ;;
    5)
        echo "Goodbye! 👋"
        exit 0
        ;;
    *)
        echo "❌ Invalid option"
        exit 1
        ;;
esac

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "✅ SETUP COMPLETE!"
echo "═══════════════════════════════════════════════════════════════"

