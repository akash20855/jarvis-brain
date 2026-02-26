import React, { useEffect, useState } from 'react'
import { useDashboardStore } from '@/store/dashboardStore'

function ChatHistory() {
  const { fetchChatHistory } = useDashboardStore()
  const [messages, setMessages] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const loadMessages = async () => {
      try {
        const userId = '1'
        const data = await fetchChatHistory(userId, 50, 0)
        setMessages(data.messages || [])
      } catch (error) {
        console.error('Failed to load chat history:', error)
      } finally {
        setLoading(false)
      }
    }

    loadMessages()
  }, [])

  return (
    <div className="page-container">
      <div className="page-header">
        <h1>Chat History</h1>
        <p>View all past conversations with Jarvis</p>
      </div>

      {loading ? (
        <div>Loading...</div>
      ) : (
        <div className="card">
          <table className="table">
            <thead>
              <tr>
                <th>Message</th>
                <th>Response</th>
                <th>Provider</th>
                <th>Time</th>
              </tr>
            </thead>
            <tbody>
              {messages.length === 0 ? (
                <tr>
                  <td colSpan="4" style={{ textAlign: 'center', padding: '40px' }}>
                    No chat history yet
                  </td>
                </tr>
              ) : (
                messages.map((msg) => (
                  <tr key={msg.id}>
                    <td>{msg.message.substring(0, 50)}...</td>
                    <td>{msg.response ? msg.response.substring(0, 50) + '...' : 'N/A'}</td>
                    <td>
                      <span className="badge badge-info">{msg.ai_provider}</span>
                    </td>
                    <td>{new Date(msg.timestamp).toLocaleString()}</td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}

export default ChatHistory
