-- ═══════════════════════════════════════════════════════════════════════════
-- JARVIS DATABASE SCHEMA
-- PostgreSQL database for persistent storage of chat, commands, and analytics
-- ═══════════════════════════════════════════════════════════════════════════

-- ═══════════════════════════════════════════════════════════════════════════
-- USERS TABLE
-- ═══════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    preferences JSONB DEFAULT '{}'::jsonb
);

CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);


-- ═══════════════════════════════════════════════════════════════════════════
-- CHAT MESSAGES TABLE
-- ═══════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS chat_messages (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    message TEXT NOT NULL,
    response TEXT,
    ai_provider VARCHAR(50),  -- 'local', 'openai', 'anthropic', 'cohere'
    ai_model VARCHAR(255),    -- 'mistral', 'gpt-4', 'claude-3-opus'
    tokens_used INTEGER,
    response_time_ms FLOAT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_saved BOOLEAN DEFAULT FALSE,
    tags TEXT[] DEFAULT '{}'::text[]
);

CREATE INDEX idx_chat_user_id ON chat_messages(user_id);
CREATE INDEX idx_chat_timestamp ON chat_messages(timestamp DESC);
CREATE INDEX idx_chat_provider ON chat_messages(ai_provider);
CREATE INDEX idx_chat_tags ON chat_messages USING GIN(tags);


-- ═══════════════════════════════════════════════════════════════════════════
-- COMMAND EXECUTION HISTORY TABLE
-- ═══════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS command_executions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    command VARCHAR(255) NOT NULL,
    arguments JSONB DEFAULT '{}'::jsonb,
    result TEXT,
    status VARCHAR(50),  -- 'success', 'error', 'timeout'
    error_message TEXT,
    execution_time_ms FLOAT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    category VARCHAR(50),  -- 'system', 'file', 'code', 'ai', 'network', 'monitor'
    tags TEXT[] DEFAULT '{}'::text[]
);

CREATE INDEX idx_commands_user_id ON command_executions(user_id);
CREATE INDEX idx_commands_timestamp ON command_executions(timestamp DESC);
CREATE INDEX idx_commands_command ON command_executions(command);
CREATE INDEX idx_commands_status ON command_executions(status);
CREATE INDEX idx_commands_category ON command_executions(category);


-- ═══════════════════════════════════════════════════════════════════════════
-- CODE SNIPPETS TABLE
-- ═══════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS code_snippets (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    code TEXT NOT NULL,
    language VARCHAR(50),  -- 'python', 'javascript', 'typescript', etc.
    tags TEXT[] DEFAULT '{}'::text[],
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_public BOOLEAN DEFAULT FALSE,
    view_count INTEGER DEFAULT 0
);

CREATE INDEX idx_snippets_user_id ON code_snippets(user_id);
CREATE INDEX idx_snippets_language ON code_snippets(language);
CREATE INDEX idx_snippets_tags ON code_snippets USING GIN(tags);
CREATE INDEX idx_snippets_created ON code_snippets(created_at DESC);


-- ═══════════════════════════════════════════════════════════════════════════
-- DAILY ANALYTICS TABLE
-- ═══════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS analytics_daily (
    id SERIAL PRIMARY KEY,
    date DATE UNIQUE NOT NULL,
    total_commands INTEGER DEFAULT 0,
    total_chats INTEGER DEFAULT 0,
    total_users INTEGER DEFAULT 0,
    avg_response_time_ms FLOAT DEFAULT 0,
    avg_command_time_ms FLOAT DEFAULT 0,
    success_rate FLOAT DEFAULT 0,  -- percentage
    top_commands TEXT[] DEFAULT '{}'::text[],
    top_providers TEXT[] DEFAULT '{}'::text[],
    error_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_analytics_date ON analytics_daily(date DESC);


-- ═══════════════════════════════════════════════════════════════════════════
-- ANALYTICS BY PROVIDER TABLE
-- ═══════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS analytics_provider (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    provider VARCHAR(50) NOT NULL,  -- 'local', 'openai', 'anthropic', 'cohere'
    model VARCHAR(255),
    request_count INTEGER DEFAULT 0,
    avg_response_time_ms FLOAT DEFAULT 0,
    total_tokens INTEGER DEFAULT 0,
    error_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(date, provider, model)
);

CREATE INDEX idx_analytics_provider_date ON analytics_provider(date DESC);
CREATE INDEX idx_analytics_provider_name ON analytics_provider(provider);


-- ═══════════════════════════════════════════════════════════════════════════
-- USER SESSIONS TABLE
-- ═══════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS user_sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    session_token VARCHAR(255) UNIQUE NOT NULL,
    ip_address VARCHAR(45),
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

CREATE INDEX idx_sessions_user_id ON user_sessions(user_id);
CREATE INDEX idx_sessions_token ON user_sessions(session_token);
CREATE INDEX idx_sessions_active ON user_sessions(is_active);


-- ═══════════════════════════════════════════════════════════════════════════
-- SAVED SEARCHES TABLE
-- ═══════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS saved_searches (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    query TEXT NOT NULL,
    search_type VARCHAR(50),  -- 'chat', 'command', 'snippet'
    filters JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, name)
);

CREATE INDEX idx_searches_user_id ON saved_searches(user_id);


-- ═══════════════════════════════════════════════════════════════════════════
-- FAVORITES TABLE
-- ═══════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS favorites (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    content_type VARCHAR(50),  -- 'command', 'snippet', 'search'
    content_id VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, content_type, content_id)
);

CREATE INDEX idx_favorites_user_id ON favorites(user_id);
CREATE INDEX idx_favorites_content_type ON favorites(content_type);


-- ═══════════════════════════════════════════════════════════════════════════
-- TRIGGERS FOR UPDATED_AT TIMESTAMPS
-- ═══════════════════════════════════════════════════════════════════════════

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_code_snippets_updated_at BEFORE UPDATE ON code_snippets
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();


-- ═══════════════════════════════════════════════════════════════════════════
-- GRANTS (if using separate user)
-- ═══════════════════════════════════════════════════════════════════════════

-- Grant permissions to jarvis user (create and execute if needed)
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO jarvis;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO jarvis;
