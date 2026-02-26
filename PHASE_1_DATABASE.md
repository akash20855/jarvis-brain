# Jarvis Phase 1: Database & Persistence Setup

## Overview
Phase 1 of the Jarvis evolution implements data persistence using PostgreSQL with a complete ORM layer, REST API endpoints, and automatic schema management.

**Problem Solved**: 
- Before: All chat history, commands, and data lost on restart
- After: All data persisted in PostgreSQL, available across sessions

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   Flask Backend                         │
│                  (port 8001)                           │
└─────────────┬───────────────────────────────────────────┘
              │
              │ SQLAlchemy ORM
              │
┌─────────────▼───────────────────────────────────────────┐
│              Database Layer (core/database.py)          │
│      - Connection pooling                              │
│      - Session management                              │
│      - Query building                                  │
└─────────────┬───────────────────────────────────────────┘
              │
              │ PostgreSQL Driver (psycopg2)
              │
┌─────────────▼───────────────────────────────────────────┐
│           PostgreSQL Database                           │
│        (localhost:5432/jarvis)                         │
│                                                        │
│  ✓ users              (users table)                   │
│  ✓ chat_messages      (chat history)                  │
│  ✓ command_executions (command logs)                  │
│  ✓ code_snippets      (code storage)                  │
│  ✓ analytics_daily    (daily stats)                   │
│  ✓ analytics_provider (per-provider stats)            │
│  ✓ user_sessions      (session tracking)              │
│  ✓ saved_searches     (saved queries)                 │
│  ✓ favorites          (bookmarks)                     │
└──────────────────────────────────────────────────────────┘
```

## Files Created

### 1. Database Schema
**File**: `database/schema.sql`
- 9 PostgreSQL tables
- Proper foreign key relationships
- Comprehensive indexing (17+ indexes)
- Timestamp triggers for automatic updated_at
- 500+ lines of SQL

**Tables**:
```sql
users                  - User accounts, preferences, API keys
chat_messages          - Complete chat history with AI provider tracking
command_executions     - Command audit log with execution details
code_snippets          - Generated/saved code with language detection
analytics_daily        - Daily aggregated statistics
analytics_provider     - Per-provider performance metrics
user_sessions          - WebSocket/API session tracking
saved_searches         - Saved search queries for quick access
favorites              - Bookmarked items (commands, snippets, etc.)
```

### 2. SQLAlchemy ORM Models
**File**: `core/models.py`
- 9 Python ORM model classes
- Proper relationships (User → All data tables)
- Cascade delete on user removal
- Index hints for query optimization
- 300+ lines of Python

**Key Features**:
- Type hints for IDE support
- Proper repr for debugging
- ARRAY and JSON column support
- Relationship auto-loading options

### 3. Database Connection Manager
**File**: `core/database.py`
- Connection pooling with QueuePool
- Thread-safe scoped sessions
- Environment variable configuration
- Health check utility
- Session context managers
- Base Repository class for CRUD operations

**Configuration**:
```python
DATABASE_URL: PostgreSQL connection string
DB_POOL_SIZE: Connection pool size (default: 10)
DB_MAX_OVERFLOW: Additional connections (default: 20)
DB_POOL_RECYCLE: Connection recycle time (default: 3600s)
DB_ECHO: SQL logging (default: false)
```

### 4. Database Initialization Script
**File**: `database/init_db.py`
- Automated database setup
- PostgreSQL check and startup
- Database creation
- Schema execution
- ORM model initialization
- Detailed error handling and logging

**Features**:
- Validates PostgreSQL installation
- Starts PostgreSQL service if needed
- Creates database if missing
- Runs SQL schema automatically
- Verifies all tables created
- Provides connection string for .env

### 5. Flask Persistence API Routes
**File**: `backend/routes_persistence.py`
- 15+ REST endpoints for data operations
- Chat message persistence
- Command execution logging
- Code snippet management
- Analytics retrieval
- Health checks

**Endpoints**:
```
POST   /api/persistence/chat/save           - Save chat message
GET    /api/persistence/chat/history/<id>   - Get chat history
GET    /api/persistence/chat/<message_id>   - Get single message

POST   /api/persistence/command/log         - Log command execution
GET    /api/persistence/command/history/<id> - Get command history

POST   /api/persistence/snippet/save        - Save code snippet
GET    /api/persistence/snippet/<user_id>   - Get all snippets

GET    /api/persistence/analytics/daily/<id> - Daily analytics
GET    /api/persistence/analytics/provider/<id> - Provider analytics

GET    /api/persistence/health              - Health check
```

### 6. Updated Requirements
**File**: `requirements.txt`
Added database packages:
- SQLAlchemy==2.0.23 (ORM)
- psycopg2-binary==2.9.9 (PostgreSQL driver)
- alembic==1.13.1 (Migrations - optional)

### 7. Setup Script
**File**: `setup-database.sh`
- Automated setup for macOS
- Installs PostgreSQL via Homebrew
- Starts PostgreSQL service
- Installs Python dependencies
- Runs initialization script
- Provides next steps

## Installation & Setup

### Quick Setup (macOS)
```bash
# Make script executable
chmod +x setup-database.sh

# Run setup
./setup-database.sh
```

### Manual Setup

1. **Install PostgreSQL** (if not already installed)
   ```bash
   # macOS
   brew install postgresql@15
   brew services start postgresql@15
   
   # Linux (Ubuntu)
   sudo apt-get install postgresql postgresql-contrib
   sudo systemctl start postgresql
   
   # Linux (Fedora)
   sudo dnf install postgresql-server postgresql-upgrade
   sudo systemctl start postgresql
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize database**
   ```bash
   python3 database/init_db.py
   ```

