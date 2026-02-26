import React, { useState, useRef, useEffect } from 'react'
import './ChatInterface.css'

function ChatInterface() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const sendMessage = async (e) => {
    e.preventDefault()
    
    if (!input.trim()) return

    // Add user message
    const userMessage = { type: 'user', text: input, timestamp: new Date() }
    setMessages(prev => [...prev, userMessage])
    setInput('')
    setLoading(true)

    try {
      // Send to backend
      const response = await fetch('http://localhost:8001/api/chat/message', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: input })
      })

      const data = await response.json()

      // Add bot response
      if (data.success) {
        const botMessage = {
          type: 'bot',
          text: data.message,
          timestamp: new Date()
        }
        setMessages(prev => [...prev, botMessage])
      } else {
        const errorMessage = {
          type: 'error',
          text: `Error: ${data.error || 'No response from server'}`,
          timestamp: new Date()
        }
        setMessages(prev => [...prev, errorMessage])
      }
    } catch (error) {
      const errorMessage = {
        type: 'error',
        text: `Connection error: ${error.message}`,
        timestamp: new Date()
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="chat-interface">
      <div className="chat-messages">
        {messages.length === 0 ? (
          <div className="chat-empty">
            <p>💬 Chat with Jarvis</p>
            <p className="subtitle">Type a message to get started</p>
          </div>
        ) : (
          messages.map((msg, idx) => (
            <div key={idx} className={`chat-message ${msg.type}`}>
              <div className="message-bubble">
                {msg.text}
              </div>
              <span className="message-time">
                {msg.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
              </span>
            </div>
          ))
        )}
        {loading && (
          <div className="chat-message bot">
            <div className="message-bubble typing">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={sendMessage} className="chat-input-form">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message... (e.g., 'hi', 'help', 'analyze')"
          className="chat-input"
          disabled={loading}
          autoFocus
        />
        <button type="submit" className="chat-send" disabled={loading || !input.trim()}>
          {loading ? '...' : '→'}
        </button>
      </form>
    </div>
  )
}

export default ChatInterface
