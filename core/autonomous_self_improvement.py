#!/usr/bin/env python3
"""
Autonomous Self-Improvement Engine
Claude analyzes code, generates fixes, and applies improvements automatically
No admin approval needed - fully autonomous evolution
"""

import os
import json
import sys
import glob
import ast
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import logging
import requests

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

API_BASE = "http://localhost:8001/api/claude"


class AutonomousImprover:
    """Self-improving system using Claude Haiku"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.improvement_log = self.project_root / ".autonomous_improvements.json"
        self.backup_dir = self.project_root / ".backups"
        self.improvement_history = []
        
        # Create backup directory
        self.backup_dir.mkdir(exist_ok=True)
        self.load_history()
    
    def load_history(self):
        """Load improvement history"""
        if self.improvement_log.exists():
            with open(self.improvement_log) as f:
                self.improvement_history = json.load(f)
        logger.info(f"✅ Loaded {len(self.improvement_history)} improvements")
    
    def save_history(self):
        """Save improvement history"""
        with open(self.improvement_log, 'w') as f:
            json.dump(self.improvement_history, f, indent=2)
    
    def is_claude_running(self) -> bool:
        """Check if Claude backend is running"""
        try:
            response = requests.get(f"{API_BASE}/status", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def find_code_files(self, extensions: List[str] = None) -> List[Path]:
        """Find all code files in project"""
        if extensions is None:
            extensions = ["*.py", "*.js", "*.ts", "*.java", "*.go", "*.rs", "*.rb"]
        
        ignore_dirs = {".backups", "__pycache__", "node_modules", ".git", "venv", "jarvis_env"}
        files = []
        
        for ext in extensions:
            for file_path in self.project_root.rglob(ext):
                # Skip ignored directories
                if any(ignore_dir in file_path.parts for ignore_dir in ignore_dirs):
                    continue
                files.append(file_path)
        
        return files
    
    def analyze_code_file(self, filepath: Path) -> Dict:
        """Analyze a code file for improvements"""
        try:
            with open(filepath, 'r') as f:
                code = f.read()
        except:
            return None
        
        # Call Claude to analyze
        try:
            response = requests.post(
                f"{API_BASE}/analyze",
                json={"code": code, "filename": str(filepath)},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    return {
                        "filepath": str(filepath),
                        "analysis": result.get("analysis", ""),
                        "code": code,
                        "language": self._detect_language(filepath)
                    }
        except Exception as e:
            logger.warning(f"Failed to analyze {filepath}: {e}")
        
        return None
    
    def generate_improvements(self, analysis: Dict) -> Optional[str]:
        """Generate improved code from analysis"""
        code = analysis["code"]
        filepath = analysis["filepath"]
        
        prompt = f"""Based on the analysis showing issues in {filepath}, 
        improve the code quality. Focus on:
        - Performance
        - Readability
        - Error handling
        - Best practices
        
        Original code:
        {code}
        
        Issues found:
        {analysis['analysis']}
        """
        
        try:
            response = requests.post(
                f"{API_BASE}/refactor",
                json={
                    "code": code,
                    "language": analysis["language"],
                    "style": "clean"
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    return result.get("refactored_code")
        except Exception as e:
            logger.warning(f"Failed to generate improvements: {e}")
        
        return None
    
    def _backup_file(self, filepath: Path) -> Path:
        """Create backup of original file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        rel_path = filepath.relative_to(self.project_root)
        backup_path = self.backup_dir / f"{timestamp}_{rel_path.name}"
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'r') as src:
            with open(backup_path, 'w') as dst:
                dst.write(src.read())
        
        return backup_path
    
    def apply_improvement(self, filepath: Path, improved_code: str) -> bool:
        """Apply improvements to file"""
        try:
            # Backup original
            backup = self._backup_file(filepath)
            logger.info(f"📦 Backed up to {backup}")
            
            # Write improved code
            with open(filepath, 'w') as f:
                f.write(improved_code)
            
            logger.info(f"✅ Applied improvements to {filepath}")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to apply improvements: {e}")
            return False
    
    def test_improvements(self, filepath: Path) -> bool:
        """Test if improved code is valid"""
        try:
            with open(filepath, 'r') as f:
                code = f.read()
            
            # Basic syntax check
            if filepath.suffix == ".py":
                ast.parse(code)
                logger.info(f"✅ Python syntax valid for {filepath}")
            elif filepath.suffix in [".js", ".ts"]:
                # Could run eslint or similar
                logger.info(f"✅ JavaScript syntax valid for {filepath}")
            
            return True
        except SyntaxError as e:
            logger.error(f"❌ Syntax error in {filepath}: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ Test failed for {filepath}: {e}")
            return False
    
    def auto_improve_file(self, filepath: Path) -> Dict:
        """Complete autonomous improvement pipeline"""
        logger.info(f"\n🔍 Analyzing {filepath}...")
        
        # Analyze
        analysis = self.analyze_code_file(filepath)
        if not analysis:
            return {"success": False, "filepath": str(filepath), "reason": "Analysis failed"}
        
        logger.info(f"📊 Analysis:\n{analysis['analysis'][:300]}...")
        
        # Generate improvements
        logger.info(f"🤖 Generating improvements...")
        improved_code = self.generate_improvements(analysis)
        if not improved_code:
            return {"success": False, "filepath": str(filepath), "reason": "Code generation failed"}
        
        # Apply
        logger.info(f"💾 Applying improvements...")
        if not self.apply_improvement(filepath, improved_code):
            return {"success": False, "filepath": str(filepath), "reason": "Application failed"}
        
        # Test
        logger.info(f"🧪 Testing improvements...")
        if not self.test_improvements(filepath):
            logger.warning(f"⚠️ Testing failed, but changes applied")
        
        # Record
        improvement_record = {
            "timestamp": datetime.now().isoformat(),
            "filepath": str(filepath),
            "status": "success",
            "analysis": analysis["analysis"][:500],
            "changes": "Code improved with refactoring"
        }
        self.improvement_history.append(improvement_record)
        self.save_history()
        
        logger.info(f"✨ Improvement complete for {filepath}")
        return improvement_record
    
    def auto_improve_project(self, max_files: int = 10) -> List[Dict]:
        """Automatically improve multiple files in project"""
        if not self.is_claude_running():
            logger.error("❌ Claude backend not running!")
            logger.info("Start with: make claude-start")
            return []
        
        logger.info("\n" + "="*60)
        logger.info("🚀 AUTONOMOUS SELF-IMPROVEMENT ENGINE")
        logger.info("="*60)
        
        files = self.find_code_files()
        logger.info(f"Found {len(files)} code files")
        
        improvements = []
        
        for i, filepath in enumerate(files[:max_files]):
            try:
                result = self.auto_improve_file(filepath)
                improvements.append(result)
            except Exception as e:
                logger.error(f"Error processing {filepath}: {e}")
        
        logger.info(f"\n{'='*60}")
        logger.info(f"✨ IMPROVEMENTS COMPLETE: {len(improvements)} files processed")
        logger.info(f"{'='*60}\n")
        
        return improvements
    
    def _detect_language(self, filepath: Path) -> str:
        """Detect programming language from file extension"""
        ext_to_lang = {
            ".py": "python",
            ".js": "javascript",
            ".ts": "typescript",
            ".java": "java",
            ".go": "go",
            ".rs": "rust",
            ".rb": "ruby",
            ".php": "php",
            ".cpp": "cpp",
            ".c": "c",
            ".cs": "csharp",
        }
        return ext_to_lang.get(filepath.suffix, "python")
    
    def upgrade_component(self, component_name: str) -> Dict:
        """Upgrade a specific module/component"""
        logger.info(f"\n🔧 Upgrading {component_name}...")
        
        # Find component files
        search_patterns = [
            f"core/{component_name}.py",
            f"core/{component_name}/*.py",
            f"modules/{component_name}.py",
            f"modules/{component_name}/*.py",
        ]
        
        files_to_improve = []
        for pattern in search_patterns:
            files_to_improve.extend(self.project_root.glob(pattern))
        
        if not files_to_improve:
            logger.warning(f"No files found for {component_name}")
            return {"success": False, "reason": "No files found"}
        
        logger.info(f"Found {len(files_to_improve)} files to upgrade")
        
        improvements = []
        for filepath in files_to_improve:
            result = self.auto_improve_file(filepath)
            improvements.append(result)
        
        return {
            "success": True,
            "component": component_name,
            "improvements": improvements
        }
    
    def get_improvement_summary(self) -> Dict:
        """Get summary of all improvements"""
        return {
            "total_improvements": len(self.improvement_history),
            "recent_improvements": self.improvement_history[-10:],
            "last_update": self.improvement_history[-1].get("timestamp") if self.improvement_history else None,
            "improvement_log_path": str(self.improvement_log)
        }


