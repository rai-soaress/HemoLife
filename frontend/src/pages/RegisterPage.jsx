import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { register, registerOng } from '../services/api'

const ACCOUNT_TYPES = [
  { value: 'doador', label: 'Doador' },
  { value: 'ong', label: 'ONG' },
  { value: 'admin', label: 'Admin' },
]

const BLOOD_TYPES = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']

export default function RegisterPage() {
  const navigate = useNavigate()
  const [accountType, setAccountType] = useState('doador')
  const [nome, setNome] = useState('')
  const [email, setEmail] = useState('')
  const [senha, setSenha] = useState('')
  const [tipoSanguineo, setTipoSanguineo] = useState('')
  const [cnpj, setCnpj] = useState('')
  const [codigoAdmin, setCodigoAdmin] = useState('')
  const [message, setMessage] = useState('')

  const isDoador = accountType === 'doador'
  const isOng = accountType === 'ong'
  const isAdmin = accountType === 'admin'

  async function handleSubmit(event) {
    event.preventDefault()
    setMessage('')

    try {
      const data = isOng
        ? await registerOng({ nome, email, senha, cnpj })
        : await register({
            nome,
            email,
            senha,
            perfil: accountType,
            tipo_sanguineo: isDoador ? tipoSanguineo : null,
            codigo_admin: isAdmin ? codigoAdmin : null,
          })

      if (data.success) {
        navigate('/login')
      } else {
        setMessage(data.message || 'Erro ao cadastrar.')
      }
    } catch (error) {
      setMessage(error.data?.message || error.message || 'Erro ao cadastrar.')
    }
  }

  return (
    <section className="panel auth-panel">
      <h1>Cadastro</h1>
      <p className="muted auth-hint">Crie a conta no perfil correto para liberar as telas certas.</p>
      {message && <p className="flash flash-error">{message}</p>}

      <div className="segmented-control" role="tablist" aria-label="Tipo de cadastro">
        {ACCOUNT_TYPES.map((type) => (
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
        <label htmlFor="nome">{isOng ? 'Nome da ONG' : 'Nome'}</label>
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

        {isDoador && (
          <div>
            <label htmlFor="tipo_sanguineo">Tipo sanguineo</label>
            <select
              id="tipo_sanguineo"
              value={tipoSanguineo}
              onChange={(event) => setTipoSanguineo(event.target.value)}
              required
            >
              <option value="">Selecione</option>
              {BLOOD_TYPES.map((type) => (
                <option key={type} value={type}>
                  {type}
                </option>
              ))}
            </select>
          </div>
        )}

        {isOng && (
          <div>
            <label htmlFor="cnpj">CNPJ</label>
            <input
              id="cnpj"
              type="text"
              value={cnpj}
              onChange={(event) => setCnpj(event.target.value)}
              autoComplete="organization"
              required
            />
          </div>
        )}

        {isAdmin && (
          <div>
            <label htmlFor="codigo_admin">Codigo de cadastro admin</label>
            <input
              id="codigo_admin"
              type="password"
              value={codigoAdmin}
              onChange={(event) => setCodigoAdmin(event.target.value)}
              autoComplete="off"
              required
            />
          </div>
        )}

        <button type="submit">
          Cadastrar como {ACCOUNT_TYPES.find((type) => type.value === accountType)?.label}
        </button>
      </form>

      <p className="muted">
        Ja tem conta? <Link to="/login">Entrar</Link>.
      </p>
    </section>
  )
}
