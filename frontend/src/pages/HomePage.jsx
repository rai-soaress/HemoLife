import { Link } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'

export default function HomePage() {
  const { user } = useAuth()

  if (!user) {
    return <div className="container">Carregando...</div>
  }

  return (
    <>
      <section className="hero">
        <div>
          {user.perfil === 'admin' ? (
            <>
              <p className="eyebrow">Admin</p>
              <h1>Painel Administrativo</h1>
              <p>Gerencie ONGs, inscrições e dados do sistema HemoLife.</p>
            </>
          ) : (
            <>
              <p className="eyebrow">Doador</p>
              <h1>Painel do Doador</h1>
              <p>Encontre ONGs e acompanhe suas inscrições.</p>
            </>
          )}
        </div>
      </section>

      <section className="grid-actions">
        {user.perfil === 'admin' ? (
          <>
            <Link className="action-card" to="/admin/ongs">
              <strong>Gerenciar ONGs</strong>
              <span>Cadastre, edite e remova ONGs.</span>
            </Link>
            <Link className="action-card" to="/admin/ongs/cadastrar">
              <strong>Cadastrar ONG</strong>
              <span>Adicione uma nova ONG ao sistema.</span>
            </Link>
            <Link className="action-card" to="/ongs">
              <strong>Ver ONGs públicas</strong>
              <span>Confira a listagem disponível para doadores.</span>
            </Link>
          </>
        ) : (
          <>
            <Link className="action-card" to="/ongs">
              <strong>Ver ONGs</strong>
              <span>Encontre ONGs disponíveis e participe.</span>
            </Link>
            <Link className="action-card" to="/minhas-ongs">
              <strong>Minhas ONGs</strong>
              <span>Acompanhe suas inscrições ativas.</span>
            </Link>
          </>
        )}
      </section>
    </>
  )
}
