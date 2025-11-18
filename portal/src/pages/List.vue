<template>
  <div class="max-w-6xl mx-auto px-4 py-6">
    <!-- TÍTULO -->
    <h1 class="text-4xl font-bold mb-6 text-gray-800">Sitios Históricos</h1>

    <!-- BARRA DE BÚSQUEDA -->
    <div class="bg-white rounded-2xl shadow p-4 mb-6 flex items-center gap-3">
      <input
        v-model="search"
        @keyup.enter="fetchData"
        type="text"
        placeholder="Buscar sitios..."
        class="w-full px-4 py-2 border border-gray-300 rounded-xl focus:outline-none focus:ring focus:ring-blue-300"
      />
      <button
        @click="fetchData"
        class="bg-blue-600 hover:bg-blue-700 text-white px-5 py-2 rounded-xl shadow transition"
      >
        🔍 Buscar
      </button>
    </div>

    <!-- FILTROS -->
    <div class="bg-white rounded-2xl shadow p-4 mb-8 flex gap-3 items-center">
      <select
        v-model="order"
        @change="fetchData"
        class="px-4 py-2 border rounded-xl focus:ring focus:ring-blue-200"
      >
        <option value="">Ordenar por...</option>
        <option value="most_visited">Más visitados</option>
        <option value="top_rated">Mejor puntuados</option>
        <option value="recent">Recientes</option>
      </select>
    </div>

    <!-- LOADING -->
    <div v-if="loading" class="text-center text-gray-500 py-8 text-lg">Cargando sitios...</div>

    <!-- SIN RESULTADOS -->
    <p
      v-if="!loading && sites.length === 0"
      class="text-center text-gray-600 bg-gray-100 p-4 rounded-xl"
    >
      No se encontraron sitios.
    </p>

    <!-- LISTADO -->
    <div v-if="!loading" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
      <SiteCard v-for="s in sites" :key="s.id" :site="s" />
    </div>

    <!-- PAGINACIÓN -->
    <div class="flex justify-center items-center gap-3 mt-10" v-if="totalPages > 1">
      <button
        @click="prevPage"
        :disabled="page === 1"
        class="px-4 py-2 border rounded-xl bg-white shadow disabled:opacity-40"
      >
        ⬅ Anterior
      </button>

      <span class="px-4 py-2 font-semibold text-gray-700 bg-gray-100 rounded-xl">
        Página {{ page }} / {{ totalPages }}
      </span>

      <button
        @click="nextPage"
        :disabled="page === totalPages"
        class="px-4 py-2 border rounded-xl bg-white shadow disabled:opacity-40"
      >
        Siguiente ➡
      </button>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import SiteCard from '../components/SiteCard.vue'
import { fetchSites } from '../api'

export default {
  name: 'ListPage',
  components: { SiteCard },

  setup() {
    const route = useRoute()
    const router = useRouter()

    const search = ref(route.query.q || '')
    const order = ref(route.query.order || '')

    const sites = ref([])
    const loading = ref(false)

    const page = ref(Number(route.query.page) || 1)
    const pageSize = 9
    const totalPages = ref(1)

    async function fetchData() {
      loading.value = true

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

        sites.value = result.items
        totalPages.value = Math.ceil(result.total / pageSize)
      } catch (e) {
        console.error('Error cargando listado:', e)
      }

      loading.value = false
    }

    function nextPage() {
      if (page.value < totalPages.value) {
        page.value++
        fetchData()
      }
    }

    function prevPage() {
      if (page.value > 1) {
        page.value--
        fetchData()
      }
    }

    onMounted(fetchData)
    watch(() => route.query, fetchData)

    return {
      sites,
      search,
      order,
      loading,
      page,
      totalPages,
      nextPage,
      prevPage,
      fetchData,
    }
  },
}
</script>
