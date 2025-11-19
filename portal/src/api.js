const API_BASE = 'http://localhost:5000/api'

async function handleFetch(res) {
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.message || 'Error en la solicitud');
  }
  return res.json();
}

export async function fetchSites(params = {}) {
  try {
    const query = new URLSearchParams(params).toString();
    const res = await fetch(`${API_BASE}/sites?${query}`);
    const data = await handleFetch(res);
    return { success: true, data };
  } catch (error) {
    console.error('fetchSites error:', error);
    return { success: false, error: error.message };
  }
}

export async function fetchSiteById(id) {
  try {
    // Agregamos el token si existe para que el backend calcule is_favorite
    const token = localStorage.getItem('auth_token');
    const headers = token ? { 'Authorization': `Bearer ${token}` } : {};

    const res = await fetch(`${API_BASE}/sites/${id}`, { headers });
    const data = await handleFetch(res);
    return { success: true, data };
  } catch (error) {
    console.error('fetchSiteById error:', error);
    return { success: false, error: error.message };
  }
}

export async function addFavorite(id) {
  try {
    const token = localStorage.getItem('auth_token');
    const res = await fetch(`${API_BASE}/sites/${id}/favorite`, { // Ajusté la URL al estándar REST usual, verifica tu backend
      method: 'POST',
      headers: { 'Authorization': `Bearer ${token}` }
    });
    await handleFetch(res);
    return { success: true };
  } catch (error) {
    console.error('addFavorite error:', error);
    return { success: false, error: error.message };
  }
}

export async function removeFavorite(id) {
  try {
    const token = localStorage.getItem('auth_token');
    const res = await fetch(`${API_BASE}/sites/${id}/favorite`, { // Ajusté la URL
      method: 'DELETE',
      headers: { 'Authorization': `Bearer ${token}` }
    });
    await handleFetch(res);
    return { success: true };
  } catch (error) {
    console.error('removeFavorite error:', error);
    return { success: false, error: error.message };
  }
}

export async function isFavoriteSite(id) {
  try {
    const token = localStorage.getItem('auth_token');
    const res = await fetch(`${API_BASE}/favorites/${id}`, {
        headers: { 'Authorization': `Bearer ${token}` }
    });
    const data = await handleFetch(res);
    return { success: true, data: data.is_favorite };
  } catch (error) {
    console.error('isFavoriteSite error:', error);
    return { success: false, error: error.message };
  }
}

// --- NUEVAS FUNCIONES NECESARIAS PARA DETAIL.VUE ---

export function isAuthenticated() {
    return !!localStorage.getItem('auth_token');
}

export function loginWithGoogle() {
    window.location.href = `${API_BASE}/auth/login/google`;
}

// --- EXPORT DEFAULT PARA COMPATIBILIDAD ---
export default {
    fetchSites,
    fetchSiteById,
    addFavorite,
    removeFavorite,
    isFavoriteSite,
    isAuthenticated,
    loginWithGoogle
};
