"""
Jarvis Brain - Unified AI Provider Manager
Supports local LLMs (Ollama) + Cloud AI (OpenAI, Claude, Cohere, HuggingFace)
"""

import requests
import json
import logging
import os
from typing import Optional, Dict, List, Tuple
from dataclasses import dataclass
from datetime import datetime
import time

logger = logging.getLogger(__name__)


@dataclass
class AIProviderConfig:
    """AI Provider configuration"""
    provider_type: str  # local, openai, anthropic, cohere, huggingface
    name: str
    status: str = "unknown"  # online, offline, error, unconfigured
    response_time: float = 0.0
    last_checked: Optional[datetime] = None
    error_message: Optional[str] = None


class UnifiedAIProvider:
    """
    Unified AI provider manager supporting multiple backends.
    Automatically selects best available provider with fallback chain.
    """
    
    def __init__(self):
        """Initialize AI provider manager"""
        self.providers: Dict[str, AIProviderConfig] = {}
        self.provider_clients: Dict[str, object] = {}
        self._init_providers()
        self._check_all_providers()
    
    def _init_providers(self):
        """Initialize all configured providers"""
        
        # LOCAL LLM (Ollama)
        if os.getenv('LOCAL_LLM_ENABLED', 'true').lower() == 'true':
            self.providers['local'] = AIProviderConfig(
                provider_type='local',
                name='Local LLM (Ollama)',
            )
        
        # OPENAI
        if os.getenv('OPENAI_API_KEY'):
            self.providers['openai'] = AIProviderConfig(
                provider_type='openai',
                name='OpenAI (GPT-4)',
            )
        
        # ANTHROPIC
        if os.getenv('ANTHROPIC_API_KEY'):
            self.providers['anthropic'] = AIProviderConfig(
                provider_type='anthropic',
                name='Anthropic (Claude)',
            )
        
        # COHERE
        if os.getenv('COHERE_API_KEY'):
            self.providers['cohere'] = AIProviderConfig(
                provider_type='cohere',
                name='Cohere',
            )
        
        # HUGGINGFACE
        if os.getenv('HUGGINGFACE_API_KEY'):
            self.providers['huggingface'] = AIProviderConfig(
                provider_type='huggingface',
                name='HuggingFace',
            )
        
        logger.info(f"✅ Initialized providers: {list(self.providers.keys())}")
    
    def _check_all_providers(self):
        """Check status of all providers"""
        for provider_id, config in self.providers.items():
            self._check_provider(provider_id)
    
    def _check_provider(self, provider_id: str) -> bool:
        """Check if a specific provider is online"""
        config = self.providers.get(provider_id)
        if not config:
            return False
        
        try:
            start_time = time.time()
            
            if provider_id == 'local':
                response = requests.get(
                    f"{os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')}/api/tags",
                    timeout=2
                )
                is_online = response.status_code == 200
            
            elif provider_id == 'openai':
                # Check if API key works (without making a request)
                is_online = bool(os.getenv('OPENAI_API_KEY'))
            
            elif provider_id == 'anthropic':
                is_online = bool(os.getenv('ANTHROPIC_API_KEY'))
            
            elif provider_id == 'cohere':
                is_online = bool(os.getenv('COHERE_API_KEY'))
            
            elif provider_id == 'huggingface':
                is_online = bool(os.getenv('HUGGINGFACE_API_KEY'))
            
            else:
                is_online = False
            
            response_time = time.time() - start_time
            config.status = 'online' if is_online else 'offline'
            config.response_time = response_time
            config.last_checked = datetime.now()
            
            return is_online
        
        except Exception as e:
            config.status = 'error'
            config.error_message = str(e)
            config.last_checked = datetime.now()
            return False
    
    def get_best_provider(self, task_type: str = 'general') -> Optional[str]:
        """Get best available provider for task type"""
        
        # Task-specific provider preferences
        preferences = {
            'code_analysis': ['local', 'openai', 'anthropic'],
            'code_generation': ['local', 'openai', 'anthropic'],
            'reasoning': ['openai', 'anthropic', 'local'],
            'vision': ['openai'],  # Only OpenAI has vision
            'chat': ['local', 'anthropic', 'openai'],
            'general': ['local', 'openai', 'anthropic', 'cohere'],
        }
        
        # Get preferred order for task type
        preferred_order = preferences.get(task_type, preferences['general'])
        
        # Check each preferred provider in order
        for provider_id in preferred_order:
            if provider_id in self.providers:
                if self._check_provider(provider_id):
                    logger.info(f"Using {provider_id} for {task_type}")
                    return provider_id
        
        # Return primary provider if configured
        primary = os.getenv('PRIMARY_PROVIDER', 'local')
        if primary in self.providers and self.providers[primary].status == 'online':
            return primary
        
        # Return any available provider
        for provider_id, config in self.providers.items():
            if config.status == 'online':
                return provider_id
        
        logger.warning(f"No online providers for {task_type}")
        return None
    
    def analyze_code(self, code: str, filename: str) -> Optional[Dict]:
        """Analyze code using best available provider"""
        
        # Use code-specific provider
        provider_id = self.get_best_provider('code_analysis')
        if not provider_id:
            return self._fallback_analysis(code)
        
        if provider_id == 'local':
            return self._analyze_with_ollama(code, filename)
        elif provider_id == 'openai':
            return self._analyze_with_openai(code, filename)
        elif provider_id == 'anthropic':
            return self._analyze_with_anthropic(code, filename)
        else:
            return self._fallback_analysis(code)
    
    def _analyze_with_ollama(self, code: str, filename: str) -> Optional[Dict]:
        """Analyze code using local Ollama"""
        try:
            ollama_url = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
            model = os.getenv('OLLAMA_CODE_MODEL', 'codellama')
            
            prompt = f"""Analyze this {filename} code for issues, improvements, and best practices:

{code}

Provide:
1. Issues found
2. Performance improvements
3. Security concerns
4. Code quality suggestions
5. Best practices violations"""
            
            response = requests.post(
                f"{ollama_url}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "provider": "local_ollama",
                    "model": model,
                    "analysis": result.get('response', ''),
                    "timestamp": datetime.now().isoformat(),
                    "success": True
                }
        except Exception as e:
            logger.error(f"Ollama analysis failed: {e}")
        
        return None
    
    def _analyze_with_openai(self, code: str, filename: str) -> Optional[Dict]:
        """Analyze code using OpenAI"""
        try:
            import openai
            
            openai.api_key = os.getenv('OPENAI_API_KEY')
            model = os.getenv('OPENAI_CODE_MODEL', 'gpt-4-turbo-preview')
            
            response = openai.ChatCompletion.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert code reviewer. Analyze code and provide detailed feedback."
                    },
                    {
                        "role": "user",
                        "content": f"""Analyze this {filename} code for issues:

{code}

Provide structured feedback on:
1. Issues
2. Improvements
3. Security
4. Quality"""
                    }
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            return {
                "provider": "openai",
                "model": model,
                "analysis": response.choices[0].message.content,
                "timestamp": datetime.now().isoformat(),
                "success": True
            }
        except Exception as e:
            logger.error(f"OpenAI analysis failed: {e}")
        
        return None
    
    def _analyze_with_anthropic(self, code: str, filename: str) -> Optional[Dict]:
        """Analyze code using Anthropic Claude"""
        try:
            import anthropic
            
            client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
            model = os.getenv('ANTHROPIC_MODEL', 'claude-3-opus-20240229')
            
            response = client.messages.create(
                model=model,
                max_tokens=2048,
                messages=[
                    {
                        "role": "user",
                        "content": f"""Analyze this {filename} code:

{code}

Provide detailed analysis on issues, improvements, and best practices."""
                    }
                ]
            )
            
            return {
                "provider": "anthropic",
                "model": model,
                "analysis": response.content[0].text,
                "timestamp": datetime.now().isoformat(),
                "success": True
            }
        except Exception as e:
            logger.error(f"Anthropic analysis failed: {e}")
        
        return None
    
    def _fallback_analysis(self, code: str) -> Dict:
        """Fallback pattern-based analysis when AI is unavailable"""
        issues = []
        
        # Pattern-based detection
        if 'import *' in code:
            issues.append("⚠️ Avoid wildcard imports")
        if '   ' in code:  # 3 spaces
            issues.append("⚠️ Inconsistent indentation (use 2 or 4 spaces)")
        if len(code.split('\n')) > 500:
            issues.append("⚠️ File too long (>500 lines)")
        if 'TODO' in code:
            issues.append("📝 Contains TODO comments")
        if 'FIXME' in code:
            issues.append("🐛 Contains FIXME comments")
        if 'print(' in code and 'logging' not in code:
            issues.append("⚠️ Uses print() instead of logging")
        
        return {
            "provider": "fallback_pattern_analysis",
            "issues": issues,
            "timestamp": datetime.now().isoformat(),
            "note": "Pattern-based analysis (AI unavailable)"
        }
    
    def get_status(self) -> Dict:
        """Get status of all providers"""
        status = {}
        for provider_id, config in self.providers.items():
            status[provider_id] = {
                "name": config.name,
                "status": config.status,
                "response_time": f"{config.response_time:.3f}s" if config.response_time else "N/A",
                "last_checked": config.last_checked.isoformat() if config.last_checked else "Never"
            }
        
        # Add best provider recommendation
        best_provider = self.get_best_provider('general')
        status['recommended'] = best_provider or 'fallback_only'
        
        return status
    
    def generate_code(self, description: str, language: str = 'python') -> Optional[str]:
        """Generate code using best available provider"""
        provider_id = self.get_best_provider('code_generation')
        if not provider_id:
            return None
        
        try:
            if provider_id == 'local':
                ollama_url = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
                model = os.getenv('OLLAMA_CODE_MODEL', 'codellama')
                
                response = requests.post(
                    f"{ollama_url}/api/generate",
                    json={
                        "model": model,
                        "prompt": f"Write {language} code: {description}",
                        "stream": False
                    },
                    timeout=60
                )
                
                if response.status_code == 200:
                    return response.json().get('response')
            
            elif provider_id == 'openai':
                import openai
                openai.api_key = os.getenv('OPENAI_API_KEY')
                
                response = openai.ChatCompletion.create(
                    model='gpt-4-turbo-preview',
                    messages=[{"role": "user", "content": f"Write {language}: {description}"}],
                    max_tokens=2000
                )
                return response.choices[0].message.content
        
        except Exception as e:
            logger.error(f"Code generation failed: {e}")
        
        return None


# Global instance
_provider_instance = None


def get_ai_provider() -> UnifiedAIProvider:
    """Get singleton AI provider instance"""
    global _provider_instance
    if _provider_instance is None:
        _provider_instance = UnifiedAIProvider()
    return _provider_instance


def check_provider_health() -> Dict:
    """Check health of all AI providers"""
    provider = get_ai_provider()
    return provider.get_status()


def analyze_code_best(code: str, filename: str) -> Optional[Dict]:
    """Analyze code using best available provider"""
    provider = get_ai_provider()
    return provider.analyze_code(code, filename)
