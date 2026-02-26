"""
Jarvis Persistence API
Flask routes for saving and retrieving chat history, command logs, and analytics
"""

from flask import Blueprint, request, jsonify
from datetime import datetime
from sqlalchemy import desc, func
from sqlalchemy.exc import SQLAlchemyError
import logging

from core.database import DatabaseManager, Repository
from core.models import (
    User, ChatMessage, CommandExecution, CodeSnippet,
    AnalyticsDaily, AnalyticsProvider, UserSession, SavedSearch, Favorite
)

logger = logging.getLogger(__name__)

# Create blueprint
persistence_bp = Blueprint('persistence', __name__, url_prefix='/api/persistence')


# ==================== CHAT PERSISTENCE ====================

@persistence_bp.route('/chat/save', methods=['POST'])
def save_chat_message():
    """Save a chat message and response"""
    try:
        data = request.json
        
        # Validate required fields
        if not data.get('user_id') or not data.get('message'):
            return jsonify({'error': 'Missing required fields'}), 400
        
        db = DatabaseManager.get_session()
        
        # Create chat message record
        chat_msg = ChatMessage(
            user_id=data['user_id'],
            message=data['message'],
            response=data.get('response'),
            ai_provider=data.get('ai_provider', 'local'),
            ai_model=data.get('ai_model', 'default')
        )
        
        db.add(chat_msg)
        db.commit()
        
        logger.info(f'✅ Chat message saved (ID: {chat_msg.id})')
        
        return jsonify({
            'success': True,
            'message_id': chat_msg.id,
            'timestamp': chat_msg.timestamp.isoformat()
        }), 201
    
    except SQLAlchemyError as e:
        logger.error(f'Database error: {e}')
        return jsonify({'error': 'Database error'}), 500
    except Exception as e:
        logger.error(f'Error saving chat message: {e}')
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()


