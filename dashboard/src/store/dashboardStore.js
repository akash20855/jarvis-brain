import { create } from 'zustand'
import api from '@/services/api'

export const useDashboardStore = create((set, get) => ({
  // State
  user: null,
  chatMessages: [],
  commandExecutions: [],
  analytics: {
    daily: [],
    provider: []
  },
  codeSnippets: [],
  loading: false,
  error: null,
  databaseConnected: false,

  // Actions
  initStore: async () => {
    set({ loading: true })
    try {
      // Load initial data
      const userId = localStorage.getItem('userId') || '1'
      
      // Check database health
      const health = await api.get('/api/persistence/health')
      set({ databaseConnected: health.status === 'healthy' })

      set({ loading: false, error: null })
    } catch (error) {
      console.error('Store initialization error:', error)
      set({ error: error.message, loading: false })
    }
  },

  // Chat operations
  fetchChatHistory: async (userId, limit = 50, offset = 0) => {
    set({ loading: true })
    try {
      const response = await api.get(`/api/persistence/chat/history/${userId}`, {
        params: { limit, offset }
      })
      set({ chatMessages: response.data.messages, loading: false, error: null })
      return response.data
    } catch (error) {
      set({ error: error.message, loading: false })
      throw error
    }
  },

  saveChatMessage: async (message) => {
    try {
      const response = await api.post('/api/persistence/chat/save', message)
      
      // Add to state
      const { chatMessages } = get()
      set({ chatMessages: [response.data, ...chatMessages] })
      
      return response.data
    } catch (error) {
      set({ error: error.message })
      throw error
    }
  },

  // Command operations
  fetchCommandHistory: async (userId, limit = 100, offset = 0, status = null) => {
    set({ loading: true })
    try {
      const response = await api.get(`/api/persistence/command/history/${userId}`, {
        params: { limit, offset, ...(status && { status }) }
      })
      set({ commandExecutions: response.data.commands, loading: false, error: null })
      return response.data
    } catch (error) {
      set({ error: error.message, loading: false })
      throw error
    }
  },

  logCommand: async (command) => {
    try {
      const response = await api.post('/api/persistence/command/log', command)
      
      // Add to state
      const { commandExecutions } = get()
      set({ commandExecutions: [response.data, ...commandExecutions] })
      
      return response.data
    } catch (error) {
      set({ error: error.message })
      throw error
    }
  },

  // Analytics operations
  fetchDailyAnalytics: async (userId) => {
    set({ loading: true })
    try {
      const response = await api.get(`/api/persistence/analytics/daily/${userId}`)
      set(state => ({
        analytics: { ...state.analytics, daily: response.data.analytics },
        loading: false,
        error: null
      }))
      return response.data
    } catch (error) {
      set({ error: error.message, loading: false })
      throw error
    }
  },

  fetchProviderAnalytics: async (userId) => {
    set({ loading: true })
    try {
      const response = await api.get(`/api/persistence/analytics/provider/${userId}`)
      set(state => ({
        analytics: { ...state.analytics, provider: response.data.analytics },
        loading: false,
        error: null
      }))
      return response.data
    } catch (error) {
      set({ error: error.message, loading: false })
      throw error
    }
  },

  // Code snippet operations
  fetchCodeSnippets: async (userId, limit = 50, offset = 0) => {
    set({ loading: true })
    try {
      const response = await api.get(`/api/persistence/snippet/${userId}`, {
        params: { limit, offset }
      })
      set({ codeSnippets: response.data.snippets, loading: false, error: null })
      return response.data
    } catch (error) {
      set({ error: error.message, loading: false })
      throw error
    }
  },

  saveCodeSnippet: async (snippet) => {
    try {
      const response = await api.post('/api/persistence/snippet/save', snippet)
      
      // Add to state
      const { codeSnippets } = get()
      set({ codeSnippets: [response.data, ...codeSnippets] })
      
      return response.data
    } catch (error) {
      set({ error: error.message })
      throw error
    }
  },

  // Health check
  healthCheck: async () => {
    try {
      const response = await api.get('/api/persistence/health')
      const healthy = response.status === 'healthy'
      set({ databaseConnected: healthy })
      return healthy
    } catch (error) {
      console.warn('Health check failed:', error)
      set({ databaseConnected: false })
      return false
    }
  },

  // Utility
  clearError: () => set({ error: null }),
  setLoading: (loading) => set({ loading })
}))
