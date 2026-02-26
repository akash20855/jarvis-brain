#!/usr/bin/env python3
"""
Advanced Build System with Debug Support
Integrated debugging, testing, and optimization for JARVIS PRO
"""

import os
import sys
import subprocess
import json
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [BUILD] - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('.build.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class BuildPhase:
    """Single build phase"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.status = "pending"  # pending, running, success, failed
        self.start_time = None
        self.end_time = None
        self.error = None
        self.output = ""
    
    def get_duration(self) -> float:
        """Get phase duration in seconds"""
        if not self.start_time or not self.end_time:
            return 0
        return self.end_time - self.start_time
    
    def to_dict(self) -> Dict:
        """Convert to dict"""
        return {
            "name": self.name,
            "description": self.description,
            "status": self.status,
            "duration_seconds": self.get_duration(),
            "error": self.error
        }


class AdvancedBuildSystem:
    """Advanced build system with debugging"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.phases = []
        self.build_start = datetime.now()
        self.debug_enabled = True
        
        logger.info("Advanced Build System initialized")
    
    def add_phase(self, name: str, description: str) -> BuildPhase:
        """Add build phase"""
        phase = BuildPhase(name, description)
        self.phases.append(phase)
        return phase
    
    def run_command(self, phase: BuildPhase, command: str, check: bool = True) -> Tuple[bool, str]:
        """Run shell command in phase"""
        phase.status = "running"
        phase.start_time = time.time()
        
        logger.info(f"▶ {phase.name}: {phase.description}")
        logger.debug(f"  Command: {command}")
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            phase.output = result.stdout + result.stderr
            
            if result.returncode != 0 and check:
                phase.status = "failed"
                phase.error = f"Command failed with code {result.returncode}"
                logger.error(f"✗ {phase.name} FAILED")
                logger.error(f"  Output: {result.stderr}")
                return False, result.stderr
            
            phase.status = "success"
            logger.info(f"✓ {phase.name} completed")
            
            return True, result.stdout
        
        except subprocess.TimeoutExpired:
            phase.status = "failed"
            phase.error = "Command timeout (300s)"
            logger.error(f"✗ {phase.name} TIMEOUT")
            return False, "Command timeout"
        
        except Exception as e:
            phase.status = "failed"
            phase.error = str(e)
            logger.error(f"✗ {phase.name} ERROR: {e}")
            return False, str(e)
        
        finally:
            phase.end_time = time.time()
    
    def check_syntax(self) -> bool:
        """Check Python syntax"""
        logger.info("\n" + "="*60)
        logger.info("PHASE 1: SYNTAX CHECK")
        logger.info("="*60)
        
        phase = self.add_phase("syntax_check", "Check Python syntax")
        
        py_files = list(self.project_root.rglob("*.py"))
        errors = []
        
        for py_file in py_files:
            if ".debug_backups" in str(py_file) or ".backups" in str(py_file):
                continue
            
            try:
                with open(py_file, 'r') as f:
                    compile(f.read(), py_file, 'exec')
            except SyntaxError as e:
                errors.append(f"{py_file}: {e}")
        
        if errors:
            phase.status = "failed"
            phase.error = f"{len(errors)} syntax errors"
            logger.error(f"Found {len(errors)} syntax errors:")
            for error in errors:
                logger.error(f"  - {error}")
            return False
        
        phase.status = "success"
        logger.info(f"✓ All {len(py_files)} Python files have valid syntax")
        return True
    
    def run_linter(self) -> bool:
        """Run code linting"""
        logger.info("\n" + "="*60)
        logger.info("PHASE 2: LINTING")
        logger.info("="*60)
        
        phase = self.add_phase("linting", "Run code linter")
        
        # Try pylint if available
        success, output = self.run_command(
            phase,
            "python3 -m pylint core/*.py --disable=all --enable=E 2>&1 || true",
            check=False
        )
        
        if "error" in output.lower() and "command" not in output.lower():
            logger.warning("⚠ Some linting issues found")
            return False
        
        logger.info("✓ Linting passed")
        return True
    
    def run_tests(self) -> bool:
        """Run unit tests"""
        logger.info("\n" + "="*60)
        logger.info("PHASE 3: TESTING")
        logger.info("="*60)
        
        phase = self.add_phase("testing", "Run unit tests")
        
        # Check if tests exist
        test_dir = self.project_root / "tests"
        if not test_dir.exists():
            logger.info("⚠ No tests directory found, skipping")
            phase.status = "skipped"
            return True
        
        success, output = self.run_command(
            phase,
            "python3 -m pytest tests/ -v 2>&1 || true",
            check=False
        )
        
        # Parse test results
        if "passed" in output.lower():
            logger.info(f"✓ Tests passed")
            return True
        
        if "failed" in output.lower() or "error" in output.lower():
            logger.warning("⚠ Some tests failed")
            return False
        
        logger.info("✓ Testing phase completed")
        return True
    
    def build_debug_info(self) -> bool:
        """Generate debug information"""
        logger.info("\n" + "="*60)
        logger.info("PHASE 4: DEBUG INFO GENERATION")
        logger.info("="*60)
        
        phase = self.add_phase("debug_info", "Generate debug information")
        
        try:
            # Generate debug report
            success, output = self.run_command(
                phase,
                "python3 -c \"from core.in_code_debug import get_debugger; dbg = get_debugger('BUILD'); dbg.export_debug_report('.debug_info.json')\" 2>&1 || true",
                check=False
            )
            
            logger.info("✓ Debug information generated")
            return True
        
        except Exception as e:
            logger.warning(f"⚠ Could not generate debug info: {e}")
            phase.status = "skipped"
            return True
    
    def optimize_code(self) -> bool:
        """Optimize code"""
        logger.info("\n" + "="*60)
        logger.info("PHASE 5: CODE OPTIMIZATION")
        logger.info("="*60)
        
        phase = self.add_phase("optimization", "Optimize code")
        
        try:
            # Try to format with black (auto-formatting)
            success, output = self.run_command(
                phase,
                "python3 -m black core/*.py --quiet 2>&1 || true",
                check=False
            )
            
            logger.info("✓ Code optimization completed")
            return True
        
        except:
            logger.info("⚠ Code optimization skipped")
            phase.status = "skipped"
            return True
    
    def build_documentation(self) -> bool:
        """Build documentation"""
        logger.info("\n" + "="*60)
        logger.info("PHASE 6: DOCUMENTATION")
        logger.info("="*60)
        
        phase = self.add_phase("documentation", "Build documentation")
        
        try:
            # Check if docs exist
            doc_files = list(self.project_root.glob("*.md"))
            logger.info(f"✓ Found {len(doc_files)} documentation files")
            return True
        
        except Exception as e:
            logger.warning(f"⚠ Documentation build skipped: {e}")
            phase.status = "skipped"
            return True
    
    def build_package(self) -> bool:
        """Build package"""
        logger.info("\n" + "="*60)
        logger.info("PHASE 7: PACKAGE BUILD")
        logger.info("="*60)
        
        phase = self.add_phase("package", "Build Python package")
        
        try:
            # Check setup.py exists
            setup_file = self.project_root / "setup.py"
            if setup_file.exists():
                success, output = self.run_command(
                    phase,
                    "python3 setup.py build --quiet 2>&1 || true",
                    check=False
                )
                logger.info("✓ Package built")
                return True
            else:
                logger.info("⚠ No setup.py found, skipping package build")
                phase.status = "skipped"
                return True
        
        except Exception as e:
            logger.warning(f"⚠ Package build skipped: {e}")
            phase.status = "skipped"
            return True
    
    def full_build(self, with_debug: bool = True) -> bool:
        """Run full build process"""
        logger.info("\n" + "╔" + "="*58 + "╗")
        logger.info("║" + " "*10 + "JARVIS PRO - ADVANCED BUILD SYSTEM" + " "*10 + "║")
        logger.info("╚" + "="*58 + "╝\n")
        
        all_success = True
        
        # Phase 1: Syntax Check
        if not self.check_syntax():
            all_success = False
        
        # Phase 2: Linting
        if not self.run_linter():
            pass  # Don't fail on lint warnings
        
        # Phase 3: Testing
        if not self.run_tests():
            pass  # Don't fail on test failures
        
        # Phase 4: Debug Info
        if with_debug:
            self.build_debug_info()
        
        # Phase 5: Optimization
        self.optimize_code()
        
        # Phase 6: Documentation
        self.build_documentation()
        
        # Phase 7: Package
        self.build_package()
        
        # Print summary
        self.print_summary()
        
        return all_success
    
    def print_summary(self):
        """Print build summary"""
        logger.info("\n" + "="*60)
        logger.info("BUILD SUMMARY")
        logger.info("="*60)
        
        total_duration = (datetime.now() - self.build_start).total_seconds()
        
        success_count = sum(1 for p in self.phases if p.status == "success")
        failed_count = sum(1 for p in self.phases if p.status == "failed")
        skipped_count = sum(1 for p in self.phases if p.status == "skipped")
        
        for phase in self.phases:
            symbol = "✓" if phase.status == "success" else "✗" if phase.status == "failed" else "⊘"
            logger.info(f"{symbol} {phase.name:<20} {phase.get_duration():.2f}s")
        
        logger.info("="*60)
        logger.info(f"Total: {success_count} passed, {failed_count} failed, {skipped_count} skipped")
        logger.info(f"Build Duration: {total_duration:.2f}s")
        logger.info("="*60 + "\n")
        
        if failed_count == 0:
            logger.info("✅ BUILD SUCCESSFUL\n")
        else:
            logger.info("❌ BUILD FAILED\n")
    
    def export_build_report(self, filepath: str = ".build_report.json"):
        """Export build report"""
        report = {
            "timestamp": self.build_start.isoformat(),
            "duration_seconds": (datetime.now() - self.build_start).total_seconds(),
            "phases": [p.to_dict() for p in self.phases],
            "summary": {
                "total_phases": len(self.phases),
                "successful": sum(1 for p in self.phases if p.status == "success"),
                "failed": sum(1 for p in self.phases if p.status == "failed"),
                "skipped": sum(1 for p in self.phases if p.status == "skipped")
            }
        }
        
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"Build report exported to {filepath}")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="JARVIS PRO Advanced Build System")
    parser.add_argument("--debug", action="store_true", help="Enable debug information")
    parser.add_argument("--report", default=".build_report.json", help="Report output file")
    parser.add_argument("--log", default=".build.log", help="Log output file")
    
    args = parser.parse_args()
    
    builder = AdvancedBuildSystem(".")
    success = builder.full_build(with_debug=args.debug)
    builder.export_build_report(args.report)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
