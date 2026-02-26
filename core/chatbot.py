"""
Jarvis Brain - Interactive Code Evolution Chatbot
Chat with AI about your code improvements
"""

import os
import json
from pathlib import Path
from core.auto_evolution import AutoEvolutionEngine


class JarvisChatbot:
    """Interactive chatbot for code evolution and improvement"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.engine = AutoEvolutionEngine(project_root)
        self.conversation_history = []
        self.current_file = None
    
    def display_welcome(self):
        """Show welcome message"""
        print("""
╔════════════════════════════════════════════════════════════════════════╗
║                                                                        ║
║        🤖 JARVIS BRAIN - CODE EVOLUTION CHATBOT                        ║
║                                                                        ║
║              Chat with AI about your code improvements                 ║
║                                                                        ║
╚════════════════════════════════════════════════════════════════════════╝

👋 Hi! I'm Jarvis, your AI code evolution assistant.

I can help you with:
  • 📊 Analyzing your code for improvements
  • 💡 Suggesting performance optimizations
  • 🔒 Finding security vulnerabilities
  • 🏗️ Recommending architectural changes
  • 📝 Refactoring suggestions

Commands:
  > analyze              Scan entire project
  > file <path>         Analyze specific file
  > suggestions          Show improvement suggestions
  > explain <code>      Explain code snippet
  > help                Show all commands
  > exit                Quit chatbot

Type your question or command:
""")
    
    def chat(self, user_input: str) -> str:
        """Process user message and return response"""
        
        user_input_lower = user_input.strip().lower()
        
        # Help command
        if user_input_lower == "help":
            return self._show_help()
        
        # Exit command
        if user_input_lower == "exit":
            return None
        
        # Analyze project
        if user_input_lower == "analyze":
            return self._analyze_project()
        
        # Analyze specific file
        if user_input_lower.startswith("file "):
            filepath = user_input_lower[5:].strip()
            return self._analyze_file(filepath)
        
        # Show suggestions
        if user_input_lower == "suggestions":
            return self._show_suggestions()
        
        # Explain code
        if user_input_lower.startswith("explain "):
            code = user_input_lower[8:].strip()
            return self._explain_code(code)
        
        # Code generation requests
        if self._is_code_generation_request(user_input_lower):
            return self._handle_code_generation(user_input)
        
        # General questions
        if any(word in user_input_lower for word in ["performance", "speed", "slow", "optimize"]):
            return self._handle_performance_question(user_input_lower)
        
        if any(word in user_input_lower for word in ["security", "safe", "vulnerable", "exploit"]):
            return self._handle_security_question(user_input_lower)
        
        if any(word in user_input_lower for word in ["refactor", "improve", "better", "quality"]):
            return self._handle_quality_question(user_input_lower)
        
        if any(word in user_input_lower for word in ["what", "how", "why", "tell", "show"]):
            return self._handle_general_question(user_input_lower)
        
        # Default response
        return f"""
I understand you want to know about: "{user_input}"

Try these commands:
  > analyze              Analyze entire project
  > file core/main.py   Analyze specific file
  > suggestions         Show all suggestions

Or ask me to:
  • generate/make/create <something>  - Generate code
  • Performance improvements
  • Security issues
  • Code quality
  • Refactoring ideas

What would you like?
"""
    
    def _show_help(self) -> str:
        """Show help message"""
        return """
📚 JARVIS CHATBOT HELP
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

COMMANDS:
  analyze              Scan entire project for improvements
  file <path>          Analyze specific Python file
  suggestions          Show top improvement suggestions
  explain <code>       Explain how to improve code
  status               Show project status
  history              Show previous improvements
  help                 Show this message
  exit                 Quit chatbot

QUESTIONS YOU CAN ASK:
  • "How can I improve performance?"
  • "Any security issues?"
  • "How do I refactor this?"
  • "What's the best practice here?"
  • "Why is this slow?"
  • "Is this safe?"

EXAMPLES:
  > analyze
  > file core/main.py
  > explain for loop with append
  > How do I optimize database queries?
  > What are security best practices?
"""
    
    def _analyze_project(self) -> str:
        """Analyze entire project"""
        print("\n🔍 Analyzing your project...\n")
        
        results = self.engine.scan_project()
        
        response = f"""
✨ PROJECT ANALYSIS COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Statistics:
  • Files Scanned: {results['scanned_files']}
  • Total Improvements Found: {results['improvements_found']}

