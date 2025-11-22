import { ref, onMounted } from 'vue'

const API_URL = import.meta.env.VITE_API_URL || ''
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

  } catch (err) {
    loggedIn.value = false
    user.value = null
  } finally {
    loading.value = false
  }
}


const login = (nextUrl) => {
  const current = nextUrl || window.location.href
  window.location.href = `${API_URL}/google/login?next=${encodeURIComponent(current)}`
}

const logout = async (nextUrl) => {
  try {
    await fetch(`${API_URL}/google/logout`, {
      method: 'GET',
      credentials: 'include'
    })
  } catch (e) {
    console.error('Error en logout backend', e)
  }

  // LIMPIEZA TOTAL FRONTEND
  loggedIn.value = false
  user.value = null

  localStorage.clear()
  sessionStorage.clear()

  // Si usas caches
  if ('caches' in window) {
    const names = await caches.keys()
    await Promise.all(names.map(n => caches.delete(n)))
  }

  const current = nextUrl || window.location.href
  window.location.href = current
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
