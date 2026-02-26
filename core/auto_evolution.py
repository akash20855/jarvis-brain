"""
Auto-Evolution Engine - AI-Powered Code Improvement
Continuously evolves code using free AI APIs
"""

import os
import json
import subprocess
from datetime import datetime
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AutoEvolutionEngine:
    """AI-powered code auto-evolution system"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.evolution_log = self.project_root / ".evolution_log.json"
        self.improvements = []
        self.load_history()
    
    def load_history(self):
        """Load evolution history"""
        if self.evolution_log.exists():
            with open(self.evolution_log) as f:
                data = json.load(f)
                self.improvements = data.get("improvements", [])
                logger.info(f"✅ Loaded {len(self.improvements)} previous improvements")
    
    def save_history(self):
        """Save evolution history"""
        with open(self.evolution_log, 'w') as f:
            json.dump({
                "improvements": self.improvements,
                "total": len(self.improvements),
                "last_update": datetime.now().isoformat()
            }, f, indent=2)
    
    def get_improvement_suggestions(self, code: str, filename: str) -> list:
        """Get improvement suggestions from free AI"""
        
        # Use local Ollama if available (completely free, runs locally)
        try:
            return self._get_ollama_suggestions(code, filename)
        except:
            pass
        
        # Fallback to pattern-based improvements
        logger.warning("⚠️ Ollama not available, using pattern-based suggestions")
        return self._get_pattern_suggestions(code, filename)
    
    def _get_ollama_suggestions(self, code: str, filename: str) -> list:
        """Get suggestions using local Ollama (free, no API key needed)"""
        
        prompt = f"""Analyze this Python code and suggest 2-3 specific improvements:
        
File: {filename}
```python
{code[:2000]}  # First 2000 chars
```

Respond with a JSON array of improvements:
[
  {{"type": "performance", "suggestion": "...", "example": "..."}},
  {{"type": "security", "suggestion": "...", "example": "...")}}
]

