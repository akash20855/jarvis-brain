"""
Jarvis Brain - Configurable AI Service Handler
Manages AI instances based on ai_config.yaml
"""

import requests
import json
import logging
import os
from typing import Optional, Dict, List
from dataclasses import dataclass
from pathlib import Path
import yaml

logger = logging.getLogger(__name__)


@dataclass
class AIService:
    """AI Service configuration"""
    name: str
    service_id: str
    ai_type: str  # ollama, openai, anthropic, local
    url: Optional[str]
    api_key: Optional[str]
    model: str
    task_type: str
    timeout: int = 30
    status: str = "offline"
    enabled: bool = True


class ConfigurableAIServiceManager:
    """Manages AI services from configuration file"""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize with config file"""
        self.config_path = Path(config_path or "ai_config.yaml")
        self.services: Dict[str, AIService] = {}
        self._load_config()
    
    def _load_config(self):
        """Load AI configuration from YAML file"""
        if not self.config_path.exists():
            logger.warning(f"Config file not found: {self.config_path}")
            self._init_default_services()
            return
        
        try:
            with open(self.config_path, 'r') as f:
                config = yaml.safe_load(f) or {}
            
            ai_config = config.get('ai', {})
            
            # Map service_id to task_type for backward compatibility
            service_type_mapping = {
                'code_analysis': 'code_analysis',
                'chat': 'chat',
                'suggestions': 'suggestions'
            }
            
            for service_id, service_config in ai_config.items():
                if not isinstance(service_config, dict):
                    continue
                
                if not service_config.get('enabled', True):
                    logger.info(f"Skipping disabled service: {service_id}")
                    continue
                
                # Resolve environment variables in api_key
                api_key = service_config.get('api_key')
                if api_key and api_key.startswith('${') and api_key.endswith('}'):
                    env_var = api_key[2:-1]
                    api_key = os.getenv(env_var)
                    if not api_key:
                        logger.warning(f"Environment variable {env_var} not set for {service_id}")
                
                service = AIService(
                    name=service_config.get('description', f'{service_id.replace("_", " ").title()}'),
                    service_id=service_id,
                    ai_type=service_config.get('type', 'ollama'),
                    url=service_config.get('url'),
                    api_key=api_key,
                    model=service_config.get('model', 'mistral'),
                    task_type=service_type_mapping.get(service_id, service_id),
                    timeout=service_config.get('timeout', 30),
                    enabled=service_config.get('enabled', True)
                )
                
                self.services[service_id] = service
                logger.info(f"Loaded service: {service_id} ({service.ai_type})")
            
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            self._init_default_services()
    
    def _init_default_services(self):
        """Fallback to default services if config fails"""
        ollama_base = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
        
        self.services = {
            'code_analysis': AIService(
                name="Code Analysis AI",
                service_id='code_analysis',
                ai_type='ollama',
                url=ollama_base,
                api_key=None,
                model='mistral',
                task_type='code_analysis'
            ),
            'chat': AIService(
                name="Chat AI",
                service_id='chat',
                ai_type='ollama',
                url=ollama_base,
                api_key=None,
                model='neural-chat',
                task_type='chat'
            ),
            'suggestions': AIService(
                name="Suggestion Generator",
                service_id='suggestions',
                ai_type='ollama',
                url=ollama_base,
                api_key=None,
                model='mistral',
                task_type='suggestions'
            )
        }
    
    def check_status(self) -> Dict[str, str]:
        """Check status of all AI services"""
        status = {}
        
        for service_id, service in self.services.items():
            if not service.enabled:
                status[service_id] = "⊘ Disabled"
                continue
            
            try:
                if service.ai_type == 'ollama':
                    response = requests.get(
                        f"{service.url}/api/tags",
                        timeout=2
                    )
                    if response.status_code == 200:
                        service.status = "online"
                        status[service_id] = "✅ Online"
                    else:
                        service.status = "error"
                        status[service_id] = "⚠️ Error"
                        
                elif service.ai_type == 'openai':
                    # Quick check for OpenAI API
                    if service.api_key:
                        service.status = "online"
                        status[service_id] = "✅ OpenAI Ready"
                    else:
                        service.status = "error"
                        status[service_id] = "❌ Missing API Key"
                        
                elif service.ai_type == 'anthropic':
                    if service.api_key:
                        service.status = "online"
                        status[service_id] = "✅ Anthropic Ready"
                    else:
                        service.status = "error"
                        status[service_id] = "❌ Missing API Key"
                        
            except requests.exceptions.ConnectionError:
                service.status = "offline"
                status[service_id] = "🔴 Offline"
            except Exception as e:
                service.status = "error"
                status[service_id] = f"❌ {str(e)[:30]}"
        
        return status
    
    def get_service(self, service_id: str) -> Optional[AIService]:
        """Get a specific service"""
        return self.services.get(service_id)
    
    def analyze_code(self, code: str, filename: str) -> Optional[List[str]]:
        """Use code analysis AI"""
        service = self.get_service('code_analysis')
        
        if not service or not service.enabled or service.status == "offline":
            logger.warning("Code analysis AI offline, using fallback")
            return self._fallback_analysis(code)
        
        try:
            if service.ai_type == 'ollama':
                return self._call_ollama(service, f"Analyze this Python code and suggest improvements:\n\n```python\n{code}\n```")
            elif service.ai_type == 'openai':
                return self._call_openai(service, code, "code_analysis")
            elif service.ai_type == 'anthropic':
                return self._call_anthropic(service, code, "code_analysis")
        except Exception as e:
            logger.error(f"Code analysis error: {e}")
        
        return self._fallback_analysis(code)
    
    def chat_response(self, message: str, context: str = "") -> Optional[str]:
        """Use chat AI"""
        service = self.get_service('chat')
        
        if not service or not service.enabled or service.status == "offline":
            logger.warning("Chat AI offline, using fallback")
            return self._fallback_response(message)
        
        try:
            prompt = f"""You are Jarvis, an AI assistant for code improvement.
{f'Context: {context}' if context else ''}

