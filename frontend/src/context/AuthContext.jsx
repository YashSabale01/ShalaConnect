import { createContext, useContext, useState, useEffect, useCallback } from 'react'
import { authApi } from '../services/api'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser]       = useState(() => {
    try { return JSON.parse(localStorage.getItem('user')) } catch { return null }
  })
  const [token, setToken]     = useState(() => localStorage.getItem('token'))
  const [loading, setLoading] = useState(true)

  // Verify token on mount
  useEffect(() => {
    const verify = async () => {
      if (!token) { setLoading(false); return }
      try {
        const res = await authApi.me()
        setUser(res.data.data)
        localStorage.setItem('user', JSON.stringify(res.data.data))
      } catch {
        localStorage.removeItem('token')
        localStorage.removeItem('user')
        setToken(null)
        setUser(null)
      } finally {
        setLoading(false)
      }
    }
    verify()
  }, [token])

  const login = useCallback(async (email, password) => {
    const res = await authApi.login({ email, password })
    const { token: newToken, user: newUser } = res.data.data
    localStorage.setItem('token', newToken)
    localStorage.setItem('user', JSON.stringify(newUser))
    setToken(newToken)
    setUser(newUser)
    return newUser
  }, [])

  const logout = useCallback(() => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    setToken(null)
    setUser(null)
  }, [])

  const refreshUser = useCallback(async () => {
    const res = await authApi.me()
    setUser(res.data.data)
    localStorage.setItem('user', JSON.stringify(res.data.data))
  }, [])

  const isAdmin      = user?.role === 'ADMIN'
  const isHeadmaster = user?.role === 'HEADMASTER'

  return (
    <AuthContext.Provider value={{ user, token, loading, login, logout, refreshUser, isAdmin, isHeadmaster }}>
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used within AuthProvider')
  return ctx
}