📈 Breakdown by Type:
"""
        for imp_type, count in results['by_type'].items():
            response += f"  • {imp_type.capitalize()}: {count}\n"
        
        if results['files']:
            response += "\n🏆 Top Files for Improvement:\n"
            sorted_files = sorted(
                results['files'].items(),
                key=lambda x: len(x[1]),
                reverse=True
            )[:5]
            
            for i, (filepath, improvements) in enumerate(sorted_files, 1):
                name = Path(filepath).name
                response += f"  {i}. {name} ({len(improvements)} improvements)\n"
        
        response += "\n💡 Next: Ask about specific files or types of improvements\n"
        return response
    
    def _analyze_file(self, filepath: str) -> str:
        """Analyze specific file"""
        file_path = self.project_root / filepath
        
        if not file_path.exists():
            return f"❌ File not found: {filepath}\n\nTry: > file core/main.py"
        
        try:
            with open(file_path) as f:
                code = f.read()
            
            suggestions = self.engine.get_improvement_suggestions(code, str(filepath))
            
            if not suggestions:
                return f"""
✅ {Path(filepath).name} looks good!

No obvious improvements found. The code follows best practices.

💪 Keep up the good work!
"""
            
            response = f"""
🔍 ANALYSIS: {Path(filepath).name}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Found {len(suggestions)} improvement opportunities:

"""
            for i, suggestion in enumerate(suggestions, 1):
                response += f"{i}. {suggestion.get('suggestion', 'Unknown')}\n"
                if 'example' in suggestion:
                    response += f"   Example: {suggestion['example']}\n"
            
            return response
        
        except Exception as e:
            return f"❌ Error analyzing file: {e}"
    
    def _show_suggestions(self) -> str:
        """Show improvement suggestions"""
        results = self.engine.scan_project()
        
        if not results['files']:
            return "✅ No improvement opportunities found! Your code is great."
        
        response = "💡 TOP IMPROVEMENT SUGGESTIONS\n" + "━" * 50 + "\n\n"
        
        sorted_files = sorted(
            results['files'].items(),
            key=lambda x: len(x[1]),
            reverse=True
        )
        
        suggestion_count = 0
        for filepath, improvements in sorted_files[:3]:
            for improvement in improvements[:2]:
                suggestion_count += 1
                response += f"{suggestion_count}. {improvement.get('suggestion', 'Unknown')}\n"
                response += f"   File: {Path(filepath).name}\n\n"
        
        response += f"\n✅ Found {results['improvements_found']} total improvements\n"
        response += "💬 Ask: > file <filename> for detailed analysis\n"
        
        return response
    
    def _explain_code(self, code_snippet: str) -> str:
        """Explain code improvement"""
        return f"""
📖 CODE EXPLANATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Your code: {code_snippet[:50]}...

Potential improvements:
  • Consider using list comprehensions for loops
  • Check for security implications
  • Look for performance bottlenecks
  • Verify all edge cases are handled

💡 To see specific suggestions, try:
   > file <filename>
   > analyze
"""
    
    def _handle_performance_question(self, question: str) -> str:
        """Answer performance questions"""
        return """
⚡ PERFORMANCE OPTIMIZATION TIPS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Common Performance Issues:
  • Using .append() in loops → Use list comprehension
  • Creating large lists → Use generators
  • Nested loops → Consider algorithms like sorting
  • Repeated calculations → Use caching/memoization
  • Large string concatenations → Use join()

Quick Wins:
  ❌ for x in items:
       result.append(x * 2)
  
  ✅ result = [x * 2 for x in items]
     → 2-3x faster!

💬 To see specific issues in your code:
   > analyze
   > file <filename>
"""
    
    def _handle_security_question(self, question: str) -> str:
        """Answer security questions"""
        return """
🔒 SECURITY BEST PRACTICES
━━━━━━━━━━━━━━━━━━━━━━━━━━

Critical Issues to Avoid:
  ❌ eval()     → Very dangerous!
  ❌ exec()     → Arbitrary code execution
  ❌ pickle     → Can execute code
  ❌ os.system()→ Command injection risks

Safe Alternatives:
  ✅ ast.literal_eval()  → Safely parse literals
  ✅ json.loads()        → For JSON data
  ✅ subprocess.run()    → Safe command execution
  ✅ Parameterized queries → Database safety

