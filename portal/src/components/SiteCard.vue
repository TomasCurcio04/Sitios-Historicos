<template>
  <router-link
    :to="{ name: 'site-detail', params: { id: site.id } }"
    class="site-card"
  >
    <div class="card-image">
      <div v-if="!site.cover_image && !site.image" class="no-image-placeholder">
        Sin<br>Portada
      </div>
      <img
        v-else
        :src="resolveUrl(site.cover_image || site.image)"
        alt="Imagen del sitio"
        class="cover-image"
        @error="handleImageError"
      />
    </div>
    
    <div class="card-content">
      <h3 class="card-title">{{ site.name }}</h3>
      <div class="card-body">
        <div class="card-info">
          <span class="label">Ciudad:</span>
          <span class="value">{{ site.city }}</span>
        </div>
        <div class="card-info">
          <span class="label">Estado:</span>
          <span class="value conservation-badge">{{ site.state_of_conservation }}</span>
        </div>
        <div class="card-info">
          <span class="label">Rating:</span>
          <span class="value">⭐ {{ site.average_rating || site.rating || '-' }}</span>
        </div>
      </div>
    </div>
  </router-link>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  site: { type: Object, required: true },
});

const placeholder = 'https://via.placeholder.com/300x200?text=Sin+Imagen';

// Manejo de URLs
const resolveUrl = (url) => {
  if (!url) return placeholder;
  if (url.startsWith('http') || url.startsWith('https')) return url;
  return `http://minio.proyecto2025.linti.unlp.edu.ar/grupo10/${url}`;
};

const handleImageError = (e) => {
  e.target.src = placeholder;
};

// Clases dinámicas
const statusClass = computed(() => {
  const status = props.site.state_of_conservation?.toLowerCase();
  if (['bueno', 'excelente', 'muy bueno'].includes(status)) return 'bg-green-500';
  if (['regular'].includes(status)) return 'bg-yellow-500';
  return 'bg-red-500';
});
</script>
