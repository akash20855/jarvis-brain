import React from 'react'
import { FiMenu, FiX, FiBell, FiUser, FiSearch } from 'react-icons/fi'
import { useDashboardStore } from '@/store/dashboardStore'
import './Navigation.css'

function Navigation({ sidebarOpen, setSidebarOpen }) {
  const { databaseConnected } = useDashboardStore()
  const [searchActive, setSearchActive] = React.useState(false)

  return (
    <header className="navigation">
      <div className="nav-left">
        <button
          className="menu-toggle"
          onClick={() => setSidebarOpen(!sidebarOpen)}
          aria-label="Toggle sidebar"
        >
          {sidebarOpen ? <FiX size={24} /> : <FiMenu size={24} />}
        </button>

        <div className="search-bar">
          <FiSearch className="search-icon" />
          <input
            type="text"
            placeholder="Search chat, commands, snippets..."
            className="search-input"
            onFocus={() => setSearchActive(true)}
            onBlur={() => setSearchActive(false)}
          />
        </div>
      </div>

      <div className="nav-right">
        {/* Database Status */}
        <div className={`db-status ${databaseConnected ? 'connected' : 'disconnected'}`}>
          <span className="status-dot"></span>
          <span className="status-text">
            {databaseConnected ? 'Connected' : 'Offline'}
          </span>
        </div>

        {/* Notifications */}
        <button className="nav-icon-btn" aria-label="Notifications">
          <FiBell size={20} />
          <span className="notification-badge">3</span>
        </button>

        {/* User Menu */}
        <button className="user-menu" aria-label="User menu">
          <div className="user-avatar">JD</div>
          <span className="user-name">John Doe</span>
        </button>
      </div>
    </header>
  )
}

export default Navigation
