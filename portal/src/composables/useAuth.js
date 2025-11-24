import { ref, onMounted } from 'vue'

const API_URL = import.meta.env.VITE_API_URL || 'https://admin-grupo10.proyecto2025.linti.unlp.edu.ar'
console.log("API_URL:", API_URL)
const loggedIn = ref(false)
const user = ref(null)
const loading = ref(true)


/**
 * Verifica el estado de la sesión con el backend
 */
const checkSession = async () => {
  loading.value = true

  try {
    const res = await fetch(`${API_URL}/google/status`, {
      credentials: 'include'
    })

    let data = {}
    try {
      data = await res.json()
    } catch {
      data = {}
    }

    loggedIn.value = !!data.logged_in
    user.value = data.user ?? null
    
    // Si está logueado pero no tiene token JWT, obtenerlo
    if (loggedIn.value && !localStorage.getItem('auth_token')) {
      try {
        const tokenRes = await fetch(`${API_URL}/api/auth/token`, {
          method: 'POST',
          credentials: 'include'
        });
        if (tokenRes.ok) {
          const tokenData = await tokenRes.json();
          localStorage.setItem('auth_token', tokenData.access_token);
        }
      } catch (tokenErr) {
        console.error('Error obteniendo token:', tokenErr);
      }
    }

  } catch (err) {
    loggedIn.value = false
    user.value = null
  } finally {
    loading.value = false
  }
}


const login = (nextUrl) => {
  // Si nextUrl es un evento del DOM, ignorarlo
  const current = (typeof nextUrl === 'string' ? nextUrl : null) || window.location.href
  window.location.href = `${API_URL}/google/login?next=${encodeURIComponent(current)}`
}

const logout = async (eventOrUrl) => {
  try {
    await fetch(`${API_URL}/google/logout`, {
      method: 'GET',
      credentials: 'include'
    })
  } catch (e) {
    console.error('Error en logout backend', e)
  }

  loggedIn.value = false
  user.value = null

  localStorage.clear()
  sessionStorage.clear()

  const currentUrl =
    typeof eventOrUrl === 'string'
      ? eventOrUrl
      : window.location.pathname

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
