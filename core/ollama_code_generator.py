"""
Ollama Code Generator Module
Provides Claude-like code generation using locally-hosted Ollama models
100% free, no API keys needed, runs entirely on your Mac
"""

import json
import subprocess
import time
from typing import List, Optional

import requests


class OllamaCodeGenerator:
    """Generate and analyze code using Ollama (local models)"""

    def __init__(self, model: str = "llama2", host: str = "localhost", port: int = 11434):
        """
        Initialize Ollama code generator
        
        Args:
            model: Model name (llama2, mistral, neural-chat, etc.)
            host: Ollama server host (default: localhost)
            port: Ollama server port (default: 11434)
        """
        self.model = model
        self.host = host
        self.port = port
        self.base_url = f"http://{host}:{port}"
        self.is_available = False
        self._check_ollama()

    def _check_ollama(self) -> bool:
        """Check if Ollama server is running and accessible"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=2)
            if response.status_code == 200:
                self.is_available = True
                print(f"✓ Ollama server is running at {self.base_url}")
                return True
        except:
            pass
        
        self.is_available = False
        print(f"✗ Ollama server not found at {self.base_url}")
        print(f"  Start Ollama with: ollama serve")
        return False

    def _extract_text(self, response_text: str) -> str:
        """Extract text from streaming response"""
        lines = response_text.strip().split('\n')
        full_text = ""
        for line in lines:
            if line:
                try:
                    data = json.loads(line)
                    if 'response' in data:
                        full_text += data['response']
                except:
                    pass
        return full_text

    def generate_code(self, description: str, language: str = "python") -> dict:
        """
        Generate code from natural language description
        
        Args:
            description: What code to generate
            language: Programming language (python, javascript, etc.)
            
        Returns:
            dict with 'code', 'explanation', and 'language'
        """
        if not self.is_available:
            return {
                'code': '',
                'explanation': 'Ollama server not running. Start with: ollama serve',
                'language': language,
                'error': True
            }

        prompt = f"""You are an expert programmer. Generate {language} code that does this:

{description}

Provide ONLY the code, no explanations. The code should be:
- Complete and runnable
- Well-structured
- Include helpful comments

Code:"""

        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": True,
                    "temperature": 0.7,
                },
                stream=True,
                timeout=120
            )

            if response.status_code != 200:
                return {
                    'code': '',
                    'explanation': f'Ollama error: {response.status_code}',
                    'language': language,
                    'error': True
                }

            code = ""
            for line in response.iter_lines():
                if line:
                    try:
                        data = json.loads(line)
                        if 'response' in data:
                            code += data['response']
                    except:
                        pass

            return {
                'code': code.strip(),
                'explanation': f'Generated {language} code using Ollama ({self.model})',
                'language': language,
                'error': False
            }

        except Exception as e:
            return {
                'code': '',
                'explanation': f'Error generating code: {str(e)}',
                'language': language,
                'error': True
            }

    def analyze_code(self, code: str) -> dict:
        """
        Analyze code for issues, style, and improvements
        
        Args:
            code: Code to analyze
            
        Returns:
            dict with analysis results
        """
        if not self.is_available:
            return {
                'analysis': 'Ollama server not running',
                'issues': [],
                'suggestions': [],
                'error': True
            }

        prompt = f"""Analyze this code and provide:
1. Any issues or bugs
2. Code quality suggestions
3. Performance improvements

Code:
```
{code}
```

Provide a concise analysis."""

        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": True,
                    "temperature": 0.5,
                },
                stream=True,
                timeout=120
            )

            analysis = ""
            for line in response.iter_lines():
                if line:
                    try:
                        data = json.loads(line)
                        if 'response' in data:
                            analysis += data['response']
                    except:
                        pass

            return {
                'analysis': analysis.strip(),
                'issues': [],
                'suggestions': [],
                'error': False
            }

        except Exception as e:
            return {
                'analysis': f'Error analyzing code: {str(e)}',
                'issues': [],
                'suggestions': [],
                'error': True
            }

    def explain_code(self, code: str) -> dict:
        """
        Explain what code does
        
        Args:
            code: Code to explain
            
        Returns:
            dict with explanation
        """
        if not self.is_available:
            return {
                'explanation': 'Ollama server not running',
                'error': True
            }

        prompt = f"""Explain what this code does in simple terms:

