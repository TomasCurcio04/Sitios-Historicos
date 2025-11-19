const API_BASE = 'http://localhost:5000/api'

async function handleFetch(res) {
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}))
    throw new Error(errorData.message || 'Error en la solicitud')
  }
  return res.json()
}

export async function fetchSites(params = {}) {
  try {
    const query = new URLSearchParams(params).toString()
    const res = await fetch(`${API_BASE}/sites?${query}`)
    const data = await handleFetch(res)
    return { success: true, data }
  } catch (error) {
    console.error('fetchSites error:', error)
    return { success: false, error: error.message }
  }
}

export async function fetchSiteById(id) {
  try {
    const res = await fetch(`${API_BASE}/sites/${id}`)
    const data = await handleFetch(res)
    return { success: true, data }
  } catch (error) {
    console.error('fetchSiteById error:', error)
    return { success: false, error: error.message }
  }
}

export async function addFavorite(id) {
  try {
    const res = await fetch(`${API_BASE}/favorites/${id}`, { method: 'POST' })
    await handleFetch(res)
    return { success: true }
  } catch (error) {
    console.error('addFavorite error:', error)
    return { success: false, error: error.message }
  }
}

export async function removeFavorite(id) {
  try {
    const res = await fetch(`${API_BASE}/favorites/${id}`, { method: 'DELETE' })
    await handleFetch(res)
    return { success: true }
  } catch (error) {
    console.error('removeFavorite error:', error)
    return { success: false, error: error.message }
  }
}

export async function isFavoriteSite(id) {
  try {
    const res = await fetch(`${API_BASE}/favorites/${id}`)
    const data = await handleFetch(res)
    return { success: true, data: data.is_favorite }
  } catch (error) {
    console.error('isFavoriteSite error:', error)
    return { success: false, error: error.message }
  }
}
