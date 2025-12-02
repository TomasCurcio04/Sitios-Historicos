import { ref, onMounted } from 'vue'

const API_URL = import.meta.env.VITE_API_URL || 'https://admin-grupo10.proyecto2025.linti.unlp.edu.ar'
console.log("API_URL:", API_URL)
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
    const params = new URLSearchParams(window.location.search)
    const tokenFromUrl = params.get('auth_token')
    
    if (tokenFromUrl) {
      localStorage.setItem('auth_token', tokenFromUrl)
      window.history.replaceState({}, document.title, window.location.pathname)
      loggedIn.value = true
      
      // Decodificar JWT para obtener datos del usuario
      const decoded = decodeJWT(tokenFromUrl)
      if (decoded) {
        user.value = {
          id: decoded.public_user_id,
          email: decoded.email,
          name: decoded.name,
          picture: decoded.picture
        }
      }
    } else {
      const token = localStorage.getItem('auth_token')
      if (token) {
        loggedIn.value = true
        const decoded = decodeJWT(token)
        if (decoded) {
          user.value = {
            id: decoded.public_user_id,
            email: decoded.email,
            name: decoded.name,
            picture: decoded.picture
          }
        }
      } else {
        loggedIn.value = false
        user.value = null
      }
    }
  } catch (err) {
    console.warn('Error checking session:', err)
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
    await fetch(`${API_URL}/google/logout`)
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
