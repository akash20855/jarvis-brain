import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { FiSend, FiSettings, FiBarChart2, FiHelpCircle } from 'react-icons/fi';
import './App.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

function App() {
  const [activeTab, setActiveTab] = useState('chat');
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [suggestions, setSuggestions] = useState([]);
  const [history, setHistory] = useState([]);
  const [config, setConfig] = useState(null);
  const [aiStatus, setAiStatus] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchAiStatus();
    fetchHistory();
    fetchConfig();
    
    // Add welcome message
    setMessages([
      {
        type: 'bot',
        content: '👋 Welcome to Jarvis Brain! Ask me anything about code improvements.'
      }
    ]);
  }, []);

  const fetchAiStatus = async () => {
    try {
      const response = await axios.get(`${API_URL}/ai/status`);
      setAiStatus(response.data);
    } catch (error) {
      console.error('Error fetching AI status:', error);
    }
  };

  const fetchHistory = async () => {
    try {
      const response = await axios.get(`${API_URL}/history/improvements?limit=10`);
      setHistory(response.data.improvements || []);
    } catch (error) {
      console.error('Error fetching history:', error);
    }
  };

  const fetchConfig = async () => {
    try {
      const response = await axios.get(`${API_URL}/config/get`);
      setConfig(response.data.config);
    } catch (error) {
      console.error('Error fetching config:', error);
    }
  };

  const handleSendMessage = async () => {
    if (!inputMessage.trim()) return;

    const userMessage = {
      type: 'user',
      content: inputMessage
    };

    setMessages([...messages, userMessage]);
    setInputMessage('');
    setLoading(true);

    try {
      if (inputMessage.toLowerCase() === 'analyze') {
        await handleAnalyze();
      } else if (inputMessage.toLowerCase().startsWith('file ')) {
        const filepath = inputMessage.substring(5);
        await handleFileAnalysis(filepath);
      } else if (inputMessage.toLowerCase() === 'suggestions') {
        await handleGetSuggestions();
      } else {
        const response = await axios.post(`${API_URL}/chat/message`, {
          message: inputMessage
        });
        
        // Handle code generation responses
        if (response.data.type === 'code_generation') {
          const codeMessage = {
            type: 'bot',
            content: `✅ Code generated and saved!
            
Language: ${response.data.language}
File: ${response.data.filename}
Location: ${response.data.filepath}

Generated Code:
\`\`\`${response.data.language}
${response.data.code}
\`\`\`

The code has been opened in VS Code. You can now test it!`
          };
          setMessages(prev => [...prev, codeMessage]);
        } else {
          const botMessage = {
            type: 'bot',
            content: response.data.message
          };
          setMessages(prev => [...prev, botMessage]);
        }
      }
    } catch (error) {
      const errorMessage = {
        type: 'bot',
        content: `❌ Error: ${error.response?.data?.error || error.message}`
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleAnalyze = async () => {
    try {
      const response = await axios.post(`${API_URL}/evolve/analyze`, {
        ai_backend: 'patterns'
      });
      const botMessage = {
        type: 'bot',
        content: `✨ Analysis Complete!\n\nFiles Scanned: ${response.data.data.scanned_files}\nImprovements Found: ${response.data.data.improvements_found}`
      };
      setMessages(prev => [...prev, botMessage]);
      setSuggestions(response.data.data.files || {});
    } catch (error) {
      throw error;
    }
  };

  const handleFileAnalysis = async (filepath) => {
    try {
      const response = await axios.post(`${API_URL}/evolve/file`, {
        filepath
      });
      const botMessage = {
        type: 'bot',
        content: `📄 ${filepath}\n\nFound ${response.data.count} suggestions:\n${response.data.suggestions.map(s => `• ${s.suggestion}`).join('\n')}`
      };
      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      throw error;
    }
  };

  const handleGetSuggestions = async () => {
    try {
      const response = await axios.get(`${API_URL}/evolve/suggestions?limit=5`);
      const suggestions = response.data.suggestions;
      const content = suggestions.length > 0
        ? `💡 Top Suggestions:\n\n${suggestions.map((s, i) => `${i + 1}. ${s.suggestion}\n   File: ${s.file}`).join('\n\n')}`
        : '✅ No suggestions at this time!';
      
      const botMessage = {
        type: 'bot',
        content
      };
      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      throw error;
    }
  };

  return (
    <div className="jarvis-app">
      <nav className="navbar">
        <div className="navbar-brand">
          <h1>🤖 Jarvis Brain</h1>
          <p>AI-Powered Code Evolution</p>
        </div>
        <div className="navbar-tabs">
          <button
            className={`tab ${activeTab === 'chat' ? 'active' : ''}`}
            onClick={() => setActiveTab('chat')}
          >
            💬 Chat
          </button>
          <button
            className={`tab ${activeTab === 'analysis' ? 'active' : ''}`}
            onClick={() => setActiveTab('analysis')}
          >
            <FiBarChart2 /> Analysis
          </button>
          <button
            className={`tab ${activeTab === 'history' ? 'active' : ''}`}
            onClick={() => setActiveTab('history')}
          >
            📊 History
          </button>
          <button
            className={`tab ${activeTab === 'settings' ? 'active' : ''}`}
            onClick={() => setActiveTab('settings')}
          >
            <FiSettings /> Settings
          </button>
        </div>
      </nav>

      <main className="main-content">
        {activeTab === 'chat' && (
          <div className="chat-container">
            <div className="messages">
              {messages.map((msg, idx) => (
                <div key={idx} className={`message message-${msg.type}`}>
                  <p>{msg.content}</p>
                </div>
              ))}
              {loading && <div className="message message-bot">⏳ Thinking...</div>}
            </div>
            <div className="input-area">
              <input
                type="text"
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                placeholder="Ask me about code improvements... (or type 'help')"
                disabled={loading}
              />
              <button onClick={handleSendMessage} disabled={loading}>
                <FiSend /> Send
              </button>
            </div>
            <div className="quick-commands">
              <button onClick={() => { setInputMessage('analyze'); }}>Analyze Project</button>
              <button onClick={() => { setInputMessage('suggestions'); }}>Show Suggestions</button>
              <button onClick={() => { setInputMessage('help'); }}>Show Commands</button>
            </div>
          </div>
        )}

        {activeTab === 'analysis' && (
          <div className="analysis-container">
            <h2>📊 Project Analysis</h2>
            <div className="status-grid">
              <div className="status-card">
                <h3>AI Backends</h3>
                {aiStatus && (
                  <div>
                    <p>
                      Ollama:{' '}
                      <span className={aiStatus.ollama.status === 'running' ? 'status-running' : 'status-offline'}>
                        {aiStatus.ollama.status === 'running' ? '✅' : '⏸️'}
                      </span>
                    </p>
                    <p>Local Patterns: ✅</p>
                  </div>
                )}
              </div>
              <div className="status-card">
                <h3>Quick Actions</h3>
                <button
                  onClick={async () => {
                    setLoading(true);
                    try {
                      await handleAnalyze();
                    } catch (e) {
                      console.error(e);
                    }
                    setLoading(false);
                  }}
                  disabled={loading}
                >
                  🔍 Scan Project
                </button>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'history' && (
          <div className="history-container">
            <h2>📈 Improvement History</h2>
            {history.length > 0 ? (
              <div className="history-list">
                {history.map((item, idx) => (
                  <div key={idx} className="history-item">
                    <h4>{item.timestamp}</h4>
                    <p>Scanned: {item.scanned_files} files</p>
                    <p>Improvements: {item.improvements}</p>
                  </div>
                ))}
              </div>
            ) : (
              <p>No history yet. Run an analysis to get started!</p>
            )}
          </div>
        )}

        {activeTab === 'settings' && (
          <div className="settings-container">
            <h2><FiSettings /> Configuration</h2>
            {config && (
              <div className="config-display">
                <pre>{JSON.stringify(config, null, 2)}</pre>
              </div>
            )}
          </div>
        )}
      </main>

      <footer className="footer">
        <p>🚀 Jarvis Brain - AI-Powered Code Evolution | Version 1.0.0</p>
      </footer>
    </div>
  );
}

export default App;
