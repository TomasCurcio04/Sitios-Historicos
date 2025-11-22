<template>
  <div class="container mx-auto py-10 max-w-3xl">

    <div v-if="loading" class="text-center py-10">
      <p class="text-gray-600 text-lg">Cargando perfil...</p>
    </div>

    <div v-else-if="!loggedIn" class="text-center space-y-4">
      <h2 class="text-3xl font-bold">Mi Perfil</h2>

      <p class="text-gray-600">
        Inicia sesión para ver tu perfil, tus reseñas y tus favoritos.
      </p>

      <div class="flex justify-center">
        <GoogleLoginButton 
          :logged-in="loggedIn" 
          :user="user" 
          @login="login" 
          @logout="logout" 
        />
      </div>
    </div>

    <div v-else class="space-y-8">

      <div class="bg-white shadow-md rounded-xl p-6 flex items-center gap-6">
        <img
          :src="user.picture"
          alt="Foto de usuario"
          class="w-20 h-20 rounded-full object-cover shadow"
        />

        <div class="flex-1">
          <h2 class="text-2xl font-bold">{{ user.name }}</h2>
          <p class="text-gray-600">{{ user.email }}</p>
        </div>

        <GoogleLoginButton 
          :logged-in="loggedIn" 
          :user="user" 
          @login="login"
          @logout="logout"
        />
      </div>

      <div class="border-b flex gap-6">
        <button
          @click="activeTab = 'reviews'"
          :class="[
            'pb-2 font-semibold transition-colors',
            activeTab === 'reviews'
              ? 'border-b-2 border-blue-600 text-blue-600'
              : 'text-gray-600 hover:text-gray-800'
          ]"
        >
          Mis Reseñas
        </button>

        <button
          @click="activeTab = 'favorites'"
          :class="[
            'pb-2 font-semibold transition-colors',
            activeTab === 'favorites'
              ? 'border-b-2 border-blue-600 text-blue-600'
              : 'text-gray-600 hover:text-gray-800'
          ]"
        >
          Mis Favoritos
        </button>
      </div>

      <div class="pt-4">
        <div v-if="activeTab === 'reviews'">
          <ReviewsList
            :reviews="sortedReviews"
            :meta="reviewsMeta"
            :loading="reviewsLoading"
            @page-change="loadReviews"
            @order-change="changeReviewsOrder"
          />
        </div>

        <div v-if="activeTab === 'favorites'">
          <FavoritesList
            :favorites="sortedFavorites"
            :meta="favoritesMeta"
            :loading="favoritesLoading"
            @page-change="loadFavorites"
            @order-change="changeFavoritesOrder"
          />
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, watch, computed } from 'vue'
import GoogleLoginButton from '../components/GoogleLoginButton.vue'
import ReviewsList from '../components/UserReviewsList.vue'
import FavoritesList from '../components/UserFavoritesList.vue'
import { useAuth } from '../composables/useAuth'
import { useApi } from '../composables/useApi'

const Api = useApi()


const { loggedIn, user, loading, login, logout } = useAuth() 

const API_URL = import.meta.env.VITE_API_URL


const activeTab = ref('reviews')
const reviews = ref([])
const reviewsMeta = ref({})
const reviewsLoading = ref(false)
const reviewsOrder = ref('desc')
const favorites = ref([])
const favoritesMeta = ref({})
const favoritesLoading = ref(false)
const favoritesOrder = ref('desc')


const loadReviews = async (page = 1) => {
  if (!loggedIn.value) return;

  reviewsLoading.value = true;

  try {
    console.log("Llamando a getMyReviews...")
    const res = await Api.getMyReviews({ page });
    console.log("Respuesta de reviews:", res)
    
    const data = res.data || {}
    reviews.value = (data.data || []).map(r => ({
      ...r,
      date: r.inserted_at
    }))
    console.log("Mapped reviews:", reviews.value)
    
    const meta = data.meta || {}
    reviewsMeta.value = {
      current_page: meta.page || 1,
      total_pages: Math.ceil((meta.total || 0) / (meta.per_page || 20)),
      total: meta.total || 0
    }
  } catch (error) {
    console.error("Error loading reviews:", error)
  } finally {
    reviewsLoading.value = false
  }
}


const changeReviewsOrder = (order) => {
  reviewsOrder.value = order
}


const loadFavorites = async (page = 1) => {
  if (!loggedIn.value) return;

  favoritesLoading.value = true;

  try {
    const res = await Api.getMyFavorites({ page });

    const data = res.data;

    favorites.value = (data.data || []).map(f => ({
        ...f,
      date: f.inserted_at
    }))
    
    const meta = data.meta || {};

    favoritesMeta.value = {
      current_page: meta.page || 1,
      total_pages: Math.ceil((meta.total || 0) / (meta.per_page || 20)),
      total: meta.total || 0
    };
  } catch (error) {
    console.error("Error loading favorites:", error);
  } finally {
    favoritesLoading.value = false;
  }
};

const changeFavoritesOrder = (order) => {
  favoritesOrder.value = order
}


const sortedReviews = computed(() => {
  return [...reviews.value].sort((a, b) => {
    const d1 = new Date(a.date)
    const d2 = new Date(b.date)
    return reviewsOrder.value === 'desc' ? d2 - d1 : d1 - d2
  })
})

const sortedFavorites = computed(() => {
  return [...favorites.value].sort((a, b) => {
    const d1 = new Date(a.date)
    const d2 = new Date(b.date)
    return favoritesOrder.value === 'desc' ? d2 - d1 : d1 - d2
  })
})



watch(loggedIn, async (isLoggedIn) => {
  if (isLoggedIn) {
    // Si el usuario acaba de iniciar sesión, cargamos los datos
    await Api.getToken();
    await loadReviews()
    await loadFavorites()
  } else {
    // Si el usuario cierra sesión, limpiamos la lista
    console.log("Usuario ha cerrado sesión, limpiando datos...")
    reviews.value = []
    favorites.value = []
    console.log("Datos limpiados.")
  }
}, { 
  // 'immediate: true' garantiza que se ejecute al inicio, una vez que useAuth 
  // ha determinado el estado inicial de la sesión.
  immediate: true 
})
</script>