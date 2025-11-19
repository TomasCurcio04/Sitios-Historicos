<template>
  <div class="max-w-4xl mx-auto px-4 py-6">
    <!-- LOADER -->
    <div v-if="loading" class="text-center text-gray-600 text-lg py-10">Cargando...</div>

    <!-- ERROR -->
    <p v-if="error" class="text-center text-red-600 font-semibold bg-red-100 p-3 rounded-xl">
      {{ error }}
    </p>

    <!-- CONTENIDO -->
    <div v-if="site" class="bg-white rounded-2xl shadow-lg overflow-hidden">
      <!-- Imagen -->
      <div class="h-64 w-full overflow-hidden">
        <img
          v-if="site.image_url"
          :src="site.image_url"
          class="w-full h-full object-cover"
          alt="Imagen del sitio"
        />
      </div>

      <!-- Info -->
      <div class="p-6">
        <h1 class="text-3xl font-bold mb-4 text-gray-800">
          {{ site.name }}
        </h1>

        <p class="text-lg text-gray-700 leading-relaxed mb-6">
          {{ site.description }}
        </p>

        <div class="space-y-2 text-gray-700">
          <p>📍 <strong>Ubicación:</strong> {{ site.location }}</p>

          <p>
            ⭐ <strong>Promedio:</strong>
            {{ site.avg_rating ?? 'Sin calificaciones' }}
          </p>
        </div>

        <!-- BOTÓN FAVORITOS -->
        <div class="mt-6">
          <button
            v-if="isLoggedIn"
            @click="toggleFavorite"
            class="w-full py-3 rounded-xl text-white font-medium shadow-md transition"
            :class="isFavorite ? 'bg-red-600 hover:bg-red-700' : 'bg-blue-600 hover:bg-blue-700'"
          >
            {{ isFavorite ? 'Quitar de favoritos' : 'Agregar a favoritos' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { fetchSiteById, addFavorite, removeFavorite, isFavoriteSite } from '../api'

export default {
  name: 'DetailPage',

  setup() {
    const route = useRoute()
    const id = route.params.id

    const loading = ref(true)
    const error = ref(null)
    const site = ref(null)

    const isLoggedIn = !!localStorage.getItem('auth_token')
    const isFavorite = ref(false)

    async function loadDetail() {
      try {
        site.value = await fetchSiteById(id)

        if (!site.value) {
          error.value = 'El sitio no existe.'
          return
        }

        if (isLoggedIn) {
          isFavorite.value = await isFavoriteSite(id)
        }
      } catch {
        error.value = 'Error cargando los datos.'
      } finally {
        loading.value = false
      }
    }

    async function toggleFavorite() {
      if (isFavorite.value) {
        await removeFavorite(id)
        isFavorite.value = false
      } else {
        await addFavorite(id)
        isFavorite.value = true
      }
    }

    onMounted(loadDetail)

    return {
      loading,
      error,
      site,
      isLoggedIn,
      isFavorite,
      toggleFavorite,
    }
  },
}
</script>
