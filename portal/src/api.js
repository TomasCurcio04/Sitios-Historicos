const API_BASE = 'http://localhost:5000/api'

export async function fetchSites(params = {}) {
  const query = new URLSearchParams(params).toString()
  const res = await fetch(`${API_BASE}/sites?${query}`)
  return res.json()
}

export async function fetchSiteById(id) {
  const res = await fetch(`${API_BASE}/sites/${id}`)
  return res.ok ? res.json() : null
}

export async function addFavorite(id) {
  return fetch(`${API_BASE}/favorites/${id}`, { method: 'POST' })
}

export async function removeFavorite(id) {
  return fetch(`${API_BASE}/favorites/${id}`, { method: 'DELETE' })
}

export async function isFavoriteSite(id) {
  const res = await fetch(`${API_BASE}/favorites/${id}`)
  const data = await res.json()
  return data.is_favorite
}
