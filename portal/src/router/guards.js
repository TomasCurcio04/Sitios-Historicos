import { getPortalStatus } from '../services/featureFlags.js'

/**
 * Guard que verifica si el portal está en mantenimiento
 * @param {Object} to - Ruta de destino
 * @param {Object} from - Ruta de origen
 * @param {Function} next - Función para continuar la navegación
 */
export async function checkPortalMaintenance(to, from, next) {
  console.log('Guard ejecutándose para:', to.name)
  
  if (to.name === 'maintenance') {
    next()
    return
  }

  try {
    const status = await getPortalStatus()
    console.log('Status del portal:', status)
    
    if (!status.enabled) {
      console.log('Redirigiendo a mantenimiento')
      next({
        name: 'maintenance',
        query: { message: status.maintenance_message }
      })
    } else {
      next()
    }
  } catch (error) {
    console.error('Error checking portal status:', error)
    next()
  }
}