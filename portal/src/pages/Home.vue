<template>
  <main class="min-h-screen bg-gray-50">

    <div class="max-w-7xl mx-auto px-4 py-12 space-y-16">

      <SectionCarousel
        title="🔥 Los más visitados"
        :fetchFn="fetchMostVisited"
        :queryParams="{ order_by: 'most-visited' }"
      />

      <SectionCarousel
        title="⭐ Mejor puntuados"
        :fetchFn="fetchTopRated"
        :queryParams="{ order_by: 'rating-5-1' }"
      />

      <SectionCarousel
        title="🆕 Recientemente agregados"
        :fetchFn="fetchRecent"
        :queryParams="{ order_by: 'latest' }"
      />

      </div>
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

// Componentes
import SectionCarousel from '../components/SectionCarousel.vue';

// API: Importamos las funciones INDIVIDUALMENTE para usarlas en el template
import {
  fetchMostVisited,
  fetchTopRated,
  fetchRecent,
  isAuthenticated // Si tienes esta función helper en api.js
} from '../api.js'; // <--- OJO: Asegúrate que la ruta sea correcta (../api.js o ../Services/api.js)

const router = useRouter();

// onMounted ya no es necesario, useAuth maneja la verificación
</script>
