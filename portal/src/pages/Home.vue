<template>
  <main class="min-h-screen bg-gray-50">

    <div class="max-w-7xl mx-auto px-4 py-12 space-y-16">

      <SectionCarousel
        title="🔥 Los más visitados"
        :fetchFn="fetchMostVisitedFromApi"
        :queryParams="{ order_by: 'most-visited' }"
      />

      <SectionCarousel
        title="⭐ Mejor puntuados"
        :fetchFn="fetchTopRatedFromApi"
        :queryParams="{ order_by: 'rating-5-1' }"
      />

      <SectionCarousel
        title="🆕 Recientemente agregados"
        :fetchFn="fetchRecentFromApi"
        :queryParams="{ order_by: 'latest' }"
      />
      <SectionCarousel
        v-if="loggedIn"
        title="❤️ Favoritos"
        :fetchFn="fetchFavoritesFromApi"
        :queryParams="{ search_favorites:true }"
      />

      </div>
  </main>
</template>

<script setup>
import SectionCarousel from '../components/SectionCarousel.vue';
import { useApi } from '@/composables/useApi.js'
import { watch } from 'vue'
import { useAuth } from '@/composables/useAuth.js'

    const api = useApi()
    
  const { loggedIn } = useAuth()

    const fetchMostVisitedFromApi = (params = {}) => {
      return api.getSites({
        ...params,
        order_by: 'most-visited',
        per_page: 4
      })
    }

    const fetchTopRatedFromApi = (params = {}) => {
      return api.getSites({
        ...params,
        order_by: 'rating-5-1',
        per_page: 4
      })
    }

    const fetchRecentFromApi = (params = {}) => {
      return api.getSites({
        ...params,
        order_by: 'latest',
        per_page: 4
      })
    }

    const fetchFavoritesFromApi = (params = {}) => {
      return api.getSites({
        ...params,
        search_favorites: true,
        per_page: 4
      })
    }
watch(loggedIn, async (isLoggedIn) => {
    }, { immediate: true });
</script>
