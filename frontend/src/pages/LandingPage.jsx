import { Link } from 'react-router-dom'

export default function LandingPage() {
  return (
    <section className="hero landing">
      <div>
        <p className="eyebrow">Doação de sangue e conexão social</p>
        <h1>HemoLife</h1>
        <p>
          Uma plataforma simples para conectar doadores, administradores e ONGs em torno de campanhas de apoio.
        </p>
        <div className="hero-actions">
          <Link className="button-link" to="/login">
            Entrar
          </Link>
          <Link className="button-link secondary-link" to="/cadastrar">
            Cadastrar
          </Link>
        </div>
      </div>
    </section>
  )
}
