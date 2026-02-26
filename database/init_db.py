#!/usr/bin/env python3
"""
Jarvis Database Initialization Script
Sets up PostgreSQL database, runs schema, and initializes models
"""

import os
import sys
import logging
import subprocess
from pathlib import Path
from sqlalchemy import text, inspect

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DatabaseInitializer:
    """Handle database initialization"""
    
    def __init__(self):
        self.db_name = 'jarvis'
        self.db_user = 'postgres'
        self.db_password = 'jarvis123'
        self.db_host = 'localhost'
        self.db_port = 5432
        self.db_url = f'postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}'
    
    def check_postgresql(self) -> bool:
        """Check if PostgreSQL is installed"""
        try:
            result = subprocess.run(['psql', '--version'], capture_output=True, text=True)
            logger.info(f'✅ PostgreSQL found: {result.stdout.strip()}')
            return True
        except FileNotFoundError:
            logger.error('❌ PostgreSQL not found. Please install PostgreSQL.')
            return False
    
    def check_postgresql_running(self) -> bool:
        """Check if PostgreSQL service is running"""
        try:
            # Try to connect to default postgres database
            cmd = [
                'psql',
                '-h', self.db_host,
                '-U', self.db_user,
                '-d', 'postgres',
                '-c', 'SELECT 1'
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
            
            if result.returncode == 0:
                logger.info('✅ PostgreSQL service is running')
                return True
            else:
                logger.error('❌ PostgreSQL service is not responding')
                return False
        except subprocess.TimeoutExpired:
            logger.error('❌ PostgreSQL connection timeout')
            return False
        except Exception as e:
            logger.error(f'❌ PostgreSQL check failed: {e}')
            return False
    
    def create_database(self) -> bool:
        """Create database if it doesn't exist"""
        try:
            cmd = [
                'psql',
                '-h', self.db_host,
                '-U', self.db_user,
                '-d', 'postgres',
                '-c', f"SELECT 1 FROM pg_database WHERE datname='{self.db_name}'"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if 'no rows' in result.stdout.lower():
                # Database doesn't exist, create it
                logger.info(f'Creating database: {self.db_name}...')
                
                cmd = [
                    'psql',
                    '-h', self.db_host,
                    '-U', self.db_user,
                    '-d', 'postgres',
                    '-c', f'CREATE DATABASE {self.db_name} WITH ENCODING "UTF8" LC_COLLATE "C" LC_CTYPE "C"'
                ]
                
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode == 0:
                    logger.info(f'✅ Database created: {self.db_name}')
                    return True
                else:
                    logger.error(f'❌ Failed to create database: {result.stderr}')
                    return False
            else:
                logger.info(f'✅ Database already exists: {self.db_name}')
                return True
        
        except Exception as e:
            logger.error(f'❌ Database creation failed: {e}')
            return False
    
    def run_schema(self) -> bool:
        """Execute SQL schema file"""
        try:
            schema_file = Path(__file__).parent.parent / 'database' / 'schema.sql'
            
            if not schema_file.exists():
                logger.error(f'❌ Schema file not found: {schema_file}')
                return False
            
            logger.info(f'Running schema from: {schema_file}...')
            
            cmd = [
                'psql',
                '-h', self.db_host,
                '-U', self.db_user,
                '-d', self.db_name,
                '-f', str(schema_file)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info('✅ SQL schema executed successfully')
                return True
            else:
                logger.error(f'❌ Schema execution failed: {result.stderr}')
                return False
        
        except Exception as e:
            logger.error(f'❌ Schema execution failed: {e}')
            return False
    
    def initialize_orm_models(self) -> bool:
        """Initialize SQLAlchemy ORM models"""
        try:
            logger.info('Initializing ORM models...')
            
            # Set environment variable for database URL
            os.environ['DATABASE_URL'] = self.db_url
            
            # Import and initialize database
            from core.database import DatabaseManager
            from core.models import Base
            
            DatabaseManager.initialize()
            
            # Verify all tables exist
            engine = DatabaseManager.get_engine()
            inspector = inspect(engine)
            tables = inspector.get_table_names()
            
            expected_tables = [
                'users', 'chat_messages', 'command_executions',
                'code_snippets', 'analytics_daily', 'analytics_provider',
                'user_sessions', 'saved_searches', 'favorites'
            ]
            
            missing_tables = set(expected_tables) - set(tables)
            
            if missing_tables:
                logger.warning(f'⚠️  Missing tables: {missing_tables}')
                logger.info('Creating missing tables...')
                Base.metadata.create_all(bind=engine)
            
            logger.info(f'✅ ORM initialized. Tables: {len(tables)}')
            return True
        
        except Exception as e:
            logger.error(f'❌ ORM initialization failed: {e}')
            return False
    
    def run(self) -> bool:
        """Run full initialization"""
        logger.info('=' * 60)
        logger.info('JARVIS DATABASE INITIALIZATION')
        logger.info('=' * 60)
        
        # Check PostgreSQL installation
        if not self.check_postgresql():
            logger.error('PostgreSQL is required. Please install it:')
            logger.error('  macOS: brew install postgresql')
            logger.error('  Linux (Ubuntu): sudo apt install postgresql')
            logger.error('  Linux (Fedora): sudo dnf install postgresql')
            return False
        
        # Check PostgreSQL service
        if not self.check_postgresql_running():
            logger.error('PostgreSQL service is not running. Please start it:')
            logger.error('  macOS: brew services start postgresql')
            logger.error('  Linux (systemd): sudo systemctl start postgresql')
            return False
        
        # Create database
        if not self.create_database():
            return False
        
        # Run schema
        if not self.run_schema():
            return False
        
        # Initialize ORM
        if not self.initialize_orm_models():
            return False
        
        logger.info('=' * 60)
        logger.info('✅ DATABASE INITIALIZATION COMPLETE')
        logger.info('=' * 60)
        logger.info(f'Database: {self.db_name}')
        logger.info(f'Host: {self.db_host}:{self.db_port}')
        logger.info(f'User: {self.db_user}')
        logger.info('')
        logger.info('Connection string for .env:')
        logger.info(f'DATABASE_URL={self.db_url}')
        logger.info('')
        logger.info('Next steps:')
        logger.info('1. Add DATABASE_URL to .env or environment')
        logger.info('2. Restart backend: python3 backend/app.py')
        logger.info('3. Access dashboard at http://localhost:3000')
        
        return True


def main():
    """Main entry point"""
    initializer = DatabaseInitializer()
    success = initializer.run()
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
