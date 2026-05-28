import { useEffect, useState } from 'react'

function Home() {
  const [unidades, setUnidades] = useState([])
  const [carregando, setCarregando] = useState(true)
  const [erro, setErro] = useState('')

  useEffect(() => {
    fetch('http://localhost:5000/api/unidades')
      .then((resposta) => {
        if (!resposta.ok) {
          throw new Error('Erro ao buscar unidades')
        }

        return resposta.json()
      })
      .then((dados) => {
        setUnidades(dados)
        setErro('')
      })
      .catch(() => {
        setErro('Nao foi possivel carregar as unidades')
      })
      .finally(() => {
        setCarregando(false)
      })
  }, [])

  return (
    <main className="pagina">
      <section className="topo">
        <h1>HemoLife</h1>
        <p>Unidades cadastradas no sistema</p>
      </section>

      {carregando && <p>Carregando unidades...</p>}
      {erro && <p className="erro">{erro}</p>}

      <section className="lista">
        {unidades.map((unidade) => (
          <article className="unidade" key={unidade.id}>
            <h2>{unidade.nome}</h2>
            <p>Telefone: {unidade.telefone}</p>
            <p>Endereco: {unidade.endereco}</p>
          </article>
        ))}
      </section>
    </main>
  )
}

export default Home