@persistence_bp.route('/chat/history/<int:user_id>', methods=['GET'])
def get_chat_history(user_id):
    """Get chat history for a user"""
    try:
        limit = request.args.get('limit', 50, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        db = DatabaseManager.get_session()
        
        # Query chat messages
        messages = db.query(ChatMessage).filter(
            ChatMessage.user_id == user_id
        ).order_by(
            desc(ChatMessage.timestamp)
        ).limit(limit).offset(offset).all()
        
        # Get total count
        total = db.query(func.count(ChatMessage.id)).filter(
            ChatMessage.user_id == user_id
        ).scalar()
        
        # Format response
        chat_data = [{
            'id': msg.id,
            'message': msg.message,
            'response': msg.response,
            'ai_provider': msg.ai_provider,
            'ai_model': msg.ai_model,
            'timestamp': msg.timestamp.isoformat()
        } for msg in reversed(messages)]
        
        return jsonify({
            'success': True,
            'total': total,
            'limit': limit,
            'offset': offset,
            'messages': chat_data
        }), 200
    
    except Exception as e:
        logger.error(f'Error retrieving chat history: {e}')
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()


@persistence_bp.route('/chat/<int:message_id>', methods=['GET'])
def get_chat_message(message_id):
    """Get a specific chat message"""
    try:
        db = DatabaseManager.get_session()
        
        msg = db.query(ChatMessage).filter(
            ChatMessage.id == message_id
        ).first()
        
        if not msg:
            return jsonify({'error': 'Message not found'}), 404
        
        return jsonify({
            'success': True,
            'message': {
                'id': msg.id,
                'user_id': msg.user_id,
                'message': msg.message,
                'response': msg.response,
                'ai_provider': msg.ai_provider,
                'ai_model': msg.ai_model,
                'timestamp': msg.timestamp.isoformat()
            }
        }), 200
    
    except Exception as e:
        logger.error(f'Error retrieving message: {e}')
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()


# ==================== COMMAND EXECUTION LOGGING ====================

@persistence_bp.route('/command/log', methods=['POST'])
def log_command_execution():
    """Log a command execution"""
    try:
        data = request.json
        
        if not data.get('user_id') or not data.get('command'):
            return jsonify({'error': 'Missing required fields'}), 400
        
        db = DatabaseManager.get_session()
        
        cmd_exec = CommandExecution(
            user_id=data['user_id'],
            command=data['command'],
            arguments=data.get('arguments', {}),
            result=data.get('result'),
            status=data.get('status', 'pending'),
            execution_time_ms=data.get('execution_time_ms', 0)
        )
        
        db.add(cmd_exec)
        db.commit()
        
        logger.info(f'✅ Command logged (ID: {cmd_exec.id})')
        
        return jsonify({
            'success': True,
            'execution_id': cmd_exec.id,
            'timestamp': cmd_exec.timestamp.isoformat()
        }), 201
    
    except SQLAlchemyError as e:
        logger.error(f'Database error: {e}')
        return jsonify({'error': 'Database error'}), 500
    except Exception as e:
        logger.error(f'Error logging command: {e}')
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()


@persistence_bp.route('/command/history/<int:user_id>', methods=['GET'])
def get_command_history(user_id):
    """Get command execution history"""
    try:
        limit = request.args.get('limit', 100, type=int)
        offset = request.args.get('offset', 0, type=int)
        status_filter = request.args.get('status')
        
        db = DatabaseManager.get_session()
        
        # Build query
        query = db.query(CommandExecution).filter(
            CommandExecution.user_id == user_id
        )
        
        if status_filter:
            query = query.filter(CommandExecution.status == status_filter)
        
        # Get total count
        total = query.count()
        
        # Get paginated results
        executions = query.order_by(
            desc(CommandExecution.timestamp)
        ).limit(limit).offset(offset).all()
        
        cmd_data = [{
            'id': exe.id,
            'command': exe.command,
            'arguments': exe.arguments,
            'result': exe.result,
            'status': exe.status,
            'execution_time_ms': exe.execution_time_ms,
            'timestamp': exe.timestamp.isoformat()
        } for exe in reversed(executions)]
        
        return jsonify({
            'success': True,
            'total': total,
            'limit': limit,
            'offset': offset,
            'commands': cmd_data
        }), 200
    
    except Exception as e:
        logger.error(f'Error retrieving command history: {e}')
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()


# ==================== CODE SNIPPETS ====================

@persistence_bp.route('/snippet/save', methods=['POST'])
def save_code_snippet():
    """Save a code snippet"""
    try:
        data = request.json
        
        if not data.get('user_id') or not data.get('code'):
            return jsonify({'error': 'Missing required fields'}), 400
        
        db = DatabaseManager.get_session()
        
        snippet = CodeSnippet(
            user_id=data['user_id'],
            title=data.get('title', 'Untitled'),
            description=data.get('description'),
            code=data['code'],
            language=data.get('language', 'python'),
            tags=data.get('tags', [])
        )
        
        db.add(snippet)
        db.commit()
        
        logger.info(f'✅ Code snippet saved (ID: {snippet.id})')
        
        return jsonify({
            'success': True,
            'snippet_id': snippet.id,
            'timestamp': snippet.timestamp.isoformat()
        }), 201
    
    except Exception as e:
        logger.error(f'Error saving snippet: {e}')
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()


@persistence_bp.route('/snippet/<int:user_id>', methods=['GET'])
def get_snippets(user_id):
    """Get all code snippets for a user"""
    try:
        limit = request.args.get('limit', 50, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        db = DatabaseManager.get_session()
        
        snippets = db.query(CodeSnippet).filter(
            CodeSnippet.user_id == user_id
        ).order_by(
            desc(CodeSnippet.timestamp)
        ).limit(limit).offset(offset).all()
        
        total = db.query(func.count(CodeSnippet.id)).filter(
            CodeSnippet.user_id == user_id
        ).scalar()
        
        snippet_data = [{
            'id': snip.id,
            'title': snip.title,
            'description': snip.description,
            'code': snip.code,
            'language': snip.language,
            'tags': snip.tags,
            'timestamp': snip.timestamp.isoformat()
        } for snip in reversed(snippets)]
        
        return jsonify({
            'success': True,
            'total': total,
            'snippets': snippet_data
        }), 200
    
    except Exception as e:
        logger.error(f'Error retrieving snippets: {e}')
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()


# ==================== ANALYTICS ====================

@persistence_bp.route('/analytics/daily/<int:user_id>', methods=['GET'])
def get_daily_analytics(user_id):
    """Get daily analytics for a user"""
    try:
        db = DatabaseManager.get_session()
        
        analytics = db.query(AnalyticsDaily).filter(
            AnalyticsDaily.user_id == user_id
        ).order_by(
            desc(AnalyticsDaily.date)
        ).limit(30).all()
        
        data = [{
            'date': ana.date.isoformat() if hasattr(ana.date, 'isoformat') else str(ana.date),
            'messages_count': ana.messages_count,
            'commands_count': ana.commands_count,
            'code_snippets_count': ana.code_snippets_count,
            'avg_response_time_ms': ana.avg_response_time_ms
        } for ana in reversed(analytics)]
        
        return jsonify({
            'success': True,
            'analytics': data
        }), 200
    
    except Exception as e:
        logger.error(f'Error retrieving analytics: {e}')
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()


@persistence_bp.route('/analytics/provider/<int:user_id>', methods=['GET'])
def get_provider_analytics(user_id):
    """Get analytics by AI provider"""
    try:
        db = DatabaseManager.get_session()
        
        analytics = db.query(AnalyticsProvider).filter(
            AnalyticsProvider.user_id == user_id
        ).order_by(
            desc(AnalyticsProvider.total_requests)
        ).all()
        
        data = [{
            'provider': ana.provider,
            'model': ana.model,
            'total_requests': ana.total_requests,
            'total_tokens_used': ana.total_tokens_used,
            'avg_response_time_ms': ana.avg_response_time_ms
        } for ana in analytics]
        
        return jsonify({
            'success': True,
            'analytics': data
        }), 200
    
    except Exception as e:
        logger.error(f'Error retrieving provider analytics: {e}')
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()


# ==================== HEALTH CHECK ====================

@persistence_bp.route('/health', methods=['GET'])
def health_check():
    """Check database health"""
    try:
        db = DatabaseManager.get_session()
        db.execute('SELECT 1')
        db.close()
        
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    except Exception as e:
        logger.error(f'Health check failed: {e}')
        return jsonify({
            'status': 'unhealthy',
            'database': 'disconnected',
            'error': str(e)
        }), 503
