<template>
  <div>
    <SearchHero @search="goToSearch" />

    <SectionCarousel
      title="Más visitados"
      :fetchFn="fetchMostVisited"
      :queryParams="{ order: 'most_visited' }"
    />

    <SectionCarousel
      title="Mejor puntuados"
      :fetchFn="fetchTopRated"
      :queryParams="{ order: 'top_rated' }"
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
      :queryParams="{ order: 'recent' }"
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

    const fetchMostVisited = (params) => fetchSites({ order: 'most_visited', limit: 4, ...params })

    const fetchTopRated = (params) => fetchSites({ order: 'top_rated', limit: 4, ...params })

    const fetchFavorites = (params) => fetchSites({ filter: 'favorites', limit: 4, ...params })

    const fetchRecent = (params) => fetchSites({ order: 'recent', limit: 4, ...params })

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