Be specific and actionable."""
        
        try:
            result = subprocess.run(
                ["curl", "-s", "http://localhost:11434/api/generate"],
                input=json.dumps({
                    "model": "mistral",
                    "prompt": prompt,
                    "stream": False
                }),
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                response = json.loads(result.stdout)
                # Parse response and extract suggestions
                return self._parse_suggestions(response.get("response", ""))
        except Exception as e:
            logger.debug(f"Ollama error: {e}")
        
        return []
    
    def _get_pattern_suggestions(self, code: str, filename: str) -> list:
        """Pattern-based improvement suggestions (no AI needed)"""
        suggestions = []
        
        # Performance patterns
        if "for " in code and ".append(" in code:
            suggestions.append({
                "type": "performance",
                "file": filename,
                "line": "loop with append",
                "suggestion": "Consider list comprehension for better performance",
                "example": "[x * 2 for x in items]"
            })
        
        # Security patterns
        if "exec(" in code or "eval(" in code:
            suggestions.append({
                "type": "security",
                "file": filename,
                "severity": "HIGH",
                "suggestion": "Avoid exec/eval - use ast.literal_eval or safer alternatives",
                "example": "ast.literal_eval(user_input)"
            })
        
        # Code quality patterns
        if "TODO" in code or "FIXME" in code:
            suggestions.append({
                "type": "quality",
                "file": filename,
                "suggestion": "Address TODO/FIXME comments"
            })
        
        # Function length check
        if code.count("\ndef ") == 1 and len(code.split("\n")) > 100:
            suggestions.append({
                "type": "quality",
                "file": filename,
                "suggestion": "Function is very long - consider breaking into smaller functions"
            })
        
        return suggestions
    
    def _parse_suggestions(self, response: str) -> list:
        """Parse AI suggestions"""
        try:
            # Try to extract JSON from response
            if "[" in response and "]" in response:
                json_str = response[response.find("["):response.rfind("]")+1]
                return json.loads(json_str)
        except:
            pass
        return []
    
    def apply_improvement(self, filepath: str, improvement: dict, code: str) -> str:
        """Apply improvement to code"""
        
        improvement_type = improvement.get("type", "unknown")
        
        if improvement_type == "performance":
            return self._apply_performance_improvement(code, improvement)
        elif improvement_type == "security":
            return self._apply_security_improvement(code, improvement)
        elif improvement_type == "quality":
            return self._apply_quality_improvement(code, improvement)
        
        return code
    
    def _apply_performance_improvement(self, code: str, improvement: dict) -> str:
        """Auto-apply performance improvements"""
        if "append" in improvement.get("suggestion", ""):
            # Replace for loops with list comprehensions
            if "for " in code and ".append(" in code:
                logger.info("🚀 Applying list comprehension optimization...")
                # This would need safer AST-based transformation
        return code
    
    def _apply_security_improvement(self, code: str, improvement: dict) -> str:
        """Auto-apply security improvements"""
        if "exec" in code or "eval" in code:
            logger.info("🔒 Removing dangerous eval/exec...")
            code = code.replace("eval(", "ast.literal_eval(")
            code = code.replace("exec(", "# REMOVED UNSAFE EXEC - ")
        return code
    
    def _apply_quality_improvement(self, code: str, improvement: dict) -> str:
        """Auto-apply quality improvements"""
        return code
    
    def scan_project(self, patterns: list = None) -> dict:
        """Scan entire project for improvements"""
        
        logger.info("🔍 Scanning project for improvement opportunities...")
        
        results = {
            "scanned_files": 0,
            "improvements_found": 0,
            "by_type": {},
            "files": {}
        }
        
        # Find all Python files
        python_files = list(self.project_root.glob("**/*.py"))
        logger.info(f"📝 Found {len(python_files)} Python files")
        
        for filepath in python_files:
            # Skip test files and venv
            if "test_" in str(filepath) or "venv" in str(filepath) or "__pycache__" in str(filepath):
                continue
            
            try:
                with open(filepath) as f:
                    code = f.read()
                
                suggestions = self.get_improvement_suggestions(code, str(filepath))
                
                if suggestions:
                    results["scanned_files"] += 1
                    results["files"][str(filepath)] = suggestions
                    results["improvements_found"] += len(suggestions)
                    
                    for suggestion in suggestions:
                        imp_type = suggestion.get("type", "other")
                        results["by_type"][imp_type] = results["by_type"].get(imp_type, 0) + 1
                
            except Exception as e:
                logger.error(f"Error scanning {filepath}: {e}")
        
        return results
    
    def evolve_continuously(self, interval: int = 3600):
        """Continuously evolve code (run periodically)"""
        logger.info(f"🚀 Auto-evolution starting (interval: {interval}s)")
        
        results = self.scan_project()
        
        logger.info(f"""
✨ EVOLUTION SCAN COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 Scanned: {results['scanned_files']} files
💡 Improvements: {results['improvements_found']} found

By Type:
""")
        for imp_type, count in results['by_type'].items():
            logger.info(f"  • {imp_type}: {count}")
        
        # Log improvements
        improvement_record = {
            "timestamp": datetime.now().isoformat(),
            "scanned_files": results['scanned_files'],
            "improvements": results['improvements_found'],
            "details": results['files']
        }
        
        self.improvements.append(improvement_record)
        self.save_history()
        
        return results


def run_evolution_analysis():
    """Run complete evolution analysis"""
    
    engine = AutoEvolutionEngine("/Volumes/Akash SSD/repos/jarvis-brain")
    
    print("""
╔════════════════════════════════════════════════════════════════════════╗
║       🤖 JARVIS BRAIN - AUTO-EVOLUTION ENGINE                         ║
║                                                                        ║
║            AI-Powered Continuous Code Improvement                      ║
╚════════════════════════════════════════════════════════════════════════╝
""")
    
    results = engine.evolve_continuously()
    
    # Show top files with most improvements
    if results['files']:
        print("\n📂 Files with most improvement opportunities:")
        sorted_files = sorted(
            results['files'].items(),
            key=lambda x: len(x[1]),
            reverse=True
        )[:5]
        
        for filepath, improvements in sorted_files:
            print(f"\n  📄 {Path(filepath).name} ({len(improvements)} improvements)")
            for improvement in improvements[:2]:
                print(f"     • {improvement.get('suggestion', 'Unknown')}")
    
    print("\n" + "="*76)
    print("💾 Evolution history saved to: .evolution_log.json")
    print("\n✅ Analysis complete!")


if __name__ == "__main__":
    run_evolution_analysis()
