import axios from 'axios';

const apiClient = axios.create({
  baseURL: (import.meta.env.VITE_API_URL || 'http://localhost:5000') + '/api',
  headers: { 'Content-Type': 'application/json' },
  withCredentials: true
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
  getMyFavorites(params = {}) {
    const token = localStorage.getItem('auth_token');

    return apiClient.get('/me/favorites', {
      params,
      headers: {
        Authorization: `Bearer ${token}`
      }
    });
  }, 
  getToken() {
    return apiClient.post('/auth/token', {})
      .then(res => {
        const token = res.data.access_token;
        localStorage.setItem('auth_token', token);
        return token;
      });
  }
};
