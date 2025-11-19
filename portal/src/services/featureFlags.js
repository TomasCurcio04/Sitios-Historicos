const API_BASE = `${API_SERVER}/api/feature-flags`

/**
 * Obtiene el estado del portal público
 * @returns {Promise<{enabled: boolean, maintenance_message?: string}>}
 */
export async function getPortalStatus() {
  try {
    const response = await fetch(`${API_BASE}/portal-status`)
    if (!response.ok) {
      throw new Error('Error al obtener estado del portal')
    }
    return await response.json()
  } catch (error) {
    console.error('Error fetching portal status:', error)
    // En caso de error, asumir que el portal está disponible
    return { enabled: true, maintenance_message: null }
  }
}

/**
 * Obtiene el estado de las reseñas
 * @returns {Promise<{enabled: boolean}>}
 */
export async function getReviewsStatus() {
  try {
    const response = await fetch(`${API_BASE}/reviews-status`)
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