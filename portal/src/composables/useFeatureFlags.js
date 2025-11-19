import { ref, onMounted } from 'vue'
import { getPortalStatus, getReviewsStatus } from '../services/featureFlags.js'

/**
 * Composable para gestionar feature flags
 * @returns {Object} Estado y métodos para feature flags
 */
export function useFeatureFlags() {
  const portalEnabled = ref(true)
  const reviewsEnabled = ref(true)
  const maintenanceMessage = ref(null)
  const loading = ref(false)

  /**
   * Verifica el estado del portal
   */
  const checkPortalStatus = async () => {
    try {
      loading.value = true
      const status = await getPortalStatus()
      portalEnabled.value = status.enabled
      maintenanceMessage.value = status.maintenance_message
    } catch (error) {
      console.error('Error checking portal status:', error)
      // En caso de error, asumir que está disponible
      portalEnabled.value = true
      maintenanceMessage.value = null
    } finally {
      loading.value = false
    }
  }

  /**
   * Verifica el estado de las reseñas
   */
  const checkReviewsStatus = async () => {
    try {
      const status = await getReviewsStatus()
      reviewsEnabled.value = status.enabled
    } catch (error) {
      console.error('Error checking reviews status:', error)
      // En caso de error, asumir que están habilitadas
      reviewsEnabled.value = true
    }
  }

  /**
   * Verifica todos los feature flags
   */
  const checkAllFlags = async () => {
    await Promise.all([
      checkPortalStatus(),
      checkReviewsStatus()
    ])
  }

  // Verificar flags al montar el componente
  onMounted(() => {
    checkAllFlags()
  })

  return {
    // Estado
    portalEnabled,
    reviewsEnabled,
    maintenanceMessage,
    loading,
    
    // Métodos
    checkPortalStatus,
    checkReviewsStatus,
    checkAllFlags
  }
}