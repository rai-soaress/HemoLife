import { useState } from 'react'

import { buscarOngs } from '../services/api.js'

function Home() {
  const [ongs, setOngs] = useState([])
  const [carregando, setCarregando] = useState(false)
  const [erro, setErro] = useState('')
  const [buscou, setBuscou] = useState(false)

  async function carregarOngs() {
    setCarregando(true)
    setErro('')
    setBuscou(true)

    try {
      const dados = await buscarOngs()
      setOngs(dados)
    } catch {
      setOngs([])
      setErro('Nao foi possivel carregar as ONGs. Verifique se o Flask esta ligado.')
    } finally {
      setCarregando(false)
    }
  }

  return (
    <main className="pagina">
      <section className="topo">
        <h1>HemoLife</h1>
        <p>ONGs cadastradas no backend Flask</p>
        <button type="button" onClick={carregarOngs} disabled={carregando}>
          {carregando ? 'Carregando...' : 'Carregar ONGs'}
        </button>
      </section>

      {carregando && <p>Carregando ONGs...</p>}
      {erro && <p className="erro">{erro}</p>}
      {!carregando && !erro && buscou && ongs.length === 0 && (
        <p className="vazio">Nenhuma ONG cadastrada</p>
      )}

      <section className="lista">
        {ongs.map((ong) => (
          <article className="unidade" key={ong.id}>
            <h2>{ong.nome}</h2>
            <p>Email: {ong.email}</p>
            <p>CNPJ: {ong.cnpj}</p>
          </article>
        ))}
      </section>
    </main>
  )
}

export default Home
