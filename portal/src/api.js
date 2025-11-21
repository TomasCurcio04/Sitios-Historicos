const API_BASE = 'http://localhost:5000/api'

async function handleFetch(res) {
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    // Si el backend devuelve un mensaje de error detallado, lo usamos
    const msg = errorData.error && errorData.error.message
                ? `${errorData.error.message}: ${JSON.stringify(errorData.error.details || '')}`
                : 'Error en la solicitud';
    throw new Error(msg);
  }
  return res.json();
}

export async function fetchSites(params = {}) {
  try {
    // --- TRADUCCIÓN DE PARÁMETROS (FRONT -> BACK) ---
    const apiParams = new URLSearchParams();

    // 1. Paginación: 'limit' -> 'per_page'
    if (params.limit) apiParams.append('per_page', params.limit);
    if (params.per_page) apiParams.append('per_page', params.per_page); // por si acaso
    if (params.page) apiParams.append('page', params.page);

    // 2. Búsqueda: 'q' -> 'search'
    if (params.q) apiParams.append('search', params.q);
    if (params.search) apiParams.append('search', params.search);

    // 3. Ordenamiento: 'order' -> 'order_by'
    // También mapeamos los valores incorrectos a los que espera marshmallow
    let orderValue = params.order || params.order_by;

    if (orderValue) {
        const orderMap = {
            'most_visited': 'most-visited', // Corrige el guion bajo
            'top_rated': 'rating-5-1',      // Mapea nombres amigables
            'latest': 'latest',
            'az': 'name-asc',
            'za': 'name-desc'
        };
        // Si existe en el mapa usamos ese, si no, enviamos lo que vino
        apiParams.append('order_by', orderMap[orderValue] || orderValue);
    }

    // Otros filtros directos
    if (params.city) apiParams.append('city', params.city);
    if (params.province) apiParams.append('province', params.province);
    if (params.tags) apiParams.append('tags', params.tags);

    // --- FIN TRADUCCIÓN ---

    const res = await fetch(`${API_BASE}/sites?${apiParams.toString()}`);
    const json = await handleFetch(res);

    // El backend devuelve directamente la lista o un objeto con data/meta?
    // Según tu schema SitesListResponseSchema, devuelve { data: [...], meta: {...} }
    // Adaptamos la respuesta para que el frontend siempre reciba { data: { items: [], total: 0 } }

    return {
        success: true,
        data: {
            items: json.data || [],
            total: json.meta ? json.meta.total : 0
        }
    };

  } catch (error) {
    console.error('fetchSites error:', error);
    return { success: false, error: error.message };
  }
}

export async function fetchSiteById(id) {
  try {
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
    const res = await fetch(`${API_BASE}/sites/${id}/favorite`, {
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
    const res = await fetch(`${API_BASE}/sites/${id}/favorite`, {
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

// --- FUNCIONES DE AUTH ---
export function isAuthenticated() {
    return !!localStorage.getItem('auth_token');
}

export function loginWithGoogle() {
    window.location.href = `${API_BASE}/auth/login/google`;
}

// --- FUNCIONES ESPECÍFICAS PARA EL HOME (Usando valores correctos) ---

export async function fetchMostVisited() {
    // Backend espera: 'most-visited'
    return fetchSites({ order: 'most-visited', limit: 4 });
}

export async function fetchTopRated() {
    // Backend espera: 'rating-5-1'
    return fetchSites({ order: 'rating-5-1', limit: 4 });
}

export async function fetchRecent() {
    // Backend espera: 'latest'
    return fetchSites({ order: 'latest', limit: 4 });
}

export async function fetchFavorites() {
    // Si tienes filtro de favoritos implementado
    return fetchSites({ search_favorites: true, limit: 4 });
}

export default {
    fetchSites,
    fetchSiteById,
    addFavorite,
    removeFavorite,
    isFavoriteSite,
    isAuthenticated,
    loginWithGoogle,
    fetchMostVisited,
    fetchTopRated,
    fetchRecent,
    fetchFavorites
};
