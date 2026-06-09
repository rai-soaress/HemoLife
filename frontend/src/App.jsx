import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Header from './components/Header'
import { AuthProvider } from './contexts/AuthContext'
import { RequireAuth, RequireAdmin } from './components/RequireAuth'
import LandingPage from './pages/LandingPage'
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import HomePage from './pages/HomePage'
import OngsPage from './pages/OngsPage'
import MinhasOngsPage from './pages/MinhasOngsPage'
import AdminOngListPage from './pages/AdminOngListPage'
import AdminOngFormPage from './pages/AdminOngFormPage'
import NotFoundPage from './pages/NotFoundPage'

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Header />
        <main className="container">
          <Routes>
            <Route path="/" element={<LandingPage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/cadastrar" element={<RegisterPage />} />
            <Route path="/home" element={<RequireAuth><HomePage /></RequireAuth>} />
            <Route path="/ongs" element={<RequireAuth><OngsPage /></RequireAuth>} />
            <Route path="/minhas-ongs" element={<RequireAuth><MinhasOngsPage /></RequireAuth>} />
            <Route path="/admin/ongs" element={<RequireAdmin><AdminOngListPage /></RequireAdmin>} />
            <Route path="/admin/ongs/cadastrar" element={<RequireAdmin><AdminOngFormPage /></RequireAdmin>} />
            <Route path="/admin/ongs/editar/:id" element={<RequireAdmin><AdminOngFormPage /></RequireAdmin>} />
            <Route path="*" element={<NotFoundPage />} />
          </Routes>
        </main>
      </BrowserRouter>
    </AuthProvider>
  )
}
