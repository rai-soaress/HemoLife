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
              <p>Gerencie ONGs e dados do sistema HemoLife.</p>
            </>
          ) : user.perfil === 'ong' ? (
            <>
              <p className="eyebrow">ONG</p>
              <h1>Painel da ONG</h1>
              <p>Acompanhe os doadores cadastrados na sua ONG.</p>
            </>
          ) : (
            <>
              <p className="eyebrow">Doador</p>
              <h1>Painel do Doador</h1>
              <p>Encontre ONGs, acompanhe inscricoes e marque exames.</p>
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
          </>
        ) : user.perfil === 'ong' ? (
          <Link className="action-card" to="/ong/painel">
            <strong>Ver cadastrados</strong>
            <span>Acesse a lista de doadores inscritos.</span>
          </Link>
        ) : (
          <>
            <Link className="action-card" to="/ongs">
              <strong>Ver ONGs</strong>
              <span>Encontre ONGs disponiveis e participe.</span>
            </Link>
            <Link className="action-card" to="/minhas-ongs">
              <strong>Minhas ONGs</strong>
              <span>Acompanhe suas inscricoes ativas.</span>
            </Link>
            <Link className="action-card" to="/exames">
              <strong>Marcar exames</strong>
              <span>Escolha unidade, data e horario.</span>
            </Link>
          </>
        )}
      </section>
    </>
  )
}
