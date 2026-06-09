const API_URL = 'http://localhost:5000/api'

export async function buscarOngs() {
  const resposta = await fetch(`${API_URL}/ongs`)

  if (!resposta.ok) {
    throw new Error('Erro ao buscar ONGs')
  }

  return resposta.json()
}
