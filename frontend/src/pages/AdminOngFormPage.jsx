import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { createAdminOng, getAdminOng, updateAdminOng } from '../services/api'

export default function AdminOngFormPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [nome, setNome] = useState('')
  const [email, setEmail] = useState('')
  const [cnpj, setCnpj] = useState('')
  const [senha, setSenha] = useState('')
  const [message, setMessage] = useState('')
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    if (!id) {
      document.title = 'Cadastrar ONG - HemoLife'
      return
    }

    document.title = 'Editar ONG - HemoLife'
    setLoading(true)
    getAdminOng(id)
      .then((data) => {
        setNome(data.nome || '')
        setEmail(data.email || '')
        setCnpj(data.cnpj || '')
      })
      .catch((error) => {
        setMessage(error.data?.message || error.message || 'Erro ao carregar ONG para edição.')
      })
      .finally(() => setLoading(false))
  }, [id])

  async function handleSubmit(event) {
    event.preventDefault()
    setMessage('')

    try {
      if (id) {
        await updateAdminOng(id, { nome, email, cnpj })
        navigate('/admin/ongs')
      } else {
        await createAdminOng({ nome, email, senha, cnpj })
        navigate('/admin/ongs')
      }
    } catch (error) {
      setMessage(error.data?.message || error.message || 'Erro ao salvar ONG.')
    }
  }

  return (
    <section className="panel form-panel">
      <div className="page-heading">
        <div>
          <h1>{id ? 'Editar ONG' : 'Cadastrar ONG'}</h1>
          <p>{id ? 'Atualize os dados da ONG' : 'Cadastre uma nova ONG no sistema'}</p>
        </div>
      </div>

      {message && <p className="flash flash-error">{message}</p>}

      {loading ? (
        <p className="empty-state">Carregando dados da ONG...</p>
      ) : (
        <form onSubmit={handleSubmit}>
          <label htmlFor="nome">Nome da ONG</label>
          <input
            id="nome"
            type="text"
            value={nome}
            onChange={(event) => setNome(event.target.value)}
            required
          />

          <label htmlFor="email">Email</label>
          <input
            id="email"
            type="email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            required
          />

          <label htmlFor="cnpj">CNPJ</label>
          <input
            id="cnpj"
            type="text"
            value={cnpj}
            onChange={(event) => setCnpj(event.target.value)}
            required
          />

          {!id && (
            <>
              <label htmlFor="senha">Senha da ONG</label>
              <input
                id="senha"
                type="password"
                value={senha}
                onChange={(event) => setSenha(event.target.value)}
                required
              />
            </>
          )}

          <button type="submit" className="button-link">
            {id ? 'Salvar Alterações' : 'Cadastrar ONG'}
          </button>
        </form>
      )}
    </section>
  )
}