Always:
  • Validate user input
  • Use principle of least privilege
  • Keep dependencies updated
  • Use security scanners

💬 Run analysis to find security issues:
   > analyze
"""
    
    def _handle_quality_question(self, question: str) -> str:
        """Answer code quality questions"""
        return """
🏗️ CODE QUALITY GUIDELINES
━━━━━━━━━━━━━━━━━━━━━━━━━━

Best Practices:
  • Keep functions small (< 30 lines)
  • Use meaningful variable names
  • Add docstrings to functions
  • Follow PEP 8 style guide
  • DRY principle (Don't Repeat Yourself)
  • Test your code thoroughly

Red Flags:
  ⚠️ Functions over 100 lines
  ⚠️ Variables named x, y, temp
  ⚠️ Missing documentation
  ⚠️ Duplicated code
  ⚠️ No error handling

Tools:
  • black - Code formatting
  • pylint - Code analysis
  • mypy - Type checking

💬 Scan your code:
   > analyze
"""
    
    def _handle_general_question(self, question: str) -> str:
        """Handle general questions"""
        return f"""
💭 Question: {question}

I'm here to help! I can:
  • Analyze your code for improvements
  • Suggest performance optimizations
  • Find security vulnerabilities
  • Help with refactoring
  • Explain best practices

Try these:
  > analyze              Full project analysis
  > file core/main.py   Specific file analysis
  > suggestions          Top suggestions
  > help                 Command help

Or ask me directly about:
  • How to improve performance?
  • Any security issues?
  • How to refactor this?
  • Best practices for X?

What would you like to know?
"""
    
    def run_interactive(self):
        """Run interactive chatbot"""
        self.display_welcome()
        
        while True:
            try:
                user_input = input("\n🤖 Jarvis> ").strip()
                
                if not user_input:
                    continue
                
                response = self.chat(user_input)
                
                if response is None:
                    print("\n👋 Goodbye! Keep improving your code!\n")
                    break
                
                print(response)
                self.conversation_history.append((user_input, response))
            
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!\n")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def _is_code_generation_request(self, user_input: str) -> bool:
        """Check if user is asking to generate/create code"""
        keywords = [
            "make", "create", "generate", "write", "build",
            "code", "script", "function", "app", "calculator",
            "program", "class", "module", "component"
        ]
        
        # Check for "make a" or "create a" etc.
        for keyword in ["make", "create", "generate", "write", "build"]:
            if user_input.startswith(keyword + " a ") or user_input.startswith(keyword + " "):
                return True
        
        return False
    
    def _handle_code_generation(self, user_input: str) -> dict:
        """Handle code generation requests and return API payload"""
        # Extract what kind of code to generate
        request = user_input.strip()
        
        # Determine language (default to Python)
        language = "python"
        if "javascript" in request.lower() or "js" in request.lower():
            language = "javascript"
        elif "html" in request.lower():
            language = "html"
        elif "bash" in request.lower() or "shell" in request.lower():
            language = "bash"
        
        # Extract filename from request or generate one
        filename = self._extract_filename(request) or "generated_code"
        
        return {
            "success": True,
            "type": "code_generation",
            "request": request,
            "language": language,
            "filename": filename,
            "message": f"🔨 I'll generate {language} code for: {request}\n\nGenerating code using Mistral AI...",
            "api_endpoint": "/api/code/create-and-open"
        }
    
    def _extract_filename(self, request: str) -> str:
        """Extract a suitable filename from the request"""
        # Simple extraction - take first meaningful word after action verb
        words = request.split()
        for i, word in enumerate(words):
            if word.lower() in ["a", "the", "some"]:
                if i + 1 < len(words):
                    filename = words[i + 1].lower()
                    # Clean up the filename
                    filename = "".join(c if c.isalnum() else "_" for c in filename)
                    return filename or "code"
        
        # Fallback: use first non-verb word
        verbs = ["make", "create", "generate", "write", "build"]
        for word in words:
            if word.lower() not in verbs and len(word) > 2:
                return word.lower()
        
        return None


def start_chatbot():
    """Start the Jarvis chatbot"""
    chatbot = JarvisChatbot("/Volumes/Akash SSD/repos/jarvis-brain")
    chatbot.run_interactive()


if __name__ == "__main__":
    start_chatbot()
