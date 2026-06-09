import { Link } from 'react-router-dom'

export default function NotFoundPage() {
  return (
    <section className="panel">
      <h1>Página não encontrada</h1>
      <p>A rota que você tentou acessar não existe.</p>
      <p>
        <Link to="/">Voltar para a página inicial</Link>
      </p>
    </section>
  )
}
