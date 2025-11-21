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
            class="search-input"
          />
          <button
            @click="emitSearch"
            class="search-button"
          >
            🔍
          </button>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'SearchHero',
  setup(_, { emit }) {
    const search = ref('')
    const emitSearch = () => emit('search', search.value)
    return { search, emitSearch }
  },
}
</script>
