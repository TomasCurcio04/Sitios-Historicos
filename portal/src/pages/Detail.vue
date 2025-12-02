<template>
  <div v-if="loading" class="loading-container">
    <div class="spinner"></div>
    <p>Cargando sitio histórico...</p>
  </div>

  <div v-else-if="error" class="error-container">
    <p>{{ error }}</p>
    <button @click="router.push('/sites')" class="btn-back">Volver al listado</button>
  </div>

  <div v-else class="detail-container">

    <header class="site-header">
      <div class="header-top">
        <button @click="goBack" class="back-btn">
          ← Volver
        </button>
      </div>

      <div class="hero-image">
        <img
          :src="resolveUrl(currentImage || site.cover_image)"
          :alt="site.name"
          @error="handleImageError"
        >
        <div class="hero-overlay">
          <h1>{{ site.name }}</h1>
          <div class="meta-badges">
            <span class="badge location">📍 {{ site.city }}, {{ site.province }}</span>
            <span class="badge status" :class="statusClass">{{ site.state_of_conservation }}</span>
          </div>
        </div>
      </div>

      <div class="gallery-thumbs" v-if="site.images && site.images.length > 0">
        <img
          v-for="img in site.images"
          :key="img.id"
          :src="resolveUrl(img.url)"
          :alt="img.title"
          class="thumb"
          :class="{ active: currentImage === img.url }"
          @click="currentImage = img.url"
          @error="handleThumbError"
        >
      </div>
    </header>

    <div class="content-grid">
      <div class="main-content">
        <div class="tags-list" v-if="site.tags && site.tags.length">
          <span v-for="tag in site.tags" :key="tag" class="tag-pill">#{{ tag }}</span>
        </div>
        <section class="description-section">
          <h3>Historia</h3>
          <div class="text-content" :class="{ collapsed: !expandedDesc }">
            {{ site.description }}
          </div>
          <button v-if="site.description && site.description.length > 300" @click="expandedDesc = !expandedDesc" class="link-btn">
            {{ expandedDesc ? 'Leer menos' : 'Leer más' }}
          </button>
        </section>
        <section class="map-section" v-show="site.lat && site.long">
          <h3>Ubicación</h3>
          <div id="map" class="map-container"></div>
        </section>

        <section class="reviews-section">
          <SiteReviewsList
            :reviews="siteReviews"
            :meta="reviewsMeta"
            :loading="reviewsLoading"
            @page-change="handleReviewsPageChange"
          />
        </section>
      </div>

      <aside class="reviews-sidebar">
        <div class="rating-card">
          <div class="rating-big">{{ site.average_rating || '0.0' }}</div>
          <div class="stars">
            <span v-for="n in 5" :key="n" :class="{ filled: n <= Math.round(site.average_rating || 0) }">★</span>
          </div>
          <div class="review-count">{{ site.reviews_count }} opiniones</div>
          <button @click="handleFavoriteClick" class="btn-fav" :class="{ active: site.is_favorite }">
            {{ site.is_favorite ? '❤️ Guardado en Favoritos' : '🤍 Marcar como Favorito' }}
          </button>
          <button @click="handleWriteReview" class="btn-review">
            ✏️ Escribir una reseña
          </button>
        </div>
      </aside>
    </div>

    <!-- Review Form Modal -->
    <ReviewForm
      v-if="showReviewForm"
      :site-id="site.id"
      :site-name="site.name"
      @submitted="onReviewSubmitted"
      @cancel="showReviewForm = false"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, computed, nextTick, onBeforeUnmount } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../api'
import { useApi } from '../composables/useApi'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import { useAuth } from '@/composables/useAuth'
import ReviewForm from '../components/ReviewForm.vue'
import SiteReviewsList from '../components/SiteReviewsList.vue'

const { loggedIn, login } = useAuth()
const { getSiteReviews } = useApi()

const props = defineProps({
  id: { type: [String, Number], required: true }
})

const route = useRoute()
const router = useRouter()
const placeholderImage = 'https://placehold.co/800x400?text=Sin+Imagen'

// Variables Reactivas
const site = ref(null)
const loading = ref(true)
const error = ref(null)
const currentImage = ref(null)
const expandedDesc = ref(false)
const map = ref(null)
const showReviewForm = ref(false)
const siteReviews = ref([])
const reviewsLoading = ref(false)
const reviewsMeta = ref(null)

// Computed
const statusClass = computed(() => {
  if (!site.value) return ''
  const status = site.value.state_of_conservation?.toLowerCase()
  if (['bueno', 'excelente', 'muy bueno'].includes(status)) return 'status-good'
  if (['regular'].includes(status)) return 'status-regular'
  return 'status-bad'
})

