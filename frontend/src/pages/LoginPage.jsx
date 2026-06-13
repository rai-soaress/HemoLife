import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { login, loginOng } from '../services/api'
import { useAuth } from '../contexts/AuthContext'

const ACCESS_TYPES = [
  { value: 'doador', label: 'Doador' },
  { value: 'admin', label: 'Admin' },
  { value: 'ong', label: 'ONG' },
]

export default function LoginPage() {
  const navigate = useNavigate()
  const { setUser } = useAuth()
  const [email, setEmail] = useState('')
  const [senha, setSenha] = useState('')
  const [accountType, setAccountType] = useState('doador')
  const [error, setError] = useState('')

  async function handleSubmit(event) {
    event.preventDefault()
    setError('')

    try {
      const data = accountType === 'ong'
        ? await loginOng(email, senha)
        : await login(email, senha, accountType)

      if (data.success) {
        setUser(data.user)
        navigate(data.user?.perfil === 'ong' ? '/ong/painel' : '/home')
      }
    } catch (error) {
      setError(error.data?.message || error.message || 'Erro ao fazer login.')
    }
  }

  return (
    <section className="panel auth-panel">
      <h1>Login</h1>
      <p className="muted auth-hint">Escolha o tipo de acesso antes de entrar.</p>
      {error && <p className="flash flash-error">{error}</p>}

      <div className="segmented-control" role="tablist" aria-label="Tipo de acesso">
        {ACCESS_TYPES.map((type) => (
          <button
            key={type.value}
            type="button"
            className={accountType === type.value ? 'active' : ''}
            onClick={() => setAccountType(type.value)}
          >
            {type.label}
          </button>
        ))}
      </div>

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

        <button type="submit">
          Entrar como {ACCESS_TYPES.find((type) => type.value === accountType)?.label}
        </button>
      </form>

      <p className="muted">
        Ainda nao tem conta? <Link to="/cadastrar">Cadastre-se</Link>.
      </p>
    </section>
  )
}
