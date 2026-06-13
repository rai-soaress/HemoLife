import { useEffect, useMemo, useState } from 'react'
import { getOngMembers } from '../services/api'
import { useAuth } from '../contexts/AuthContext'

export default function OngDashboardPage() {
  const { user } = useAuth()
  const [membros, setMembros] = useState([])
  const [message, setMessage] = useState('')
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')

  useEffect(() => {
    loadMembers()
  }, [])

  async function loadMembers() {
    try {
      const data = await getOngMembers()
      setMembros(data.membros || [])
    } catch (error) {
      setMessage(error.data?.message || error.message || 'Erro ao carregar cadastrados.')
    } finally {
      setLoading(false)
    }
  }

  const filteredMembers = useMemo(() => {
    const term = searchTerm.trim().toLowerCase()
    if (!term) {
      return membros
    }

    return membros.filter((membro) =>
      [membro.nome, membro.email, membro.tipo_sanguineo]
        .filter(Boolean)
        .some((value) => value.toLowerCase().includes(term)),
    )
  }, [membros, searchTerm])

  return (
    <>
      <section className="page-heading">
        <div>
          <h1>Painel da ONG</h1>
          <p>{user?.nome} pode acompanhar os doadores inscritos aqui.</p>
        </div>
        <div className="search-bar">
          <input
            type="search"
            value={searchTerm}
            onChange={(event) => setSearchTerm(event.target.value)}
            placeholder="Buscar por nome, email ou sangue"
            aria-label="Buscar cadastrados"
          />
        </div>
      </section>

      {message && <p className="flash flash-error">{message}</p>}

      {loading ? (
        <p className="empty-state">Carregando cadastrados...</p>
      ) : filteredMembers.length === 0 ? (
        <p className="empty-state">
          {searchTerm.trim()
            ? 'Nenhum cadastrado encontrado para essa busca.'
            : 'Ainda nao ha doadores cadastrados nesta ONG.'}
        </p>
      ) : (
        <section className="card-list">
          {filteredMembers.map((membro) => (
            <article className="list-card" key={membro.id}>
              <div>
                <h2>{membro.nome}</h2>
                <p>{membro.email}</p>
                <p className="muted">Tipo sanguineo: {membro.tipo_sanguineo || 'Nao informado'}</p>
              </div>
            </article>
          ))}
        </section>
      )}
    </>
  )
}
