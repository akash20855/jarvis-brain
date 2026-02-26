#!/usr/bin/env python3
"""
AutoDebug Engine - Autonomous Bug Detection & Fixing
Automatically finds, analyzes, and fixes bugs without manual intervention
"""

import os
import json
import sys
import ast
import subprocess
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import logging
import requests

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

API_BASE = "http://localhost:8001/api/claude"


class CodeAnalyzer:
    """Analyze code for potential bugs and issues"""
    
    def __init__(self):
        self.issues = []
    
    def analyze_python_file(self, filepath: Path) -> List[Dict]:
        """Analyze Python file for issues"""
        issues = []
        
        try:
            with open(filepath, 'r') as f:
                code = f.read()
        except:
            return issues
        
        # Syntax check
        try:
            ast.parse(code)
        except SyntaxError as e:
            issues.append({
                "type": "syntax_error",
                "severity": "critical",
                "line": e.lineno,
                "message": f"Syntax error: {e.msg}",
                "code": code
            })
            return issues
        
        # Pattern-based issues
        lines = code.split('\n')
        
        # Check for common issues
        patterns = {
            "unused_variable": r'^\s*(\w+)\s*=\s*\w+$',
            "bare_except": r'except\s*:',
            "missing_docstring": r'^def\s+\w+\(',
            "print_debugging": r'print\(',
            "hardcoded_paths": r'["\']\/[a-zA-Z0-9\/]+["\']',
        }
        
        for i, line in enumerate(lines, 1):
            if 'except:' in line and 'except Exception' not in line:
                issues.append({
                    "type": "bare_except",
                    "severity": "medium",
                    "line": i,
                    "message": "Bare except clause - should catch specific exceptions",
                    "code": line.strip()
                })
            
            if 'import *' in line:
                issues.append({
                    "type": "wildcard_import",
                    "severity": "medium",
                    "line": i,
                    "message": "Wildcard import - may cause namespace pollution",
                    "code": line.strip()
                })
            
            if re.match(r'^\s*#\s*TODO|FIXME|BUG|HACK', line):
                issues.append({
                    "type": "todo_marker",
                    "severity": "low",
                    "line": i,
                    "message": f"Found marker in code: {line.strip()}",
                    "code": line.strip()
                })
        
        return issues
    
    def analyze_javascript_file(self, filepath: Path) -> List[Dict]:
        """Analyze JavaScript file for issues"""
        issues = []
        
        try:
            with open(filepath, 'r') as f:
                code = f.read()
        except:
            return issues
        
        lines = code.split('\n')
        
        # Check for common JS issues
        for i, line in enumerate(lines, 1):
            if '== true' in line or '== false' in line:
                issues.append({
                    "type": "loose_comparison",
                    "severity": "medium",
                    "line": i,
                    "message": "Use strict comparison (=== instead of ==)",
                    "code": line.strip()
                })
            
            if 'var ' in line and 'var ' in line[:line.find('var ') + 5]:
                issues.append({
                    "type": "var_usage",
                    "severity": "low",
                    "line": i,
                    "message": "Use 'let' or 'const' instead of 'var'",
                    "code": line.strip()
                })
            
            if 'console.log' in line:
                issues.append({
                    "type": "debug_logging",
                    "severity": "low",
                    "line": i,
                    "message": "Debug console.log left in code",
                    "code": line.strip()
                })
        
        return issues


