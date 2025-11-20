<template>
  <div>
    <SearchHero @search="goToSearch" />

    <SectionCarousel
      title="Más visitados"
      :fetchFn="fetchMostVisited"
      :queryParams="{ order_by: 'most-visited'}"
    />

    <SectionCarousel
      title="Mejor puntuados"
      :fetchFn="fetchTopRated"
      :queryParams="{ order_by: 'rating-5-1' }"
    />

    <SectionCarousel
      v-if="isLoggedIn"
      title="Favoritos"
      :fetchFn="fetchFavorites"
      :queryParams="{ filter: 'favorites' }"
    />

    <SectionCarousel
      title="Recientemente agregados"
      :fetchFn="fetchRecent"
      :queryParams="{ order: 'latest' }"
    />
  </div>
</template>

<script>
import SectionCarousel from '../components/SectionCarousel.vue'
import SearchHero from '../components/SearchHero.vue'
import { fetchSites } from '../api.js'

export default {
  name: 'HomePage',

  components: { SectionCarousel, SearchHero },

  setup() {
    const isLoggedIn = !!localStorage.getItem('auth_token')

    // Adaptamos las funciones de fetch
    const fetchMostVisited = async (params) => {
      const result = await fetchSites({ order: 'most_visited', limit: 4, ...params })
      return result.success ? result.data : []
    }

    const fetchTopRated = async (params) => {
      const result = await fetchSites({ order: 'top_rated', limit: 4, ...params })
      return result.success ? result.data : []
    }

    const fetchFavorites = async (params) => {
      const result = await fetchSites({ filter: 'favorites', limit: 4, ...params })
      return result.success ? result.data : []
    }

    const fetchRecent = async (params) => {
      const result = await fetchSites({ order: 'recent', limit: 4, ...params })
      return result.success ? result.data : []
    }

    function goToSearch(q) {
      window.location.href = `/sites?q=${encodeURIComponent(q)}`
    }

    return {
      isLoggedIn,
      fetchMostVisited,
      fetchTopRated,
      fetchFavorites,
      fetchRecent,
      goToSearch,
    }
  },
}
</script>
