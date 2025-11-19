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
        <button @click="router.push('/sites')" class="back-btn">
          ← Volver
        </button>
      </div>

      <div class="hero-image">
        <img
          :src="currentImage || site.cover_image || '/placeholder.jpg'"
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
          :src="img.url"
          :alt="img.title"
          class="thumb"
          :class="{ active: currentImage === img.url }"
          @click="currentImage = img.url"
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
          <button
            v-if="site.description && site.description.length > 300"
            @click="expandedDesc = !expandedDesc"
            class="link-btn"
          >
            {{ expandedDesc ? 'Leer menos' : 'Leer más' }}
          </button>
        </section>

        <section class="map-section" v-if="site.lat && site.long">
          <h3>Ubicación</h3>
          <div id="map" class="map-container"></div>
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
  </div>
</template>

<script setup>
import { ref, onMounted, computed, nextTick } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '../api'; // Usa el export default que agregamos a tu api.js
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

const props = defineProps({
  id: { type: [String, Number], required: true }
});

const route = useRoute();
const router = useRouter();

// Variables Reactivas
const site = ref(null);
const loading = ref(true);
const error = ref(null);
const currentImage = ref(null);
const expandedDesc = ref(false);
const map = ref(null);

// Clases para el estado (verde, amarillo, rojo)
const statusClass = computed(() => {
  if (!site.value) return '';
  const status = site.value.state_of_conservation?.toLowerCase();
  if (['bueno', 'excelente', 'muy bueno'].includes(status)) return 'status-good';
  if (['regular'].includes(status)) return 'status-regular';
  return 'status-bad';
});

// --- MÉTODOS ---

const fetchSite = async () => {
  try {
    loading.value = true;
    const siteId = props.id || route.params.id;

    // Llamada a tu API usando la función fetchSiteById
    const response = await api.fetchSiteById(siteId);

    if (response.success) {
        site.value = response.data;
        nextTick(() => { initMap(); });
    } else {
        error.value = response.error || 'No se pudo cargar el sitio.';
    }
  } catch (err) {
    console.error(err);
    error.value = 'Error de conexión.';
  } finally {
    loading.value = false;
  }
};

const initMap = () => {
  if (!site.value || !site.value.lat || !site.value.long || map.value) return;

  // Fix iconos Leaflet
  delete L.Icon.Default.prototype._getIconUrl;
  L.Icon.Default.mergeOptions({
    iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
    iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
  });

  map.value = L.map('map').setView([site.value.lat, site.value.long], 14);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap'
  }).addTo(map.value);

  L.marker([site.value.lat, site.value.long])
    .addTo(map.value)
    .bindPopup(`<b>${site.value.name}</b><br>${site.value.city}`);
};

const handleFavoriteClick = async () => {
  if (!api.isAuthenticated()) {
    if(confirm("Debes iniciar sesión para guardar favoritos. ¿Ir al login?")) {
        api.loginWithGoogle();
    }
    return;
  }

  const id = site.value.id;
  let res;

  try {
    if (site.value.is_favorite) {
        res = await api.removeFavorite(id);
        if (res.success) site.value.is_favorite = false;
    } else {
        res = await api.addFavorite(id);
        if (res.success) site.value.is_favorite = true;
    }

    if (!res.success) alert('Error: ' + (res.error || 'No se pudo actualizar favorito'));
  } catch (e) {
    alert('Error de conexión al guardar favorito');
  }
};

const handleWriteReview = () => {
    if (!api.isAuthenticated()) {
        if(confirm("Debes iniciar sesión para opinar. ¿Ir al login?")) {
            api.loginWithGoogle();
        }
    } else {
        alert("Formulario de reseña pendiente.");
    }
};

const handleImageError = (e) => {
  e.target.src = 'https://via.placeholder.com/800x400?text=Sin+Imagen';
};

onMounted(() => {
  fetchSite();
});
</script>

<style scoped src="../assets/detail.css"></style>
