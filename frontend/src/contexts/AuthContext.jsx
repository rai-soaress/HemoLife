import { createContext, useContext, useEffect, useState } from 'react'
import { getSession, logout as logoutApi } from '../services/api'

const AuthContext = createContext({
  user: null,
  loading: true,
  setUser: () => {},
  signOut: () => {},
})

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    getSession()
      .then((data) => {
        if (data?.authenticated) {
          setUser(data.user)
        }
      })
      .catch(() => {
        setUser(null)
      })
      .finally(() => setLoading(false))
  }, [])

  async function signOut() {
    try {
      await logoutApi()
    } catch (error) {
      console.error('Erro ao deslogar', error)
    }
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, loading, setUser, signOut }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  return useContext(AuthContext)
}
