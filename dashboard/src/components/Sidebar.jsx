import React from 'react'
import { useLocation } from 'react-router-dom'
import { FiMenu, FiX, FiHome, FiMessageSquare, FiTerminal, FiBarChart2, FiCode, FiSettings, FiLogOut } from 'react-icons/fi'
import './Sidebar.css'

function Sidebar({ isOpen }) {
  const location = useLocation()

  const menuItems = [
    { path: '/', icon: FiHome, label: 'Dashboard' },
    { path: '/chat-history', icon: FiMessageSquare, label: 'Chat History' },
    { path: '/command-history', icon: FiTerminal, label: 'Commands' },
    { path: '/analytics', icon: FiBarChart2, label: 'Analytics' },
    { path: '/code-snippets', icon: FiCode, label: 'Snippets' },
    { path: '/settings', icon: FiSettings, label: 'Settings' }
  ]

  const isActive = (path) => location.pathname === path

  return (
    <aside className={`sidebar ${isOpen ? 'open' : 'closed'}`}>
      <nav className="sidebar-nav">
        <div className="sidebar-brand">
          <div className="brand-icon">🧠</div>
          {isOpen && <span className="brand-text">Jarvis</span>}
        </div>

        <ul className="nav-menu">
          {menuItems.map((item) => {
            const Icon = item.icon
            return (
              <li key={item.path}>
                <a
                  href={item.path}
                  className={`nav-link ${isActive(item.path) ? 'active' : ''}`}
                  title={item.label}
                >
                  <Icon className="nav-icon" />
                  {isOpen && <span>{item.label}</span>}
                </a>
              </li>
            )
          })}
        </ul>

        <div className="sidebar-footer">
          <button className="logout-btn" title="Logout">
            <FiLogOut className="logout-icon" />
            {isOpen && <span>Logout</span>}
          </button>
        </div>
      </nav>
    </aside>
  )
}

export default Sidebar
