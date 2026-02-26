"""
Jarvis API Blueprint - 10 REST API endpoints for super-chat system
Integrates super_chat.py with Flask backend
"""

from flask import Blueprint, request, jsonify
import asyncio
from core.super_chat import SuperFastChatEngine

# Initialize blueprint
jarvis_bp = Blueprint('jarvis', __name__, url_prefix='/api/jarvis')

# Global chat engine instance
_chat_engine = None


def get_chat_engine():
    """Get or create chat engine instance"""
    global _chat_engine
    if _chat_engine is None:
        _chat_engine = SuperFastChatEngine()
    return _chat_engine


# ==================== CHAT ENDPOINTS ====================

@jarvis_bp.route('/chat', methods=['POST'])
def chat():
    """Ultra-fast chat with command execution (<100ms)"""
    try:
        data = request.get_json()
        user = data.get('user', 'anonymous')
        message = data.get('message', '')
        
        if not message:
            return jsonify({"error": "Message required"}), 400
        
        # Run async function
        chat_engine = get_chat_engine()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        response = loop.run_until_complete(
            chat_engine.process_message(user, message)
        )
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==================== COMMAND ENDPOINTS ====================

@jarvis_bp.route('/command/execute', methods=['POST'])
def execute_command():
    """Execute a single command"""
    try:
        data = request.get_json()
        command = data.get('command', '')
        args = data.get('args', [])
        
        if not command:
            return jsonify({"error": "Command required"}), 400
        
        chat_engine = get_chat_engine()
        result = asyncio.run(chat_engine.executor.execute(command, *args))
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@jarvis_bp.route('/command/batch', methods=['POST'])
def batch_execute():
    """Execute multiple commands in parallel"""
    try:
        data = request.get_json()
        commands = data.get('commands', [])
        
        if not commands:
            return jsonify({"error": "Commands required"}), 400
        
        chat_engine = get_chat_engine()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        results = loop.run_until_complete(
            chat_engine.batch_execute(commands)
        )
        
        return jsonify({"results": results, "count": len(results)})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@jarvis_bp.route('/command/list', methods=['GET'])
def list_commands():
    """List all 100+ available commands"""
    try:
        chat_engine = get_chat_engine()
        commands = chat_engine.list_commands()
        
        # Add quick info
        total = sum(len(cmds) for cmds in commands.values())
        
        return jsonify({
            "success": True,
            "total_commands": total,
            "categories": commands,
            "categories_count": len(commands)
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@jarvis_bp.route('/command/help', methods=['GET'])
def command_help():
    """Get help for commands"""
    try:
        category = request.args.get('category', None)
        chat_engine = get_chat_engine()
        help_text = chat_engine._get_help(category)
        
        return jsonify({
            "success": True,
            "help": help_text,
            "category": category
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@jarvis_bp.route('/command/search', methods=['GET'])
def search_commands():
    """Search commands by keyword"""
    try:
        query = request.args.get('q', '')
        
        if not query or len(query) < 2:
            return jsonify({"error": "Query too short (min 2 chars)"}), 400
        
        chat_engine = get_chat_engine()
        results = chat_engine.search_commands(query)
        
        return jsonify({
            "success": True,
            "query": query,
            "results": results,
            "count": len(results)
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==================== CHAT HISTORY ENDPOINTS ====================

@jarvis_bp.route('/chat/history', methods=['GET'])
def get_history():
    """Get chat message history"""
    try:
        limit = request.args.get('limit', type=int)
        chat_engine = get_chat_engine()
        history = chat_engine.get_history(limit)
        
        return jsonify({
            "success": True,
            "history": history,
            "count": len(history)
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@jarvis_bp.route('/chat/clear', methods=['POST'])
def clear_history():
    """Clear chat history"""
    try:
        chat_engine = get_chat_engine()
        result = chat_engine.clear_history()
        
        return jsonify({
            "success": True,
            "message": "History cleared",
            **result
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==================== STATISTICS & MONITORING ====================

@jarvis_bp.route('/stats', methods=['GET'])
def get_stats():
    """Get chat performance statistics"""
    try:
        chat_engine = get_chat_engine()
        stats = chat_engine.get_stats()
        
        return jsonify({
            "success": True,
            "stats": stats
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@jarvis_bp.route('/status', methods=['GET'])
def get_status():
    """Get system status and health"""
    try:
        import psutil
        import os
        
        chat_engine = get_chat_engine()
        stats = chat_engine.get_stats()
        
        # Get system info
        status = {
            "success": True,
            "system": {
                "cpu_percent": psutil.cpu_percent(interval=0.1),
                "memory_percent": psutil.virtual_memory().percent,
                "disk_percent": psutil.disk_usage('/').percent,
                "processes": len(psutil.pids())
            },
            "application": {
                "uptime": "running",
                "messages_processed": stats["total_messages"],
                "commands_executed": stats["total_commands"],
                "avg_response_time_ms": stats["avg_response_time_ms"],
                "cache_hit_rate": stats["cache_hit_rate"]
            },
            "capabilities": {
                "available_commands": stats["available_commands"],
                "async_enabled": True,
                "caching_enabled": True,
                "websocket_ready": True,
                "batch_execution": True
            }
        }
        
        return jsonify(status)
    
    except Exception as e:
        return jsonify({"error": str(e), "success": False}), 500


@jarvis_bp.route('/quick-reference', methods=['GET'])
def quick_reference():
    """Get quick reference guide"""
    try:
        chat_engine = get_chat_engine()
        commands = chat_engine.list_commands()
        
        reference = {
            "success": True,
            "quick_reference": {
                "system_commands": f"{len(commands.get('system', []))} commands",
                "file_operations": f"{len(commands.get('file', []))} commands",
                "code_analysis": f"{len(commands.get('code', []))} commands",
                "ai_commands": f"{len(commands.get('ai', []))} commands",
                "network_commands": f"{len(commands.get('net', []))} commands",
                "monitoring_commands": f"{len(commands.get('monitor', []))} commands"
            },
            "api_examples": {
                "chat": "POST /api/jarvis/chat {'user': 'john', 'message': 'hello'}",
                "command": "POST /api/jarvis/command/execute {'command': 'system.date'}",
                "batch": "POST /api/jarvis/command/batch {'commands': [['system.date'], ['system.info']]}",
                "search": "GET /api/jarvis/command/search?q=file",
                "history": "GET /api/jarvis/chat/history?limit=50",
                "stats": "GET /api/jarvis/stats"
            },
            "performance": {
                "target_response_time": "<100ms",
                "caching": "LRU with 1000 entries",
                "parallel_execution": "Supports batch commands"
            }
        }
        
        return jsonify(reference)
    
    except Exception as e:
        return jsonify({"error": str(e), "success": False}), 500


# Export blueprint for registration in main app
__all__ = ['jarvis_bp', 'get_chat_engine']
