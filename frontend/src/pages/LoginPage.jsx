import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { login } from '../services/api'
import { useAuth } from '../contexts/AuthContext'

export default function LoginPage() {
  const navigate = useNavigate()
  const { setUser } = useAuth()
  const [email, setEmail] = useState('')
  const [senha, setSenha] = useState('')
  const [error, setError] = useState('')

  async function handleSubmit(event) {
    event.preventDefault()
    setError('')

    try {
      const data = await login(email, senha)
      if (data.success) {
        setUser(data.user)
        navigate('/home')
      }
    } catch (error) {
      const fallback =
        error.data?.message === 'Login required'
          ? 'Sessão inválida. Tente novamente com suas credenciais.'
          : error.data?.message || error.message || 'Erro ao fazer login.'
      setError(fallback)
    }
  }

  return (
    <section className="panel auth-panel">
      <h1>Login</h1>
      {error && <p className="flash flash-error">{error}</p>}
      <form onSubmit={handleSubmit}>
        <label htmlFor="email">Email</label>
        <input
          id="email"
          type="email"
          value={email}
          onChange={(event) => setEmail(event.target.value)}
          autoComplete="email"
          required
        />

        <label htmlFor="senha">Senha</label>
        <input
          id="senha"
          type="password"
          value={senha}
          onChange={(event) => setSenha(event.target.value)}
          autoComplete="current-password"
          required
        />

        <button type="submit">Entrar</button>
      </form>
      <p className="muted">
        Ainda não tem conta? <Link to="/cadastrar">Cadastre-se</Link>.
      </p>
    </section>
  )
}
