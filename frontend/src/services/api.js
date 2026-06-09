const BASE_URL = import.meta.env.VITE_API_BASE_URL || '';

async function apiFetch(path, options = {}) {
  const response = await fetch(`${BASE_URL}${path}`, {
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers || {}),
    },
    ...options,
  });

  const data = await response.json().catch(() => null);

  if (!response.ok) {
    const errorMessage = response.status === 401
      ? data?.message || 'Acesso não autorizado. Faça login.'
      : data?.message || 'Erro de rede';
    const error = new Error(errorMessage);
    error.status = response.status;
    error.data = data;
    throw error;
  }

  return data;
}

export function getSession() {
  return apiFetch('/usuarios/session');
}

export function login(email, senha) {
  return apiFetch('/usuarios/login', {
    method: 'POST',
    body: JSON.stringify({ email, senha }),
  });
}

export function register(nome, email, senha, perfil, tipo_sanguineo) {
  return apiFetch('/usuarios/cadastrar', {
    method: 'POST',
    body: JSON.stringify({ nome, email, senha, perfil, tipo_sanguineo }),
  });
}

export function logout() {
  return apiFetch('/usuarios/logout', { method: 'POST' });
}

export function getOngs() {
  return apiFetch('/usuarios/ongs');
}

export function subscribeOng(id) {
  return apiFetch(`/usuarios/ongs/inscrever/${id}`, { method: 'POST' });
}

export function cancelSubscription(id) {
  return apiFetch(`/usuarios/ongs/cancelar/${id}`, { method: 'POST' });
}

export function getMyOngs() {
  return apiFetch('/usuarios/minhas-ongs');
}

export function getAdminOngs() {
  return apiFetch('/usuarios/admin/ongs');
}

export function createAdminOng(payload) {
  return apiFetch('/usuarios/admin/ongs/cadastrar', {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

export function getAdminOng(id) {
  return apiFetch(`/usuarios/admin/ongs/${id}`);
}

export function updateAdminOng(id, payload) {
  return apiFetch(`/usuarios/admin/ongs/${id}`, {
    method: 'PUT',
    body: JSON.stringify(payload),
  });
}

export function deleteAdminOng(id) {
  return apiFetch(`/usuarios/admin/ongs/${id}`, {
    method: 'DELETE',
  });
}
