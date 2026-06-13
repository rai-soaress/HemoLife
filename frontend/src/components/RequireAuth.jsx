import { Navigate, useLocation } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'

export function RequireAuth({ children }) {
  const { user, loading } = useAuth()
  const location = useLocation()

  if (loading) {
    return <div className="container">Carregando...</div>
  }

  if (!user) {
    return <Navigate to="/login" state={{ from: location }} replace />
  }

  return children
}

export function RequireAdmin({ children }) {
  const { user, loading } = useAuth()

  if (loading) {
    return <div className="container">Carregando...</div>
  }

  if (!user) {
    return <Navigate to="/login" replace />
  }

  if (user.perfil !== 'admin') {
    return <Navigate to="/home" replace />
  }

  return children
}

export function RequireOng({ children }) {
  const { user, loading } = useAuth()

  if (loading) {
    return <div className="container">Carregando...</div>
  }

  if (!user) {
    return <Navigate to="/login" replace />
  }

  if (user.perfil !== 'ong') {
    return <Navigate to="/home" replace />
  }

  return children
}

export function RequireDoador({ children }) {
  const { user, loading } = useAuth()

  if (loading) {
    return <div className="container">Carregando...</div>
  }

  if (!user) {
    return <Navigate to="/login" replace />
  }

  if (user.perfil !== 'doador') {
    return <Navigate to="/home" replace />
  }

  return children
}
