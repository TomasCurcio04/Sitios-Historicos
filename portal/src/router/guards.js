import { getPortalStatus } from '../services/featureFlags.js'

/**
 * Guard que verifica si el portal está en mantenimiento
 * @param {Object} to - Ruta de destino
 * @param {Object} from - Ruta de origen
 * @param {Function} next - Función para continuar la navegación
 */
export async function checkPortalMaintenance(to, from, next) {
  // Si ya estamos en la página de mantenimiento, permitir acceso
  if (to.name === 'maintenance') {
    next()
    return
  }

  try {
    const status = await getPortalStatus()
    
    if (!status.enabled) {
      // Portal en mantenimiento, redirigir a página de mantenimiento
      next({
        name: 'maintenance',
        query: { message: status.maintenance_message }
      })
    } else {
      // Portal disponible, continuar navegación
      next()
    }
  } catch (error) {
    console.error('Error checking portal status:', error)
    // En caso de error, permitir acceso (fail-safe)
    next()
  }
}