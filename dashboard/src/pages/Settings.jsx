import React from 'react'

function Settings() {
  return (
    <div className="page-container">
      <div className="page-header">
        <h1>Settings</h1>
        <p>Configure your Jarvis preferences</p>
      </div>

      <div className="grid">
        <div className="card">
          <div className="card-header">
            <h2>General Settings</h2>
          </div>
          <div className="card-body">
            <div style={{ padding: '20px' }}>
              <div style={{ marginBottom: '16px' }}>
                <label style={{ display: 'block', marginBottom: '4px', fontWeight: '500' }}>
                  Theme
                </label>
                <select style={{ width: '100%', padding: '8px' }}>
                  <option>Light</option>
                  <option>Dark</option>
                  <option>Auto</option>
                </select>
              </div>
              <button className="btn-primary">Save</button>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="card-header">
            <h2>API Integration</h2>
          </div>
          <div className="card-body">
            <div style={{ padding: '20px' }}>
              <p>Configure your AI provider settings</p>
              <button className="btn-secondary">Manage Providers</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Settings
