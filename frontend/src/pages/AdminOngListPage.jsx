import { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { getAdminOngs, deleteAdminOng } from '../services/api'

export default function AdminOngListPage() {
  const [ongs, setOngs] = useState([])
  const [message, setMessage] = useState('')
  const [loading, setLoading] = useState(true)
  const navigate = useNavigate()

  useEffect(() => {
    loadAdminOngs()
  }, [])

  async function loadAdminOngs() {
    try {
      const data = await getAdminOngs()
      setOngs(data || [])
    } catch (error) {
      setMessage(error.data?.message || error.message || 'Erro ao carregar ONGs administrativas.')
    } finally {
      setLoading(false)
    }
  }

  async function handleDelete(id) {
    if (!window.confirm('Tem certeza que deseja excluir esta ONG?')) {
      return
    }

    try {
      const data = await deleteAdminOng(id)
      setMessage(data.message || 'ONG removida com sucesso.')
      await loadAdminOngs()
    } catch (error) {
      setMessage(error.data?.message || error.message || 'Erro ao excluir ONG.')
    }
  }

  return (
    <>
      <section className="page-heading admin-heading">
        <div>
          <h1>Administração de ONGs</h1>
          <p>Gerencie, edite e remova registros de ONGs diretamente daqui.</p>
        </div>
        <div>
          <Link className="button-link secondary-link" to="/admin/ongs/cadastrar">
            Nova ONG
          </Link>
        </div>
      </section>

      {message && <p className="flash flash-message">{message}</p>}

      {loading ? (
        <p className="empty-state">Carregando ONGs...</p>
      ) : ongs.length === 0 ? (
        <p className="empty-state">Nenhuma ONG cadastrada ainda.</p>
      ) : (
        <section className="card-list">
          {ongs.map((ong) => (
            <article className="list-card" key={ong.id}>
              <div>
                <h2>{ong.nome}</h2>
                <p>{ong.email}</p>
                <p className="muted">CNPJ: {ong.cnpj}</p>
              </div>
              <div className="card-actions">
                <button className="secondary" onClick={() => navigate(`/admin/ongs/editar/${ong.id}`)}>
                  Editar
                </button>
                <button className="delete" onClick={() => handleDelete(ong.id)}>
                  Excluir
                </button>
              </div>
            </article>
          ))}
        </section>
      )}
    </>
  )
}
