<template>
  <section class="hero-banner">
    <div class="hero-content">
      <div class="hero-text">
        <h1 class="hero-title">Descubrí los Sitios Históricos</h1>
        <p class="hero-subtitle">Buscá, explorá y conocé los lugares más importantes de nuestra historia.</p>
      </div>
      
      <div class="hero-search">
        <div class="search-box">
          <input
            v-model="search"
            @keyup.enter="emitSearch"
            type="text"
            placeholder="Buscar un sitio..."
            class="search-input mobile-hidden"
          />
          <button
            @click="emitSearch"
            class="search-button mobile-full-width"
          >
            🔍 <span class="mobile-only">Ver Sitios</span>
          </button>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'SearchHero',
  setup(_, { emit }) {
    const search = ref('')
    const router = useRouter()
    
    const emitSearch = () => {
      if (window.innerWidth < 768) {
        // En móviles, navegar directamente a la lista de sitios
        router.push({ path: '/sites-list', query: search.value ? { q: search.value } : {} })
      } else {
        // En desktop, usar el comportamiento original
        emit('search', search.value)
      }
    }
    
    return { search, emitSearch }
  },
}
</script>
