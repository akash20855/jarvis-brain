#!/usr/bin/env python3
"""
In-Code Debug Module - Advanced Debugging Features for JARVIS PRO
Built-in debugging, profiling, and diagnostics directly in code
"""

import sys
import time
import traceback
import inspect
import functools
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional
import json
from pathlib import Path
import logging

# Setup logging
logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('.debug.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class DebugTracer:
    """Trace execution flow through code"""
    
    def __init__(self, name: str = "Application"):
        self.name = name
        self.traces = []
        self.call_stack = []
        self.start_time = time.time()
    
    def enter_function(self, func_name: str, args: tuple, kwargs: dict):
        """Log function entry"""
        timestamp = datetime.now().isoformat()
        depth = len(self.call_stack)
        
        trace = {
            "type": "enter",
            "function": func_name,
            "timestamp": timestamp,
            "depth": depth,
            "args": str(args),
            "kwargs": str(kwargs)
        }
        
        self.traces.append(trace)
        self.call_stack.append(func_name)
        
        logger.debug(f"{'  ' * depth}→ {func_name}({len(args)} args, {len(kwargs)} kwargs)")
    
    def exit_function(self, func_name: str, result: Any = None, error: Optional[Exception] = None):
        """Log function exit"""
        timestamp = datetime.now().isoformat()
        depth = len(self.call_stack) - 1
        
        trace = {
            "type": "exit",
            "function": func_name,
            "timestamp": timestamp,
            "depth": depth,
            "result": str(result) if result else "None",
            "error": str(error) if error else None
        }
        
        self.traces.append(trace)
        if self.call_stack and self.call_stack[-1] == func_name:
            self.call_stack.pop()
        
        if error:
            logger.error(f"{'  ' * depth}← {func_name} [ERROR: {error}]")
        else:
            logger.debug(f"{'  ' * depth}← {func_name}")
    
    def log_variable(self, name: str, value: Any):
        """Log variable value"""
        logger.debug(f"   {name} = {repr(value)}")
    
    def get_call_stack(self) -> List[str]:
        """Get current call stack"""
        return self.call_stack.copy()
    
    def export_traces(self) -> Dict:
        """Export all traces"""
        return {
            "application": self.name,
            "total_traces": len(self.traces),
            "duration_seconds": time.time() - self.start_time,
            "call_stack_depth": len(self.call_stack),
            "traces": self.traces
        }


class PerformanceProfiler:
    """Profile function performance"""
    
    def __init__(self):
        self.profiles = {}
        self.current_profile = None
    
    def start_profile(self, func_name: str):
        """Start profiling a function"""
        if func_name not in self.profiles:
            self.profiles[func_name] = {
                "calls": 0,
                "total_time": 0,
                "min_time": float('inf'),
                "max_time": 0,
                "errors": 0
            }
        
        self.current_profile = {
            "func_name": func_name,
            "start_time": time.time()
        }
    
    def end_profile(self, error: bool = False):
        """End profiling"""
        if not self.current_profile:
            return
        
        elapsed = time.time() - self.current_profile["start_time"]
        func_name = self.current_profile["func_name"]
        
        profile = self.profiles[func_name]
        profile["calls"] += 1
        profile["total_time"] += elapsed
        profile["min_time"] = min(profile["min_time"], elapsed)
        profile["max_time"] = max(profile["max_time"], elapsed)
        
        if error:
            profile["errors"] += 1
        
        self.current_profile = None
    
    def get_profile(self, func_name: str) -> Dict:
        """Get profile for function"""
        if func_name not in self.profiles:
            return None
        
        profile = self.profiles[func_name]
        avg_time = profile["total_time"] / profile["calls"] if profile["calls"] > 0 else 0
        
        return {
            "function": func_name,
            "calls": profile["calls"],
            "total_time_ms": profile["total_time"] * 1000,
            "avg_time_ms": avg_time * 1000,
            "min_time_ms": profile["min_time"] * 1000,
            "max_time_ms": profile["max_time"] * 1000,
            "errors": profile["errors"]
        }
    
    def get_all_profiles(self) -> List[Dict]:
        """Get all profiles"""
        return [self.get_profile(name) for name in self.profiles.keys()]


class BreakPoint:
    """Conditional breakpoint system"""
    
    def __init__(self):
        self.breakpoints = []
        self.break_hits = 0
        self.paused = False
    
    def add_breakpoint(self, file: str, line: int, condition: Optional[Callable] = None):
        """Add breakpoint"""
        bp = {
            "id": len(self.breakpoints),
            "file": file,
            "line": line,
            "condition": condition,
            "hits": 0
        }
        self.breakpoints.append(bp)
        logger.info(f"Breakpoint added: {file}:{line}")
        return bp["id"]
    
    def check_breakpoint(self, file: str, line: int, context: Dict = None) -> bool:
        """Check if breakpoint should trigger"""
        for bp in self.breakpoints:
            if bp["file"] == file and bp["line"] == line:
                # Check condition if exists
                if bp["condition"] and context:
                    if not bp["condition"](context):
                        continue
                
                bp["hits"] += 1
                self.break_hits += 1
                logger.warning(f"BREAKPOINT HIT: {file}:{line} (hit #{bp['hits']})")
                return True
        
        return False


class InCodeDebugger:
    """Main in-code debugger"""
    
    def __init__(self, app_name: str = "JARVIS"):
        self.app_name = app_name
        self.tracer = DebugTracer(app_name)
        self.profiler = PerformanceProfiler()
        self.breakpoints = BreakPoint()
        self.debug_enabled = True
        self.debug_level = "INFO"  # TRACE, DEBUG, INFO, WARNING, ERROR
        
        logger.info(f"InCodeDebugger initialized for {app_name}")
    
    def debug_function(self, enable_trace: bool = True, enable_profile: bool = True):
        """Decorator to add debugging to functions"""
        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                func_name = func.__name__
                
                if enable_trace:
                    self.tracer.enter_function(func_name, args, kwargs)
                
                if enable_profile:
                    self.profiler.start_profile(func_name)
                
                try:
                    result = func(*args, **kwargs)
                    
                    if enable_profile:
                        self.profiler.end_profile(error=False)
                    
                    if enable_trace:
                        self.tracer.exit_function(func_name, result)
                    
                    return result
                
                except Exception as e:
                    if enable_profile:
                        self.profiler.end_profile(error=True)
                    
                    if enable_trace:
                        self.tracer.exit_function(func_name, error=e)
                    
                    logger.exception(f"Error in {func_name}: {e}")
                    raise
            
            return wrapper
        return decorator
    
    def checkpoint(self, name: str, context: Optional[Dict] = None):
        """Log a debug checkpoint"""
        logger.info(f"CHECKPOINT: {name}")
        if context:
            logger.debug(f"Context: {json.dumps(context, default=str)}")
    
    def inspect_object(self, obj: Any, name: str = "Object"):
        """Inspect object properties"""
        logger.debug(f"\n{'='*60}")
        logger.debug(f"Object Inspection: {name}")
        logger.debug(f"{'='*60}")
        logger.debug(f"Type: {type(obj)}")
        logger.debug(f"Value: {repr(obj)}")
        
        if hasattr(obj, '__dict__'):
            logger.debug(f"Attributes: {obj.__dict__}")
        
        if callable(obj):
            logger.debug(f"Callable: Yes")
            try:
                sig = inspect.signature(obj)
                logger.debug(f"Signature: {sig}")
            except:
                pass
        
        logger.debug(f"{'='*60}\n")
    
    def dump_state(self, state: Dict, name: str = "State"):
        """Dump application state"""
        logger.info(f"\nState Dump: {name}")
        logger.info(json.dumps(state, indent=2, default=str))
    
    def get_execution_report(self) -> Dict:
        """Get complete execution debug report"""
        return {
            "application": self.app_name,
            "timestamp": datetime.now().isoformat(),
            "tracing": self.tracer.export_traces(),
            "profiling": {
                "total_functions": len(self.profiler.profiles),
                "profiles": self.profiler.get_all_profiles()
            },
            "breakpoints": {
                "total": len(self.breakpoints.breakpoints),
                "hits": self.breakpoints.break_hits
            }
        }
    
    def export_debug_report(self, filepath: str = ".debug_report.json"):
        """Export debug report to file"""
        report = self.get_execution_report()
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2)
        logger.info(f"Debug report exported to {filepath}")