// --- NUEVA FUNCIÓN PARA RESOLVER URLS ---
// --- FUNCIÓN CORREGIDA PARA RESOLVER URLS ---
const resolveUrl = (url) => {
  // 1. Si es nulo, devuelve placeholder
  if (!url) return placeholderImage

  // 2. Si la URL ya viene completa (empieza con http), la usamos tal cual
  if (url.startsWith('http') || url.startsWith('https')) {
    return url
  }

  // 3. Si es una ruta relativa (lo que devuelve tu backend), le pegamos el dominio de la UNLP
  // NOTA: Agregamos '/grupo10/' porque vimos que es necesario en la URL que me pasaste
  return `http://minio.proyecto2025.linti.unlp.edu.ar/grupo10/${url}`
}

// --- MÉTODOS EXISTENTES ---

const fetchSite = async () => {
  // Eliminamos el try/finally para controlar manualmente el loading
  loading.value = true
  try {
    const siteId = props.id || route.params.id
    const response = await api.fetchSiteById(siteId)

    if (response.success) {
      site.value = response.data

      // CORRECCIÓN: Ocultamos el loading AHORA para que el HTML del mapa se renderice
      loading.value = false

      // Ahora sí, esperamos a que el DOM se actualice y buscamos el mapa
      nextTick(() => {
        initMap()
        fetchSiteReviews()
      })
    } else {
      error.value = response.error || 'No se pudo cargar el sitio.'
      loading.value = false
    }
  } catch (err) {
    console.error("Error fetchSite:", err)
    error.value = 'Error de conexión.'
    loading.value = false
  }
}

const fetchSiteReviews = async (page = 1) => {
  if (!site.value) return

  reviewsLoading.value = true
  try {
    const response = await getSiteReviews(site.value.id, { page, per_page: 10 })
    console.log("Respuesta de reviews:", response)
    if (response.data && response.data.data) {
      siteReviews.value = response.data.data
      reviewsMeta.value = response.data.meta
    } else {
      siteReviews.value = []
      reviewsMeta.value = null
    }
  } catch (err) {
    console.error("Error fetching site reviews:", err)
    siteReviews.value = []
    reviewsMeta.value = null
  } finally {
    reviewsLoading.value = false
  }
}

const handleReviewsPageChange = (newPage) => {
  fetchSiteReviews(newPage)
}

const initMap = () => {
  if (!site.value || !site.value.lat || !site.value.long) return
  const mapContainer = document.getElementById('map')
  if (!mapContainer) {
      console.warn("Contenedor del mapa no encontrado.")
      return
  }
  if (map.value) {
      map.value.remove()
      map.value = null
  }

  // Fix iconos Leaflet
  delete L.Icon.Default.prototype._getIconUrl
  L.Icon.Default.mergeOptions({
    iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
    iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
  })

  map.value = L.map('map').setView([site.value.lat, site.value.long], 14)

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
  }).addTo(map.value)

  L.marker([site.value.lat, site.value.long])
    .addTo(map.value)
    .bindPopup(`<b>${site.value.name}</b><br>${site.value.city}`)
}

const handleFavoriteClick = async () => {
  if (!loggedIn.value) {
    if (confirm("Debes iniciar sesión para guardar favoritos. ¿Ir al login?")) {
      // Redirige al login de Google y vuelve a ESTA página después
      login(window.location.href)
    }
    return
  }

  const id = site.value.id
  let res

  try {
    if (site.value.is_favorite) {
      res = await api.removeFavorite(id)
      if (res.success) site.value.is_favorite = false
    } else {
      res = await api.addFavorite(id)
      if (res.success) site.value.is_favorite = true
    }

    if (!res.success) {
      alert('Error: ' + (res.error || 'No se pudo actualizar favorito'))
    }
  } catch (e) {
    alert('Error de conexión al guardar favorito')
  }
}

const handleWriteReview = () => {
    if (!api.isAuthenticated()) {
        if(confirm("Debes iniciar sesión para dejar una reseña. ¿Ir al login?")) {
            api.loginWithGoogle()
        }
        return
    } else {
       showReviewForm.value = true
    }
}

const onReviewSubmitted = (reviewData) => {
  // Refresh the site data and reviews to show updated ratings
  showReviewForm.value = false
  fetchSite()
  fetchSiteReviews()
  alert('¡Reseña enviada exitosamente!')
}

const handleImageError = (e) => {
  e.target.src = placeholderImage
}

const handleThumbError = (e) => {
    e.target.style.display = 'none'
}

const goBack = () => {
  // Si hay query params, volver con filtros
  if (Object.keys(route.query).length > 0) {
    router.push({
      path: '/sites-list',
      query: route.query
    })
  } else {
    // Si no hay filtros, usar history normal
    router.back()
  }
}

onMounted(() => {
  fetchSite()
})

onBeforeUnmount(() => {
    if (map.value) {
        map.value.remove()
    }
})
</script>

<style scoped src="../assets/detail.css"></style>

<style scoped>
.reviews-section {
  margin-top: 2rem;
}
</style>
