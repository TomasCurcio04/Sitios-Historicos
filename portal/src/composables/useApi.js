import axios from 'axios'

const apiClient = axios.create({
  baseURL: (import.meta.env.VITE_API_URL || 'https://admin-grupo10.proyecto2025.linti.unlp.edu.ar') + '/api',
  headers: { 'Content-Type': 'application/json' },
  withCredentials: true
})

apiClient.interceptors.response.use(
  (response) => response,

  (error) => {
    if (error.response && error.response.status === 401) {
      const message = error.response?.data?.error?.message

      if (
        message === "Token expired" ||
        message === "Authentication required"
      ) {
        console.warn("Sesión expirada o inválida, cerrando sesión...")

        localStorage.removeItem('auth_token')
        localStorage.removeItem('token')
        sessionStorage.clear()

        window.location.href = "/login"
      }
    }

    return Promise.reject(error)
  }
)

export function useApi() {
  const api = {
    getSites(params) {
      const config = { params }

      //Si search_favorites es true, agregar el token de autenticación en los headers
      if (params && params.search_favorites) {
        const token = localStorage.getItem('auth_token')
        if (token) {
          config.headers = {
            Authorization: `Bearer ${token}`
          }
        }
      }
      return apiClient.get('/sites', config)
    },
    getTags() {
      return apiClient.get('/metadata/tags')
    },
    getStates() {
      return apiClient.get('/metadata/states')
    },
    searchFilter(params) {
      return apiClient.get('/search/filter', { params })
    },
    getMyFavorites(params = {}) {
      const token = localStorage.getItem('auth_token')
      return apiClient.get('/me/favorites', {
        params,
        headers: {
          Authorization: `Bearer ${token}`
        }
      })
    },
    // getToken() {
    //   return apiClient.post('/auth/token', {})
    //     .then(res => {
    //       const token = res.data.access_token
    //       localStorage.setItem('token', token)
    //       return token
    //     })
    // },
    getMyReviews(params = {}) {
      const token = localStorage.getItem('auth_token')
      return apiClient.get('/me/reviews', {
        params,
        headers: {
          Authorization: `Bearer ${token}`
        }
      })
    },
    createReview(siteId, reviewData) {
      const token = localStorage.getItem('auth_token')
      return apiClient.post(`/sites/${siteId}/reviews`, reviewData, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      })
    },
    getSiteReviews(siteId, params = {}) {
      return apiClient.get(`/sites/${siteId}/reviews`, { params });
    },
    getReviewsStatus() {
      return apiClient.get('/feature-flags/reviews-status');
    },

    updateReview(siteId, reviewId, reviewData) {
      const token = localStorage.getItem('auth_token')
      return apiClient.put(`/sites/${siteId}/reviews/${reviewId}`, reviewData, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      })
    },
    deleteReview(siteId, reviewId) {
      const token = localStorage.getItem('auth_token')
      return apiClient.delete(`/sites/${siteId}/reviews/${reviewId}`, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      })
    },
    deleteMyReview(siteId, reviewId) {
      return api.deleteReview(siteId, reviewId)
    },
    updateMyReview(siteId, reviewId, reviewData) {
      const token = localStorage.getItem('auth_token')
      return apiClient.put(`/sites/${siteId}/reviews/${reviewId}`, reviewData, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      })
    }
  }
  return api
};