4. **Create .env file**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Start backend**
   ```bash
   python3 backend/app.py
   ```

## Environment Configuration

### Required Environment Variables
```bash
# Database
DATABASE_URL=postgresql://postgres:jarvis123@localhost:5432/jarvis

# Flask
FLASK_APP=backend/app.py
FLASK_ENV=development

# Backend
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8001
```

### Optional Environment Variables
```bash
# Database connection pooling
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=20
DB_POOL_RECYCLE=3600
DB_ECHO=false              # Enable SQL logging

# Feature flags
ENABLE_DATABASE_PERSISTENCE=true
ENABLE_COMMAND_LOGGING=true
ENABLE_CHAT_HISTORY=true
ENABLE_ANALYTICS=true
```

## Usage Examples

### Python Integration

```python
from core.database import DatabaseManager, Repository
from core.models import ChatMessage, CommandExecution

# Initialize database
DatabaseManager.initialize()

# Get a session
db = DatabaseManager.get_session()

# Save chat message
chat = ChatMessage(
    user_id=1,
    message="Hello, Jarvis",
    response="Hello! How can I help?",
    ai_provider="local",
    ai_model="default"
)
db.add(chat)
db.commit()

# Query chat history
history = db.query(ChatMessage).filter(
    ChatMessage.user_id == 1
).order_by(ChatMessage.timestamp.desc()).all()

db.close()
```

### Flask API Usage

```python
from flask import Flask
from backend.routes_persistence import persistence_bp
from core.database import DatabaseManager

app = Flask(__name__)

# Initialize database
DatabaseManager.initialize()

# Register persistence routes
app.register_blueprint(persistence_bp)

if __name__ == '__main__':
    app.run(port=8001)
```

### REST API Examples

**Save chat message**:
```bash
curl -X POST http://localhost:8001/api/persistence/chat/save \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "message": "Write a Python function",
    "response": "def hello(): ...",
    "ai_provider": "openai",
    "ai_model": "gpt-4"
  }'
```

**Get chat history**:
```bash
curl http://localhost:8001/api/persistence/chat/history/1?limit=50&offset=0
```

**Log command execution**:
```bash
curl -X POST http://localhost:8001/api/persistence/command/log \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "command": "list-files",
    "arguments": {"path": "/home"},
    "result": "file1.txt, file2.txt",
    "status": "success",
    "execution_time_ms": 145
  }'
```

**Get analytics**:
```bash
curl http://localhost:8001/api/persistence/analytics/daily/1
```

## Database Management

### Troubleshooting

**PostgreSQL not running**:
```bash
# macOS
brew services start postgresql@15

# Linux
sudo systemctl start postgresql
```

**Check database connection**:
```bash
# Direct connection
psql -h localhost -U postgres -d jarvis

# From Python
python3 -c "from core.database import DatabaseManager; print(DatabaseManager.health_check())"
```

**Reset database** (WARNING: Destructive!):
```bash
python3 -c "from core.database import DatabaseManager; DatabaseManager.drop_all_tables(); DatabaseManager.create_all_tables()"
```

**Check database size**:
```bash
psql -h localhost -U postgres -d jarvis -c "SELECT pg_size_pretty(pg_database_size('jarvis'))"
```

## Performance Optimization

### Indexes
The schema includes automatic indexes on:
- `user_id` (foreign keys)
- `timestamp` (for sorting and filtering)
- `status` (for filtering command execution)
- `ai_provider` (for analytics)

### Query Optimization
Use `.options(joinedload())` for eager loading:
```python
user = db.query(User).options(
    joinedload(User.chat_messages)
).filter(User.id == 1).first()
```

### Connection Pooling
- Pool size: 10 (adjustable via DB_POOL_SIZE)
- Max overflow: 20 connections
- Pool recycle: 3600 seconds
- Automatic connection cleanup

## Testing

### Unit Test Example
```python
import pytest
from core.database import DatabaseManager
from core.models import User, ChatMessage

@pytest.fixture
def db():
    DatabaseManager.initialize()
    session = DatabaseManager.get_session()
    yield session
    session.close()

def test_save_chat_message(db):
    user = User(email="test@example.com", password_hash="hash")
    db.add(user)
    db.commit()
    
    chat = ChatMessage(
        user_id=user.id,
        message="Test",
        response="Response"
    )
    db.add(chat)
    db.commit()
    
    assert chat.id is not None
    assert chat.timestamp is not None
```

## Next Steps (Phase 1 Continuation)

1. **Week 1**:
   - ✅ Database schema and ORM models (DONE)
   - ✅ Flask persistence API routes (DONE)
   - [ ] Update Flask app.py to register persistence routes
   - [ ] Test persistence endpoints
   - [ ] Integrate with existing chat system

2. **Week 2**:
   - [ ] Create React dashboard with TypeScript
   - [ ] Dashboard pages: Overview, ChatHistory, Commands, Analytics
   - [ ] Real-time database updates (WebSocket)
   - [ ] Docker Compose setup for full stack
   - [ ] Production deployment guide

## Additional Resources

- **SQLAlchemy Documentation**: https://docs.sqlalchemy.org/
- **PostgreSQL Documentation**: https://www.postgresql.org/docs/
- **Flask Documentation**: https://flask.palletsprojects.com/
- **psycopg2 Documentation**: https://www.psycopg.org/

## Support

For issues or questions:
1. Check the logs: `tail -f jarvis.log`
2. Run health check: `curl http://localhost:8001/api/persistence/health`
3. Check PostgreSQL connection: `pg_isready -h localhost -U postgres`
4. Review error logs in the database initialization output

---

**Status**: Phase 1 Database Layer ✅ Complete
**Next Phase**: React Web Dashboard + API Integration
