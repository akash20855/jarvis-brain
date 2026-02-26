"""
Claude Code Generator - Uses Claude Haiku 4.5 for code generation and analysis
Built-in AI provider for all coding tasks in Jarvis
"""

import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class ClaudeCodeGenerator:
    """Generate and analyze code using Claude Haiku 4.5"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "claude-3-5-haiku-20241022"):
        """
        Initialize Claude Code Generator
        
        Args:
            api_key: Anthropic API key (or use ANTHROPIC_API_KEY env var)
            model: Claude model to use (default: claude-3-5-haiku-20241022)
        """
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        self.model = model
        self.workspace_dir = Path(__file__).parent.parent / "generated_code"
        self.created_files = []
        
        if not self.api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY not set. Set it with: "
                "export ANTHROPIC_API_KEY='sk-ant-...'"
            )
        
        # Check if API key looks like a placeholder
        if self.api_key == 'your_api_key_here' or self.api_key.startswith('your_'):
            raise ValueError(
                "ANTHROPIC_API_KEY appears to be a placeholder. "
                "Please set a valid API key. Get one from: https://console.anthropic.com/account/keys"
            )
        
        self.workspace_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            import anthropic
            self.client = anthropic.Anthropic(api_key=self.api_key)
            # Test the API key by making a simple request
            try:
                self.client.messages.create(
                    model=self.model,
                    max_tokens=10,
                    messages=[{"role": "user", "content": "test"}]
                )
                logger.info("Claude API key is valid")
            except Exception as api_error:
                logger.warning(f"Claude API validation failed: {str(api_error)[:100]}")
                # Don't raise here - allow the client to be created even if validation fails
                # This allows offline mode or retry later
        except ImportError:
            logger.error("anthropic package not installed. Install with: pip install anthropic")
            raise
    
    def generate_code(self, request: str, language: str = "python") -> Dict:
        """
        Generate code from natural language request using Claude
        
        Args:
            request: Natural language description of what to generate
            language: Programming language (python, javascript, etc.)
        
        Returns:
            Dict with generated code, filename, and metadata
        """
        try:
            prompt = self._create_generation_prompt(request, language)
            
            message = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            code = message.content[0].text
            
            # Extract code from markdown blocks if present
            code = self._extract_code_from_markdown(code, language)
            
            # Generate filename
            filename = self._generate_filename(request, language)
            
            # Save to workspace
            filepath = self.workspace_dir / filename
            filepath.write_text(code)
            self.created_files.append(str(filepath))
            
            return {
                "success": True,
                "code": code,
                "filename": filename,
                "filepath": str(filepath),
                "language": language,
                "model": self.model,
                "created_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Code generation error: {e}")
            return {
                "success": False,
                "error": str(e),
                "model": self.model
            }
    
    def analyze_code(self, code: str, filename: str = "") -> Dict:
        """
        Analyze code and provide improvement suggestions
        
        Args:
            code: Code to analyze
            filename: Optional filename for context
        
        Returns:
            Dict with analysis results and suggestions
        """
        try:
            prompt = f"""You are an expert code reviewer. Analyze this code and provide specific improvement suggestions.

File: {filename or 'unknown'}

Code:
```
{code}
```

Provide your analysis in this format:
1. **Summary**: One-line summary of the code
2. **Issues**: List any bugs, security issues, or problems
3. **Improvements**: 3-5 specific improvement suggestions
4. **Performance**: Any performance optimizations
5. **Refactoring**: Suggest refactoring opportunities

