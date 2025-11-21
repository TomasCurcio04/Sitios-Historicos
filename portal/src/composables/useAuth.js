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

    const data = await res.json()

    loggedIn.value = data.logged_in
    user.value = data.user
  } catch (error) {
    console.error('Error verificando la sesión:', error)
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

const logout = (nextUrl) => {
  const current = nextUrl || window.location.href
  window.location.href = `${API_URL}/google/logout?next=${encodeURIComponent(current)}`
}

export function useAuth() {
  onMounted(async () => {
  await checkSession()

  if (loggedIn.value) {
    await saveToken()
  }
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
