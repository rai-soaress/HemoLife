import { useEffect, useState } from 'react'
import { cancelExame, createExame, getExames } from '../services/api'

const HORARIOS = ['08:00', '09:00', '10:00', '11:00', '14:00', '15:00', '16:00']

export default function ExamesPage() {
  const [exames, setExames] = useState([])
  const [ongs, setOngs] = useState([])
  const [unidades, setUnidades] = useState([])
  const [ongId, setOngId] = useState('')
  const [unidadeId, setUnidadeId] = useState('')
  const [dataExame, setDataExame] = useState('')
  const [horario, setHorario] = useState(HORARIOS[0])
  const [message, setMessage] = useState('')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadExames()
  }, [])

  async function loadExames() {
    try {
      const data = await getExames()
      setExames(data.exames || [])
      setOngs(data.ongs || [])
      setUnidades(data.unidades || [])
      if (!ongId && data.ongs?.length) {
        setOngId(String(data.ongs[0].id))
      }
      if (!unidadeId && data.unidades?.length) {
        setUnidadeId(String(data.unidades[0].id))
      }
    } catch (error) {
      setMessage(error.data?.message || error.message || 'Erro ao carregar exames.')
    } finally {
      setLoading(false)
    }
  }

  async function handleSubmit(event) {
    event.preventDefault()
    setMessage('')

    try {
      const data = await createExame({
        ong_id: ongId,
        unidade_id: unidadeId,
        data_exame: dataExame,
        horario,
      })
      setMessage(data.message || 'Exame agendado com sucesso.')
      setDataExame('')
      await loadExames()
    } catch (error) {
      setMessage(error.data?.message || error.message || 'Erro ao agendar exame.')
    }
  }

  async function handleCancel(id) {
    try {
      const data = await cancelExame(id)
      setMessage(data.message || 'Exame cancelado com sucesso.')
      await loadExames()
    } catch (error) {
      setMessage(error.data?.message || error.message || 'Erro ao cancelar exame.')
    }
  }

  return (
    <>
      <section className="page-heading">
        <div>
          <h1>Exames</h1>
          <p>Agende exames por uma ONG em que voce ja esta inscrito.</p>
        </div>
      </section>

      {message && <p className="flash flash-message">{message}</p>}

      <section className="panel form-panel">
        <h2>Novo agendamento</h2>
        {ongs.length === 0 && (
          <p className="empty-state">Inscreva-se em uma ONG antes de marcar exames.</p>
        )}
        <form onSubmit={handleSubmit}>
          <label htmlFor="ong">ONG</label>
          <select
            id="ong"
            value={ongId}
            onChange={(event) => setOngId(event.target.value)}
            required
            disabled={ongs.length === 0}
          >
            {ongs.map((ong) => (
              <option key={ong.id} value={ong.id}>
                {ong.nome}
              </option>
            ))}
          </select>

          <label htmlFor="unidade">Unidade</label>
          <select
            id="unidade"
            value={unidadeId}
            onChange={(event) => setUnidadeId(event.target.value)}
            required
            disabled={unidades.length === 0}
          >
            {unidades.map((unidade) => (
              <option key={unidade.id} value={unidade.id}>
                {unidade.nome} - {unidade.endereco}
              </option>
            ))}
          </select>

          <label htmlFor="data_exame">Data</label>
          <input
            id="data_exame"
            type="date"
            value={dataExame}
            onChange={(event) => setDataExame(event.target.value)}
            required
          />

          <label htmlFor="horario">Horario</label>
          <select id="horario" value={horario} onChange={(event) => setHorario(event.target.value)} required>
            {HORARIOS.map((item) => (
              <option key={item} value={item}>
                {item}
              </option>
            ))}
          </select>

          <button type="submit" disabled={ongs.length === 0 || unidades.length === 0}>
            Agendar exame
          </button>
        </form>
      </section>

      <section className="page-heading">
        <div>
          <h1>Meus exames</h1>
          <p>Acompanhe seus agendamentos.</p>
        </div>
      </section>

      {loading ? (
        <p className="empty-state">Carregando exames...</p>
      ) : exames.length === 0 ? (
        <p className="empty-state">Voce ainda nao marcou nenhum exame.</p>
      ) : (
        <section className="card-list">
          {exames.map((exame) => (
            <article className="list-card" key={exame.id}>
              <div>
                <h2>{exame.unidade.nome}</h2>
                <p>{exame.data_exame} as {exame.horario}</p>
                <p className="muted">
                  ONG: {exame.ong.nome} | {exame.unidade.endereco} | Status: {exame.status}
                </p>
              </div>
              {exame.status !== 'cancelado' && (
                <button className="secondary" onClick={() => handleCancel(exame.id)}>
                  Cancelar
                </button>
              )}
            </article>
          ))}
        </section>
      )}
    </>
  )
}
