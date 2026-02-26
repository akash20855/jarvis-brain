import React, { useEffect, useState } from 'react'
import { FiMessageSquare, FiTerminal, FiCode, FiTrendingUp } from 'react-icons/fi'
import { useDashboardStore } from '@/store/dashboardStore'
import ChatInterface from '@/components/ChatInterface'
import './Dashboard.css'

function Dashboard() {
  const { fetchChatHistory, fetchCommandHistory, fetchCodeSnippets, fetchDailyAnalytics } = useDashboardStore()
  const [stats, setStats] = useState({
    totalMessages: 0,
    totalCommands: 0,
    totalSnippets: 0,
    averageResponseTime: 0
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const loadDashboardData = async () => {
      try {
        const userId = '1' // Get from auth
        
        const [chatData, cmdData, snippetData, analyticsData] = await Promise.all([
          fetchChatHistory(userId, 1, 0),
          fetchCommandHistory(userId, 1, 0),
          fetchCodeSnippets(userId, 1, 0),
          fetchDailyAnalytics(userId)
        ])

        setStats({
          totalMessages: chatData.total || 0,
          totalCommands: cmdData.total || 0,
          totalSnippets: snippetData.total || 0,
          averageResponseTime: analyticsData.analytics?.[0]?.avg_response_time_ms || 0
        })
      } catch (error) {
        console.error('Failed to load dashboard data:', error)
      } finally {
        setLoading(false)
      }
    }

    loadDashboardData()
  }, [])

  if (loading) {
    return (
      <div className="dashboard-loading">
        <div className="spinner"></div>
        <p>Loading dashboard...</p>
      </div>
    )
  }

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>Dashboard</h1>
        <p className="subtitle">Welcome back! Here's your Jarvis activity overview.</p>
      </div>

      {/* Chat Interface - Main Feature */}
      <div className="chat-section">
        <ChatInterface />
      </div>

      {/* Stats Cards */}
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon chat">
            <FiMessageSquare />
          </div>
          <div className="stat-content">
            <h3>Chat Messages</h3>
            <p className="stat-value">{stats.totalMessages.toLocaleString()}</p>
            <span className="stat-subtitle">Total conversations</span>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon command">
            <FiTerminal />
          </div>
          <div className="stat-content">
            <h3>Commands Executed</h3>
            <p className="stat-value">{stats.totalCommands.toLocaleString()}</p>
            <span className="stat-subtitle">Total executions</span>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon code">
            <FiCode />
          </div>
          <div className="stat-content">
            <h3>Code Snippets</h3>
            <p className="stat-value">{stats.totalSnippets.toLocaleString()}</p>
            <span className="stat-subtitle">Saved snippets</span>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon trending">
            <FiTrendingUp />
          </div>
          <div className="stat-content">
            <h3>Avg Response Time</h3>
            <p className="stat-value">{stats.averageResponseTime.toFixed(0)}ms</p>
            <span className="stat-subtitle">Per interaction</span>
          </div>
        </div>
      </div>

      {/* Recent Activity */}
      <div className="dashboard-grid">
        <div className="card">
          <div className="card-header">
            <h2>Recent Chat Activity</h2>
          </div>
          <div className="card-body">
            <div className="activity-list">
              <p className="empty-placeholder">No recent messages yet</p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="card-header">
            <h2>AI Provider Usage</h2>
          </div>
          <div className="card-body">
            <div className="provider-list">
              <div className="provider-item">
                <span className="provider-name">Local (Ollama)</span>
                <span className="provider-count">0 requests</span>
              </div>
              <div className="provider-item">
                <span className="provider-name">OpenAI</span>
                <span className="provider-count">0 requests</span>
              </div>
              <div className="provider-item">
                <span className="provider-name">Claude</span>
                <span className="provider-count">0 requests</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Quick Links */}
      <div className="card">
        <div className="card-header">
          <h2>Quick Actions</h2>
        </div>
        <div className="card-body">
          <div className="quick-actions">
            <a href="/chat-history" className="action-button">
              View Chat History
            </a>
            <a href="/command-history" className="action-button">
              Command Logs
            </a>
            <a href="/code-snippets" className="action-button">
              Browse Snippets
            </a>
            <a href="/analytics" className="action-button">
              Analytics
            </a>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Dashboard
