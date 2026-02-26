# JARVIS Pro: Build & Debug Integration Guide

## Overview

This guide demonstrates how to use JARVIS's integrated build and debugging systems to develop, test, and optimize your code with zero manual intervention.

## 📦 Advanced Build System

### 7-Phase Build Pipeline

The build system automatically executes 7 phases in sequence:

```
Phase 1: Syntax Check   → Python AST validation
Phase 2: Linting        → Code quality analysis (pylint)
Phase 3: Testing        → Unit tests (pytest)
Phase 4: Debug Info     → Debug data generation
Phase 5: Optimization   → Code formatting (black)
Phase 6: Documentation  → Markdown validation
Phase 7: Packaging      → Python package creation
```

### Quick Build Commands

```bash
# Fast build (syntax check only)
make build-fast

# Advanced build with debug support
make build-advanced

# Show build report
make build-report

# Clean build artifacts
make build-clean

# Full debug suite (all phases + profiling)
make debug-full
```

### Direct Usage

```bash
# Basic build
python3 core/advanced_build.py

# Build with debug information
python3 core/advanced_build.py --debug

# Build with custom report file
python3 core/advanced_build.py --report my_build_report.json

# Build with custom log file
python3 core/advanced_build.py --log my_build.log

# Combine options
python3 core/advanced_build.py --debug --report report.json --log build.log
```

### Output Files

After each build, you get:

- **`.build.log`** - Complete build log with timestamps
- **`.build_report.json`** - JSON report with phase details, timings, errors

### Example Build Report

```json
{
  "timestamp": "2024-01-20T10:30:45.123456",
  "total_time": 45.23,
  "status": "success",
  "phases": {
    "syntax_check": {
      "status": "success",
      "duration": 5.12,
      "files_checked": 42,
      "errors": 0
    },
    "linting": {
      "status": "success",
      "duration": 12.45,
      "issues": 3,
      "warnings": 7
    }
  }
}
```

## 🔍 In-Code Debugging

### Decorator-Based Integration

Add the `@debug_function()` decorator to any function:

```python
from core.in_code_debug import debug_function

@debug_function()
def my_complex_function(x, y):
    result = x + y
    return result
```

### Automatic Tracing Example

```python
from core.in_code_debug import debug_function, checkpoint, export_report

@debug_function()
def process_data(items):
    checkpoint("Starting data processing")
    
    results = []
    for item in items:
        checkpoint(f"Processing item: {item}")
        result = transform(item)
        results.append(result)
    
    checkpoint("Processing complete")
    export_report()  # Export debug data
    return results
```

### Available Debug Functions

#### 1. **Tracing with Checkpoints**

```python
from core.in_code_debug import checkpoint

def my_function():
    checkpoint("Starting operation")
    # ... code ...
    checkpoint("Halfway done")
    # ... more code ...
    checkpoint("Complete", {"status": "success"})
```

#### 2. **Performance Profiling**

```python
from core.in_code_debug import InCodeDebugger

debugger = InCodeDebugger("MyFunction")
debugger.start_profile("expensive_operation")
# ... do expensive work ...
debugger.end_profile("expensive_operation")

print(debugger.profiler.get_stats("expensive_operation"))
```

#### 3. **Object Inspection**

```python
from core.in_code_debug import inspect

def debug_my_object():
    obj = MyClass()
    inspect(obj)  # Prints all attributes and their values
```

#### 4. **State Dumping**

```python
from core.in_code_debug import dump_state

def capture_state():
    state = {
        "timestamp": datetime.now(),
        "variables": locals(),
        "status": "processing"
    }
    dump_state(state)  # Saves to .debug_state.json
```

#### 5. **Full Report Export**

```python
from core.in_code_debug import export_report

def save_debug_info():
    export_report()  # Exports .debug_report.json with all data
```

### Debug Command Reference

```bash
# View debug logs (last 50 lines)
make debug-logs

# View debug report
make debug-report

# Run with tracing enabled
make debug-trace

# Show performance profile
make debug-profile

# Full debug suite
make debug-full
```

## 🔄 Complete Workflow: Build → Debug → Test

### Scenario 1: Develop a New Module

```bash
# Step 1: Create your module
cat > my_module.py << 'EOF'
from core.in_code_debug import debug_function, checkpoint

@debug_function()
def analyze_data(data):
    checkpoint("Starting analysis")
    result = sum(data) / len(data)
    checkpoint(f"Result: {result}")
    return result
EOF

# Step 2: Run advanced build with debug
make build-advanced

# Step 3: Check build report
make build-report

# Step 4: View debug logs
make debug-logs
```

### Scenario 2: Debug Failing Code

```bash
# Step 1: Add debugging to the problematic function
# (Edit your function, add @debug_function() decorator)

# Step 2: Run full debug suite
make debug-full

# Step 3: Review debug report and logs
make debug-report
make debug-logs

# Step 4: Auto-fix with JARVIS
make pro-debug 5  # Fix up to 5 issues
```

### Scenario 3: Performance Optimization

