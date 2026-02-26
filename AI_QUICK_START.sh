#!/bin/bash

# ═══════════════════════════════════════════════════════════════════════════
# JARVIS AI - LOCAL LLM & CLOUD AI INTEGRATION - QUICK SETUP
# ═══════════════════════════════════════════════════════════════════════════

clear

cat << 'EOF'

╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║         🚀 JARVIS AI - LOCAL LLMS + CLOUD AI INTEGRATION                ║
║                                                                           ║
║      Run Llama 3 / Mistral on Mac M4  OR  Connect to OpenAI/Claude      ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝


═══════════════════════════════════════════════════════════════════════════
✨ WHAT YOU GET
═══════════════════════════════════════════════════════════════════════════

🏠 LOCAL LLM (Mac M4)
   ├─ Free (no API costs)
   ├─ Private (data stays on Mac)
   ├─ Fast (<1s response)
   ├─ Offline capable
   ├─ Powered by Ollama
   └─ Models: Llama 3, Mistral, CodeLlama

☁️  CLOUD AI (Powerful)
   ├─ OpenAI GPT-4 (best reasoning)
   ├─ Anthropic Claude (long context)
   ├─ Cohere (fast, reliable)
   ├─ HuggingFace (open source)
   └─ Automatic fallback system


═══════════════════════════════════════════════════════════════════════════
🎯 THREE SETUP OPTIONS
═══════════════════════════════════════════════════════════════════════════

1️⃣  LOCAL LLM ONLY (Privacy, Free)
    ✅ Best for: Personal projects, offline work
    ✅ Cost: Free
    ✅ Privacy: 100% (nothing leaves Mac)
    ✅ Setup: 15 minutes

2️⃣  CLOUD AI ONLY (Best Capability)
    ✅ Best for: Production, complex tasks
    ✅ Cost: Pay per request ($0.03-0.06 per 1K tokens)
    ✅ Privacy: Sent to cloud provider
    ✅ Setup: 5 minutes

3️⃣  HYBRID (Both Local + Cloud)
    ✅ Best for: Maximum flexibility
    ✅ Cost: Free local + optional cloud
    ✅ Privacy: Choose per task
    ✅ Setup: 20 minutes


═══════════════════════════════════════════════════════════════════════════
🚀 START HERE: RUN SETUP IN 3 SECONDS
═══════════════════════════════════════════════════════════════════════════

bash /Volumes/Akash\ SSD/repos/jarvis-brain/setup-ai.sh

Then follow the menu (just type 1, 2, 3, or 4)!


═══════════════════════════════════════════════════════════════════════════
📋 WHAT EACH OPTION DOES
═══════════════════════════════════════════════════════════════════════════

OPTION 1: LOCAL LLM
─────────────────
Automatically:
  1. Installs Ollama (if not already installed)
  2. Downloads Mistral model (7B, ~5GB)
  3. Starts Ollama service
  4. Creates configuration files
  5. Sets up Jarvis to use local AI
  ✅ Result: Free local AI ready to use!

OPTION 2: CLOUD AI
──────────────────
Automatically:
  1. Creates configuration template
  2. Shows you where to get API keys
  3. Sets up Jarvis for cloud providers
  4. Creates provider switching script
  ✅ Result: Ready to add your API key

OPTION 3: BOTH
──────────────
Combines options 1 + 2:
  1. Sets up local Ollama
  2. Creates cloud AI templates
  3. Enables hybrid mode
  4. Creates switching script
  ✅ Result: Complete flexibility!

OPTION 4: VIEW DOCS
───────────────────
Shows complete guide with:
  - Detailed setup instructions
  - Troubleshooting
  - Performance comparisons
  - API key information
  ✅ Result: Full knowledge base


═══════════════════════════════════════════════════════════════════════════
⚡ QUICK COMMANDS (After setup)
═══════════════════════════════════════════════════════════════════════════

Switch AI providers:
$ bash /Volumes/Akash\ SSD/repos/jarvis-brain/switch-ai.sh
  Choose: Local LLM, OpenAI, Claude, etc.

List installed models:
$ ollama list

Test local model:
$ ollama run mistral "Hello, how are you?"

Check AI status:
$ curl http://localhost:8001/api/ai/status

Restart Jarvis:
$ bash /Volumes/Akash\ SSD/repos/jarvis-brain/start-auto.sh


═══════════════════════════════════════════════════════════════════════════
💾 CONFIG FILES CREATED
═══════════════════════════════════════════════════════════════════════════

After setup, these files are created:

.env.local
  ├─ Local LLM configuration
  ├─ Ollama settings
  └─ Port 11434 (Ollama service)

.env.cloud
  ├─ Cloud AI templates
  ├─ API key placeholders
  └─ Provider-specific settings

.env (current)
  └─ Active configuration (auto-selected)

.env.llm
  └─ Master LLM configuration with all options


═══════════════════════════════════════════════════════════════════════════
🎓 MODELS YOU GET
═══════════════════════════════════════════════════════════════════════════

If you choose LOCAL LLM, you can select from:

llama2          7B   ├─ General coding & chat
llama2:13b      13B  ├─ More capability
mistral         7B   ├─ Fast, balanced (⭐ recommended)
codellama       7B   ├─ Specialized for coding
codellama:34b   34B  ├─ Very powerful but slow
neural-chat     7B   └─ Optimized for chatting

Each model is ~5-15GB depending on size.


