import React from 'react'

function CommandHistory() {
  return (
    <div className="page-container">
      <div className="page-header">
        <h1>Command History</h1>
        <p>View executed commands and their results</p>
      </div>

      <div className="card">
        <table className="table">
          <thead>
            <tr>
              <th>Command</th>
              <th>Status</th>
              <th>Execution Time</th>
              <th>Result</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td colSpan="4" style={{ textAlign: 'center', padding: '40px' }}>
                No command history yet
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default CommandHistory
