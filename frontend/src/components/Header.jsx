import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'

export default function Header() {
  const { user, loading, signOut } = useAuth()
  const navigate = useNavigate()

  async function handleLogout() {
    await signOut()
    navigate('/login')
  }

  return (
    <header className="topbar">
      <Link className="brand" to="/">
        HemoLife
      </Link>
      <nav>
        {!loading && (
          <>
            {user ? (
              <>
                {user.perfil === 'ong' ? (
                  <Link to="/ong/painel">Painel ONG</Link>
                ) : (
                  <Link to="/home">Home</Link>
                )}
                {user.perfil === 'doador' && (
                  <>
                    <Link to="/ongs">ONGs</Link>
                    <Link to="/minhas-ongs">Minhas ONGs</Link>
                    <Link to="/exames">Exames</Link>
                  </>
                )}
                {user.perfil === 'admin' && (
                  <Link to="/admin/ongs">Admin</Link>
                )}
                <button type="button" className="secondary" onClick={handleLogout}>
                  Sair
                </button>
              </>
            ) : (
              <>
                <Link to="/login">Login</Link>
                <Link to="/cadastrar">Cadastro</Link>
              </>
            )}
          </>
        )}
      </nav>
    </header>
  )
}
