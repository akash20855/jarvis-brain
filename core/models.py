"""
Jarvis Database Models
SQLAlchemy ORM models for persistent storage
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Float, JSONB, ForeignKey, Index, func
from sqlalchemy.dialects.postgresql import ARRAY, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class User(Base):
    """User account model"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    preferences = Column(JSON, default={})
    
    # Relationships
    chat_messages = relationship('ChatMessage', back_populates='user', cascade='all, delete-orphan')
    command_executions = relationship('CommandExecution', back_populates='user', cascade='all, delete-orphan')
    code_snippets = relationship('CodeSnippet', back_populates='user', cascade='all, delete-orphan')
    sessions = relationship('UserSession', back_populates='user', cascade='all, delete-orphan')
    saved_searches = relationship('SavedSearch', back_populates='user', cascade='all, delete-orphan')
    favorites = relationship('Favorite', back_populates='user', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.username}>'


class ChatMessage(Base):
    """Chat message history model"""
    __tablename__ = 'chat_messages'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    message = Column(Text, nullable=False)
    response = Column(Text)
    ai_provider = Column(String(50), index=True)  # 'local', 'openai', 'anthropic', 'cohere'
    ai_model = Column(String(255))  # 'mistral', 'gpt-4', 'claude-3-opus'
    tokens_used = Column(Integer)
    response_time_ms = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    is_saved = Column(Boolean, default=False)
    tags = Column(ARRAY(String), default=[])
    
    # Relationships
    user = relationship('User', back_populates='chat_messages')
    
    __table_args__ = (
        Index('idx_chat_timestamp', 'timestamp'),
        Index('idx_chat_provider', 'ai_provider'),
    )
    
    def __repr__(self):
        return f'<ChatMessage {self.id} by {self.user_id}>'


class CommandExecution(Base):
    """Command execution history model"""
    __tablename__ = 'command_executions'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    command = Column(String(255), nullable=False, index=True)
    arguments = Column(JSON, default={})
    result = Column(Text)
    status = Column(String(50), index=True)  # 'success', 'error', 'timeout'
    error_message = Column(Text)
    execution_time_ms = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    category = Column(String(50), index=True)  # 'system', 'file', 'code', 'ai', 'network', 'monitor'
    tags = Column(ARRAY(String), default=[])
    
    # Relationships
    user = relationship('User', back_populates='command_executions')
    
    __table_args__ = (
        Index('idx_commands_timestamp', 'timestamp'),
        Index('idx_commands_status', 'status'),
        Index('idx_commands_category', 'category'),
    )
    
    def __repr__(self):
        return f'<CommandExecution {self.command} - {self.status}>'


class CodeSnippet(Base):
    """Code snippet storage model"""
    __tablename__ = 'code_snippets'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    code = Column(Text, nullable=False)
    language = Column(String(50), index=True)  # 'python', 'javascript', 'typescript', etc.
    tags = Column(ARRAY(String), default=[])
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_public = Column(Boolean, default=False)
    view_count = Column(Integer, default=0)
    
    # Relationships
    user = relationship('User', back_populates='code_snippets')
    
    __table_args__ = (
        Index('idx_snippets_created', 'created_at'),
        Index('idx_snippets_language', 'language'),
    )
    
    def __repr__(self):
        return f'<CodeSnippet {self.title}>'


class AnalyticsDaily(Base):
    """Daily analytics aggregation model"""
    __tablename__ = 'analytics_daily'
    
    id = Column(Integer, primary_key=True)
    date = Column(String(10), unique=True, nullable=False, index=True)  # YYYY-MM-DD
    total_commands = Column(Integer, default=0)
    total_chats = Column(Integer, default=0)
    total_users = Column(Integer, default=0)
    avg_response_time_ms = Column(Float, default=0)
    avg_command_time_ms = Column(Float, default=0)
    success_rate = Column(Float, default=0)  # percentage
    top_commands = Column(ARRAY(String), default=[])
    top_providers = Column(ARRAY(String), default=[])
    error_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<AnalyticsDaily {self.date}>'


class AnalyticsProvider(Base):
    """Provider-specific analytics model"""
    __tablename__ = 'analytics_provider'
    
    id = Column(Integer, primary_key=True)
    date = Column(String(10), nullable=False, index=True)  # YYYY-MM-DD
    provider = Column(String(50), nullable=False, index=True)  # 'local', 'openai', 'anthropic', 'cohere'
    model = Column(String(255))
    request_count = Column(Integer, default=0)
    avg_response_time_ms = Column(Float, default=0)
    total_tokens = Column(Integer, default=0)
    error_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        Index('idx_analytics_provider_date', 'date'),
        Index('idx_analytics_provider_name', 'provider'),
    )
    
    def __repr__(self):
        return f'<AnalyticsProvider {self.date} - {self.provider}>'


class UserSession(Base):
    """User session tracking model"""
    __tablename__ = 'user_sessions'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    session_token = Column(String(255), unique=True, nullable=False, index=True)
    ip_address = Column(String(45))
    user_agent = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_activity = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)
    is_active = Column(Boolean, default=True, index=True)
    
    # Relationships
    user = relationship('User', back_populates='sessions')
    
    def __repr__(self):
        return f'<UserSession {self.session_token[:10]}...>'


class SavedSearch(Base):
    """Saved search queries model"""
    __tablename__ = 'saved_searches'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    query = Column(Text, nullable=False)
    search_type = Column(String(50))  # 'chat', 'command', 'snippet'
    filters = Column(JSON, default={})
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship('User', back_populates='saved_searches')
    
    def __repr__(self):
        return f'<SavedSearch {self.name}>'


class Favorite(Base):
    """Favorite items model"""
    __tablename__ = 'favorites'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    content_type = Column(String(50))  # 'command', 'snippet', 'search'
    content_id = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship('User', back_populates='favorites')
    
    def __repr__(self):
        return f'<Favorite {self.content_type}:{self.content_id}>'


# Export all models
__all__ = [
    'Base',
    'User',
    'ChatMessage',
    'CommandExecution',
    'CodeSnippet',
    'AnalyticsDaily',
    'AnalyticsProvider',
    'UserSession',
    'SavedSearch',
    'Favorite',
]
