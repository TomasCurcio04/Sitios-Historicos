import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:5000/api',
  headers: { 'Content-Type': 'application/json' },
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
  }
};
