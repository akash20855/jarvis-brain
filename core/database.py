"""
Jarvis Database Connection & Session Management
Handles database connection, session creation, and migrations
"""

import os
from sqlalchemy import create_engine, event, pool
from sqlalchemy.orm import sessionmaker, Session, scoped_session
from sqlalchemy.pool import QueuePool
import logging

logger = logging.getLogger(__name__)


class DatabaseConfig:
    """Database configuration management"""
    
    def __init__(self):
        # Get database URL from environment or use default
        self.database_url = os.getenv(
            'DATABASE_URL',
            'postgresql://postgres:jarvis123@localhost:5432/jarvis'
        )
        
        # Connection pool settings
        self.pool_size = int(os.getenv('DB_POOL_SIZE', 10))
        self.max_overflow = int(os.getenv('DB_MAX_OVERFLOW', 20))
        self.pool_recycle = int(os.getenv('DB_POOL_RECYCLE', 3600))
        
        # Logging
        self.echo = os.getenv('DB_ECHO', 'false').lower() == 'true'


class DatabaseManager:
    """Database connection and session management"""
    
    _engine = None
    _SessionLocal = None
    _scoped_session = None
    
    @classmethod
    def initialize(cls):
        """Initialize database connection"""
        config = DatabaseConfig()
        
        try:
            # Create engine with connection pooling
            cls._engine = create_engine(
                config.database_url,
                poolclass=QueuePool,
                pool_size=config.pool_size,
                max_overflow=config.max_overflow,
                pool_recycle=config.pool_recycle,
                echo=config.echo,
                connect_args={
                    'connect_timeout': 10,
                    'options': '-c statement_timeout=30000'
                }
            )
            
            # Test connection
            with cls._engine.connect() as conn:
                conn.execute('SELECT 1')
            
            logger.info('✅ Database connection established')
            
            # Create session factory
            cls._SessionLocal = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=cls._engine,
                expire_on_commit=False
            )
            
            # Create scoped session for thread safety
            cls._scoped_session = scoped_session(cls._SessionLocal)
            
            # Setup event listeners
            cls._setup_event_listeners()
            
            logger.info('✅ Database session factory created')
            
        except Exception as e:
            logger.error(f'❌ Database initialization failed: {e}')
            raise
    
    @classmethod
    def _setup_event_listeners(cls):
        """Setup SQLAlchemy event listeners"""
        if cls._engine is None:
            return
        
        @event.listens_for(cls._engine, 'connect')
        def receive_connect(dbapi_conn, connection_record):
            """Setup connection options"""
            # Enable UUID support if needed
            # dbapi_conn.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
            pass
        
        @event.listens_for(pool.Pool, 'connect')
        def receive_pool_connect(dbapi_conn, connection_record):
            """Configure pool connection"""
            pass
    
    @classmethod
    def get_session(cls) -> Session:
        """Get a database session"""
        if cls._SessionLocal is None:
            cls.initialize()
        return cls._SessionLocal()
    
    @classmethod
    def get_scoped_session(cls):
        """Get thread-local scoped session"""
        if cls._scoped_session is None:
            cls.initialize()
        return cls._scoped_session
    
    @classmethod
    def get_engine(cls):
        """Get database engine"""
        if cls._engine is None:
            cls.initialize()
        return cls._engine
    
    @classmethod
    def create_all_tables(cls):
        """Create all database tables"""
        if cls._engine is None:
            cls.initialize()
        
        try:
            from core.models import Base
            Base.metadata.create_all(bind=cls._engine)
            logger.info('✅ All database tables created')
        except Exception as e:
            logger.error(f'❌ Failed to create tables: {e}')
            raise
    
    @classmethod
    def drop_all_tables(cls):
        """Drop all database tables (WARNING: destructive)"""
        if cls._engine is None:
            cls.initialize()
        
        try:
            from core.models import Base
            Base.metadata.drop_all(bind=cls._engine)
            logger.info('⚠️  All database tables dropped')
        except Exception as e:
            logger.error(f'❌ Failed to drop tables: {e}')
            raise
    
    @classmethod
    def close_session(cls):
        """Close scoped session"""
        if cls._scoped_session is not None:
            cls._scoped_session.remove()
    
    @classmethod
    def health_check(cls) -> bool:
        """Check database health"""
        try:
            session = cls.get_session()
            session.execute('SELECT 1')
            session.close()
            return True
        except Exception as e:
            logger.error(f'Database health check failed: {e}')
            return False


# Session dependency for FastAPI/Flask
def get_db() -> Session:
    """Get database session (for use with dependency injection)"""
    db = DatabaseManager.get_session()
    try:
        yield db
    finally:
        db.close()


# Repository base class for common DB operations
class Repository:
    """Base repository for database operations"""
    
    def __init__(self, session: Session = None):
        self.session = session or DatabaseManager.get_session()
    
    def commit(self):
        """Commit transaction"""
        try:
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            logger.error(f'Commit failed: {e}')
            raise
    
    def rollback(self):
        """Rollback transaction"""
        self.session.rollback()
    
    def close(self):
        """Close session"""
        self.session.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.rollback()
        self.close()


# Initialize database on import
logger.info('Initializing database...')
DatabaseManager.initialize()