═══════════════════════════════════════════════════════════════════════════
💰 PRICING (If you use cloud AI)
═══════════════════════════════════════════════════════════════════════════

OpenAI GPT-4:      $0.06 per 1K input tokens
                   $0.18 per 1K output tokens
                   (Good for complex tasks)

Claude Opus:       $0.015 per 1K input tokens
                   $0.075 per 1K output tokens
                   (Better long-context analysis)

Cohere:            $0.50-15 per 1M tokens
                   (Most cost-effective)

Local Llama:       FREE (just electricity)
                   (Best for cost)


═══════════════════════════════════════════════════════════════════════════
🔄 SWITCHING PROVIDERS (After setup)
═══════════════════════════════════════════════════════════════════════════

After setup completes, use this to switch:

bash /Volumes/Akash\ SSD/repos/jarvis-brain/switch-ai.sh

Then choose:
  1. Local LLM (Ollama)
  2. OpenAI (GPT-4)
  3. Claude (Anthropic)
  4. Cohere
  5. HuggingFace

Changes take effect immediately!


═══════════════════════════════════════════════════════════════════════════
✅ AFTER SETUP: CHECK STATUS
═══════════════════════════════════════════════════════════════════════════

Check if everything is working:

# See AI provider health
curl http://localhost:8001/api/ai/status

# Test local model
ollama run mistral "test"

# View logs
tail -f /Volumes/Akash\ SSD/repos/jarvis-brain/backend.log

# Check Ollama is running
lsof -i :11434


═══════════════════════════════════════════════════════════════════════════
🎯 RECOMMENDED SETUP
═══════════════════════════════════════════════════════════════════════════

For Mac M4 users (best of both worlds):

Step 1: Run setup
  bash setup-ai.sh
  → Choose option 3 (Both)

Step 2: Get cloud API key (optional)
  → OpenAI: https://platform.openai.com/api-keys
  → Add to .env file

Step 3: Use hybrid mode
  → Local for fast tasks (free)
  → Cloud for complex tasks (when needed)

Result:
  ✅ Free local AI for 80% of work
  ✅ Powerful cloud for 20% of complex tasks
  ✅ Complete flexibility
  ✅ Automatic fallback system


═══════════════════════════════════════════════════════════════════════════
🆚 COMPARISON: LOCAL vs CLOUD
═══════════════════════════════════════════════════════════════════════════

                    Local LLM          Cloud AI
─────────────────────────────────────────────────
Cost                Free               $0.01-0.50
Speed               Medium             Fast
Privacy             100%               Low
Capability          Good               Excellent
Offline             Yes                No
Setup time          15 min             5 min
Context size        2-4K tokens        100-200K tokens
Latency             <1s                2-5s
Quality             ⭐⭐⭐           ⭐⭐⭐⭐⭐
Best for            Coding             Reasoning


═══════════════════════════════════════════════════════════════════════════
❓ FAQ
═══════════════════════════════════════════════════════════════════════════

Q: Do I need an API key for local LLM?
A: No! Local LLM (Ollama) runs on your Mac, no API key needed.

Q: How much disk space needed?
A: ~5GB per model (Mistral 7B = 5GB, CodeLlama = 5GB)

Q: Can I run multiple models?
A: Yes! Pull multiple models, use switch-ai.sh to select.

Q: Does local LLM work offline?
A: Yes! Completely offline, no internet needed.

Q: What if I want to switch later?
A: Easy! Run: bash switch-ai.sh (5 seconds to switch)

Q: Which is fastest?
A: Local is faster (no network latency)

Q: Which is most capable?
A: Cloud (OpenAI GPT-4 or Claude)

Q: Can I use both?
A: Yes! Hybrid mode tries local first, falls back to cloud.

Q: What if all providers are offline?
A: Jarvis uses pattern-based fallback analysis.


═══════════════════════════════════════════════════════════════════════════
📚 FILES CREATED
═══════════════════════════════════════════════════════════════════════════

After complete setup, you'll have:

/Volumes/Akash\ SSD/repos/jarvis-brain/
├── setup-ai.sh                    (This script)
├── switch-ai.sh                   (Created by setup)
├── .env.local                     (Local LLM config)
├── .env.cloud                     (Cloud AI config)
├── .env.llm                       (Master config)
├── .env                           (Current active)
├── core/unified_ai_provider.py    (Backend module)
└── AI_SETUP_COMPLETE_GUIDE.md     (Full documentation)


═══════════════════════════════════════════════════════════════════════════
🚀 START NOW!
═══════════════════════════════════════════════════════════════════════════

Run this command and follow the menu:

  bash /Volumes/Akash\ SSD/repos/jarvis-brain/setup-ai.sh

Takes 5 seconds to choose, rest happens automatically!


═══════════════════════════════════════════════════════════════════════════
✨ What happens next:
═══════════════════════════════════════════════════════════════════════════

1. Choose your setup (Local, Cloud, or Both)
2. System automatically:
   - Downloads models
   - Configures providers
   - Creates scripts
   - Sets up switching
   
3. You're ready to use:
   - Local AI (free)
   - Cloud AI (powerful)
   - Or switch between them!

4. Start Jarvis:
   bash /Volumes/Akash\ SSD/repos/jarvis-brain/start-auto.sh


═══════════════════════════════════════════════════════════════════════════

Ready? Run the setup now! 👉

  bash /Volumes/Akash\ SSD/repos/jarvis-brain/setup-ai.sh

═══════════════════════════════════════════════════════════════════════════

EOF