User: {message}

Provide helpful, concise responses about code improvements."""
            
            if service.ai_type == 'ollama':
                return self._call_ollama_single(service, prompt)
            elif service.ai_type == 'openai':
                return self._call_openai_chat(service, prompt)
            elif service.ai_type == 'anthropic':
                return self._call_anthropic_chat(service, prompt)
        except Exception as e:
            logger.error(f"Chat error: {e}")
        
        return self._fallback_response(message)
    
    def _call_ollama(self, service: AIService, prompt: str) -> List[str]:
        """Call Ollama API"""
        response = requests.post(
            f"{service.url}/api/generate",
            json={
                "model": service.model,
                "prompt": prompt,
                "stream": False
            },
            timeout=service.timeout
        )
        
        if response.status_code == 200:
            result = response.json()
            suggestions = result.get('response', '').split('\n')
            return [s.strip() for s in suggestions if s.strip()]
        
        return []
    
    def _call_ollama_single(self, service: AIService, prompt: str) -> str:
        """Call Ollama for single response"""
        response = requests.post(
            f"{service.url}/api/generate",
            json={
                "model": service.model,
                "prompt": prompt,
                "stream": False
            },
            timeout=service.timeout
        )
        
        if response.status_code == 200:
            return response.json().get('response', '')
        return ""
    
    def _call_openai(self, service: AIService, code: str, task: str) -> List[str]:
        """Call OpenAI API"""
        # Placeholder - implement based on OpenAI docs
        logger.info(f"OpenAI {task} not yet implemented")
        return self._fallback_analysis(code)
    
    def _call_openai_chat(self, service: AIService, prompt: str) -> str:
        """Call OpenAI Chat API"""
        logger.info("OpenAI chat not yet implemented")
        return self._fallback_response(prompt)
    
    def _call_anthropic(self, service: AIService, code: str, task: str) -> List[str]:
        """Call Anthropic Claude API"""
        try:
            import anthropic
            
            client = anthropic.Anthropic(api_key=service.api_key)
            
            prompt = f"""You are an expert code analyst. Analyze this code and provide 3-5 specific, actionable improvement suggestions.

Task: {task}
Code:
```
{code}
```

Provide each suggestion as a separate line starting with a dash (-). Be concise and focus on real improvements."""
            
            message = client.messages.create(
                model=service.model,
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}]
            )
            
            response = message.content[0].text
            suggestions = [s.strip() for s in response.split('\n') if s.strip().startswith('-')]
            
            return suggestions or ["Code looks good!"] 
        except ImportError:
            logger.error("anthropic package not installed. Install with: pip install anthropic")
            return self._fallback_analysis(code)
        except Exception as e:
            logger.error(f"Anthropic API error: {e}")
            return self._fallback_analysis(code)
    
    def _call_anthropic_chat(self, service: AIService, prompt: str) -> str:
        """Call Anthropic Claude Chat API"""
        try:
            import anthropic
            
            client = anthropic.Anthropic(api_key=service.api_key)
            
            message = client.messages.create(
                model=service.model,
                max_tokens=2048,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return message.content[0].text
        except ImportError:
            logger.error("anthropic package not installed. Install with: pip install anthropic")
            return self._fallback_response(prompt)
        except Exception as e:
            logger.error(f"Anthropic API error: {e}")
            return self._fallback_response(prompt)
    
    def _fallback_analysis(self, code: str) -> List[str]:
        """Fallback analysis without AI"""
        suggestions = []
        
        if ".append(" in code and "for " in code:
            suggestions.append("Use list comprehension instead of append in loop")
        
        if "eval(" in code or "exec(" in code:
            suggestions.append("SECURITY: Replace eval/exec with safe alternatives")
        
        if len(code.split('\n')) > 100:
            suggestions.append("Function is long - consider splitting into smaller functions")
        
        return suggestions or ["Code looks good!"]
    
    def _fallback_response(self, message: str) -> str:
        """Fallback chat response"""
        keywords = {
            "performance": "Performance optimization: Use list comprehensions, avoid nested loops",
            "security": "Security best practices: Avoid eval/exec, validate input",
            "refactor": "Refactoring tips: Keep functions small, extract methods",
        }
        
        for keyword, response in keywords.items():
            if keyword.lower() in message.lower():
                return response
        
        return "I'm here to help with code improvements!"
    
    def get_service_info(self) -> Dict:
        """Get all service information"""
        return {
            "config_file": str(self.config_path),
            "config_exists": self.config_path.exists(),
            "services": [
                {
                    "id": service.service_id,
                    "name": service.name,
                    "type": service.ai_type,
                    "model": service.model,
                    "status": service.status,
                    "enabled": service.enabled
                }
                for service in self.services.values()
            ],
            "all_online": all(s.status == "online" for s in self.services.values() if s.enabled),
            "any_offline": any(s.status == "offline" for s in self.services.values() if s.enabled)
        }
    
    def reload_config(self):
        """Reload configuration from file"""
        self.services.clear()
        self._load_config()
        logger.info("Configuration reloaded")


# Global instance
ai_manager = ConfigurableAIServiceManager()
