"""
Groq Code Generator Module
Uses Groq API for fast, free code generation and analysis
No installation needed, just provide your free API key
"""

import logging
import os
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class GroqCodeGenerator:
    """Generate and analyze code using Groq API (free & fast)"""

    def __init__(self, api_key: Optional[str] = None, model: str = "llama-3.3-70b-versatile"):
        """
        Initialize Groq Code Generator
        
        Args:
            api_key: Groq API key (or use GROQ_API_KEY env var)
            model: Groq model to use (default: llama-3.3-70b-versatile - latest free powerful model)
        """
        self.api_key = api_key or os.getenv('GROQ_API_KEY')
        self.model = model
        
        if not self.api_key:
            raise ValueError(
                "GROQ_API_KEY not set. Set it with: "
                "export GROQ_API_KEY='gsk-...'\n"
                "Get free key from: https://console.groq.com/keys"
            )
        
        try:
            from groq import Groq
            self.client = Groq(api_key=self.api_key)
            logger.info(f"✓ Groq initialized with model: {self.model}")
        except ImportError:
            logger.error("groq package not installed. Install with: pip install groq")
            raise

    def generate_code(self, description: str, language: str = "python") -> Dict:
        """
        Generate code from natural language description
        
        Args:
            description: What code to generate
            language: Programming language (python, javascript, etc.)
            
        Returns:
            dict with generated code
        """
        try:
            prompt = f"""Generate {language} code that does the following:

{description}

Requirements:
- Provide ONLY the code in a code block
- Make it complete and runnable
- Include helpful comments
- Follow {language} best practices"""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=2048,
            )
            
            code = response.choices[0].message.content
            # Extract code from markdown if needed
            if "```" in code:
                parts = code.split("```")
                code = parts[1] if len(parts) > 1 else code
                if code.startswith(language):
                    code = code[len(language):].lstrip("\n")
                if code.endswith("```"):
                    code = code[:-3]
            
            return {
                "success": True,
                "code": code.strip(),
                "language": language
            }
        except Exception as e:
            logger.error(f"Code generation error: {e}")
            return {
                "success": False,
                "error": str(e),
                "language": language
            }

    def analyze_code(self, code: str, language: str = "python") -> Dict:
        """
        Analyze code for issues and improvements
        
        Args:
            code: Code to analyze
            language: Programming language
            
        Returns:
            dict with analysis
        """
        try:
            prompt = f"""Analyze this {language} code and provide:
1. Any bugs or issues
2. Code quality suggestions
3. Performance improvements

Code:
```{language}
{code}
```

Provide a concise, structured analysis."""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5,
                max_tokens=1024,
            )
            
            analysis = response.choices[0].message.content
            
            return {
                "success": True,
                "analysis": analysis,
                "language": language
            }
        except Exception as e:
            logger.error(f"Code analysis error: {e}")
            return {
                "success": False,
                "error": str(e),
                "language": language
            }

    def explain_code(self, code: str, language: str = "python") -> Dict:
        """
        Explain what code does
        
        Args:
            code: Code to explain
            language: Programming language
            
        Returns:
            dict with explanation
        """
        try:
            prompt = f"""Explain what this {language} code does in clear, simple terms:

```{language}
{code}
```

Explain:
1. The main purpose
2. How it works step by step
3. Key functions or classes used"""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5,
                max_tokens=1024,
            )
            
            explanation = response.choices[0].message.content
            
            return {
                "success": True,
                "explanation": explanation,
                "language": language
            }
        except Exception as e:
            logger.error(f"Code explanation error: {e}")
            return {
                "success": False,
                "error": str(e),
                "language": language
            }

    def generate_test(self, code: str, language: str = "python") -> Dict:
        """
        Generate unit tests for code
        
        Args:
            code: Code to generate tests for
            language: Programming language
            
        Returns:
            dict with generated tests
        """
        try:
            prompt = f"""Generate comprehensive unit tests for this {language} code.
Use the best testing framework for {language}.
Include edge cases and error conditions.

Code to test:
```{language}
{code}
```

Generate only the test code in a code block."""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=2048,
            )
            
            tests = response.choices[0].message.content
            # Extract code from markdown if needed
            if "```" in tests:
                parts = tests.split("```")
                tests = parts[1] if len(parts) > 1 else tests
                if tests.startswith(language):
                    tests = tests[len(language):].lstrip("\n")
                if tests.endswith("```"):
                    tests = tests[:-3]
            
            return {
                "success": True,
                "tests": tests.strip(),
                "language": language
            }
        except Exception as e:
            logger.error(f"Test generation error: {e}")
            return {
                "success": False,
                "error": str(e),
                "language": language
            }

    def refactor_code(self, code: str, language: str = "python", style: str = "clean") -> Dict:
        """
        Refactor code according to best practices
        
        Args:
            code: Code to refactor
            language: Programming language
            style: Refactoring style (clean, performance, readability)
            
        Returns:
            dict with refactored code
        """
        try:
            prompt = f"""Refactor this {language} code for {style} code style.
Apply best practices and modern patterns.

Original code:
```{language}
{code}
```

Provide the refactored code in a code block."""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.6,
                max_tokens=2048,
            )
            
            refactored = response.choices[0].message.content
            # Extract code from markdown if needed
            if "```" in refactored:
                parts = refactored.split("```")
                refactored = parts[1] if len(parts) > 1 else refactored
                if refactored.startswith(language):
                    refactored = refactored[len(language):].lstrip("\n")
                if refactored.endswith("```"):
                    refactored = refactored[:-3]
            
            return {
                "success": True,
                "refactored": refactored.strip(),
                "language": language,
                "style": style
            }
        except Exception as e:
            logger.error(f"Code refactoring error: {e}")
            return {
                "success": False,
                "error": str(e),
                "language": language
            }

    def status(self) -> Dict:
        """Get status of Groq connection"""
        try:
            # Test the API with a simple request
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "test"}],
                temperature=0.5,
                max_tokens=10,
            )
            
            if response.choices[0].message.content:
                return {
                    "status": "online",
                    "model": self.model,
                    "backend": "groq",
                    "success": True
                }
        except Exception as e:
            logger.warning(f"Groq status check failed: {e}")
        
        return {
            "status": "offline",
            "backend": "groq",
            "success": False,
            "error": "Unable to connect to Groq API"
        }
