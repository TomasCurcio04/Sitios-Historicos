import { ref, onMounted } from 'vue'

const API_URL = import.meta.env.VITE_API_URL || 'https://admin-grupo10.proyecto2025.linti.unlp.edu.ar'
const loggedIn = ref(false)
const user = ref(null)
const loading = ref(true)



const decodeJWT = (token) => {
  try {
    const parts = token.split('.')
    if (parts.length !== 3) return null
    const decoded = JSON.parse(atob(parts[1]))
    return decoded
  } catch (err) {
    console.error('Error decoding JWT:', err)
    return null
  }
}

/**
 * Verifica el estado de la sesión con el backend
 */
const checkSession = async () => {
  loading.value = true
  try {
    // Intentar obtener token del backend
    const tokenResp = await fetch(`${API_URL}/api/auth/token`, {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' }
    })

    if (tokenResp.ok) {
      const data = await tokenResp.json()
      const token = data?.access_token

      if (token) {
        // Guardar token en localStorage
        localStorage.setItem('auth_token', token)
        loggedIn.value = true

        // Decodificar JWT para obtener datos del usuario
        const decoded = decodeJWT(token)
        if (decoded) {
          user.value = {
            id: decoded.public_user_id,
            email: decoded.email,
            name: decoded.name,
            picture: decoded.picture
          }
        }
        return
      }
    }

    // Si no hay token disponible → limpiar
    loggedIn.value = false
    user.value = null
    localStorage.removeItem('auth_token')
  } catch (err) {
    console.warn('Error checking session:', err)
    loggedIn.value = false
    user.value = null
    localStorage.removeItem('auth_token')
  } finally {
    loading.value = false
  }
}



const login = (nextUrl) => {
  const current = (typeof nextUrl === 'string' ? nextUrl : null) || window.location.href
  window.location.href = `${API_URL}/google/login?next=${encodeURIComponent(current)}`

}

const logout = async (eventOrUrl) => {
  try {
    await fetch(`${API_URL}/google/logout`, { credentials: 'include' })
  } catch (err) {
    console.warn('Logout request failed', err)
  }
  localStorage.removeItem('token')
  localStorage.removeItem('auth_token')
  sessionStorage.clear()
  loggedIn.value = false
  user.value = null


  const currentUrl = typeof eventOrUrl === 'string' ? eventOrUrl : window.location.pathname
  window.location.href = currentUrl
}



export function useAuth() {
  onMounted(async () => {
    await checkSession()

  })

  return {
    loggedIn,
    user,
    loading,
    login,
    logout,
    checkSession
  }
}
