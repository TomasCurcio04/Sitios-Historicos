import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://localhost:5000/api',
  headers: { 'Content-Type': 'application/json' },
  withCredentials: true
});

apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth_token'); // donde guardes el token
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});


export default {
  getSites(params) {
    return apiClient.get('/sites',{ params });
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
  getMyFavorites(params) {
    return apiClient.get('/me/favorites', { params });
  },
  getToken() {
    return apiClient.post('/auth/token', {});
  }
};
