# 🤖 How to Configure Your AI in Jarvis Brain

## Quick Start

Your AI configuration is now in **`ai_config.yaml`** - you can edit it directly in VS Code!

### Common Setups

#### Option 1: Using Local Ollama (Recommended for Mac)
```yaml
ai:
  code_analysis:
    type: "ollama"
    url: "http://localhost:11434"  # Change this line only
    model: "mistral"
```

#### Option 2: Using Docker Ollama
```yaml
ai:
  code_analysis:
    type: "ollama"
    url: "http://host.docker.internal:11434"  # For Docker on Mac/Windows
    model: "mistral"
```

#### Option 3: Using OpenAI API
```yaml
ai:
  code_analysis:
    enabled: true
    type: "openai"
    api_key: "${OPENAI_API_KEY}"  # Set environment variable first
    model: "gpt-4"
    timeout: 30
```

#### Option 4: Using Anthropic Claude
```yaml
ai:
  code_analysis:
    enabled: true
    type: "anthropic"
    api_key: "${ANTHROPIC_API_KEY}"
    model: "claude-3-opus"
    timeout: 30
```

## Step-by-Step Instructions

### To Change Your AI Provider:

1. **Open `ai_config.yaml` in VS Code** (Now available in Explorer)
   - Edit the `type:` field to `openai`, `anthropic`, `ollama`, or `local`
   - Update the `url:` or `api_key:` as needed

2. **Set Environment Variables** (if using OpenAI/Anthropic)
   ```bash
   export OPENAI_API_KEY="sk-..."
   export ANTHROPIC_API_KEY="sk-ant-..."
   ```

3. **Restart Jarvis** for changes to take effect

## Checking Your AI Status

Run this command to see which AI services are available:

```bash
cd /Volumes/Akash\ SSD/repos/jarvis-brain
python3 -c "from core.ai_services import ai_manager; import json; print(json.dumps(ai_manager.get_service_info(), indent=2))"
```

## Changing AI Models

Change the `model:` field to any available model:

**For Ollama:**
- `mistral` (fast, good for coding)
- `neural-chat` (conversational)
- `llama2` (general purpose)
- `codellama` (code-specific)

**For OpenAI:**
- `gpt-4`
- `gpt-4-turbo`
- `gpt-3.5-turbo`

**For Anthropic:**
- `claude-3-opus`
- `claude-3-sonnet`
- `claude-3-haiku`

## Troubleshooting

### AI Not Connecting?
Check these in order:
1. Is your AI service running? (Ollama: `ollama serve`, Docker: `docker-compose up`)
2. Is the URL correct? (Local: `localhost`, Docker: `host.docker.internal`)
3. Run status check command above

### Want to Test an AI Quickly?
```bash
python3 -c "
from core.ai_services import ai_manager
ai_manager.check_status()  # Check all services
response = ai_manager.chat_response('Hello!')  # Test chat
print(response)
"
```

## Files You Can Now Edit in VS Code

✅ `ai_config.yaml` - Your AI settings
✅ `.vscode/settings.json` - VS Code settings  
✅ `configs/config.yaml` - General Jarvis config
✅ All Python files with debug/execution support

Happy coding! 🚀
