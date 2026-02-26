# 🤖 JARVIS AI - LOCAL LLMS & CLOUD AI SETUP GUIDE

## Overview

Your Jarvis system now supports **both local and cloud AI providers**, giving you complete flexibility:

### 🏠 **Local LLMs (Run on Mac M4)**
- **Free** - No API costs
- **Private** - Data stays on your Mac
- **Fast** - No network latency
- **Offline** - Works completely offline
- **Models**: Llama 3, Mistral, CodeLlama, Neural-Chat

### ☁️ **Cloud AI Services (Advanced)**
- **OpenAI GPT-4** - Most capable reasoning
- **Anthropic Claude** - Long context, analysis
- **Cohere** - Fast, cost-effective
- **HuggingFace** - Open source models

---

## 🚀 QUICK START

### **Option 1: Local LLM Only (Recommended for Privacy)**

```bash
# Run the setup wizard
bash /Volumes/Akash\ SSD/repos/jarvis-brain/setup-ai.sh

# Choose option 1 (Local LLM)
# Select model (Mistral recommended)
# Done! Everything configured
```

**What you get:**
- ✅ Ollama installed
- ✅ Mistral/CodeLlama downloaded
- ✅ Running on port 11434
- ✅ Integration configured

### **Option 2: Cloud AI Only (Best Capability)**

```bash
bash /Volumes/Akash\ SSD/repos/jarvis-brain/setup-ai.sh

# Choose option 2 (Cloud AI)
# Add your API keys to .env
# Done!
```

### **Option 3: Hybrid (Best of Both)**

```bash
bash /Volumes/Akash\ SSD/repos/jarvis-brain/setup-ai.sh

# Choose option 3 (Both local and cloud)
# Setup Ollama + add cloud API keys
# Switch between them anytime!
```

---

## 🏠 Local LLM Setup (Mac M4)

