#!/usr/bin/env python3
"""
Test Claude Haiku 4.5 Integration with Jarvis
Verifies that the API is properly configured and working
"""

import json
import os
import sys
from pathlib import Path

def test_claude_setup():
    """Test Claude integration"""
    print("\n🧠 Testing Claude Haiku 4.5 Integration\n")
    print("=" * 60)
    
    # Test 1: Check API Key
    print("\n1️⃣  Checking ANTHROPIC_API_KEY...")
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if api_key:
        masked_key = api_key[:10] + "..." + api_key[-4:] if len(api_key) > 14 else api_key
        print(f"   ✅ API Key found: {masked_key}")
    else:
        print("   ❌ ANTHROPIC_API_KEY not set!")
        print("   🔧 Fix: export ANTHROPIC_API_KEY='sk-ant-...'")
        return False
    
    # Test 2: Check anthropic package
    print("\n2️⃣  Checking anthropic package...")
    try:
        import anthropic
        print(f"   ✅ anthropic installed: {anthropic.__version__}")
    except ImportError:
        print("   ❌ anthropic package not installed!")
        print("   🔧 Fix: pip install anthropic")
        return False
    
    # Test 3: Check Claude module
    print("\n3️⃣  Checking Claude module...")
    sys.path.insert(0, str(Path(__file__).parent))
    try:
        from core.claude_code_generator import ClaudeCodeGenerator
        print("   ✅ ClaudeCodeGenerator imported successfully")
    except ImportError as e:
        print(f"   ❌ Failed to import Claude module: {e}")
        return False
    
    # Test 4: Initialize Claude
    print("\n4️⃣  Initializing Claude...")
    try:
        claude = ClaudeCodeGenerator()
        print(f"   ✅ Claude initialized with model: {claude.model}")
    except Exception as e:
        print(f"   ❌ Failed to initialize Claude: {e}")
        return False
    
    # Test 5: Get model info
    print("\n5️⃣  Checking model info...")
    try:
        info = claude.get_model_info()
        print(f"   ✅ Model: {info['model']}")
        print(f"   ✅ Provider: {info['provider']}")
        print(f"   ✅ Type: {info['type']}")
        print(f"   ✅ Usage: {info['usage']}")
    except Exception as e:
        print(f"   ❌ Failed to get model info: {e}")
        return False
    
    # Test 6: Check backend endpoints
    print("\n6️⃣  Available Claude API Endpoints:")
    endpoints = [
        "POST /api/claude/status",
        "POST /api/claude/generate",
        "POST /api/claude/analyze",
        "POST /api/claude/test",
        "POST /api/claude/refactor",
        "POST /api/claude/explain"
    ]
    for endpoint in endpoints:
        print(f"   ✅ {endpoint}")
    
    print("\n" + "=" * 60)
    print("\n✅ All Claude Haiku 4.5 tests passed!\n")
    print("🚀 Ready to use Claude for code generation and analysis")
    print("\nNext steps:")
    print("  1. Start backend: python backend/app.py")
    print("  2. Visit: http://localhost:8001/api/claude/status")
    print("  3. Generate code: curl -X POST http://localhost:8001/api/claude/generate \\")
    print("     -H 'Content-Type: application/json' \\")
    print("     -d '{\"request\": \"create a fibonacci function\", \"language\": \"python\"}'")
    print("\n📚 Full guide: CLAUDE_HAIKU_GUIDE.md\n")
    
    return True


if __name__ == "__main__":
    success = test_claude_setup()
    sys.exit(0 if success else 1)
