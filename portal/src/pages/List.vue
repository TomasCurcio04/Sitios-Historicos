<template>
  <div>
    <div class="max-w-7xl mx-auto px-4 py-8">
      <div class="flex flex-col md:flex-row justify-between items-center mb-8 gap-4">
        <h1 class="text-3xl font-bold text-gray-800">Sitios Históricos</h1>

        <div class="flex gap-2 w-full md:w-auto">
          <select
            v-model="order"
            @change="fetchData"
            class="px-4 py-2 border border-gray-300 rounded-lg bg-white focus:ring-2 focus:ring-blue-500 outline-none"
          >
            <option value="">Más recientes</option>
            <option value="az">A-Z</option>
            <option value="za">Z-A</option>
          </select>
        </div>
      </div>

    <hr class="my-16 border-gray-200">

    <div v-if="loading" class="flex justify-center py-20 ml-6">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
    </div>

    <div v-else class="ml-6">
      <div v-if="sites.length > 0" class="sites-grid">
        <SiteCard
          v-for="site in sites"
          :key="site.id"
          :site="site"
        />
      </div>

      <div v-else class="text-center py-20 bg-gray-50 rounded-xl">
        <p class="text-xl text-gray-500">No se encontraron sitios con esa búsqueda.</p>
        <button @click="resetFilters" class="mt-4 text-blue-600 hover:underline">
          Limpiar filtros
        </button>
      </div>
    </div>

    <div v-if="!loading && sites.length > 0" class="mt-10 flex justify-center items-center gap-4 ml-6">
      <button
        @click="prevPage"
        :disabled="page === 1"
        class="px-4 py-2 border rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        Anterior
      </button>

      <span class="text-gray-600">
        Página {{ page }} de {{ totalPages }}
      </span>

      <button
        @click="nextPage"
        :disabled="page >= totalPages"
        class="px-4 py-2 border rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        Siguiente
      </button>
    </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import SiteCard from '../components/SiteCard.vue'
import { fetchSites } from '../api.js'

// Router y Route
const route = useRoute()
const router = useRouter()

// Estado reactivo
const search = ref(route.query.q || '')
const order = ref(route.query.order || '')
const sites = ref([])
const loading = ref(false)

// Paginación
const page = ref(Number(route.query.page) || 1)
const pageSize = 9
const totalPages = ref(1)



// Función principal de carga
async function fetchData() {
  loading.value = true

  // Actualizar URL sin recargar
  router.replace({
    query: {
      q: search.value || undefined,
      order: order.value || undefined,
      page: page.value !== 1 ? page.value : undefined,
    },
  })

  try {
    const result = await fetchSites({
      q: search.value,
      order: order.value,
      page: page.value,
      limit: pageSize,
    })

    if (result.success) {
      sites.value = result.data.items || []
      // Asegurarnos de que totalPages sea al menos 1
      const total = result.data.total || 0
      totalPages.value = Math.ceil(total / pageSize) || 1
    } else {
      console.error('Error fetchSites:', result.error)
      sites.value = []
      totalPages.value = 1
    }
  } catch (e) {
    console.error('Error cargando listado:', e)
    sites.value = []
  } finally {
    loading.value = false
  }
}

// Navegación de páginas
function nextPage() {
  if (page.value < totalPages.value) {
    page.value++
    fetchData()
    window.scrollTo({ top: 0, behavior: 'smooth' }) // Subir al cambiar página
  }
}

function prevPage() {
  if (page.value > 1) {
    page.value--
    fetchData()
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
}

function resetFilters() {
  search.value = ''
  order.value = ''
  page.value = 1
  fetchData()
}

// Ciclo de vida
onMounted(fetchData)

// Observar cambios en la URL (por si usan el botón Atrás del navegador)
watch(
  () => route.query,
  (newQuery) => {
    if (newQuery.q !== search.value) search.value = newQuery.q || ''
    if (newQuery.page) page.value = Number(newQuery.page)
    // No llamamos a fetchData aquí directamente si ya se llama por los v-models,
    // pero es buena práctica para sincronizar historial.
  }
)
</script>