```bash
# Step 1: Profile the code
make debug-profile

# Step 2: Build with optimization
python3 core/advanced_build.py --debug

# Step 3: Auto-improve performance
make pro-improve 10

# Step 4: Verify improvements
make build-advanced
make debug-profile
```

## 🎯 Integration with JARVIS Pro Model

### Auto-Build on Error

```bash
# CLI version - auto-builds after improvement
python3 jarvis_pro_model.py improve 10 --build

# Or manually
make pro-improve 5
make build-advanced
```

### Interactive Mode with Debugging

```bash
# Start interactive mode
make pro-interactive

# Then type:
# "improve performance"
# "debug the project"
# "build with full debugging"
# "show me the debug report"
```

## 📊 Real-World Examples

### Example 1: REST API Endpoint with Debugging

```python
from core.in_code_debug import debug_function, checkpoint
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/analyze', methods=['POST'])
@debug_function()
def analyze():
    checkpoint("API call received")
    data = request.get_json()
    
    checkpoint(f"Processing {len(data)} items")
    results = process_items(data)
    
    checkpoint("Returning results")
    return jsonify({"results": results})

if __name__ == '__main__':
    app.run(debug=True)
```

### Example 2: Data Pipeline with Profiling

```python
from core.in_code_debug import debug_function, checkpoint, export_report

@debug_function()
def data_pipeline():
    checkpoint("Loading data")
    data = load_data()
    
    checkpoint("Transforming data")
    transformed = transform(data)
    
    checkpoint("Validating results")
    validate(transformed)
    
    checkpoint("Pipeline complete")
    export_report()
    return transformed
```

### Example 3: Multi-Step Workflow

```python
from core.in_code_debug import InCodeDebugger, checkpoint

debugger = InCodeDebugger("DataWorkflow")

def workflow():
    checkpoint("Starting workflow")
    
    debugger.start_profile("load")
    step1_data = load_data()
    debugger.end_profile("load")
    
    debugger.start_profile("process")
    result = process(step1_data)
    debugger.end_profile("process")
    
    checkpoint("Workflow success", {"items": len(result)})
    return result
```

## 🚀 Advanced Configuration

### Custom Build Phases

Edit `core/advanced_build.py` to add custom phases:

```python
class CustomBuildSystem(AdvancedBuildSystem):
    def custom_phase(self):
        """Your custom build phase"""
        phase = BuildPhase("custom", "Custom Processing")
        phase.start()
        
        # Your logic here
        result = your_custom_logic()
        
        phase.complete(status="success" if result else "failure")
        self.phases.append(phase)
```

### Debug Output Formats

Control debug output with environment variables:

```bash
# JSON output only (no logs)
DEBUG_FORMAT=json make build-advanced

# Verbose logging
DEBUG_LEVEL=verbose make debug-full

# Silent mode
DEBUG_SILENT=true make build-fast
```

## 📈 Monitoring & Reporting

### Build Metrics Dashboard

```bash
# Quick metrics
python3 -c "
import json
with open('.build_report.json') as f:
    report = json.load(f)
    print(f\"Build Time: {report['total_time']:.2f}s\")
    print(f\"Status: {report['status']}\")
    for phase, data in report['phases'].items():
        print(f\"  {phase}: {data['duration']:.2f}s\")
"
```

### Debug Data Analysis

```bash
# Extract all checkpoints from debug report
python3 -c "
import json
with open('.debug_report.json') as f:
    report = json.load(f)
    for checkpoint in report.get('checkpoints', []):
        print(f\"{checkpoint['time']}: {checkpoint['message']}\")
"
```

## 🔧 Troubleshooting

### Build Fails at Linting Phase

```bash
# Check linting errors in detail
python3 -m pylint core/*.py --disable=all --enable=E,W

# Auto-fix with black
python3 -m black core/ --line-length 100
```

### Debug Report Not Generated

```bash
# Ensure @debug_function decorator is present
grep -r "@debug_function" . --include="*.py"

# Manually trigger debug collection
python3 -c "from core.in_code_debug import export_report; export_report()"
```

### Build Timeout on Large Projects

```bash
# Skip slower phases
python3 core/advanced_build.py --skip-test --skip-lint

# Or use fast build
make build-fast
```

## 📚 Related Documentation

- [JARVIS PRO MODEL](JARVIS_PRO_MODEL.md) - Main features
- [PRO_INTEGRATION_GUIDE](PRO_INTEGRATION_GUIDE.md) - Full integration
- [IN_CODE_DEBUG.md](IN_CODE_DEBUG.md) - Debug system details
- [ADVANCED_BUILD.md](ADVANCED_BUILD.md) - Build system details

## ✅ Quick Reference

| Command | Purpose |
|---------|---------|
| `make build-fast` | Quick syntax check |
| `make build-advanced` | Full build with debug |
| `make build-clean` | Remove build artifacts |
| `make debug-logs` | View debug logs |
| `make debug-report` | View debug report |
| `make debug-full` | Complete debug suite |
| `make pro-debug 5` | Auto-fix 5 bugs |
| `make pro-improve 10` | Improve 10 files |

---

**Happy Building & Debugging! 🚀**
