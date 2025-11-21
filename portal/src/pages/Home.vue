<template>
  <main class="min-h-screen bg-gray-50">

    <SearchHero @search="handleSearch" />

    <div class="max-w-7xl mx-auto px-4 py-12 space-y-16">

      <SectionCarousel
        title="🔥 Los más visitados"
        :fetchFn="fetchMostVisited"
      />

      <SectionCarousel
        title="⭐ Mejor puntuados"
        :fetchFn="fetchTopRated"
      />

      <SectionCarousel
        title="🆕 Recientemente agregados"
        :fetchFn="fetchRecent"
      />

      </div>
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

// Componentes
import SectionCarousel from '../components/SectionCarousel.vue';
import SearchHero from '../components/SearchHero.vue';

// API: Importamos las funciones INDIVIDUALMENTE para usarlas en el template
import {
  fetchMostVisited,
  fetchTopRated,
  fetchRecent,
  isAuthenticated // Si tienes esta función helper en api.js
} from '../api.js'; // <--- OJO: Asegúrate que la ruta sea correcta (../api.js o ../Services/api.js)

const router = useRouter();
const isLoggedIn = ref(false);

// --- LÓGICA DE BÚSQUEDA ---
const handleSearch = (query) => {
  // En lugar de buscar aquí, mandamos al usuario a la página de lista
  // que ya está programada para buscar y mostrar resultados lindos.
  router.push({
    name: 'sites-list1', // Asegúrate que este nombre coincida con router/index.js
    query: { q: query }
  });
};

onMounted(() => {
  // Verificamos si hay usuario (ajusta según tu lógica de auth real)
  // isLoggedIn.value = isAuthenticated();
  // O chequeando token:
  isLoggedIn.value = !!localStorage.getItem('auth_token');
});
</script>