# Global debugger instance
_debugger = None


def get_debugger(app_name: str = "JARVIS") -> InCodeDebugger:
    """Get or create global debugger"""
    global _debugger
    if _debugger is None:
        _debugger = InCodeDebugger(app_name)
    return _debugger


def debug_function(enable_trace: bool = True, enable_profile: bool = True):
    """Global debug decorator"""
    debugger = get_debugger()
    return debugger.debug_function(enable_trace, enable_profile)


def checkpoint(name: str, context: Optional[Dict] = None):
    """Log a global checkpoint"""
    debugger = get_debugger()
    debugger.checkpoint(name, context)


def inspect(obj: Any, name: str = "Object"):
    """Globally inspect object"""
    debugger = get_debugger()
    debugger.inspect_object(obj, name)


def dump_state(state: Dict, name: str = "State"):
    """Globally dump state"""
    debugger = get_debugger()
    debugger.dump_state(state, name)


def get_report() -> Dict:
    """Get global debug report"""
    debugger = get_debugger()
    return debugger.get_execution_report()


def export_report(filepath: str = ".debug_report.json"):
    """Export global debug report"""
    debugger = get_debugger()
    debugger.export_debug_report(filepath)


# Example usage
if __name__ == "__main__":
    # Get debugger
    dbg = get_debugger("TestApp")
    
    # Use decorator
    @dbg.debug_function(enable_trace=True, enable_profile=True)
    def test_function(x, y):
        """Test function"""
        dbg.checkpoint("In test_function", {"x": x, "y": y})
        return x + y
    
    @dbg.debug_function()
    def complex_operation():
        """Complex operation"""
        dbg.checkpoint("Start complex operation")
        result = test_function(5, 10)
        dbg.checkpoint("Got result", {"result": result})
        return result * 2
    
    # Run test
    print("Running debug test...")
    result = complex_operation()
    print(f"Result: {result}")
    
    # Export report
    dbg.export_debug_report()
    print("\nDebug report exported to .debug_report.json")
    
    # Show profiling
    print("\nPerformance Profiles:")
    for profile in dbg.profiler.get_all_profiles():
        print(f"  {profile['function']}: {profile['avg_time_ms']:.2f}ms avg")
