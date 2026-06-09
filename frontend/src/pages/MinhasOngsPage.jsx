import { useEffect, useState } from 'react'
import { getMyOngs, cancelSubscription } from '../services/api'

export default function MinhasOngsPage() {
  const [ongs, setOngs] = useState([])
  const [message, setMessage] = useState('')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadMinhasOngs()
  }, [])

  async function loadMinhasOngs() {
    try {
      const data = await getMyOngs()
      setOngs(data.ongs || [])
    } catch (error) {
      setMessage(error.data?.message || error.message || 'Erro ao carregar suas ONGs.')
    } finally {
      setLoading(false)
    }
  }

  async function handleCancel(id) {
    try {
      const data = await cancelSubscription(id)
      setMessage(data.message || 'Inscrição cancelada com sucesso.')
      await loadMinhasOngs()
    } catch (error) {
      setMessage(error.data?.message || error.message || 'Erro ao cancelar inscrição.')
    }
  }

  return (
    <>
      <section className="page-heading">
        <h1>Minhas ONGs</h1>
        <p>Veja suas inscrições ativas e cancele quando quiser.</p>
      </section>

      {message && <p className="flash flash-message">{message}</p>}

      {loading ? (
        <p className="empty-state">Carregando suas ONGs...</p>
      ) : ongs.length === 0 ? (
        <p className="empty-state">Você ainda não está inscrito em nenhuma ONG.</p>
      ) : (
        <section className="card-list">
          {ongs.map((ong) => (
            <article className="list-card" key={ong.id}>
              <div>
                <h2>{ong.nome}</h2>
                <p>{ong.email}</p>
                <p className="muted">CNPJ: {ong.cnpj}</p>
              </div>
              <button className="secondary" onClick={() => handleCancel(ong.id)}>
                Cancelar inscrição
              </button>
            </article>
          ))}
        </section>
      )}
    </>
  )
}
