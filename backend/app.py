"""
Jarvis Brain - Backend API
Full-stack server for AI-powered code evolution
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from pathlib import Path
import json
import logging
from datetime import datetime
import sys
import os

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.auto_evolution import AutoEvolutionEngine
from core.chatbot import JarvisChatbot
from core.code_generator import CodeGenerator

app = Flask(__name__)
CORS(app)

# Initialize engines
project_root = Path(__file__).parent.parent / "jarvis-brain"
evolution_engine = AutoEvolutionEngine(str(project_root))
chatbot = JarvisChatbot(str(project_root))
code_generator = CodeGenerator()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.route("/", methods=["GET"])
def root():
    """API root - returns server info"""
    return jsonify({
        "name": "Jarvis Brain API",
        "version": "1.0.0",
        "description": "Full-stack AI-powered code evolution system",
        "status": "online",
        "api_url": "http://localhost:8000/api",
        "docs": "API endpoints starting with /api/*"
    })


@app.route("/api", methods=["GET"])
@app.route("/api/", methods=["GET"])
def api_root():
    """API root - lists available endpoints"""
    return jsonify({
        "success": True,
        "message": "Jarvis Brain API",
        "version": "1.0.0",
        "endpoints": {
            "health": "GET /api/health",
            "project": "GET /api/project/status",
            "ai": "GET /api/ai/status",
            "chat": ["POST /api/chat/message", "GET /api/chat/commands"],
            "evolve": ["GET /api/evolve/suggestions", "POST /api/evolve/analyze", "POST /api/evolve/file"],
            "history": "GET /api/history/improvements",
            "config": ["GET /api/config/get", "POST /api/config/set"]
        }
    })


@app.route("/api/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "online",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    })


@app.route("/api/project/status", methods=["GET"])
def project_status():
    """Get project status"""
    return jsonify({
        "project_root": str(project_root),
        "status": "ready",
        "features": [
            "auto_evolution",
            "chatbot",
            "code_analysis",
            "ai_integration"
        ]
    })


@app.route("/api/ai/status", methods=["GET"])
def ai_status():
    """Check AI backend status"""
    import os
    import requests
    
    # Get Ollama URLs from environment or use defaults
    ollama_url = os.getenv('OLLAMA_BASE_URL', 'http://host.docker.internal:11434')
    
    ollama_running = False
    try:
        requests.get(f"{ollama_url}/api/tags", timeout=2)
        ollama_running = True
    except:
        pass
    
    return jsonify({
        "ollama": {
            "status": "online" if ollama_running else "offline",
            "url": ollama_url
        },
        "local_patterns": {
            "status": "ready",
            "description": "Works offline"
        }
    })


@app.route("/api/evolve/analyze", methods=["POST"])
def analyze_project():
    """Analyze entire project for improvements"""
    try:
        data = request.get_json() or {}
        ai_backend = data.get("ai_backend", "patterns")
        
        logger.info(f"Starting project analysis with {ai_backend}...")
        
        results = evolution_engine.scan_project()
        
        # Add timestamp
        results["timestamp"] = datetime.now().isoformat()
        results["ai_backend"] = ai_backend
        
        return jsonify({
            "success": True,
            "data": results
        })
    
    except Exception as e:
        logger.error(f"Analysis error: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route("/api/evolve/file", methods=["POST"])
def analyze_file():
    """Analyze specific file"""
    try:
        data = request.get_json()
        filepath = data.get("filepath")
        
        if not filepath:
            return jsonify({"success": False, "error": "filepath required"}), 400
        
        file_path = project_root / filepath
        
        if not file_path.exists():
            return jsonify({"success": False, "error": f"File not found: {filepath}"}), 404
        
        with open(file_path) as f:
            code = f.read()
        
        suggestions = evolution_engine.get_improvement_suggestions(code, filepath)
        
        return jsonify({
            "success": True,
            "file": filepath,
            "suggestions": suggestions,
            "count": len(suggestions)
        })
    
    except Exception as e:
        logger.error(f"File analysis error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/evolve/suggestions", methods=["GET"])
def get_suggestions():
    """Get top suggestions"""
    try:
        limit = request.args.get("limit", 10, type=int)
        
        results = evolution_engine.scan_project()
        
        # Collect all suggestions
        all_suggestions = []
        for filepath, suggestions in results.get("files", {}).items():
            for suggestion in suggestions:
                suggestion["file"] = filepath
                all_suggestions.append(suggestion)
        
        # Sort by severity
        severity_order = {"high": 0, "medium": 1, "low": 2}
        all_suggestions.sort(
            key=lambda x: severity_order.get(x.get("severity", "low"), 3)
        )
        
        return jsonify({
            "success": True,
            "suggestions": all_suggestions[:limit],
            "total": len(all_suggestions)
        })
    
    except Exception as e:
        logger.error(f"Get suggestions error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/chat/message", methods=["POST"])
def chat_message():
    """Send message to chatbot"""
    try:
        data = request.get_json()
        message = data.get("message", "").strip()
        
        if not message:
            return jsonify({"success": False, "error": "message required"}), 400
        
        response = chatbot.chat(message)
        
        if response is None:
            response = "Goodbye!"
        
        # Check if response is a code generation request (dict)
        if isinstance(response, dict) and response.get("type") == "code_generation":
            # Handle code generation
            code_request = response.get("request")
            language = response.get("language", "python")
            filename = response.get("filename", "generated_code")
            
            try:
                # Generate code
                generated_code = code_generator.generate_code(code_request, language)
                
                if generated_code.get("error"):
                    return jsonify({
                        "success": False,
                        "error": generated_code.get("error"),
                        "type": "code_generation"
                    })
                
                # Save code
                filepath = code_generator.save_code(
                    generated_code.get("code"),
                    filename,
                    language
                )
                
                # Open in VS Code
                code_generator.open_in_vscode(filepath.get("filepath"))
                
                return jsonify({
                    "success": True,
                    "type": "code_generation",
                    "message": "✅ Code generated and opened in VS Code!",
                    "code": generated_code.get("code"),
                    "language": language,
                    "filename": filename,
                    "filepath": filepath.get("filepath")
                })
            
            except Exception as e:
                logger.error(f"Code generation error: {e}")
                return jsonify({
                    "success": False,
                    "type": "code_generation",
                    "error": str(e)
                }), 500
        
        return jsonify({
            "success": True,
            "message": response,
            "timestamp": datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"Chat error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/chat/commands", methods=["GET"])
def chat_commands():
    """Get available chat commands"""
    return jsonify({
        "success": True,
        "commands": {
            "analyze": "Scan entire project",
            "file": "Analyze specific file (file <path>)",
            "suggestions": "Show top suggestions",
            "help": "Show help",
            "status": "Show project status"
        }
    })


@app.route("/api/history/improvements", methods=["GET"])
def history_improvements():
    """Get improvement history"""
    try:
        limit = request.args.get("limit", 20, type=int)
        
        evolution_log = project_root / ".evolution_log.json"
        
        if not evolution_log.exists():
            return jsonify({
                "success": True,
                "improvements": [],
                "total": 0
            })
        
        with open(evolution_log) as f:
            data = json.load(f)
        
        improvements = data.get("improvements", [])[-limit:]
        
        return jsonify({
            "success": True,
            "improvements": improvements,
            "total": len(improvements)
        })
    
    except Exception as e:
        logger.error(f"History error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/config/get", methods=["GET"])
def get_config():
    """Get configuration"""
    try:
        config_file = project_root / ".evolution_config.json"
        
        if config_file.exists():
            with open(config_file) as f:
                config = json.load(f)
        else:
            config = {
                "auto_evolution": {
                    "enabled": True,
                    "ai_backend": "patterns",
                    "scan_interval_seconds": 3600
                }
            }
        
        return jsonify({
            "success": True,
            "config": config
        })
    
    except Exception as e:
        logger.error(f"Config error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/config/set", methods=["POST"])
def set_config():
    """Update configuration"""
    try:
        data = request.get_json()
        config_file = project_root / ".evolution_config.json"
        
        with open(config_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        return jsonify({
            "success": True,
            "message": "Configuration updated"
        })
    
    except Exception as e:
        logger.error(f"Config update error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


# ============================================================================
# CODE GENERATION ENDPOINTS
# ============================================================================

@app.route("/api/generate/code", methods=["POST"])
def generate_code():
    """
    Generate code based on natural language request
    
    Request JSON:
    {
        "request": "make a calculator",
        "language": "python"  # optional, defaults to python
    }
    """
    try:
        data = request.get_json()
        if not data or "request" not in data:
            return jsonify({"success": False, "error": "Missing 'request' field"}), 400
        
        code_request = data.get("request")
        language = data.get("language", "python")
        
        logger.info(f"Generating code: {code_request[:50]}...")
        generated_code = code_generator.generate_code(code_request, language)
        
        return jsonify({
            "success": True,
            "code": generated_code,
            "language": language,
            "request": code_request
        })
    
    except Exception as e:
        logger.error(f"Code generation error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/code/save", methods=["POST"])
def save_code():
    """
    Save generated code to a file
    
    Request JSON:
    {
        "code": "print('hello')",
        "filename": "script.py",
        "language": "python"
    }
    """
    try:
        data = request.get_json()
        if not all(k in data for k in ["code", "filename", "language"]):
            return jsonify({"success": False, "error": "Missing required fields"}), 400
        
        filepath = code_generator.save_code(
            data["code"],
            data["filename"],
            data["language"]
        )
        
        return jsonify({
            "success": True,
            "message": "Code saved successfully",
            "filepath": filepath
        })
    
    except Exception as e:
        logger.error(f"Code save error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/code/execute", methods=["POST"])
def execute_code():
    """
    Execute code from a file
    
    Request JSON:
    {
        "filepath": "/path/to/script.py"
    }
    """
    try:
        data = request.get_json()
        if "filepath" not in data:
            return jsonify({"success": False, "error": "Missing 'filepath' field"}), 400
        
        output = code_generator.execute_code(data["filepath"])
        
        return jsonify({
            "success": True,
            "output": output,
            "filepath": data["filepath"]
        })
    
    except Exception as e:
        logger.error(f"Code execution error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/code/create-and-open", methods=["POST"])
def create_and_open_code():
    """
    Generate code, save it, and open in VS Code
    
    Request JSON:
    {
        "request": "make a calculator",
        "filename": "calculator.py",
        "language": "python"
    }
    """
    try:
        data = request.get_json()
        if not all(k in data for k in ["request", "filename", "language"]):
            return jsonify({"success": False, "error": "Missing required fields"}), 400
        
        # Generate code
        logger.info(f"Creating code for: {data['request'][:50]}...")
        generated_code = code_generator.generate_code(data["request"], data["language"])
        
        # Save code
        filepath = code_generator.save_code(
            generated_code,
            data["filename"],
            data["language"]
        )
        
        # Open in VS Code
        code_generator.open_in_vscode(filepath)
        
        return jsonify({
            "success": True,
            "message": "Code generated, saved, and opened in VS Code",
            "code": generated_code,
            "filepath": filepath,
            "language": data["language"]
        })
    
    except Exception as e:
        logger.error(f"Create and open error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/code/list", methods=["GET"])
def list_code_files():
    """
    List all generated code files in the workspace
    """
    try:
        workspace_dir = Path(__file__).parent.parent / "generated_code"
        
        if not workspace_dir.exists():
            return jsonify({
                "success": True,
                "files": [],
                "message": "No generated code files yet"
            })
        
        files = []
        for file in workspace_dir.glob("*"):
            if file.is_file():
                files.append({
                    "name": file.name,
                    "path": str(file),
                    "created": datetime.fromtimestamp(file.stat().st_ctime).isoformat()
                })
        
        return jsonify({
            "success": True,
            "files": files,
            "total": len(files)
        })
    
    except Exception as e:
        logger.error(f"List files error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({"success": False, "error": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({"success": False, "error": "Internal server error"}), 500


if __name__ == "__main__":
    logger.info("🚀 Starting Jarvis Brain Backend API...")
    logger.info("📡 Listening on http://localhost:8000")
    app.run(debug=True, host="0.0.0.0", port=8000)