```
{code}
```

Provide a clear, concise explanation."""

        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": True,
                    "temperature": 0.5,
                },
                stream=True,
                timeout=120
            )

            explanation = ""
            for line in response.iter_lines():
                if line:
                    try:
                        data = json.loads(line)
                        if 'response' in data:
                            explanation += data['response']
                    except:
                        pass

            return {
                'explanation': explanation.strip(),
                'error': False
            }

        except Exception as e:
            return {
                'explanation': f'Error explaining code: {str(e)}',
                'error': True
            }

    def generate_test(self, code: str, language: str = "python") -> dict:
        """
        Generate test cases for code
        
        Args:
            code: Code to test
            language: Programming language
            
        Returns:
            dict with test code
        """
        if not self.is_available:
            return {
                'tests': '',
                'explanation': 'Ollama server not running',
                'error': True
            }

        if language == "python":
            test_framework = "pytest"
        elif language == "javascript":
            test_framework = "jest"
        else:
            test_framework = "standard tests"

        prompt = f"""Generate {test_framework} test cases for this {language} code:

```
{code}
```

Provide ONLY the test code, ready to run:"""

        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": True,
                    "temperature": 0.7,
                },
                stream=True,
                timeout=120
            )

            tests = ""
            for line in response.iter_lines():
                if line:
                    try:
                        data = json.loads(line)
                        if 'response' in data:
                            tests += data['response']
                    except:
                        pass

            return {
                'tests': tests.strip(),
                'explanation': f'Generated {test_framework} tests',
                'error': False
            }

        except Exception as e:
            return {
                'tests': '',
                'explanation': f'Error generating tests: {str(e)}',
                'error': True
            }

    def refactor_code(self, code: str, language: str = "python") -> dict:
        """
        Refactor code for better quality
        
        Args:
            code: Code to refactor
            language: Programming language
            
        Returns:
            dict with refactored code
        """
        if not self.is_available:
            return {
                'code': '',
                'explanation': 'Ollama server not running',
                'error': True
            }

        prompt = f"""Refactor this {language} code to be cleaner and more maintainable:

```
{code}
```

Provide ONLY the refactored code:"""

        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": True,
                    "temperature": 0.7,
                },
                stream=True,
                timeout=120
            )

            refactored = ""
            for line in response.iter_lines():
                if line:
                    try:
                        data = json.loads(line)
                        if 'response' in data:
                            refactored += data['response']
                    except:
                        pass

            return {
                'code': refactored.strip(),
                'explanation': 'Code refactored for better quality',
                'error': False
            }

        except Exception as e:
            return {
                'code': '',
                'explanation': f'Error refactoring code: {str(e)}',
                'error': True
            }

    def status(self) -> dict:
        """Get Ollama server status"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=2)
            if response.status_code == 200:
                data = response.json()
                return {
                    'status': 'running',
                    'model': self.model,
                    'available_models': len(data.get('models', [])),
                    'url': f"{self.base_url}"
                }
        except:
            pass

        return {
            'status': 'not_running',
            'model': self.model,
            'message': 'Start Ollama with: ollama serve',
            'help': 'Download from https://ollama.ai'
        }


# Example usage
if __name__ == "__main__":
    # Initialize with Ollama
    generator = OllamaCodeGenerator(model="llama2")

    # Check status
    print("Status:", generator.status())
    print()

    # Generate code
    if generator.is_available:
        print("Generating Python function...")
        result = generator.generate_code(
            "Create a function that returns fibonacci numbers up to n",
            language="python"
        )
        print("Generated code:")
        print(result['code'])
        print()

        # Analyze the generated code
        print("Analyzing code...")
        analysis = generator.analyze_code(result['code'])
        print("Analysis:")
        print(analysis['analysis'])
    else:
        print("Please start Ollama first:")
        print("  1. Download from https://ollama.ai")
        print("  2. Run: ollama serve")
        print("  3. In another terminal: ollama pull llama2")