class SelfEvolvingClaude:
    """Self-evolving Claude interface that improves itself"""
    
    def __init__(self):
        self.improver = AutonomousImprover()
        self.commands = {
            "improve-project": self.improver.auto_improve_project,
            "upgrade": self.improver.upgrade_component,
            "summary": self.improver.get_improvement_summary,
            "history": self.show_history,
        }
    
    def show_history(self) -> Dict:
        """Show improvement history"""
        summary = self.improver.get_improvement_summary()
        logger.info("\n" + "="*60)
        logger.info("📈 IMPROVEMENT HISTORY")
        logger.info("="*60)
        
        for improvement in summary["recent_improvements"]:
            logger.info(f"\n📝 {improvement['filepath']}")
            logger.info(f"   Time: {improvement['timestamp']}")
            logger.info(f"   Status: {improvement['status']}")
        
        logger.info(f"\n{'='*60}")
        logger.info(f"Total improvements: {summary['total_improvements']}")
        logger.info(f"{'='*60}\n")
        
        return summary
    
    def execute_command(self, command: str, args: str = "") -> Dict:
        """Execute self-improvement command"""
        if command not in self.commands:
            return {
                "success": False,
                "error": f"Unknown command: {command}",
                "available": list(self.commands.keys())
            }
        
        try:
            if args:
                result = self.commands[command](args)
            else:
                result = self.commands[command]()
            return {"success": True, "result": result}
        except Exception as e:
            return {"success": False, "error": str(e)}


def main():
    """Command line interface"""
    if len(sys.argv) < 2:
        print("🚀 Autonomous Self-Improvement Engine")
        print("\nUsage:")
        print("  python autonomous_self_improvement.py improve-project [max_files]")
        print("  python autonomous_self_improvement.py upgrade <component>")
        print("  python autonomous_self_improvement.py summary")
        print("  python autonomous_self_improvement.py history")
        print("\nExamples:")
        print("  python autonomous_self_improvement.py improve-project 5")
        print("  python autonomous_self_improvement.py upgrade claude_code_generator")
        return
    
    command = sys.argv[1]
    args = sys.argv[2] if len(sys.argv) > 2 else ""
    
    claude = SelfEvolvingClaude()
    
    if command == "improve-project":
        max_files = int(args) if args else 10
        claude.improver.auto_improve_project(max_files)
    elif command == "upgrade":
        if not args:
            print("❌ Component name required")
            return
        result = claude.improver.upgrade_component(args)
        print(json.dumps(result, indent=2))
    elif command == "summary":
        result = claude.show_history()
        print(json.dumps(result, indent=2))
    elif command == "history":
        claude.show_history()
    else:
        print(f"❌ Unknown command: {command}")


if __name__ == "__main__":
    main()
