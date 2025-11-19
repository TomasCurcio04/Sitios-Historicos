const API_BASE = 'http://localhost:5000/api/feature-flags'

/**
 * Obtiene el estado del portal público
 * @returns {Promise<{enabled: boolean, maintenance_message?: string}>}
 */
export async function getPortalStatus() {
  try {
    console.log('Consultando:', `${API_BASE}/portal-status`)
    const response = await fetch(`${API_BASE}/portal-status`, {
      method: 'GET',
      mode: 'cors',
      credentials: 'include'
    })
    console.log('Response status:', response.status)
    if (!response.ok) {
      const text = await response.text()
      console.log('Response text:', text)
      throw new Error(`HTTP ${response.status}: ${text}`)
    }
    const data = await response.json()
    console.log('Respuesta del servidor:', data)
    return data
  } catch (error) {
    console.error('Error fetching portal status:', error)
    return { enabled: true, maintenance_message: null }
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
      mode: 'cors',
      credentials: 'include'
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