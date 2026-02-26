import React from 'react'

function Analytics() {
  return (
    <div className="page-container">
      <div className="page-header">
        <h1>Analytics</h1>
        <p>View usage statistics and trends</p>
      </div>

      <div className="grid grid-2">
        <div className="card">
          <div className="card-header">
            <h2>Daily Activity</h2>
          </div>
          <div className="card-body">
            <p style={{ textAlign: 'center', padding: '40px', color: '#9ca3af' }}>Chart coming soon</p>
          </div>
        </div>

        <div className="card">
          <div className="card-header">
            <h2>Provider Usage</h2>
          </div>
          <div className="card-body">
            <p style={{ textAlign: 'center', padding: '40px', color: '#9ca3af' }}>Chart coming soon</p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Analytics
