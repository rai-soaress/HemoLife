import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { register } from '../services/api'

export default function RegisterPage() {
  const navigate = useNavigate()
  const [nome, setNome] = useState('')
  const [email, setEmail] = useState('')
  const [senha, setSenha] = useState('')
  const [perfil, setPerfil] = useState('doador')
  const [tipoSanguineo, setTipoSanguineo] = useState('')
  const [message, setMessage] = useState('')

  const isAdmin = perfil === 'admin'

  async function handleSubmit(event) {
    event.preventDefault()
    setMessage('')

    try {
      const data = await register(nome, email, senha, perfil, isAdmin ? null : tipoSanguineo)
      if (data.success) {
        navigate('/login')
      } else {
        setMessage(data.message || 'Erro ao cadastrar.')
      }
    } catch (error) {
      const fallback =
        error.data?.message === 'Login required'
          ? 'Não é necessário estar logado para cadastrar. Tente novamente.'
          : error.data?.message || error.message || 'Erro ao cadastrar.'
      setMessage(fallback)
    }
  }

  return (
    <section className="panel auth-panel">
      <h1>Cadastro</h1>
      {message && <p className="flash flash-error">{message}</p>}
      <form onSubmit={handleSubmit}>
        <label htmlFor="nome">Nome</label>
        <input
          id="nome"
          type="text"
          value={nome}
          onChange={(event) => setNome(event.target.value)}
          autoComplete="name"
          required
        />

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
          autoComplete="new-password"
          required
        />

        <label htmlFor="perfil">Perfil</label>
        <select id="perfil" value={perfil} onChange={(event) => setPerfil(event.target.value)} required>
          <option value="doador">Doador</option>
          <option value="admin">Admin</option>
        </select>

        {!isAdmin && (
          <div id="campo_tipo_sanguineo">
            <label htmlFor="tipo_sanguineo">Tipo sanguíneo</label>
            <select
              id="tipo_sanguineo"
              value={tipoSanguineo}
              onChange={(event) => setTipoSanguineo(event.target.value)}
              required
            >
              <option value="">Selecione</option>
              <option value="A+">A+</option>
              <option value="A-">A-</option>
              <option value="B+">B+</option>
              <option value="B-">B-</option>
              <option value="AB+">AB+</option>
              <option value="AB-">AB-</option>
              <option value="O+">O+</option>
              <option value="O-">O-</option>
            </select>
          </div>
        )}

        <button type="submit">Cadastrar</button>
      </form>
      <p className="muted">
        Já tem conta? <Link to="/login">Entrar</Link>.
      </p>
    </section>
  )
}
