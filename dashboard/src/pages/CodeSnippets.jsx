import React from 'react'

function CodeSnippets() {
  return (
    <div className="page-container">
      <div className="page-header">
        <h1>Code Snippets</h1>
        <p>Manage and browse saved code snippets</p>
      </div>

      <div className="card">
        <div className="card-header">
          <h2>Your Snippets</h2>
          <button className="btn-primary">New Snippet</button>
        </div>
        <div className="card-body">
          <div style={{ textAlign: 'center', padding: '40px', color: '#9ca3af' }}>
            No code snippets yet
          </div>
        </div>
      </div>
    </div>
  )
}

export default CodeSnippets
