<template>
  <router-link
    :to="{ name: 'site-detail', params: { id: site.id } }"
    class="block bg-white rounded-xl shadow hover:shadow-lg transition overflow-hidden cursor-pointer no-underline"
  >
    <div class="bg-red-500 text-white text-xs p-1 text-center">
      DEBUG ID: {{ site.id || 'SIN ID' }}
    </div>

    <div class="relative h-32 w-full bg-gray-200">
      <img
        :src="resolveUrl(site.cover_image || site.image)"
        alt="Imagen del sitio"
        class="h-full w-full object-cover"
        @error="handleImageError"
      />
      <span v-if="site.state_of_conservation"
            class="absolute top-2 right-2 text-xs px-2 py-1 rounded-full font-bold text-white shadow-sm"
            :class="statusClass">
        {{ site.state_of_conservation }}
      </span>
    </div>

    <div class="p-3">
      <h3 class="font-semibold text-gray-800 truncate mb-1">{{ site.name }}</h3>

      <div class="flex justify-between items-center">
        <p class="text-sm text-gray-500 flex items-center gap-1">
            <span>⭐</span>
            {{ site.average_rating || site.rating || '-' }}
        </p>
        <span class="text-xs text-gray-400 flex items-center gap-1">
          📍 {{ site.city }}
        </span>
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
