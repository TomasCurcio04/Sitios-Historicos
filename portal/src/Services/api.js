import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:5000/api',
  headers: { 'Content-Type': 'application/json' },
});

// Helper para obtener token desde localStorage (soporta string o JSON)
function getTokenFromStorage() {
  const raw = localStorage.getItem('token');
  if (!raw) return null;
  try {
    const parsed = JSON.parse(raw);
    // busca propiedades comunes
    return parsed?.token || parsed?.access_token || parsed?.auth_token || parsed;
  } catch {
    return raw;
  }
}

// Interceptor: añade Authorization si hay token
apiClient.interceptors.request.use(
  (config) => {
    const token = getTokenFromStorage();
    if (token) {
      config.headers = config.headers || {};
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

export default {
  getSites(params) {
    return apiClient.get('/sites', { params });
  },
  getTags() {
    return apiClient.get('/metadata/tags');
  },
  getStates() {
    return apiClient.get('/metadata/states');
  },
  searchFilter(params) {
    return apiClient.get('/search/filter', { params });
  },
  getMyFavorites({ page = 1 }) {
    // ya no hace falta pasar headers aquí, el interceptor añade Authorization
    return apiClient.get('/me/favorites', { params: { page } });
  }
}