### Prerequisites
- Mac mini M4 with at least 8GB RAM
- Ollama installed (or we'll install it)
- ~5-10GB disk space per model

### Installation

```bash
# Option A: Homebrew (recommended)
brew install ollama

# Option B: Direct download
# Visit https://ollama.ai/download/mac
```

### Download Models

```bash
# Most popular (recommended)
ollama pull mistral         # 7B model, balanced

# Code-specific
ollama pull codellama       # 7B for code
ollama pull codellama:13b   # More capable

# Larger models (L1 if you have RAM)
ollama pull llama2:70b      # Very capable but slow

# Chat-optimized
ollama pull neural-chat     # Chat conversations

# Compact (5GB)
ollama pull phi             # Fast, small
```

### Start Ollama Service

```bash
# Background service (stays running)
ollama serve

# Or in a terminal with logs
ollama serve 2>&1 | tee ollama.log
```

**Ollama will be available at:** `http://localhost:11434`

### Test Local Models

```bash
# Test Mistral
ollama run mistral "Explain machine learning in one sentence"

# Test CodeLlama
ollama run codellama "Write Python code to reverse a string"

# View installed models
ollama list

# Remove model if needed
ollama rm mistral
```

---

## ☁️ Cloud AI Setup

### OpenAI (GPT-4 - Recommended)

1. **Get API Key**
   - Visit: https://platform.openai.com/api-keys
   - Click "Create new secret key"
   - Copy the key (starts with `sk-`)

2. **Add to Configuration**
   ```bash
   # Edit .env file
   vi /Volumes/Akash\ SSD/repos/jarvis-brain/.env
   
   # Add:
   AI_TYPE=openai
   OPENAI_API_KEY=sk-...your-key...
   OPENAI_ENABLED=true
   ```

3. **Test Connection**
   ```bash
   # Start Jarvis
   bash /Volumes/Akash\ SSD/repos/jarvis-brain/start-auto.sh
   
   # Backend will show: OpenAI: ✅ Online
   ```

### Claude (Anthropic)

1. **Get API Key**
   - Visit: https://console.anthropic.com
   - Click "Get API key"
   - Copy the key (starts with `sk-ant-`)

2. **Add to Configuration**
   ```bash
   AI_TYPE=anthropic
   ANTHROPIC_API_KEY=sk-ant-...your-key...
   ANTHROPIC_ENABLED=true
   ```

### Cohere

1. **Sign Up**
   - Visit: https://cohere.io

2. **Get API Key**
   - Dashboard → API Keys → Create new

3. **Configure**
   ```bash
   AI_TYPE=cohere
   COHERE_API_KEY=...your-key...
   COHERE_ENABLED=true
   ```

---

## 🔄 Switch Between Providers

### Using the Switch Script

```bash
bash /Volumes/Akash\ SSD/repos/jarvis-brain/switch-ai.sh
```

Choose:
1. **Local LLM** - Mistral, CodeLlama, etc.
2. **OpenAI** - GPT-4
3. **Claude** - Anthropic
4. **Cohere** - Cohere
5. **HuggingFace** - Open source

### Manual Switch

```bash
# Use local LLM
cp /Volumes/Akash\ SSD/repos/jarvis-brain/.env.local \
   /Volumes/Akash\ SSD/repos/jarvis-brain/.env

# Or use cloud AI
cp /Volumes/Akash\ SSD/repos/jarvis-brain/.env.cloud \
   /Volumes/Akash\ SSD/repos/jarvis-brain/.env

# Edit and set your API key
nano /Volumes/Akash\ SSD/repos/jarvis-brain/.env

# Restart Jarvis
bash /Volumes/Akash\ SSD/repos/jarvis-brain/start-auto.sh
```

---

## 📊 Performance Comparison

### Mac M4 Local Llama Performance

```
Model            Size    Memory   Speed        Quality
─────────────────────────────────────────────────────
Phi              3B      2GB      ⚡⚡⚡ Fast   ⭐⭐
Mistral          7B      4-5GB    ⚡⚡ Medium  ⭐⭐⭐
CodeLlama        7B      4-5GB    ⚡⚡ Medium  ⭐⭐⭐
Llama 2          13B     8GB      ⚡ Slow    ⭐⭐⭐⭐
CodeLlama 34B    34B     20GB+    Very Slow   ⭐⭐⭐⭐⭐
```

### Cloud AI Performance

```
Service          Speed           Quality        Cost
───────────────────────────────────────────────────────
OpenAI GPT-4     2-5 sec        ⭐⭐⭐⭐⭐     $$
Claude Opus      1-4 sec        ⭐⭐⭐⭐      $$
Cohere           <1 sec         ⭐⭐⭐       $
Local Mistral    3-10 sec       ⭐⭐⭐       Free
```

---

## 🎯 Task-Specific Recommendations

| Task | Recommended | Reason |
|------|-------------|--------|
| **Code Analysis** | Local CodeLlama | Fast, specialized, free |
| **Bug Fixing** | OpenAI GPT-4 | Complex reasoning needed |
| **Documentation** | Local Mistral | Fast enough, free |
| **Complex Reasoning** | Claude Opus | Long context (200K tokens) |
| **Chat** | Local Neural-Chat | Conversational optimized |
| **Vision/Images** | GPT-4 Vision | Only cloud can do this |
| **Cost-Conscious** | Local Mistral | Free, good quality |

---

## 🔧 Configuration Details

### Local LLM Settings (.env.local)

```bash
# Which Ollama service to use
OLLAMA_BASE_URL=http://localhost:11434

# Different models for different tasks
OLLAMA_MODEL=mistral                # General purpose
OLLAMA_CODE_MODEL=codellama         # Code analysis
OLLAMA_CHAT_MODEL=neural-chat       # Conversation

# Performance tuning for M4
OLLAMA_NUM_THREAD=8                 # M4 has 8 cores
OLLAMA_CONTEXT_SIZE=2048            # Tokens (more = slower)
OLLAMA_MEMORY_FRACTION=0.8           # Use 80% of RAM
```

### Cloud AI Settings (.env.cloud)

```bash
# Primary cloud provider
AI_TYPE=openai

# OpenAI specifics
OPENAI_API_KEY=sk-...               # Your API key
OPENAI_MODEL=gpt-4-turbo-preview    # Model to use
OPENAI_TEMPERATURE=0.7              # 0=focused, 1=creative
OPENAI_MAX_TOKENS=2000              # Response length
```

---

## 🐛 Troubleshooting

### "Ollama connection refused"
```bash
# Check if Ollama is running
lsof -i :11434

# If not, start it
ollama serve

# If still fails, check logs
cat /tmp/ollama.log
```

### "OpenAI authentication failed"
```bash
# Check API key is correct
echo $OPENAI_API_KEY

# Verify in .env file
grep OPENAI_API_KEY /Volumes/Akash\ SSD/repos/jarvis-brain/.env

# Get new key from: https://platform.openai.com/api-keys
```

### "All providers offline"
```bash
# Check backend status
curl http://localhost:8001/api/ai/status

# Start local Ollama if you want local AI
ollama serve

# Or add cloud API key to .env
```

### "Model not found"
```bash
# List installed models
ollama list

# Install missing model
ollama pull mistral

# Or change model name in .env
# OLLAMA_MODEL=mistral
```

---

## 💡 Advanced Configuration

### Hybrid Mode (Local + Cloud Fallback)

```bash
# In .env:
HYBRID_MODE=true
PRIMARY_PROVIDER=local              # Try local first
SECONDARY_PROVIDER=openai           # Fall back to OpenAI
TERTIARY_PROVIDER=anthropic         # Final fallback
```

**How it works:**
1. Try local LLM (fast, free)
2. If local fails → use OpenAI (powerful)
3. If OpenAI fails → use Claude (backup)
4. Pattern analysis (always works)

### Task-Specific Routing

```bash
# In .env:
CODE_ANALYSIS_PROVIDER=local
CODE_GENERATION_PROVIDER=local
REASONING_PROVIDER=openai           # Use cloud for complex tasks
CHAT_PROVIDER=local
VISION_PROVIDER=openai              # Only cloud has vision
```

### Custom Model Parameters

```bash
# For Ollama fine-tuning
OLLAMA_TEMPERATURE=0.5              # Lower = more focused
OLLAMA_TOP_P=0.9                    # Nucleus sampling
OLLAMA_TOP_K=40                     # Top K sampling
```

---

## 📈 Scaling & Optimization

### For Best Performance on M4

1. **Use Mistral (7B) as default**
   - Balanced speed/quality
   - ~5GB RAM
   - CodeLlama for coding tasks

2. **Disable unused models**
   ```bash
   ollama rm llama2:70b    # Remove if not using
   ollama rm codellama:34b # Frees up space
   ```

3. **Optimize context window**
   ```bash
   # .env
   OLLAMA_CONTEXT_SIZE=2048    # Good balance
   # or 4096 if you have 16GB+ RAM
   ```

4. **Run on external GPU (if you add one)**
   ```bash
   # Ollama will auto-detect GPU
   # Very fast with Metal acceleration
   ```

---

## 🎓 Learning Resources

### Local LLMs
- Ollama docs: https://ollama.ai
- Mistral: https://www.mistral.ai
- MetaLlama: https://www.llama.com

### Cloud AI
- OpenAI: https://platform.openai.com/docs
- Anthropic: https://docs.anthropic.com
- Cohere: https://docs.cohere.io

---

## 📞 Support

### Check System Status
```bash
curl http://localhost:8001/api/ai/status
```

**Output:**
```json
{
  "ai_type": "local",
  "services": {
    "ollama": {
      "status": "online",
      "models": ["mistral", "codellama", "neural-chat"]
    }
  }
}
```

### View Logs
```bash
# Backend logs
tail -f /Volumes/Akash\ SSD/repos/jarvis-brain/backend.log

# Ollama logs
tail -f /tmp/ollama.log

# VS Code Jarvis output
# View → Output → Select "Jarvis"
```

---

## 🎯 Getting Started

**For complete privacy & no costs:**
```bash
bash /Volumes/Akash\ SSD/repos/jarvis-brain/setup-ai.sh
# Choose option 1: Local LLM
# Let it download Mistral
# Done!
```

**For best capabilities:**
```bash
bash /Volumes/Akash\ SSD/repos/jarvis-brain/setup-ai.sh
# Choose option 2 or 3
# Add your OpenAI API key
# Switch to OpenAI provider
# Done!
```

**For flexibility (recommended):**
```bash
bash /Volumes/Akash\ SSD/repos/jarvis-brain/setup-ai.sh
# Choose option 3: Both
# Get best of both worlds
# Switch anytime with: bash switch-ai.sh
```

---

## ✨ Summary

| Aspect | Local LLM | Cloud AI |
|--------|-----------|----------|
| **Cost** | Free | Pay per request |
| **Privacy** | 100% | Sent to cloud |
| **Speed** | Medium | Fast |
| **Capability** | Good | Excellent |
| **Offline** | Yes | No |
| **Setup Time** | 15 min | 5 min |
| **Latency** | <1s | 2-5s |

**Choose local for:** Privacy, offline work, cost savings
**Choose cloud for:** Best results, complex tasks, vision

**Best practice:** Use both! Local for speed, cloud for capability.
