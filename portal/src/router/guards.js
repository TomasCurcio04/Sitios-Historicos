import { getPortalStatus } from '../services/featureFlags.js'

/**
 * Guard que verifica si el portal está en mantenimiento
 * @param {Object} to - Ruta de destino
 * @param {Object} from - Ruta de origen
 * @param {Function} next - Función para continuar la navegación
 */
export async function checkPortalMaintenance(to, from, next) {
  if (to.name === 'maintenance') {
    next()
    return
  }

  try {
    const status = await getPortalStatus()
    
    if (!status.enabled) {
      next({ name: 'maintenance' })
    } else {
      next()
    }
  } catch (error) {
    console.error('Portal status check failed:', error)
    next({ name: 'maintenance' })
  }
}