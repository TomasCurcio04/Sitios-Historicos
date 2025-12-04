const API_BASE = (import.meta.env.VITE_API_URL || 'https://admin-grupo10.proyecto2025.linti.unlp.edu.ar') + '/api/feature-flags'

/**
 * Obtiene el estado del portal público
 * @returns {Promise<{enabled: boolean, maintenance_message?: string}>}
 */
export async function getPortalStatus() {
  try {
    // Primero probar endpoint de test
    const testResponse = await fetch(`${API_BASE}/test`, {
      method: 'GET',
      mode: 'cors'
    })


    const response = await fetch(`${API_BASE}/portal-status`, {
      method: 'GET',
      mode: 'cors'
    })


    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`)
    }

    const text = await response.text()

    return JSON.parse(text)
  } catch (error) {
    console.error('getPortalStatus error:', error)
    throw error
  }
}

/**
 * Obtiene el estado de las reseñas
 * @returns {Promise<{enabled: boolean}>}
 */
export async function getReviewsStatus() {
  try {
    const response = await fetch(`${API_BASE}/reviews-status`, {
      method: 'GET',
      mode: 'cors'
    })
    if (!response.ok) {
      throw new Error('Error al obtener estado de reseñas')
    }
    return await response.json()
  } catch (error) {
    console.error('Error fetching reviews status:', error)
    // En caso de error, asumir que las reseñas están habilitadas
    return { enabled: true }
  }
}