Be specific and actionable."""
            
            message = self.client.messages.create(
                model=self.model,
                max_tokens=2048,
                messages=[{"role": "user", "content": prompt}]
            )
            
            analysis = message.content[0].text
            
            return {
                "success": True,
                "analysis": analysis,
                "model": self.model,
                "filename": filename
            }
            
        except Exception as e:
            logger.error(f"Code analysis error: {e}")
            return {
                "success": False,
                "error": str(e),
                "filename": filename
            }
    
    def generate_test(self, code: str, language: str = "python") -> Dict:
        """
        Generate unit tests for code
        
        Args:
            code: Code to generate tests for
            language: Programming language
        
        Returns:
            Dict with generated test code
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
            
            message = self.client.messages.create(
                model=self.model,
                max_tokens=3096,
                messages=[{"role": "user", "content": prompt}]
            )
            
            tests = message.content[0].text
            tests = self._extract_code_from_markdown(tests, language)
            
            filename = self._generate_filename("test", language, prefix="test_")
            filepath = self.workspace_dir / filename
            filepath.write_text(tests)
            self.created_files.append(str(filepath))
            
            return {
                "success": True,
                "tests": tests,
                "filename": filename,
                "filepath": str(filepath),
                "language": language
            }
            
        except Exception as e:
            logger.error(f"Test generation error: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def refactor_code(self, code: str, language: str = "python", style: str = "clean") -> Dict:
        """
        Refactor code according to best practices
        
        Args:
            code: Code to refactor
            language: Programming language
            style: Refactoring style (clean, performance, readable, etc.)
        
        Returns:
            Dict with refactored code
        """
        try:
            styles = {
                "clean": "focus on code cleanliness, readability, and maintainability",
                "performance": "focus on performance optimizations",
                "readable": "focus on maximum readability and documentation",
                "pythonic": "follow Python best practices and idioms (PEP 8)"
            }
            
            style_desc = styles.get(style, styles["clean"])
            
            prompt = f"""Refactor this {language} code to {style_desc}.
Keep the same functionality but improve the code quality.

Original code:
```{language}
{code}
```

Return only the refactored code in a code block, with inline comments explaining key changes."""
            
            message = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                messages=[{"role": "user", "content": prompt}]
            )
            
            refactored = message.content[0].text
            refactored = self._extract_code_from_markdown(refactored, language)
            
            filename = self._generate_filename(f"refactored_{style}", language)
            filepath = self.workspace_dir / filename
            filepath.write_text(refactored)
            self.created_files.append(str(filepath))
            
            return {
                "success": True,
                "refactored_code": refactored,
                "filename": filename,
                "filepath": str(filepath),
                "style": style,
                "language": language
            }
            
        except Exception as e:
            logger.error(f"Code refactoring error: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def explain_code(self, code: str) -> Dict:
        """
        Explain what code does in simple terms
        
        Args:
            code: Code to explain
        
        Returns:
            Dict with explanation
        """
        try:
            prompt = f"""Explain this code in simple terms that a junior developer can understand.

Code:
```
{code}
```

Provide:
1. **What it does**: Overall purpose
2. **Key steps**: Main logic broken down
3. **Key concepts**: Any important patterns or concepts
4. **Potential issues**: Any gotchas or edge cases"""
            
            message = self.client.messages.create(
                model=self.model,
                max_tokens=2048,
                messages=[{"role": "user", "content": prompt}]
            )
            
            explanation = message.content[0].text
            
            return {
                "success": True,
                "explanation": explanation,
                "model": self.model
            }
            
        except Exception as e:
            logger.error(f"Code explanation error: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _create_generation_prompt(self, request: str, language: str) -> str:
        """Create a detailed prompt for code generation"""
        return f"""You are an expert {language} developer. Generate complete, production-ready {language} code that fulfills this request:

{request}

Requirements:
- Include proper error handling
- Add docstrings/comments explaining key parts
- Follow {language} best practices and conventions
- Make it modular and reusable
- Include type hints where applicable

Return ONLY the code in a code block:
```{language}
[YOUR CODE HERE]
```"""
    
    def _extract_code_from_markdown(self, text: str, language: str = "") -> str:
        """Extract code from markdown code blocks"""
        if "```" not in text:
            return text
        
        parts = text.split("```")
        for i, part in enumerate(parts):
            if i % 2 == 1:  # Code blocks are at odd indices
                # Skip language identifier
                lines = part.split("\n")
                if lines[0].strip().lower() in ["python", "javascript", "java", "typescript", "bash", "html", "css", "sql", "go", "rust", "cpp", "csharp", "ruby", "php"]:
                    return "\n".join(lines[1:]).rstrip()
                return part.rstrip()
        
        return text
    
    def _generate_filename(self, request: str, language: str, prefix: str = "") -> str:
        """Generate a meaningful filename from request"""
        extensions = {
            "python": "py",
            "javascript": "js",
            "typescript": "ts",
            "java": "java",
            "cpp": "cpp",
            "csharp": "cs",
            "go": "go",
            "rust": "rs",
            "ruby": "rb",
            "php": "php",
            "html": "html",
            "css": "css",
            "sql": "sql",
            "bash": "sh"
        }
        
        # Clean request to valid filename
        name = request.lower()
        name = "".join(c if c.isalnum() else "_" for c in name)
        name = "_".join(name.split())[:30]  # Limit length
        
        ext = extensions.get(language.lower(), "txt")
        return f"{prefix}{name}.{ext}"
    
    def get_created_files(self) -> List[str]:
        """Get list of files created by this generator"""
        return self.created_files
    
    def get_model_info(self) -> Dict:
        """Get information about the model"""
        return {
            "model": self.model,
            "provider": "anthropic",
            "type": "claude",
            "usage": "code generation, analysis, testing, refactoring",
            "created_files": len(self.created_files)
        }


# Global instance for easy access
_global_generator: Optional[ClaudeCodeGenerator] = None


def get_claude_generator(api_key: Optional[str] = None) -> ClaudeCodeGenerator:
    """Get or create global Claude code generator instance"""
    global _global_generator
    
    if _global_generator is None:
        _global_generator = ClaudeCodeGenerator(api_key=api_key)
    
    return _global_generator


def reset_generator():
    """Reset the global generator instance"""
    global _global_generator
    _global_generator = None
