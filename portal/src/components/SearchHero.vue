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
            @input="validateSearch"
            @keypress="preventInvalidChars"
            type="text"
            placeholder="Buscar un sitio..."
            class="search-input mobile-hidden"
            :class="{ 'input-error': searchError }"
            maxlength="100"
          />
          <div v-if="searchError" class="error-text">{{ searchError }}</div>
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
    const searchError = ref('')
    const router = useRouter()
    
    const validateSearch = () => {
      const trimmed = search.value.trim()
      if (trimmed.length > 0) {
        if (trimmed.length < 2) {
          searchError.value = 'La búsqueda debe tener al menos 2 caracteres'
          return false
        }
        if (!/^[a-zA-ZÀ-ſ\d\s\-\.]+$/.test(trimmed)) {
          searchError.value = 'Solo se permiten letras, números, espacios, guiones y puntos'
          return false
        }
        if (trimmed.length > 100) {
          searchError.value = 'La búsqueda no puede exceder 100 caracteres'
          return false
        }
      }
      searchError.value = ''
      return true
    }
    
    const emitSearch = () => {
      if (search.value.trim() && !validateSearch()) {
        // Mostrar mensaje de error por 3 segundos
        setTimeout(() => {
          if (searchError.value) searchError.value = ''
        }, 3000)
        return
      }
      
      if (window.innerWidth < 768) {
        // En móviles, navegar directamente a la lista de sitios
        router.push({ path: '/sites-list', query: search.value ? { q: search.value } : {} })
      } else {
        // En desktop, usar el comportamiento original
        emit('search', search.value)
      }
    }
    
    const preventInvalidChars = (event) => {
      const char = event.key
      // Permitir: letras, números, espacios, guiones, puntos, backspace, delete, etc.
      if (!/[a-zA-ZÀ-ſ\d\s\-\.]/.test(char) && !['Backspace', 'Delete', 'ArrowLeft', 'ArrowRight', 'Tab'].includes(char)) {
        event.preventDefault()
      }
    }
    
    return { search, searchError, emitSearch, validateSearch, preventInvalidChars }
  },
}
</script>
<style scoped>
.input-error {
  border-color: #dc2626 !important;
  box-shadow: 0 0 0 3px rgba(220, 38, 38, 0.1) !important;
}

.error-text {
  color: #dc2626;
  font-size: 0.75rem;
  margin-top: 0.25rem;
  position: absolute;
  top: 100%;
  left: 0;
}

.search-box {
  position: relative;
}
</style>