class AutoDebugger:
    """Autonomous bug detection and fixing"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.debug_log = self.project_root / ".autodebug.json"
        self.backup_dir = self.project_root / ".debug_backups"
        self.debug_history = []
        self.analyzer = CodeAnalyzer()
        
        self.backup_dir.mkdir(exist_ok=True)
        self.load_history()
    
    def load_history(self):
        """Load debug history"""
        if self.debug_log.exists():
            with open(self.debug_log) as f:
                self.debug_history = json.load(f)
        logger.info(f"✅ Loaded {len(self.debug_history)} debug records")
    
    def save_history(self):
        """Save debug history"""
        with open(self.debug_log, 'w') as f:
            json.dump(self.debug_history, f, indent=2)
    
    def is_claude_running(self) -> bool:
        """Check if Claude backend is running"""
        try:
            response = requests.get(f"{API_BASE}/status", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def find_code_files(self) -> List[Path]:
        """Find all code files"""
        extensions = ["*.py", "*.js", "*.ts", "*.java"]
        ignore_dirs = {".backups", "__pycache__", "node_modules", ".git", "venv", "jarvis_env", ".debug_backups"}
        files = []
        
        for ext in extensions:
            for file_path in self.project_root.rglob(ext):
                if any(ignore_dir in file_path.parts for ignore_dir in ignore_dirs):
                    continue
                files.append(file_path)
        
        return files
    
    def scan_for_bugs(self, filepath: Path) -> List[Dict]:
        """Scan file for bugs"""
        if filepath.suffix == ".py":
            return self.analyzer.analyze_python_file(filepath)
        elif filepath.suffix in [".js", ".ts"]:
            return self.analyzer.analyze_javascript_file(filepath)
        return []
    
    def _backup_file(self, filepath: Path) -> Path:
        """Backup file before fixing"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        rel_path = filepath.relative_to(self.project_root)
        backup_path = self.backup_dir / f"{timestamp}_{rel_path.name}"
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'r') as src:
            with open(backup_path, 'w') as dst:
                dst.write(src.read())
        
        return backup_path
    
    def analyze_with_claude(self, code: str, issues: List[Dict], filepath: Path) -> Optional[str]:
        """Use Claude to analyze and generate fixes"""
        if not issues:
            return None
        
        issues_text = "\n".join([
            f"- Line {i['line']}: {i['type']} - {i['message']}"
            for i in issues
        ])
        
        prompt = f"""
        File: {filepath}
        
        Issues found in the code:
        {issues_text}
        
        Please analyze these issues and provide fixed code.
        Focus on:
        1. Critical errors (syntax, runtime errors)
        2. Logic bugs
        3. Performance issues
        4. Security vulnerabilities
        5. Code quality improvements
        
        Respond with corrected code that fixes all issues.
        """
        
        try:
            response = requests.post(
                f"{API_BASE}/refactor",
                json={
                    "code": code,
                    "language": "python" if filepath.suffix == ".py" else "javascript",
                    "style": "clean"
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    return result.get("refactored_code")
        except Exception as e:
            logger.warning(f"Claude analysis failed: {e}")
        
        return None
    
    def apply_fix(self, filepath: Path, fixed_code: str) -> bool:
        """Apply bug fixes to file"""
        try:
            # Backup
            backup = self._backup_file(filepath)
            logger.info(f"📦 Backed up to {backup}")
            
            # Write fixed code
            with open(filepath, 'w') as f:
                f.write(fixed_code)
            
            logger.info(f"✅ Applied fixes to {filepath}")
            return True
        except Exception as e:
            logger.error(f"Failed to apply fix: {e}")
            return False
    
    def verify_fix(self, filepath: Path) -> Tuple[bool, str]:
        """Verify fix is valid"""
        try:
            with open(filepath, 'r') as f:
                code = f.read()
            
            if filepath.suffix == ".py":
                ast.parse(code)
                return True, "✅ Python syntax valid"
            
            return True, "✅ File syntax valid"
        except SyntaxError as e:
            return False, f"❌ Syntax error: {e}"
        except Exception as e:
            return False, f"❌ Verification error: {e}"
    
    def auto_debug_file(self, filepath: Path) -> Dict:
        """Complete autonomous debugging pipeline"""
        logger.info(f"\n🔍 Scanning {filepath}...")
        
        # Scan
        issues = self.scan_for_bugs(filepath)
        if not issues:
            logger.info("✅ No issues found")
            return {
                "filepath": str(filepath),
                "status": "clean",
                "issues_found": 0
            }
        
        logger.info(f"🐛 Found {len(issues)} issues:")
        for issue in issues:
            logger.info(f"   - {issue['type']} (line {issue['line']}): {issue['message']}")
        
        # Read code
        with open(filepath, 'r') as f:
            code = f.read()
        
        # Analyze with Claude
        logger.info(f"🤖 Analyzing with Claude...")
        fixed_code = self.analyze_with_claude(code, issues, filepath)
        
        if not fixed_code:
            logger.warning(f"⚠️ Claude could not generate fixes")
            return {
                "filepath": str(filepath),
                "status": "failed",
                "issues_found": len(issues),
                "reason": "Fix generation failed"
            }
        
        # Apply fix
        logger.info(f"💾 Applying fixes...")
        if not self.apply_fix(filepath, fixed_code):
            return {
                "filepath": str(filepath),
                "status": "failed",
                "issues_found": len(issues),
                "reason": "Fix application failed"
            }
        
        # Verify
        valid, msg = self.verify_fix(filepath)
        if not valid:
            logger.warning(f"⚠️ Verification warning: {msg}")
        else:
            logger.info(msg)
        
        # Record
        debug_record = {
            "timestamp": datetime.now().isoformat(),
            "filepath": str(filepath),
            "status": "fixed",
            "issues_found": len(issues),
            "issues": [
                {"type": i["type"], "line": i["line"], "severity": i["severity"]}
                for i in issues
            ],
            "verified": valid
        }
        
        self.debug_history.append(debug_record)
        self.save_history()
        
        logger.info(f"✨ Debugging complete for {filepath}")
        return debug_record
    
    def auto_debug_project(self, max_files: int = None) -> List[Dict]:
        """Scan and fix bugs in entire project"""
        if not self.is_claude_running():
            logger.error("❌ Claude backend not running!")
            return []
        
        logger.info("\n" + "="*60)
        logger.info("🚀 AUTONOMOUS DEBUG ENGINE")
        logger.info("="*60)
        
        files = self.find_code_files()
        logger.info(f"Found {len(files)} code files")
        
        if max_files:
            files = files[:max_files]
        
        debug_results = []
        
        for filepath in files:
            try:
                result = self.auto_debug_file(filepath)
                debug_results.append(result)
            except Exception as e:
                logger.error(f"Error processing {filepath}: {e}")
        
        # Summary
        logger.info(f"\n{'='*60}")
        fixed = sum(1 for r in debug_results if r.get("status") == "fixed")
        clean = sum(1 for r in debug_results if r.get("status") == "clean")
        logger.info(f"✨ DEBUG COMPLETE: {fixed} fixed, {clean} clean")
        logger.info(f"{'='*60}\n")
        
        return debug_results
    
    def watch_mode(self, interval: int = 5):
        """Continuous monitoring mode"""
        logger.info(f"\n👀 AutoDebug Watch Mode - Scanning every {interval}s")
        logger.info("Press Ctrl+C to stop")
        logger.info("="*60)
        
        import time
        try:
            while True:
                files = self.find_code_files()
                bugs_found = 0
                
                for filepath in files:
                    issues = self.scan_for_bugs(filepath)
                    if issues:
                        bugs_found += len(issues)
                        logger.warning(f"🐛 {filepath}: {len(issues)} issues")
                
                if bugs_found > 0:
                    logger.warning(f"⚠️ Total {bugs_found} issues found - Running auto-fix...")
                    self.auto_debug_project()
                else:
                    logger.info(f"✅ All files clean")
                
                time.sleep(interval)
        except KeyboardInterrupt:
            logger.info("\n👋 Watch mode stopped")


def main():
    """CLI interface"""
    if len(sys.argv) < 2:
        print("🐛 AutoDebug Engine - Autonomous Bug Detection & Fixing")
        print("\nUsage:")
        print("  python auto_debug.py scan [max_files]     - Scan and fix bugs")
        print("  python auto_debug.py watch [interval]     - Continuous monitoring")
        print("  python auto_debug.py report               - Show debug report")
        print("\nExamples:")
        print("  python auto_debug.py scan 10")
        print("  python auto_debug.py watch 5")
        return
    
    command = sys.argv[1]
    debugger = AutoDebugger()
    
    if command == "scan":
        max_files = int(sys.argv[2]) if len(sys.argv) > 2 else None
        results = debugger.auto_debug_project(max_files)
        print(json.dumps(results, indent=2))
    
    elif command == "watch":
        interval = int(sys.argv[2]) if len(sys.argv) > 2 else 5
        debugger.watch_mode(interval)
    
    elif command == "report":
        summary = {
            "total_fixes": len(debugger.debug_history),
            "recent_fixes": debugger.debug_history[-10:],
            "log_file": str(debugger.debug_log)
        }
        print(json.dumps(summary, indent=2))
    
    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
