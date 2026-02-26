#!/usr/bin/env python3
"""
JARVIS Pro: Integrated Build & Debug Automation

This script combines the build and debug systems for seamless development.
Usage: python3 build-debug.py [--debug] [--improve] [--monitor] [--report]
"""

import sys
import argparse
import json
import subprocess
from pathlib import Path
from datetime import datetime
from core.advanced_build import AdvancedBuildSystem
from core.in_code_debug import InCodeDebugger, export_report, checkpoint


class BuildDebugIntegration:
    """Integrated build and debug workflow"""
    
    def __init__(self, debug=False, improve=False, monitor=False):
        self.debug = debug
        self.improve = improve
        self.monitor = monitor
        self.build_system = AdvancedBuildSystem()
        self.debugger = InCodeDebugger("BuildDebugIntegration")
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "build": None,
            "debug": None,
            "improve": None,
            "status": "pending"
        }
    
    def run_build(self):
        """Execute the build pipeline"""
        print("\n" + "="*70)
        print("🔨 PHASE 1: ADVANCED BUILD")
        print("="*70)
        
        checkpoint("Starting build phase")
        
        try:
            self.build_system.execute_build()
            self.results["build"] = {
                "status": "success",
                "phases": len(self.build_system.phases),
                "total_time": sum(p.duration for p in self.build_system.phases)
            }
            checkpoint("Build phase completed successfully")
            return True
        except Exception as e:
            print(f"❌ Build failed: {e}")
            self.results["build"] = {"status": "failed", "error": str(e)}
            checkpoint(f"Build phase failed: {e}")
            return False
    
    def run_debug(self):
        """Execute debug collection"""
        print("\n" + "="*70)
        print("🔍 PHASE 2: DEBUG ANALYSIS")
        print("="*70)
        
        checkpoint("Starting debug analysis phase")
        
        try:
            # Check for debug files
            debug_log = Path(".debug.log")
            debug_report = Path(".debug_report.json")
            build_report = Path(".build_report.json")
            
            debug_info = {
                "status": "success",
                "files_found": []
            }
            
            if debug_log.exists():
                lines = debug_log.read_text().count('\n')
                debug_info["files_found"].append(f"debug.log ({lines} lines)")
                print(f"✅ Found debug log: {lines} lines")
            
            if debug_report.exists():
                report = json.loads(debug_report.read_text())
                debug_info["files_found"].append("debug_report.json")
                print(f"✅ Found debug report with {len(report)} entries")
            
            if build_report.exists():
                report = json.loads(build_report.read_text())
                debug_info["phases_analyzed"] = len(report.get("phases", {}))
                debug_info["files_found"].append(f"build_report.json ({debug_info['phases_analyzed']} phases)")
                print(f"✅ Found build report with {debug_info['phases_analyzed']} phases")
            
            self.results["debug"] = debug_info
            checkpoint("Debug analysis phase completed")
            return True
        except Exception as e:
            print(f"❌ Debug analysis failed: {e}")
            self.results["debug"] = {"status": "failed", "error": str(e)}
            checkpoint(f"Debug analysis failed: {e}")
            return False
    
    def run_improve(self):
        """Auto-improve the codebase"""
        print("\n" + "="*70)
        print("✨ PHASE 3: AUTO-IMPROVEMENT")
        print("="*70)
        
        checkpoint("Starting auto-improvement phase")
        
        try:
            # Use JARVIS Pro Model to improve code
            print("🤖 Using JARVIS Pro Model for auto-improvement...")
            result = subprocess.run(
                [sys.executable, "jarvis_pro_model.py", "improve", "10"],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                self.results["improve"] = {
                    "status": "success",
                    "output": result.stdout[:500]  # First 500 chars
                }
                checkpoint("Auto-improvement completed successfully")
                print("✅ Auto-improvement complete")
                return True
            else:
                error = result.stderr or "Unknown error"
                self.results["improve"] = {"status": "failed", "error": error}
                checkpoint(f"Auto-improvement failed: {error}")
                print(f"⚠️  Auto-improvement warning: {error[:100]}")
                return False
        except subprocess.TimeoutExpired:
            self.results["improve"] = {"status": "timeout"}
            checkpoint("Auto-improvement timed out")
            print("⏱️  Auto-improvement timed out (>60s)")
            return False
        except Exception as e:
            self.results["improve"] = {"status": "failed", "error": str(e)}
            checkpoint(f"Auto-improvement error: {e}")
            print(f"❌ Auto-improvement error: {e}")
            return False
    
    def monitor_project(self):
        """Continuous monitoring mode"""
        print("\n" + "="*70)
        print("👀 PHASE 4: PROJECT MONITORING")
        print("="*70)
        
        checkpoint("Starting continuous monitoring")
        
        try:
            import time
            monitor_iterations = 0
            max_iterations = 3
            
            while monitor_iterations < max_iterations:
                monitor_iterations += 1
                print(f"\n🔄 Monitoring iteration {monitor_iterations}/{max_iterations}")
                
                # Quick build check
                print("  • Running syntax check...")
                result = subprocess.run(
                    [sys.executable, "core/advanced_build.py"],
                    capture_output=True,
                    timeout=30
                )
                
                if result.returncode == 0:
                    print("    ✅ Syntax check passed")
                else:
                    print("    ❌ Syntax errors detected")
                
                if monitor_iterations < max_iterations:
                    print("  Waiting 5 seconds before next check...")
                    time.sleep(5)
            
            self.results["monitor"] = {
                "status": "success",
                "iterations": monitor_iterations
            }
            checkpoint(f"Monitoring completed ({monitor_iterations} iterations)")
            print(f"\n✅ Monitoring complete ({monitor_iterations} iterations)")
            return True
        except Exception as e:
            self.results["monitor"] = {"status": "failed", "error": str(e)}
            checkpoint(f"Monitoring failed: {e}")
            print(f"❌ Monitoring error: {e}")
            return False
    
    def generate_report(self):
        """Generate integrated report"""
        print("\n" + "="*70)
        print("📊 INTEGRATED REPORT")
        print("="*70)
        
        # Update final status
        all_passed = all(
            self.results.get(key, {}).get("status") == "success"
            for key in ["build", "debug", "improve"] if self.results.get(key)
        )
        self.results["status"] = "success" if all_passed else "partial"
        
        # Print summary
        print(f"\n⏰ Timestamp: {self.results['timestamp']}")
        print(f"📈 Overall Status: {self.results['status'].upper()}")
        
        for phase, data in self.results.items():
            if phase not in ["timestamp", "status"] and isinstance(data, dict):
                status = data.get("status", "unknown").upper()
                icon = "✅" if status == "SUCCESS" else "❌" if status == "FAILED" else "⏱️"
                print(f"\n{icon} {phase.upper()}")
                for key, value in data.items():
                    if key not in ["status", "error"] and not isinstance(value, list):
                        print(f"   • {key}: {value}")
                if "error" in data:
                    print(f"   • Error: {data['error'][:100]}")
        
        # Save report
        report_file = Path(".build_debug_report.json")
        report_file.write_text(json.dumps(self.results, indent=2))
        print(f"\n💾 Report saved to {report_file}")
        
        # Export debug report
        try:
            export_report()
            print("💾 Debug data exported")
        except:
            pass
    
    def execute(self):
        """Execute the complete workflow"""
        print("\n" + "🚀 "*20)
        print("JARVIS PRO: BUILD & DEBUG INTEGRATION")
        print("🚀 "*20)
        
        # Phase 1: Build
        if not self.run_build():
            print("\n⚠️  Build failed, skipping remaining phases")
            self.generate_report()
            return 1
        
        # Phase 2: Debug
        if not self.run_debug():
            print("\n⚠️  Debug analysis had issues")
        
        # Phase 3: Auto-Improve (optional)
        if self.improve:
            if not self.run_improve():
                print("\n⚠️  Auto-improvement had issues")
        else:
            print("\nℹ️  Skipping auto-improvement (use --improve to enable)")
        
        # Phase 4: Monitor (optional)
        if self.monitor:
            if not self.run_monitor():
                print("\n⚠️  Monitoring had issues")
        else:
            print("\nℹ️  Skipping continuous monitoring (use --monitor to enable)")
        
        # Generate final report
        self.generate_report()
        
        # Exit code
        return 0 if self.results["status"] == "success" else 1


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="JARVIS Pro: Integrated Build & Debug System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 build-debug.py                    # Build only
  python3 build-debug.py --debug            # Build with debug analysis
  python3 build-debug.py --debug --improve  # Build, debug, and improve
  python3 build-debug.py --monitor          # Continuous monitoring
  python3 build-debug.py --all              # Everything
        """
    )
    
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug analysis phase"
    )
    parser.add_argument(
        "--improve",
        action="store_true",
        help="Enable auto-improvement phase"
    )
    parser.add_argument(
        "--monitor",
        action="store_true",
        help="Enable continuous monitoring"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Enable all phases"
    )
    parser.add_argument(
        "--report",
        type=str,
        default=".build_debug_report.json",
        help="Report output file (default: .build_debug_report.json)"
    )
    
    args = parser.parse_args()
    
    # Handle --all flag
    if args.all:
        args.debug = True
        args.improve = True
        args.monitor = True
    
    # Create and execute
    integration = BuildDebugIntegration(
        debug=args.debug,
        improve=args.improve,
        monitor=args.monitor
    )
    
    try:
        exit_code = integration.execute()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        integration.generate_report()
        exit_code = 2
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        integration.generate_report()
        exit_code = 3
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
