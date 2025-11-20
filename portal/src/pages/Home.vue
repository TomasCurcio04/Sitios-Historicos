<template>
  <main>
    <SearchHero @search="goToSearch" />

    <div v-if="hasSearched" class="mt-8">
      <h2 class="text-xl mb-4">Resultados de búsqueda</h2>

      <div v-if="searchResults.length > 0" class="sites-grid">
        <div v-for="site in searchResults" :key="site.id" class="site-card">
          <img
            v-if="site.cover_image"
            :src="`http://minio.proyecto2025.linti.unlp.edu.ar/grupo10/${site.cover_image}`"
            :alt="site.name"
            class="cover-image"
          />
          <span v-else style="font-size: 0.8rem; color: #888;">Sin imagen</span>

          <div class="card-header">
            <h2 class="card-title">{{ site.name }}</h2>
          </div>

          <div class="card-body">
            <div class="card-info">
              <span class="label">Ciudad:</span>
              <span class="value">{{ site.city }}</span>
            </div>
            <div class="card-info">
              <span class="label">Provincia:</span>
              <span class="value">{{ site.province }}</span>
            </div>
            <div>
              <span class="label">Tags:</span>
              <span class="value">{{ site.tags.join(', ') }}</span>
            </div>
          </div>
        </div>
      </div>

      <div v-else>
        No se encontraron sitios con ese nombre.
      </div>
    </div>

    <!-- Secciones del Home -->
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
  </main>
</template>

<script>
import SectionCarousel from '../components/SectionCarousel.vue'
import SearchHero from '../components/SearchHero.vue'
import api from '../Services/api.js'  

export default {
  name: 'HomePage',
  components: { SectionCarousel, SearchHero },
  data() {
    return {
      isLoggedIn: !!localStorage.getItem('auth_token'),
      searchResults: [],
      hasSearched: false
    }
  },
  methods: {
    async buscarSitio(q) {
      try {
        this.hasSearched = true
        const params = { search: q, per_page: 20, page: 1 }
        const res = await api.getSites(params)
        this.searchResults = res.data.data
      } catch (err) {
        console.error("Error buscando sitio:", err)
      }
    },
    goToSearch(q) {
      this.buscarSitio(q)
    }
  }
}
</script>
