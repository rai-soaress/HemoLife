import { useEffect, useState } from 'react'
import { getOngs, subscribeOng, cancelSubscription } from '../services/api'

export default function OngsPage() {
  const [ongs, setOngs] = useState([])
  const [inscritas, setInscritas] = useState([])
  const [message, setMessage] = useState('')
  const [searchTerm, setSearchTerm] = useState('')

  useEffect(() => {
    loadOngs()
  }, [])

  async function loadOngs() {
    try {
      const data = await getOngs()
      setOngs(data.ongs || [])
      setInscritas(data.inscritas || [])
    } catch (error) {
      setMessage(error.data?.message || error.message || 'Erro ao buscar ONGs.')
    }
  }

  async function handleSubscribe(id) {
    try {
      const data = await subscribeOng(id)
      setMessage(data.message || 'Inscrição realizada com sucesso.')
      loadOngs()
    } catch (error) {
      setMessage(error.data?.message || error.message || 'Erro ao inscrever.')
    }
  }

  async function handleCancel(id) {
    try {
      const data = await cancelSubscription(id)
      setMessage(data.message || 'Inscrição cancelada com sucesso.')
      loadOngs()
    } catch (error) {
      setMessage(error.data?.message || error.message || 'Erro ao cancelar inscrição.')
    }
  }

  const filteredOngs = ongs.filter((ong) => {
    const term = searchTerm.trim().toLowerCase()
    if (!term) {
      return true
    }

    return [ong.nome, ong.email, ong.cnpj]
      .filter(Boolean)
      .some((value) => value.toLowerCase().includes(term))
  })

  return (
    <>
      <section className="page-heading">
        <div>
          <h1>ONGs</h1>
          <p>Escolha uma ONG para acompanhar e apoiar.</p>
        </div>
        <div className="search-bar">
          <input
            type="search"
            value={searchTerm}
            onChange={(event) => setSearchTerm(event.target.value)}
            placeholder="Procurar ONG por nome, email ou CNPJ"
            aria-label="Buscar ONGs"
          />
        </div>
      </section>

      {message && <p className="flash flash-message">{message}</p>}

      <section className="card-list">
        {filteredOngs.length > 0 ? (
          filteredOngs.map((ong) => (
            <article className="list-card" key={ong.id}>
              <div>
                <h2>{ong.nome}</h2>
                <p>{ong.email}</p>
                <p className="muted">CNPJ: {ong.cnpj}</p>
              </div>
              {inscritas.includes(ong.id) ? (
                <button className="secondary" onClick={() => handleCancel(ong.id)}>
                  Cancelar inscrição
                </button>
              ) : (
                <button onClick={() => handleSubscribe(ong.id)}>Inscrever-se</button>
              )}
            </article>
          ))
        ) : (
          <p className="empty-state">
            {searchTerm.trim()
              ? 'Nenhuma ONG encontrada para essa busca.'
              : 'Nenhuma ONG cadastrada.'}
          </p>
        )}
      </section>
    </>
  )
}
