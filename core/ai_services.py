"""
Jarvis Brain - Separate AI Service Handler
Manages independent AI instances for different tasks
"""

import requests
import json
import logging
import os
from typing import Optional, Dict, List
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class AIService:
    """AI Service configuration"""
    name: str
    url: str
    model: str
    task_type: str  # code_analysis, chat, suggestions
    status: str = "offline"  # online, offline, error


class AIServiceManager:
    """Manages separate AI instances"""
    
    def __init__(self):
        self.services: Dict[str, AIService] = {}
        self._init_services()
    
    def _init_services(self):
        """Initialize AI services"""
        
        # Get Ollama URLs from environment or use defaults
        # For Docker on macOS/Windows: use host.docker.internal
        # For local/Linux: use localhost
        ollama_base = os.getenv('OLLAMA_BASE_URL', 'http://host.docker.internal:11434')
        ollama_chat = os.getenv('OLLAMA_CHAT_URL', 'http://host.docker.internal:11435')
        ollama_suggestions = os.getenv('OLLAMA_SUGGESTIONS_URL', 'http://host.docker.internal:11436')
        
        # Code Analysis AI (Ollama instance 1)
        self.services['code_analysis'] = AIService(
            name="Code Analysis AI",
            url=ollama_base,
            model="mistral",
            task_type="code_analysis"
        )
        
        # Chat AI (Ollama instance 2 or Copilot)
        self.services['chat'] = AIService(
            name="Chat AI",
            url=ollama_chat,
            model="neural-chat",
            task_type="chat"
        )
        
        # Suggestion Generator (Local or Ollama instance 3)
        self.services['suggestions'] = AIService(
            name="Suggestion Generator",
            url=ollama_suggestions,
            model="mistral",
            task_type="suggestions"
        )
    
    def check_status(self) -> Dict[str, str]:
        """Check status of all AI services"""
        status = {}
        
        for service_id, service in self.services.items():
            try:
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
            except requests.exceptions.ConnectionError:
                service.status = "offline"
                status[service_id] = "🔴 Offline"
            except Exception as e:
                service.status = "error"
                status[service_id] = f"❌ {str(e)[:30]}"
        
        return status
    
    def analyze_code(self, code: str, filename: str) -> Optional[List[str]]:
        """Use dedicated code analysis AI"""
        service = self.services.get('code_analysis')
        
        if not service or service.status == "offline":
            logger.warning("Code analysis AI offline, using fallback")
            return self._fallback_analysis(code)
        
        try:
            prompt = f"""Analyze this Python code and suggest 2-3 improvements:

```python
{code}
```

Focus on:
- Performance issues
- Security vulnerabilities
- Code quality issues

Give specific, actionable suggestions."""
            
            response = requests.post(
                f"{service.url}/api/generate",
                json={
                    "model": service.model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                suggestions = result.get('response', '').split('\n')
                return [s.strip() for s in suggestions if s.strip()]
        
        except Exception as e:
            logger.error(f"Code analysis error: {e}")
        
        return self._fallback_analysis(code)
    
    def chat_response(self, message: str, context: str = "") -> Optional[str]:
        """Use dedicated chat AI"""
        service = self.services.get('chat')
        
        if not service or service.status == "offline":
            logger.warning("Chat AI offline, using fallback")
            return self._fallback_response(message)
        
        try:
            prompt = f"""You are Jarvis, an AI assistant for code improvement.
{f'Context: {context}' if context else ''}

User: {message}

Provide helpful, concise responses about code improvements."""
            
            response = requests.post(
                f"{service.url}/api/generate",
                json={
                    "model": service.model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', '')
        
        except Exception as e:
            logger.error(f"Chat error: {e}")
        
        return self._fallback_response(message)
    
    def generate_suggestions(self, files_data: Dict) -> List[str]:
        """Use dedicated suggestion generator AI"""
        service = self.services.get('suggestions')
        
        if not service or service.status == "offline":
            logger.warning("Suggestion AI offline, using fallback")
            return self._fallback_suggestions()
        
        try:
            prompt = f"""Based on the following code files, provide top 5 improvement suggestions:

{json.dumps(files_data, indent=2)[:1000]}...

Give specific, prioritized improvements."""
            
            response = requests.post(
                f"{service.url}/api/generate",
                json={
                    "model": service.model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                suggestions = result.get('response', '').split('\n')
                return [s.strip() for s in suggestions if s.strip()]
        
        except Exception as e:
            logger.error(f"Suggestion generation error: {e}")
        
        return self._fallback_suggestions()
    
    def _fallback_analysis(self, code: str) -> List[str]:
        """Fallback code analysis without AI"""
        suggestions = []
        
        # Pattern-based analysis
        if ".append(" in code and "for " in code:
            suggestions.append("Use list comprehension instead of append in loop - 2-3x faster")
        
        if "eval(" in code or "exec(" in code:
            suggestions.append("SECURITY: Replace eval/exec with ast.literal_eval or json.loads")
        
        if len(code.split('\n')) > 100:
            suggestions.append("Function is long - consider splitting into smaller functions")
        
        if "TODO" in code or "FIXME" in code:
            suggestions.append("Remove TODO/FIXME comments - use issue tracking instead")
        
        return suggestions or ["Code looks good!"]
    
    def _fallback_response(self, message: str) -> str:
        """Fallback chat response"""
        keywords = {
            "performance": "Performance optimization: Use list comprehensions, avoid nested loops, cache results",
            "security": "Security best practices: Avoid eval/exec, validate input, use parameterized queries",
            "refactor": "Refactoring tips: Keep functions small, extract methods, follow DRY principle",
            "help": "Available commands: analyze, file <path>, suggestions, status, history"
        }
        
        for keyword, response in keywords.items():
            if keyword.lower() in message.lower():
                return response
        
        return "I'm here to help with code improvements! Try asking about performance, security, or refactoring."
    
    def _fallback_suggestions(self) -> List[str]:
        """Fallback suggestions without AI"""
        return [
            "Use list comprehensions for better performance",
            "Add type hints for better code clarity",
            "Extract long functions into smaller modules",
            "Add docstrings to document code",
            "Use meaningful variable names"
        ]
    
    def get_service_info(self) -> Dict:
        """Get all service information"""
        return {
            "services": [
                {
                    "id": service_id,
                    "name": service.name,
                    "url": service.url,
                    "model": service.model,
                    "task_type": service.task_type,
                    "status": service.status
                }
                for service_id, service in self.services.items()
            ],
            "all_online": all(s.status == "online" for s in self.services.values()),
            "fallback_active": any(s.status == "offline" for s in self.services.values())
        }


# Global instance
ai_manager = AIServiceManager()
