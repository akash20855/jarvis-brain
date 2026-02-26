import React, { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { useDashboardStore } from '@/store/dashboardStore'
import Navigation from '@/components/Navigation'
import Sidebar from '@/components/Sidebar'
import Dashboard from '@/pages/Dashboard'
import ChatHistory from '@/pages/ChatHistory'
import CommandHistory from '@/pages/CommandHistory'
import Analytics from '@/pages/Analytics'
import CodeSnippets from '@/pages/CodeSnippets'
import Settings from '@/pages/Settings'
import '@/App.css'

function App() {
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const [loading, setLoading] = useState(true)
  const { initStore, healthCheck } = useDashboardStore()

  useEffect(() => {
    const init = async () => {
      try {
        // Initialize store with user data
        await initStore()
        
        // Check backend health
        const healthy = await healthCheck()
        if (!healthy) {
          console.warn('⚠️ Database connection may be unavailable')
        }
      } catch (error) {
        console.error('Failed to initialize dashboard:', error)
      } finally {
        setLoading(false)
      }
    }

    init()
  }, [initStore, healthCheck])

  if (loading) {
    return (
      <div className="loading-container">
        <div className="spinner"></div>
        <p>Initializing Jarvis Dashboard...</p>
      </div>
    )
  }

  return (
    <Router>
      <div className="app-container">
        <Navigation sidebarOpen={sidebarOpen} setSidebarOpen={setSidebarOpen} />
        
        <div className="app-layout">
          <Sidebar isOpen={sidebarOpen} />
          
          <main className={`main-content ${!sidebarOpen ? 'full-width' : ''}`}>
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/chat-history" element={<ChatHistory />} />
              <Route path="/command-history" element={<CommandHistory />} />
              <Route path="/analytics" element={<Analytics />} />
              <Route path="/code-snippets" element={<CodeSnippets />} />
              <Route path="/settings" element={<Settings />} />
            </Routes>
          </main>
        </div>
      </div>
    </Router>
  )
}

export default App
